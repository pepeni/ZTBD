crime_register_table = '''
CREATE TABLE IF NOT EXISTS CrimeRegister (
    ID SERIAL PRIMARY KEY,
    AREA_ID INT REFERENCES Area(AREA_ID),
    CRIME_ID INT REFERENCES Crime(CRIME_ID),
    VICTIM_ID INT REFERENCES Victim(VICTIM_ID),
    PERMIS_ID INT REFERENCES Permis(PERMIS_ID),
    WEAPON_ID INT REFERENCES Weapon(WEAPON_ID),
    STATUS_ID VARCHAR(5) REFERENCES Status(STATUS_ID),
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
CREATE TABLE IF NOT EXISTS Area (
    AREA_ID SERIAL PRIMARY KEY,
    AREA_NAME VARCHAR(30)
)
'''

crime_table = '''
CREATE TABLE IF NOT EXISTS Crime (
    CRIME_ID SERIAL PRIMARY KEY,
    DESCRIPTION VARCHAR(60)
)
'''

victim_table = '''
CREATE TABLE IF NOT EXISTS Victim (
    VICTIM_ID SERIAL PRIMARY KEY,
    VICT_AGE INT,
    VICT_SEX VARCHAR(1),
    VICT_DESCENT VARCHAR(1)
)
'''

permis_table = '''
CREATE TABLE IF NOT EXISTS Permis (
    PERMIS_ID SERIAL PRIMARY KEY,
    PERMIS_DESC VARCHAR(100)
)
'''

weapon_table = '''
CREATE TABLE IF NOT EXISTS Weapon (
    WEAPON_ID SERIAL PRIMARY KEY,
    WEAPON_DESC VARCHAR(60)
)
'''

status_table = '''
CREATE TABLE IF NOT EXISTS Status (
    STATUS_ID VARCHAR(5) PRIMARY KEY,
    STATUS_DESC VARCHAR(60)
)
'''

insert_crime_register_query = '''
INSERT INTO CrimeRegister (ID, AREA_ID, CRIME_ID, VICTIM_ID, PERMIS_ID, WEAPON_ID, STATUS_ID, DATE_OCC, LOCATION, LAT, LON)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
'''

insert_area_query = '''
INSERT INTO Area (AREA_ID, AREA_NAME)
VALUES (%s, %s);
'''

insert_crime_query = '''
INSERT INTO Crime (CRIME_ID, DESCRIPTION)
VALUES (%s, %s);
'''

insert_victim_query = '''
INSERT INTO Victim (VICTIM_ID, VICT_AGE, VICT_SEX, VICT_DESCENT)
VALUES (%s, %s, %s, %s);
'''

insert_permis_query = '''
INSERT INTO Permis (PERMIS_ID, PERMIS_DESC)
VALUES (%s, %s);
'''

insert_weapon_query = '''
INSERT INTO Weapon (WEAPON_ID, WEAPON_DESC)
VALUES (%s, %s);
'''

insert_status_query = '''
INSERT INTO Status (STATUS_ID, STATUS_DESC)
VALUES (%s, %s);
'''
