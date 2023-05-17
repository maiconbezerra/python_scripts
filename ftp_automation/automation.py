from modules import ftp, pgp, file_ops, log, aws
import time
import os
import sys
import datetime

#  Gets passwords from AWS Secrets Manager
aws_secrets = aws.secrets_mgr_get(secret_name='secret_name', region='sa-east-1')

#  FTP Server information - Homolog
citi_ftp_prod = {'host': 'ftp_server.com',
                 'user': 'USER',
                 'pass': aws_secrets['ftp_prod'],
                 'down_dir': '/download/',
                 'uplo_dir': '/upload/'}

#  Working directories
local_dir = {'download': 'D:\\localpath\\Download\\',
             'staging': 'D:\\localpath\\Staging\\',
             'quarantine': 'D:\\localpath\\Quarantine\\',
             'chk_retorno': 'D:\\localpath\\Checked\\Retorno\\',
             'chk_remessa': 'D:\\localpath\\Checked\\Remessa\\',
             'upload': 'D:\\localpath\\Upload\\',
             'remessa': 'D:\\localpath\\TEST\\Remessa\\'}

#  PAG directories
destination_path = [
    'D:\\localpath\\TEST\\Retorno\\Folder1\\',
    'D:\\localpath\\TEST\\Retorno\\Folder2\\',
    'D:\\localpath\\TEST\\Retorno\\Folder3\\',
    'D:\\localpath\\TEST2\\'
]

#  PGP information
pgp_recipient = 'rcpt_prod'

#  Project Name
project_name = 'Name1'

#  Sets logging configuration
logging_filename = datetime.date.today().strftime("%Y%m%d-automation.log")
logging_dir = "D:\\localpath\\Log\\"
logging_retention = 14


#  Write output in logging file
logging_file = open(os.path.join(logging_dir,  logging_filename), 'a')
sys.stdout = logging_file

'''
FTP TLS - DOWNLOAD
'''

#  Logging file header
log.logging_top(automation_name=project_name)

#  Controls FTP TLS connection
citi_ftps_download_session = ftp.ftp_tls_connect(host=citi_ftp_prod['host'],
                                                 user=citi_ftp_prod['user'],
                                                 passwd=citi_ftp_prod['pass'])

if citi_ftps_download_session != 'ftp_connect_fail':

    #  Changes to new directory /mailbox
    citi_ftps_chgdir = ftp.ftp_chg_dir(ftp_session=citi_ftps_download_session, dir=citi_ftp_prod['down_dir'])

    if citi_ftps_chgdir != 'dir_not_found':
        #  List existing files in directory
        citi_ftps_list_files = ftp.ls_ftp_files(ftp_session=citi_ftps_download_session)

        #  Download files in directory
        if citi_ftps_list_files:
            citi_ftps_download = ftp.ftp_download(download_path=local_dir['download'],
                                                  ftp_files=citi_ftps_list_files,
                                                  ftp_session=citi_ftps_download_session)
        else:
            print(time.strftime('%Y-%m-%d %H:%M:%S'), f'*INFO* No files to download at time')

    #  Ending FTP session
    citi_ftps_download_session.quit()


'''
CHECKING FILES
'''

#  File validation step
citi_downloaded_files = os.listdir(local_dir['download'])
file_validation = file_ops.file_fmt_chk(citi_downloaded_files)

if citi_downloaded_files:

    #  Move files in wrong format to QUARANTINE folder
    file_ops.file_move(files=file_validation['chk_fail'],
                       src_dir=local_dir['download'],
                       dst_dir=local_dir['quarantine'])

    #  Move files in right format to CHECKED folder
    file_ops.file_move(files=file_validation['chk_pass'],
                       src_dir=local_dir['download'],
                       dst_dir=local_dir['chk_retorno'])

'''
DECRYPT FILES WITH PGP
'''

if file_validation['chk_pass']:

    #  Listing encrypted files
    encrypted_files = file_validation['chk_pass']

    #  Decrypting files
    pgp.pgp_decrypt_file(passphrase=aws_secrets['citi_prod_passphrase'],
                         encrypted_files_dir=local_dir['chk_retorno'],
                         decrypted_files_dir=local_dir['staging'],
                         encrypted_files=encrypted_files)

else:
    print(time.strftime('%Y-%m-%d %H:%M:%S'), f'*INFO* No files to decrypt at time')

#  Copy files from Staging folder to Destination folder
if os.listdir(local_dir['staging']):

    #  Copying
    for i in destination_path:
        file_ops.file_copy(files=os.listdir(local_dir['staging']), src_dir=local_dir['staging'], dst_dir=i)

    #  Delete files from staging folder
    file_ops.file_delete(files=os.listdir(local_dir['staging']), dir=local_dir['staging'])


'''
ENCRYPT FILES WITH PGP
'''

#  File encryption routine
if os.listdir(local_dir['remessa']):
    for file in os.listdir(local_dir['remessa']):

        #  Encrypting files
        pgp.pgp_encrypt_file(recipient=pgp_recipient,
                             decrypted_files=file,
                             decrypted_files_dir=local_dir['remessa'],
                             encrypted_files_dir=local_dir['upload'])
else:
    print(time.strftime('%Y-%m-%d %H:%M:%S'), f'*INFO* No files to encrypt at time')


#  FTP upload routine
if os.listdir(local_dir['upload']):
    #  Connecting to FTP server
    citi_ftps_upload_session = ftp.ftp_tls_connect(host=citi_ftp_prod['host'],
                                                   user=citi_ftp_prod['user'],
                                                   passwd=citi_ftp_prod['pass'])

    #  Change to /postbox directory
    ftp.ftp_chg_dir(ftp_session=citi_ftps_upload_session, dir=citi_ftp_prod['uplo_dir'])

    #  Upload files
    ftp.ftp_upload(files=os.listdir(local_dir['upload']),
                   upload_dir=local_dir['upload'],
                   ftp_session=citi_ftps_upload_session)

    #  Move files after upload
    file_ops.file_move(files=os.listdir(local_dir['upload']),
                       src_dir=local_dir['upload'],
                       dst_dir=local_dir['chk_remessa'])

else:
    print(time.strftime('%Y-%m-%d %H:%M:%S'), f'*INFO* No files to upload at time')


#  Logging bottom
log.logging_bottom(automation_name=project_name)

'''
    CLEAR AND CLOSING LOGGING FILE
'''
# Clear logging file that match with retention config
logging_files = log.list_log_files(logging_dir)
log.clear_logging(logging_retention, logging_files)

#  Closing loggin file
logging_file.close()
