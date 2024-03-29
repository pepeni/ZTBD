import pymongo
from options import MONGO_HOST, MONGO_PORT, MONGO_PASS, MONGO_USERNAME, MONGO_AUTH_DB

client = pymongo.MongoClient(MONGO_HOST, MONGO_PORT,
                             username=MONGO_USERNAME,
                             password=MONGO_PASS,
                             authSource=MONGO_AUTH_DB)

db = client['ZTBD']

collection = db['crimes']

document = {'klucz': 'moja wartość'}
collection.insert_one(document)

# Przykład odczytu danych z kolekcji
result = collection.find()
for i in result:
    print(i)

# Zakończenie połączenia
client.close()