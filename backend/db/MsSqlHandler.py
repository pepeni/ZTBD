import pyodbc
import pyodbc as odbc

from backend.TableScripts.msSqlTables import *
from backend.crimedatapreprocessing.CrimeDataProcessor import CrimeDataProcessor
from backend.db.DbHandler import DbHandler
from dotenv import load_dotenv
import os
import numpy as np


class MsSqlHandler(DbHandler):
    def __init__(self, crime_data_processor: CrimeDataProcessor):
        super().__init__(crime_data_processor)

        load_dotenv()
        DRIVER_NAME = os.getenv("MS_SQL_DRIVER_NAME")
        SERVER_NAME = os.getenv("MS_SQL_SERVER_NAME")
        DATABASE_NAME = os.getenv("MS_SQL_DATABASE_NAME")
        self.connection_string = f"""
                                            DRIVER={{{DRIVER_NAME}}};
                                            SERVER={SERVER_NAME};
                                            DATABASE={DATABASE_NAME};
                                            Trusted_Connection=yes;
                                        """

        temporary_data = self.all_data
        temporary_data['Victim ID'] = range(1, len(temporary_data) + 1)
        temporary_data.drop(columns=['Victim age'], inplace=True)
        self.victim_data = self.victim_data.copy()
        self.victim_data.insert(0, 'Victim ID', list(range(1, len(self.all_data) + 1)))
        self.crime_register_data = temporary_data[
            ['id', 'Area', 'Crime code', 'Victim ID', 'Premise code', 'Weapon used code', 'Status', 'Date', 'Location',
             'Latitude', 'Longitude']]

        self.init_database()

    def init_database(self):
        try:
            # Połączenie
            with odbc.connect(self.connection_string) as conn:
                cursor = conn.cursor()
                insert_all = False

                list_of_tables = {'Area': area_table, 'Crime': crime_table, 'Victim': victim_table, 'Permis': permis_table,
                                  'Weapon': weapon_table, 'Status': status_table, 'CrimeRegister': crime_register_table}
                for i in list_of_tables.keys():
                    cursor.execute("SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = ?", (i,))

                    # Jeśli tabela istnieje
                    if cursor.fetchone()[0] == 1:
                        pass

                    # Jeśli tabela nie istnieje, dodaje ją
                    else:
                        print("Dodaję tabelę", i)
                        cursor.execute(list_of_tables[i])
                        conn.commit()
                        insert_all = True

                if insert_all:

                    # Wstaw dane do wszystkich tabeli poza crime register
                    self.insert_data(self.area_data, insert_area_table, cursor, conn)
                    self.insert_data(self.crime_code_data, insert_crime_table, cursor, conn)
                    self.insert_data(self.victim_data, insert_victim_table, cursor, conn)
                    self.insert_data(self.premise_data, insert_permis_table, cursor, conn)
                    self.insert_data(self.weapon_data, insert_weapon_table, cursor, conn)
                    self.insert_data(self.status_data, insert_status_table, cursor, conn)

        except odbc.Error as e:
            print(f"Błąd: {e}")

    def insert_all(self):
        try:
            with odbc.connect(self.connection_string) as conn:
                cursor = conn.cursor()

                # Wstaw dane do crime register tabeli
                self.insert_data(self.crime_register_data, insert_crime_register_table, cursor, conn)

        except pyodbc.Error as e:
            print(f"Wystąpił błąd: {e}")

    def insert_data(self, df, insert_query, cursor, conn):

        try:
            # Wstaw dane do tabeli
            df = df.dropna(subset=df.columns[0])
            df = df.replace(np.nan, None)

            for row in df.itertuples(index=False):
                cursor.execute(insert_query, row)
            conn.commit()

        except pyodbc.Error as e:
            print(f"Wystąpił błąd podczas dodawania danych do tabeli: {e}")

    # Wstaw count danych do tabeli CrimeRegister
    def insert(self, count: int):
        try:
            with odbc.connect(self.connection_string) as conn:
                cursor = conn.cursor()
                df = self.crime_register_data.head(count).copy()
                self.insert_data(df, insert_crime_register_table, cursor, conn)
                print(f"Dodano {count} danych do Crime register.")

        except pyodbc.Error as e:
            print(f"Wystąpił błąd: {e}")

    def delete(self, count: int):
        try:
            with odbc.connect(self.connection_string) as conn:
                cursor = conn.cursor()

                query = """
                        DELETE FROM CrimeRegister
                        WHERE ID IN (
                            SELECT TOP {} ID
                            FROM CrimeRegister
                            ORDER BY ID DESC
                        )
                        """.format(count)

                cursor.execute(query)
                conn.commit()

                print(f"Usunięto {count} wierszy o największym ID.")

        except pyodbc.Error as e:
            print(f"Wystąpił błąd: {e}")

    def delete_all(self):

        try:
            with odbc.connect(self.connection_string) as conn:
                cursor = conn.cursor()

                query = """DELETE FROM CrimeRegister;"""

                cursor.execute(query)
                conn.commit()

                print(f"Usunięto Wszystkie dane z Crime Register")

        except pyodbc.Error as e:
            print(f"Wystąpił błąd: {e}")

    def update(self, count: int):

        try:
            with odbc.connect(self.connection_string) as conn:
                cursor = conn.cursor()

                query = """
                    UPDATE CrimeRegister 
                    SET LON = ?, AREA_ID = ?
                    WHERE ID IN (
                        SELECT TOP(?) ID 
                        FROM CrimeRegister 
                        ORDER BY ID DESC
                    )
                """

                lon_value = 12.555
                area_value = 1

                cursor.execute(query, (lon_value, area_value, count))
                conn.commit()

                print(f"Zaktualizowano {count} wierszy o największym ID.")

        except pyodbc.Error as e:
            print(f"Wystąpił błąd: {e}")

    def select(self, count: int):
        self.select_template(f"SELECT TOP({count}) * FROM CrimeRegister;")

    def where_select(self, count: int):
        self.select_template(f"SELECT TOP({count}) * FROM CrimeRegister WHERE AREA_ID = 1;")

    def join_select(self, count: int):
        self.select_template(f"""
            SELECT TOP({count}) c.*, s.STATUS_DESC 
            FROM CrimeRegister c 
            JOIN Status s ON s.STATUS_ID = c.STATUS_ID 
            WHERE s.STATUS_DESC = 'Invest Cont';
            """)

    def where_and_order_by_select(self, count: int):
        self.select_template(f"""
            SELECT TOP({count}) * 
            FROM CrimeRegister 
            WHERE AREA_ID = 1
            ORDER BY DATE_OCC DESC;
            """)

    def complicated_select(self, count: int):
        self.select_template(f"""
            SELECT TOP({count}) *
            FROM CrimeRegister c 
            JOIN Area a ON a.AREA_ID = c.AREA_ID 
            JOIN Weapon w ON w.WEAPON_ID = c.WEAPON_ID
            JOIN Victim v ON v.VICTIM_ID = c.VICTIM_ID
            WHERE a.AREA_NAME = 'Central' AND w.WEAPON_DESC = 'RIFLE'
            ORDER BY v.VICT_AGE;
            """)

    def select_template(self, select_text):

        # Wykonanie zapytania
        try:
            with odbc.connect(self.connection_string) as conn:
                cursor = conn.cursor()
                query = f"""{select_text}"""

                cursor.execute(query)

        except pyodbc.Error as e:
            print(f"Wystąpił błąd: {e}")
