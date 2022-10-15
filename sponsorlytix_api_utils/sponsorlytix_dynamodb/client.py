import os
import boto3

REGION = os.environ.get('AWS_REGION_NAME')
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
DYNAMO_ENDPOINT = os.environ.get('DYNAMO_ENDPOINT')


class SponsorlytixDynamoClient:

    def __init__(self):
        self.endpoint_url = DYNAMO_ENDPOINT
        self.client = boto3.client('dynamodb', endpoint_url=self.endpoint_url, region_name=REGION, aws_access_key_id=AWS_ACCESS_KEY_ID,
                                   aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

    def get_table(self, table_name):
        table = self.get_resource(self.endpoint_url).Table(table_name)
        return table.table_arn

    @classmethod
    def get_resource(cls, endpoint_url):
        return boto3.resource(
            'dynamodb',
            region_name=REGION,
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            endpoint_url=endpoint_url)

    def delete_all_tables(self):
        table_names = [
            table for table in self.client.list_tables()['TableNames']
        ]
        for table_name in table_names:
            self.client.delete_table(
                TableName=table_name
            )
