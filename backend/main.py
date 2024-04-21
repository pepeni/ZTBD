from backend.crimedatapreprocessing.CrimeDataProcessor import CrimeDataProcessor
from backend.db.MongoHandler import MongoHandler

crime_data_processor = CrimeDataProcessor()
mongo_handler = MongoHandler(crime_data_processor)
mongo_handler.insert(10)