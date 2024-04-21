from crimedatapreprocessing.preprocessing import raw_data, clean_data
from dBInits.MongoInit import MongoInit

raw_data = raw_data()
crime_code, area, premise, weapon, status, victim = clean_data()

mongo_init = MongoInit(crime_code, area, premise, weapon, status, victim, raw_data)
mongo_init.insert_data()
