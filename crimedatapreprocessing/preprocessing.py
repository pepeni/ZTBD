import pandas as pd

from crime_columns import CrimeColumns
import download


def drop_unnecessary_columns(df: pd.DataFrame) -> pd.DataFrame:
    columns_to_drop = ["Date Rptd", "TIME OCC", "Rpt Dist No", "Part 1-2", "Mocodes", "Cross Street"]
    return df.drop(columns=columns_to_drop)


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


CRIME_CODE_COLUMNS = [CrimeColumns.CRIME_CODE.value, CrimeColumns.CRIME_CODE_DESC.value]
AREA_COLUMNS = [CrimeColumns.AREA.value, CrimeColumns.AREA_NAME.value]
PREMISE_COLUMNS = [CrimeColumns.PREMISE_CODE.value, CrimeColumns.PREMISE_DESC.value]
WEAPON_COLUMNS = [CrimeColumns.WEAPON_USED_CODE.value, CrimeColumns.WEAPON_USED_DESC.value]
STATUS_COLUMNS = [CrimeColumns.STATUS.value, CrimeColumns.STATUS_DESC.value]
VICTIM_COLUMNS = [CrimeColumns.VICTIM_AGE.value, CrimeColumns.VICTIM_SEX.value, CrimeColumns.VICTIM_DESCENT.value]


def extract_crime_code_data(df: pd.DataFrame) -> pd.DataFrame:
    return df[CRIME_CODE_COLUMNS].drop_duplicates(CRIME_CODE_COLUMNS[0])


def extract_area_data(df: pd.DataFrame) -> pd.DataFrame:
    return df[AREA_COLUMNS].drop_duplicates(AREA_COLUMNS[0])


def extract_premise_data(df: pd.DataFrame) -> pd.DataFrame:
    return df[PREMISE_COLUMNS].drop_duplicates(PREMISE_COLUMNS[0])


def extract_weapon_data(df: pd.DataFrame) -> pd.DataFrame:
    return df[WEAPON_COLUMNS].drop_duplicates(WEAPON_COLUMNS[0])


def extract_status_data(df: pd.DataFrame) -> pd.DataFrame:
    return df[STATUS_COLUMNS].drop_duplicates(STATUS_COLUMNS[0])


def extract_victim_data(df: pd.DataFrame) -> pd.DataFrame:
    return df[VICTIM_COLUMNS]


download.download_crime_data()

df = pd.read_csv(download.CRIME_DATA_FILENAME)
df = drop_unnecessary_columns(df)
df = rename_columns(df)

crime_code_df = extract_crime_code_data(df)
area_df = extract_area_data(df)
premise_df = extract_premise_data(df)
weapon_df = extract_weapon_data(df)

status_df = extract_status_data(df)
victim_df = extract_victim_data(df)
