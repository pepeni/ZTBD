from abc import abstractmethod, ABC

import pandas as pd


class DbInit(ABC):
    DB_NAME = 'ZTBD'

    def __init__(self, crime_code: pd.DataFrame, area: pd.DataFrame, premise: pd.DataFrame, weapon: pd.DataFrame,
                 status: pd.DataFrame, victim: pd.DataFrame, all_data: pd.DataFrame):
        self.crime_code = crime_code
        self.area = area
        self.premise = premise
        self.weapon = weapon
        self.status = status
        self.victim = victim
        self.all_data = all_data

    @abstractmethod
    def insert_data(self):
        pass
