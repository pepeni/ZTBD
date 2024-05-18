import os

import pymongo
from dotenv import load_dotenv
from pymongo.errors import PyMongoError

from backend.crimedatapreprocessing.CrimeColumns import CrimeColumns
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
            result = collection.insert_many(self.all_data.head(count).to_dict(orient='records'))
            print(f"Inserted {len(result.inserted_ids)} records")
        except PyMongoError as e:
            print(f"Error: {e}")

    def insert_all(self):
        try:
            client = self.get_mongo_client()
            db = client[self.DB_NAME]
            collection = db[self.COLLECTION_NAME]
            result = collection.insert_many(self.all_data.to_dict(orient='records'))
            print(f"Inserted {len(result.inserted_ids)} records")
        except PyMongoError as e:
            print(f"Error: {e}")

    def update(self, count: int):
        ids = self.all_data.head(count)[CrimeColumns.ID.value].to_list()
        mongo_filter = {"id": {"$in": ids}}
        mongo_updater = {"$set": {CrimeColumns.LATITUDE.value: 12.555, CrimeColumns.AREA.value: 1}}
        try:
            client = self.get_mongo_client()
            db = client[self.DB_NAME]
            collection = db[self.COLLECTION_NAME]
            result = collection.update_many(mongo_filter, mongo_updater)
            print(f"Updated {result.modified_count} records")
        except PyMongoError as e:
            print(f"Error: {e}")

    def delete(self, count: int):
        try:
            client = self.get_mongo_client()
            db = client[self.DB_NAME]
            collection = db[self.COLLECTION_NAME]
            result = collection.delete_many({"id": {"$in": self.all_data.head(count)[CrimeColumns.ID.value].to_list()}})
            print(f"Deleted {result.deleted_count} records")
        except PyMongoError as e:
            print(f"Error: {e}")
        pass

    def delete_all(self):
        try:
            client = self.get_mongo_client()
            db = client[self.DB_NAME]
            collection = db[self.COLLECTION_NAME]
            result = collection.delete_many({})
            print(f"Removed {result.deleted_count} records")
        except PyMongoError as e:
            print(f"Error: {e}")

    def select(self, count: int):
        try:
            client = self.get_mongo_client()
            db = client[self.DB_NAME]
            collection = db[self.COLLECTION_NAME]
            result = collection.find().limit(count)
        except PyMongoError as e:
            print(f"Error: {e}")

    def where_select(self, count: int):
        try:
            client = self.get_mongo_client()
            db = client[self.DB_NAME]
            collection = db[self.COLLECTION_NAME]
            result = collection.find({CrimeColumns.AREA.value: 1}).limit(count)
        except PyMongoError as e:
            print(f"Error: {e}")

    def join_select(self, count: int):
        try:
            client = self.get_mongo_client()
            db = client[self.DB_NAME]
            collection = db[self.COLLECTION_NAME]
            result = collection.find({
                CrimeColumns.STATUS_DESC.value: 'Invest Cont'
            }).sort({CrimeColumns.DATE.value: -1}).limit(count)
        except PyMongoError as e:
            print(f"Error: {e}")

    def where_and_order_by_select(self, count: int):
        try:
            client = self.get_mongo_client()
            db = client[self.DB_NAME]
            collection = db[self.COLLECTION_NAME]
            result = collection.find({CrimeColumns.AREA.value: 1}).sort({CrimeColumns.DATE.value: -1}).limit(count)
        except PyMongoError as e:
            print(f"Error: {e}")

    def complicated_select(self, count: int):
        try:
            client = self.get_mongo_client()
            db = client[self.DB_NAME]
            collection = db[self.COLLECTION_NAME]
            result = collection.find({
                CrimeColumns.AREA_NAME.value: 'Newton',
                CrimeColumns.WEAPON_USED_DESC.value: 'RIFLE'
            }).sort({CrimeColumns.DATE.value: -1}).limit(count)
            for x in result[1:10]:
                print(x)
        except PyMongoError as e:
            print(f"Error: {e}")

    @staticmethod
    def get_mongo_client():
        load_dotenv()
        return pymongo.MongoClient(os.environ['MONGO_HOST'], int(os.environ['MONGO_PORT']),
                                   username=os.environ['MONGO_USERNAME'],
                                   password=os.environ['MONGO_PASS'],
                                   authSource=os.environ['MONGO_AUTH_DB'])
