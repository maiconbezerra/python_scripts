import json
import boto3
from botocore.exceptions import ClientError


def s3_upload_file(bucket, src_path, dst_path):
    """
    Upload file do AWS S3 bucket
    :param bucket - Inform bucket name to be used to upload file
    :param src_path - Inform source file to be uploaded
    :param dst_path - Inform s3 bucket folder when the files will be stored
    """

    s3 = boto3.resource("s3")
    s3.meta.client.upload_file(src_path, bucket, dst_path)


def secrets_mgr_get(secret_name, region):
    """
    Recover Secrets Manager key
    :param secret_name - Name of secret field
    :param region - Name of used region
    """

    # Input values in variables
    secret_name = secret_name
    region_name = region

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        raise e

    # Decrypts secret
    secret = get_secret_value_response['SecretString']
    passwd = json.loads(secret)

    return passwd['password']


def secrets_mgr_put(secret_name, region, key, value):
    """
    Update secret value in Secrets Manager

    :param secret_name - Name of secret
    :param region - Region where Secrets Manager is hosted
    :param key - Key is a field to update
    :param value - Value to the value to key associated
    """

    # Input values in variables
    secret_name = secret_name
    region_name = region

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(service_name='secretsmanager', region_name=region_name)

    try:
        put_secret_value = client.put_secret_value(SecretId=secret_name, SecretString='{"' + key + '":"' + value + '"}')
    except:
        print('Unable to update field')


def sns_publish(topic_arn, msg_subject, msg_body, region='sa-east-1'):
    """
    Update secret value in Secrets Manager

    :param topic_arn - ARN of SNS Topic to be used
    :param msg_subject - Message in mail Subject
    :param msg_body - Email message
    :param region - Region of SNS. By default, uses sa-east-1 if no option was chosen
    """

    sns = boto3.client('sns', region_name=region)

    sns.publish(
        TargetArn=topic_arn,
        Message=msg_body,
        Subject=msg_subject
    )

