import requests
import os.path
import pandas as pd

from backend.crimedatapreprocessing.CrimeColumns import CrimeColumns


class CrimeDataProcessor:
    CRIME_DATA_URL = "https://data.lacity.org/api/views/2nrs-mtv8/rows.csv?accessType=DOWNLOAD"
    CRIME_DATA_FILENAME = 'crimedata.csv'

    CRIME_CODE_COLUMNS = [CrimeColumns.CRIME_CODE.value, CrimeColumns.CRIME_CODE_DESC.value]
    AREA_COLUMNS = [CrimeColumns.AREA.value, CrimeColumns.AREA_NAME.value]
    PREMISE_COLUMNS = [CrimeColumns.PREMISE_CODE.value, CrimeColumns.PREMISE_DESC.value]
    WEAPON_COLUMNS = [CrimeColumns.WEAPON_USED_CODE.value, CrimeColumns.WEAPON_USED_DESC.value]
    STATUS_COLUMNS = [CrimeColumns.STATUS.value, CrimeColumns.STATUS_DESC.value]
    VICTIM_COLUMNS = [CrimeColumns.VICTIM_AGE.value, CrimeColumns.VICTIM_SEX.value, CrimeColumns.VICTIM_DESCENT.value]

    def __init__(self):
        self.download_crime_data()
        df = pd.read_csv(self.CRIME_DATA_FILENAME)
        df = self.drop_unnecessary_columns(df)
        self.crime_data = self.rename_columns(df)

    def crime_code_data(self) -> pd.DataFrame:
        return self.extract_crime_code_data(self.crime_data)

    def area_data(self) -> pd.DataFrame:
        return self.extract_area_data(self.crime_data)

    def premise_data(self) -> pd.DataFrame:
        return self.extract_premise_data(self.crime_data)

    def weapon_data(self) -> pd.DataFrame:
        return self.extract_weapon_data(self.crime_data)

    def status_data(self) -> pd.DataFrame:
        return self.extract_status_data(self.crime_data)

    def victim_data(self) -> pd.DataFrame:
        return self.extract_victim_data(self.crime_data)

    def all_data(self) -> pd.DataFrame:
        return self.crime_data

    def download_crime_data(self):
        if not os.path.exists(self.CRIME_DATA_FILENAME):
            print("Downloading crime data ...")
            response = requests.get(self.CRIME_DATA_URL)
            with open(self.CRIME_DATA_FILENAME, 'w') as file:
                file.write(response.text)
            print("Downloading completed")

    @staticmethod
    def drop_unnecessary_columns(df: pd.DataFrame) -> pd.DataFrame:
        columns_to_drop = ["Date Rptd", "TIME OCC", "Rpt Dist No", "Part 1-2", "Mocodes", "Cross Street"]
        return df.drop(columns=columns_to_drop)

    @staticmethod
    def rename_columns(df: pd.DataFrame) -> pd.DataFrame:
        rename_dict = {
            'DR_NO': CrimeColumns.ID.value,
            'DATE OCC': CrimeColumns.DATE.value,
            'AREA': CrimeColumns.AREA.value,
            'AREA NAME': CrimeColumns.AREA_NAME.value,
            'Crm Cd': CrimeColumns.CRIME_CODE.value,
            'Crm Cd Desc': CrimeColumns.CRIME_CODE_DESC.value,
            'Vict Age': CrimeColumns.VICTIM_AGE.value,
            'Vict Sex': CrimeColumns.VICTIM_SEX.value,
            'Vict Descent': CrimeColumns.VICTIM_DESCENT.value,
            'Premis Cd': CrimeColumns.PREMISE_CODE.value,
            'Premis Desc': CrimeColumns.PREMISE_DESC.value,
            'Weapon Used Cd': CrimeColumns.WEAPON_USED_CODE.value,
            'Weapon Desc': CrimeColumns.WEAPON_USED_DESC.value,
            'Status': CrimeColumns.STATUS.value,
            'Desc': CrimeColumns.STATUS_DESC.value,
            'Crm Cd 1': CrimeColumns.CRIME_CODE_1.value,
            'Crm Cd 2': CrimeColumns.CRIME_CODE_2.value,
            'Crm Cd 3': CrimeColumns.CRIME_CODE_3.value,
            'Crm Cd 4': CrimeColumns.CRIME_CODE_4.value,
            'LOCATION': CrimeColumns.LOCATION.value,
            'LAT': CrimeColumns.LATITUDE.value,
            'LON': CrimeColumns.LONGITUDE.value
        }
        return df.rename(columns=rename_dict)

    def extract_crime_code_data(self, df: pd.DataFrame) -> pd.DataFrame:
        return df[self.CRIME_CODE_COLUMNS].drop_duplicates(self.CRIME_CODE_COLUMNS[0])

    def extract_area_data(self, df: pd.DataFrame) -> pd.DataFrame:
        return df[self.AREA_COLUMNS].drop_duplicates(self.AREA_COLUMNS[0])

    def extract_premise_data(self, df: pd.DataFrame) -> pd.DataFrame:
        return df[self.PREMISE_COLUMNS].drop_duplicates(self.PREMISE_COLUMNS[0])

    def extract_weapon_data(self, df: pd.DataFrame) -> pd.DataFrame:
        return df[self.WEAPON_COLUMNS].drop_duplicates(self.WEAPON_COLUMNS[0])

    def extract_status_data(self, df: pd.DataFrame) -> pd.DataFrame:
        return df[self.STATUS_COLUMNS].drop_duplicates(self.STATUS_COLUMNS[0])

    def extract_victim_data(self, df: pd.DataFrame) -> pd.DataFrame:
        return df[self.VICTIM_COLUMNS]