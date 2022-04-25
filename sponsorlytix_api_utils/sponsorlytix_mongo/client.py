from pymongo import MongoClient


class SponsorlytixMongoClient:

    def __init__(self, host, port, db_name):
        client = MongoClient(host, port)
        self.database = client.get_database(db_name)

    def get_collection(self, collection_name):
        return self.database.get_collection(collection_name)

    @classmethod
    def get_database(cls, host, port, db_name):
        client = MongoClient(host, port)
        return client.get_database(db_name)

    @classmethod
    def drop_database(self, host, port, db_name):
        client = MongoClient(host, port)
        if db_name in client.list_database_names():
            client.drop_database(db_name)
