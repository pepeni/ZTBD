import pyodbc as odbc
from options import DRIVER_NAME, SERVER_NAME, DATABASE_NAME


    #uid=<username>;
    #pwd=<password>;
connection_string = f"""
    DRIVER={{{DRIVER_NAME}}};
    SERVER={SERVER_NAME};
    DATABASE={DATABASE_NAME};
    Trusted_Connection=yes;
"""


try:

    conn = odbc.connect(connection_string)
    cursor = conn.cursor()

    # Tutaj możesz wykonywać operacje na bazie danych, np. wykonując zapytania SQL

    create_table_query = f'''
            CREATE TABLE osoby (
                ID INT PRIMARY KEY,
                Name NVARCHAR(255),
                Age INT
            );
        '''

    cursor.execute(create_table_query)
    conn.commit()

    insert_record_query = f'''
            INSERT INTO osoby (ID, Name, Age) VALUES (1, 'John Doe', 30), (2, 'Kacper Zieba', 28);
        '''

    cursor.execute(insert_record_query)
    conn.commit()

    select_query = f'''
        SELECT * FROM osoby;
    '''

    cursor.execute(select_query)
    rows = cursor.fetchall()
    for row in rows:
        print(row)

    drop_table_query = f'DROP TABLE osoby;'
    cursor.execute(drop_table_query)
    conn.commit()


except odbc.Error as e:
    print(f"Błąd połączenia: {e}")

finally:
    # Zawsze zamykaj połączenie, gdy skończysz pracę
    if conn:
        conn.close()