from pymongo import MongoClient


class SponsorlytixMongoClient:

    def __init__(self, host, port, db_name):
        client = MongoClient(host, port)
        self.client = client.get_database(db_name)

    def get_collection(self, collection_name):
        return self.client.get_collection(collection_name)

    @classmethod
    def get_client(cls, host, port, db_name):
        client = MongoClient(host, port)
        return client.get_database(db_name)