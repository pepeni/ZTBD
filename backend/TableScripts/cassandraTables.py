crimeRegister = '''
    CREATE TABLE IF NOT EXISTS ztbd.CrimeRegister (
    ID int,
    AREA_ID int,
    CRIME_ID int,
    VICTIM_ID int,
    PERMIS_ID int,
    WEAPON_ID int,
    STATUS_ID int,
    DATE_OCC timestamp,
    LOCATION text,
    LAT double,
    LON double,
    PRIMARY KEY (ID, DATE_OCC)
)
'''

joinSelectTable = '''
    CREATE TABLE IF NOT EXISTS ztbd.JoinSelectTable (
    STATUS_DESC text PRIMARY KEY,
    ID int,
    AREA_ID int,
    CRIME_ID int,
    VICTIM_ID int,
    PERMIS_ID int,
    WEAPON_ID int,
    STATUS_ID int,
    DATE_OCC timestamp,
    LOCATION text,
    LAT double,
    LON double
)
'''

complicatedSelectTable = '''
    CREATE TABLE IF NOT EXISTS ztbd.ComplicatedSelectTable (
    ID int,
    AREA_ID int,
    AREA_NAME text,
    CRIME_ID int,
    VICTIM_ID int,
    VICT_AGE int,
    VICT_SEX text,
    VICT_DESCENT text,
    PERMIS_ID int,
    WEAPON_ID int,
    WEAPON_DESC text,
    STATUS_ID int,
    DATE_OCC timestamp,
    LOCATION text,
    LAT double,
    LON double,
    PRIMARY KEY ((AREA_NAME, WEAPON_DESC), ID)
)
'''