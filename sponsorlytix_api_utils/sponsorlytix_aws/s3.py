import json
import logging
import numbers
import boto3
import os


class S3Client:
    def __init__(self):
        self.client = boto3.client('s3')

    def upload_json_to_s3(self, bucket_name: str, data, object_key: str):
        self.client.put_object(
            Body=json.dumps(data),
            Bucket=bucket_name,
            Key=object_key)

    def download_file(self, bucket_name: str, object_key: str, destination: str):
        self.client.download_file(bucket_name, object_key, destination)

    def get_object(self, bucket_name: str, object_key: str):
        return self.client.get_object(Bucket=bucket_name, Key=object_key)

    def put_object(self, bucket_name: str, binary_data, object_key: str):
        self.client.put_object(Body=binary_data, Bucket=bucket_name,
                               Key=object_key)

    def generate_presigned_url(self, bucket_name: str, object_key: str, expire_in: int):
        return self.client.generate_presigned_url(
            ClientMethod='get_object',
            Params={'Bucket': bucket_name, 'Key': object_key},
            ExpiresIn=expire_in)

    def upload_file_to_S3(self, local_file_path, object_key, remove_local_file=True, multipart_upload=False, bucket_name=None):
        """
        Upload a file to an S3 bucket

        :param local_file_path: File to upload
        :param bucket: Bucket to upload to
        :param object_name: S3 object name
        :return: URLs if file was uploaded, else None
        """
        try:
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

            self.client.upload_file(
                local_file_path, bucket_name, object_key, Config=multipart_config
            )
            location = self.client.get_bucket_location(
                Bucket=bucket_name)['LocationConstraint']

            return dict(file_path=f'{local_file_path}', url=f'https://{bucket_name}.s3-{location}.amazonaws.com/{object_key}')
        except Exception as ex:
            logging.error(
                f'Error while trying to upload file: {local_file_path}', exc_info=ex)
            return None
        finally:
            if remove_local_file:
                os.remove(local_file_path)
