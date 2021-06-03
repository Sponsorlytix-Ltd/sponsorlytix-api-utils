import os

from pymongo import MongoClient


class SponsorlytixMongoClient:

    def __init__(self, mongodb_config, db_name='sponsorlytix'):
        url, port = mongodb_config.get('url'), mongodb_config.get('port')
        client = MongoClient(url, port)
        self.client = client[db_name]

    def get_collection(self, collection_name):
        return self.client[collection_name]

    @classmethod
    def get_client(db_name='sponsorlytix'):
        mongo_url = os.environ.get('MONGO_URL')
        mongo_conn = MongoClient(mongo_url, 27017)
        return mongo_conn[db_name]
