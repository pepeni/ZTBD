crimeRegister = '''
    CREATE TABLE IF NOT EXISTS ztbd.CrimeRegister (
        ID INT PRIMARY KEY,
        AREA_ID INT,
        AREA_NAME varchar,
        CRIME_ID INT,
        CRIME_DESCRIPTION varchar,
        VICT_AGE INT,
        VICT_SEX varchar,
        VICT_DESCENT varchar,
        PERMIS_ID INT,
        PERMIS_DESC varchar,
        WEAPON_ID INT,
        WEAPON_DESC varchar,
        STATUS_ID INT,
        STATUS_DESC varchar,
        DR_NO varchar,
        DATE_RPTD TIMESTAMP,
        DATE_OCC TIMESTAMP,
        TIME_OCC varchar,
        LOCATION varchar,
        LAT FLOAT,
        LON FLOAT
    )
'''