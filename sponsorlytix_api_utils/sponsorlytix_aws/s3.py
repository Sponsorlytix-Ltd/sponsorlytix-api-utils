import json
import numbers
import boto3
import os

BUCKET = os.environ.get('AWS_S3_BUCKET_NAME')


def upload_json_to_s3(data, object_location: str):
    s3 = boto3.client('s3')
    s3.put_object(
        Body=json.dumps(data),
        Bucket=BUCKET,
        Key=object_location)


def download_file(object_location: str, destination: str):
    s3 = boto3.client('s3')
    s3.download_file(BUCKET, object_location, destination)


def generate_presigned_url(object_location: str, expire_in: int):
    return boto3.client('s3').generate_presigned_url(
        ClientMethod='get_object',
        Params={'Bucket': BUCKET, 'Key': object_location},
        ExpiresIn=expire_in)
