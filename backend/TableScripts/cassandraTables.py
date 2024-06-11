

crimeRegister = '''
    CREATE TABLE IF NOT EXISTS ztbd.CrimeRegister (
    ID int,
    AREA_ID int,
    AREA_NAME text,
    CRIME_ID int,
    CRIME_DESCRIPTION text,
    VICT_AGE int,
    VICT_SEX text,
    VICT_DESCENT text,
    PREMIS_ID int,
    PREMIS_DESC text,
    WEAPON_ID int,
    WEAPON_DESC text,
    STATUS_ID text,
    STATUS_DESC text,
    DATE_OCC text,
    LOCATION text,
    LAT double,
    LON double,
    PRIMARY KEY (ID)
)
'''

insert_query_crime_register = """
        INSERT INTO CrimeRegister (ID, AREA_ID, AREA_NAME, CRIME_ID, CRIME_DESCRIPTION, VICT_AGE, VICT_SEX, VICT_DESCENT, PREMIS_ID, PREMIS_DESC, WEAPON_ID, WEAPON_DESC, STATUS_ID, STATUS_DESC, DATE_OCC, LOCATION, LAT, LON)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

orderBySelectTable = '''
    CREATE TABLE IF NOT EXISTS ztbd.OrderBySelectTable (
    ID int,
    AREA_ID int,
    AREA_NAME text,
    CRIME_ID int,
    CRIME_DESCRIPTION text,
    VICT_AGE int,
    VICT_SEX text,
    VICT_DESCENT text,
    PREMIS_ID int,
    PREMIS_DESC text,
    WEAPON_ID int,
    WEAPON_DESC text,
    STATUS_ID text,
    STATUS_DESC text,
    DATE_OCC text,
    LOCATION text,
    LAT double,
    LON double,
    PRIMARY KEY (ID, DATE_OCC)
) WITH CLUSTERING ORDER BY (DATE_OCC DESC);
'''

insert_query_order_by_select = """
        INSERT INTO OrderBySelectTable (ID, AREA_ID, AREA_NAME, CRIME_ID, CRIME_DESCRIPTION, VICT_AGE, VICT_SEX, VICT_DESCENT, PREMIS_ID, PREMIS_DESC, WEAPON_ID, WEAPON_DESC, STATUS_ID, STATUS_DESC, DATE_OCC, LOCATION, LAT, LON)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

complicatedSelectTable = '''
    CREATE TABLE IF NOT EXISTS ztbd.ComplicatedSelectTable (
    ID int,
    AREA_ID int,
    AREA_NAME text,
    CRIME_ID int,
    CRIME_DESCRIPTION text,
    VICT_AGE int,
    VICT_SEX text,
    VICT_DESCENT text,
    PREMIS_ID int,
    PREMIS_DESC text,
    WEAPON_ID int,
    WEAPON_DESC text,
    STATUS_ID text,
    STATUS_DESC text,
    DATE_OCC text,
    LOCATION text,
    LAT double,
    LON double,
    PRIMARY KEY (ID, VICT_AGE)
) WITH CLUSTERING ORDER BY (VICT_AGE DESC);
'''

insert_query_complicated_select = """
        INSERT INTO ComplicatedSelectTable (ID, AREA_ID, AREA_NAME, CRIME_ID, CRIME_DESCRIPTION, VICT_AGE, VICT_SEX, VICT_DESCENT, PREMIS_ID, PREMIS_DESC, WEAPON_ID, WEAPON_DESC, STATUS_ID, STATUS_DESC, DATE_OCC, LOCATION, LAT, LON)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """