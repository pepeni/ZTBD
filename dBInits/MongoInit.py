import pymongo
from pymongo.errors import PyMongoError
from options import MONGO_HOST, MONGO_PORT, MONGO_PASS, MONGO_USERNAME, MONGO_AUTH_DB

def mongoInit():
    try:
        client = pymongo.MongoClient(MONGO_HOST, MONGO_PORT,
                                     username=MONGO_USERNAME,
                                     password=MONGO_PASS,
                                     authSource=MONGO_AUTH_DB)

        db = client['ZTBD']
        collection = db['CrimeRegister']

        #TODO wprowadzić dane, jeśli ich nie ma

    except PyMongoError as e:
        print(f"Błąd: {e}")

    finally:
        if client:
            client.close()

if __name__ == "__main__":
    mongoInit()