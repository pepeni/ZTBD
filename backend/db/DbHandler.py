from abc import abstractmethod, ABC

from backend.crimedatapreprocessing.CrimeDataProcessor import CrimeDataProcessor


class DbHandler(ABC):
    DB_NAME = 'ZTBD'

    def __init__(self, crime_data_processor: CrimeDataProcessor):
        self.all_data = crime_data_processor.all_data()
        self.crime_code_data = crime_data_processor.crime_code_data()
        self.area_data = crime_data_processor.area_data()
        self.premise_data = crime_data_processor.premise_data()
        self.weapon_data = crime_data_processor.weapon_data()
        self.status_data = crime_data_processor.status_data()
        self.victim_data = crime_data_processor.victim_data()

    @abstractmethod
    def insert(self, count: int):
        pass
