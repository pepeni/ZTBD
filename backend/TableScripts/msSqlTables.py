crime_register_table = '''
CREATE TABLE CrimeRegister (
    ID INT PRIMARY KEY,
    AREA_ID INT FOREIGN KEY REFERENCES Area(AREA_ID),
    CRIME_ID INT FOREIGN KEY REFERENCES Crime(CRIME_ID),
    VICTIM_ID INT FOREIGN KEY REFERENCES Victim(VICTIM_ID),
    PERMIS_ID INT FOREIGN KEY REFERENCES Permis(PERMIS_ID),
    WEAPON_ID INT FOREIGN KEY REFERENCES Weapon(WEAPON_ID),
    STATUS_ID VARCHAR(5) FOREIGN KEY REFERENCES Status(STATUS_ID),
    DATE_OCC DATE,
    LOCATION VARCHAR(40),
    LAT FLOAT,
    LON FLOAT
)
'''

insert_crime_register_table = '''INSERT INTO CrimeRegister (ID, AREA_ID, CRIME_ID, VICTIM_ID, PERMIS_ID, WEAPON_ID, STATUS_ID, DATE_OCC, LOCATION, LAT, LON)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);'''

area_table = '''
CREATE TABLE Area (
    AREA_ID INT PRIMARY KEY,
    AREA_NAME VARCHAR(30)
)
'''

insert_area_table = '''INSERT INTO Area (AREA_ID, AREA_NAME)
VALUES (?, ?);'''

crime_table = '''
CREATE TABLE Crime (
    CRIME_ID INT PRIMARY KEY,
    DESCRIPTION VARCHAR(60)
)
'''

insert_crime_table = '''INSERT INTO Crime (CRIME_ID, DESCRIPTION)
VALUES (?, ?);'''

victim_table = '''
CREATE TABLE Victim (
    VICTIM_ID INT PRIMARY KEY,
    VICT_AGE INT,
    VICT_SEX VARCHAR(1),
    VICT_DESCENT VARCHAR(1)
)
'''

insert_victim_table = '''INSERT INTO Victim (VICTIM_ID, VICT_AGE, VICT_SEX, VICT_DESCENT)
VALUES (?, ?, ?, ?);'''

permis_table = '''
CREATE TABLE Permis (
    PERMIS_ID INT PRIMARY KEY,
    PERMIS_DESC VARCHAR(100)
)
'''

insert_permis_table = '''INSERT INTO Permis (PERMIS_ID, PERMIS_DESC)
VALUES (?, ?);'''

weapon_table = '''
CREATE TABLE Weapon (
    WEAPON_ID INT PRIMARY KEY,
    WEAPON_DESC VARCHAR(60)
)
'''

insert_weapon_table = '''INSERT INTO Weapon (WEAPON_ID, WEAPON_DESC)
VALUES (?, ?);'''

status_table = '''
CREATE TABLE Status (
    STATUS_ID VARCHAR(5) PRIMARY KEY,
    STATUS_DESC VARCHAR(60)
)
'''

insert_status_table = '''INSERT INTO Status (STATUS_ID, STATUS_DESC)
VALUES (?, ?);'''

