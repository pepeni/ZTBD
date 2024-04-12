crime_register_table = '''
CREATE TABLE CrimeRegister (
    ID INT PRIMARY KEY,
    AREA_ID INT FOREIGN KEY REFERENCES Area(AREA_ID),
    CRIME_ID INT FOREIGN KEY REFERENCES Crime(CRIME_ID),
    DR_NO Varchar(9),
    DATE_RPTD DATE,
    DATE_OCC DATE,
    TIME_OCC Varchar(30)
)
'''

area_table = '''
CREATE TABLE Area (
    AREA_ID INT PRIMARY KEY,
    AREA_NAME VARCHAR(30)
)
'''

crime_table = '''
CREATE TABLE Crime (
    CRIME_ID INT PRIMARY KEY,
    DESCRIPTION VARCHAR(60)
)
'''