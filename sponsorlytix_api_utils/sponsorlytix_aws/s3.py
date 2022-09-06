import json
import logging
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


def upload_file_to_S3(local_file_path, object_name, remove_local_file=True, multipart_upload=False, s3_bucket=None):
    """
    Upload a file to an S3 bucket

    :param local_file_path: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name
    :return: URLs if file was uploaded, else None
    """
    if not s3_bucket:
        s3_bucket = BUCKET

    try:
        s3_client = boto3.client('s3')

        multipart_config = None
        if multipart_upload:
            THRESHOLD = os.environ.get('AWS_S3_MULTIPART_THRESHOLD')
            CONCURRENCY = os.environ.get('AWS_S3_MAX_CONCURRENCY')
            CHUNKSIZE = os.environ.get('AWS_S3_MULTIPART_CHUNKSIZE')
            THREADS = os.environ.get('AWS_S3_USE_THREADS')
            multipart_config = boto3.s3.transfer.TransferConfig(multipart_threshold=THRESHOLD,
                                                                max_concurrency=CONCURRENCY,
                                                                multipart_chunksize=CHUNKSIZE,
                                                                use_threads=THREADS)

        s3_client.upload_file(
            local_file_path, s3_bucket, object_name, Config=multipart_config
        )
        location = s3_client.get_bucket_location(
            Bucket=s3_bucket)['LocationConstraint']

        return dict(file_path=f'{local_file_path}', url=f'https://{s3_bucket}.s3-{location}.amazonaws.com/{object_name}')
    except Exception as ex:
        logging.error(
            f'Error while trying to upload file: {local_file_path}', exc_info=ex)
        return None
    finally:
        if remove_local_file:
            os.remove(local_file_path)
