import os

import pymongo
from dotenv import load_dotenv
from pymongo.errors import PyMongoError

from backend.crimedatapreprocessing.CrimeDataProcessor import CrimeDataProcessor
from backend.db.DbHandler import DbHandler


class MongoHandler(DbHandler):
    COLLECTION_NAME = 'Crimes'

    def __init__(self, crime_data_processor: CrimeDataProcessor):
        super().__init__(crime_data_processor)
        self.init_database()

    def init_database(self):
        try:
            client = self.get_mongo_client()
            db = client[self.DB_NAME]
            collection = db[self.COLLECTION_NAME]
        except PyMongoError as e:
            print(f"Error: {e}")

    def insert(self, count: int):
        try:
            client = self.get_mongo_client()
            db = client[self.DB_NAME]
            collection = db[self.COLLECTION_NAME]
            collection.insert_many(self.all_data.head(count).to_dict(orient='records'))
            print(f"Inserted {count} records")
        except PyMongoError as e:
            print(f"Error: {e}")

    def insert_all(self):
        pass

    def update(self, count: int):
        pass

    def delete(self, count: int):
        pass

    def delete_all(self):
        try:
            client = self.get_mongo_client()
            db = client[self.DB_NAME]
            collection = db[self.COLLECTION_NAME]
            collection.delete_many({})
            print(f"Removed all records")
        except PyMongoError as e:
            print(f"Error: {e}")

    @staticmethod
    def get_mongo_client():
        load_dotenv()
        return pymongo.MongoClient(os.environ['MONGO_HOST'], int(os.environ['MONGO_PORT']),
                                   username=os.environ['MONGO_USERNAME'],
                                   password=os.environ['MONGO_PASS'],
                                   authSource=os.environ['MONGO_AUTH_DB'])
