import pymongo
from pymongo.errors import PyMongoError

from dBInits.DbInit import DbInit
from dBInits.options import MONGO_HOST, MONGO_PORT, MONGO_PASS, MONGO_USERNAME, MONGO_AUTH_DB


class MongoInit(DbInit):
    COLLECTION_NAME = 'Crimes'

    def insert_data(self):
        try:
            client = pymongo.MongoClient(MONGO_HOST, MONGO_PORT,
                                         username=MONGO_USERNAME,
                                         password=MONGO_PASS,
                                         authSource=MONGO_AUTH_DB)

            db = client[self.DB_NAME]
            collection = db[self.COLLECTION_NAME]
            collection.insert_many(self.all_data.to_dict(orient='records'))

        except PyMongoError as e:
            print(f"Error: {e}")
