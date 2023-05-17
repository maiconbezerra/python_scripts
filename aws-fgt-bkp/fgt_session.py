import fgt_login
import aws
import time
import os


def lambda_handler(event, context):

    try:

        '''
        Input Information
        '''

        #  Firewall list
        fgt_fw = ['10.0.0.254']
        fgt_all_nodes = list()

        #  Firewall Connection info
        fgt_user = 'lambda_backup'
        fgt_ssh_port = 22022

        #  Backup info
        fgt_bkp_path = '/tmp/'

        #  S3 info
        aws_bucket_name = 'bucket_name'
        aws_bucket_folder = 'firewalls/'

        #  Command  lines
        fgt_cmd_chgnode = f'execute ha manage'
        fgt_cmd_shcfg = 'show'


        '''
        AWS Secrets Manager 
        '''

        #  Recover password from Secrets Manager
        fgt_pwd = aws.secrets_mgr_get("secret_name", "sa-east-1")


        '''
        Fortigate SSH connection
        '''

        #  Connect to firewall appliances
        fgt_session = fgt_login.connect_fortigate(fgt_fw[0], fgt_user, fgt_pwd, fgt_ssh_port)


        '''
        Backup active node
        '''

        #  Getting appliance hostname
        fgt_hostname = fgt_login.dectect_hostname(fgt_session)

        #  Adding active node
        fgt_all_nodes.append(fgt_hostname)

        #  Starts active node backup
        bkp_file_path = fgt_bkp_path + fgt_hostname + '.conf'
        fgt_bkp_filepath = open(bkp_file_path, 'w')
        fgt_bkp_anode = fgt_session.send_command_timing(fgt_cmd_shcfg)
        fgt_bkp_filepath.write(fgt_bkp_anode)
        fgt_bkp_filepath.close()


        '''
        Backup passive nodes
        '''

        #  Getting cluster information. Return a list with (hostname, serial_number, cluster_index) of each passive node
        fgt_clus_info = fgt_login.detect_passive_node(fgt_session)

        #  Backup passive nodes
        #  Using method write_channel and read_channel, to use active node as a jump host
        for i in fgt_clus_info:

            #  Adding active node
            fgt_all_nodes.append(i[0])

            #  Changing node
            fgt_session.write_channel(fgt_cmd_chgnode + ' ' + i[2] + ' ' + fgt_user + '\n')
            time.sleep(1)

            #  Checking screen
            output = fgt_session.read_channel()

            #  Input password
            if 'password' in output:
                fgt_session.write_channel(fgt_pwd + '\n')
            time.sleep(1)

            #  Backup parameter
            output += fgt_session.read_channel()
            fgt_session.write_channel(fgt_cmd_shcfg + '\n')
            time.sleep(60)

            #  Starts passive node backup
            bkp_file_path = fgt_bkp_path + i[0] + '.conf'
            fgt_bkp_filepath = open(bkp_file_path,'w')
            fgt_bkp_filepath.write(fgt_session.read_channel())  # Write backup in file
            fgt_bkp_filepath.close()
            time.sleep(1)


        '''
        Upload files to AWS S3
        '''

        #  list files in backup folder
        fgt_bkp_files = os.listdir(fgt_bkp_path)

        #  Upload files to AWS bucket
        for f in fgt_bkp_files:
            for n in fgt_all_nodes:
                if n in f:
                    aws.s3_upload_file(bucket=aws_bucket_name, src_path=fgt_bkp_path + f, dst_path=aws_bucket_folder + n + '/' + f)

    except Exception as e:

        #  Input SNS information
        sns_arn = 'arn:aws:sns:sa-east-1:607150308374:backup-alert'
        msg_subject = 'Lambda - aws-fgt-backup'
        msg = 'event: Backup Failed \n' \
              'name: Lambda_aws-fgt-backup\n' \
              f'date: {time.strftime("%d-%m-%Y %H:%M:%S")}\n' \
              f'information:\n\n {e}'

        #  Publish message from Lambda to SNS
        aws.sns_publish(topic_arn=sns_arn, msg_subject=msg_subject, msg_body=msg)

