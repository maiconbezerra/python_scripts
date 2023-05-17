import fgt_login
import aws
import security

def lambda_handler(event, context):

    #  Firewall appliances connection list
    fgt_fw = ['10.0.0.254']

    #  Connection info
    fgt_user = 'lambda_backup'
    fgt_ssh_port = 22022

    #  Get password from AWS Secrets Manager
    fgt_pwd = aws.secrets_mgr_get("secret_name", "sa-east-1")

    #  Login fortigate
    fgt_session = fgt_login.connect_fortigate(fgt_fw[0], fgt_user, fgt_pwd, fgt_ssh_port)

    #  Generate new password
    new_pass = security.password_generator(16)

    #  Change to new password user lambda_backup
    fgt_login.change_password(fgt_session=fgt_session, username=fgt_user, new_pwd=new_pass)

    #  Update password in Secrets Manager
    aws.secrets_mgr_put(secret_name='secret_name', region='sa-east-1', key='password', value=new_pass)