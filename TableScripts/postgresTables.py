crime_register_table = '''
CREATE TABLE CrimeRegister (
    ID SERIAL PRIMARY KEY,
    AREA_ID INT REFERENCES Area(AREA_ID),
    CRIME_ID INT REFERENCES Crime(CRIME_ID),
    VICTIM_ID INT REFERENCES Victim(VICTIM_ID),
    PERMIS_ID INT REFERENCES Permis(PERMIS_ID),
    WEAPON_ID INT REFERENCES Weapon(WEAPON_ID),
    STATUS_ID INT REFERENCES Status(STATUS_ID),
    DR_NO VARCHAR(9),
    DATE_RPTD DATE,
    DATE_OCC DATE,
    TIME_OCC VARCHAR(20),
    LOCATION VARCHAR(40),
    LAT FLOAT,
    LON FLOAT
)
'''

area_table = '''
CREATE TABLE Area (
    AREA_ID SERIAL PRIMARY KEY,
    AREA_NAME VARCHAR(30)
)
'''

crime_table = '''
CREATE TABLE Crime (
    CRIME_ID SERIAL PRIMARY KEY,
    DESCRIPTION VARCHAR(60)
)
'''

victim_table = '''
CREATE TABLE Victim (
    VICTIM_ID SERIAL PRIMARY KEY,
    VICT_AGE INT,
    VICT_SEX VARCHAR(1),
    VICT_DESCENT VARCHAR(1)
)
'''

permis_table = '''
CREATE TABLE Permis (
    PERMIS_ID SERIAL PRIMARY KEY,
    PERMIS_DESC VARCHAR(60)
)
'''

weapon_table = '''
CREATE TABLE Weapon (
    WEAPON_ID SERIAL PRIMARY KEY,
    WEAPON_DESC VARCHAR(60)
)
'''

status_table = '''
CREATE TABLE Status (
    STATUS_ID SERIAL PRIMARY KEY,
    STATUS_DESC VARCHAR(60)
)
'''