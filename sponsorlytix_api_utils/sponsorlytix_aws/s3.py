import json
import boto3
import os

BUCKET = os.environ.get('AWS_S3_BUCKET_NAME')


def upload_json_to_s3(data, location: str):
    s3 = boto3.client('s3')
    s3.put_object(
        Body=json.dumps(data),
        Bucket=BUCKET,
        Key=location)


def download_file(location: str, destination: str):
    s3 = boto3.client('s3')
    s3.download_file(BUCKET, location, destination)
