from abc import abstractmethod, ABC

from backend.crimedatapreprocessing.CrimeDataProcessor import CrimeDataProcessor


class DbHandler(ABC):
    DB_NAME = 'ZTBD'

    def __init__(self, crime_data_processor: CrimeDataProcessor) -> None:
        self.all_data = crime_data_processor.all_data()
        self.crime_code_data = crime_data_processor.crime_code_data()
        self.area_data = crime_data_processor.area_data()
        self.premise_data = crime_data_processor.premise_data()
        self.weapon_data = crime_data_processor.weapon_data()
        self.status_data = crime_data_processor.status_data()
        self.victim_data = crime_data_processor.victim_data()

    @abstractmethod
    def insert(self, count: int) -> None:
        pass

    @abstractmethod
    def insert_all(self) -> None:
        pass

    @abstractmethod
    def update(self, count: int) -> None:
        pass

    @abstractmethod
    def delete(self, count: int) -> None:
        pass

    @abstractmethod
    def delete_all(self) -> None:
        pass

    @abstractmethod
    def select(self, count: int) -> None:
        pass

    @abstractmethod
    def where_select(self, count: int) -> None:
        pass

    @abstractmethod
    def join_select(self, count: int) -> None:
        pass

    @abstractmethod
    def where_and_order_by_select(self, count: int) -> None:
        pass

    @abstractmethod
    def complicated_select(self, count: int) -> None:
        pass

    @abstractmethod
    def complicated_with_aggregation_select(self, count: int) -> None:
        pass
