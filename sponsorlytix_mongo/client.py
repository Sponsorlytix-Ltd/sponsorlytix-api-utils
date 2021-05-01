from pymongo import MongoClient


class SponsorlytixMongoClient:

    def __init__(self, mongodb_config, db_name='sponsorlytix'):
        url, port = mongodb_config.get('url'), mongodb_config.get('port')
        client = MongoClient(url, port)
        self.client = client[db_name]

    def get_collection(self, collection_name):
        return self.client[collection_name]
