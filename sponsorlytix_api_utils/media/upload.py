import os
import boto3

BUCKET = os.environ.get('AWS_S3_BUCKET_NAME')

def upload_media(file_path : str):
    session = boto3.Session(
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
    )
    
    s3 = session.resource('s3')
    s3.meta.client.upload_file(Filename=file_path, Bucket=BUCKET, Key='s3_sponsorlytix_key')
    