import pyodbc
import pyodbc as odbc

from backend.TableScripts.msSqlTables import *
from backend.crimedatapreprocessing.CrimeDataProcessor import CrimeDataProcessor
from backend.db.DbHandler import DbHandler
from dotenv import load_dotenv
import os
import numpy as np
import pandas as pd
from itertools import count as iter_count

class MsSqlHandler(DbHandler):
    def __init__(self, crime_data_processor: CrimeDataProcessor):
        super().__init__(crime_data_processor)
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
        # uid=<username>;
        # pwd=<password>;
        load_dotenv()
        DRIVER_NAME = os.getenv("DRIVER_NAME")
        SERVER_NAME = os.getenv("SERVER_NAME")
        DATABASE_NAME = os.getenv("DATABASE_NAME")
        connection_string = f"""
            DRIVER={{{DRIVER_NAME}}};
            SERVER={SERVER_NAME};
            DATABASE={DATABASE_NAME};
            Trusted_Connection=yes;
        """

        try:
            # Połączenie
            conn = odbc.connect(connection_string)
            cursor = conn.cursor()

            # Sprawdzam, czy istnieją tabele

            list_of_tables = {'Area': area_table, 'Crime': crime_table, 'Victim': victim_table, 'Permis': permis_table,
                              'Weapon': weapon_table, 'Status': status_table, 'CrimeRegister': crime_register_table}
            for i in list_of_tables.keys():
                cursor.execute("SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = ?", (i,))

                # Jeśli tabela istnieje
                if cursor.fetchone()[0] == 1:
                    print("Tabela", i, "istnieje.")

                # Jeśli tabela nie istnieje, dodaje ją
                else:
                    print("Dodaję tabelę", i)
                    cursor.execute(list_of_tables[i])
                    conn.commit()
        except odbc.Error as e:
            print(f"Błąd: {e}")

        finally:
            if conn:
                conn.close()

    def init_insert(self):
        load_dotenv()
        DRIVER_NAME = os.getenv("DRIVER_NAME")
        SERVER_NAME = os.getenv("SERVER_NAME")
        DATABASE_NAME = os.getenv("DATABASE_NAME")
        connection_string = f"""
                    DRIVER={{{DRIVER_NAME}}};
                    SERVER={SERVER_NAME};
                    DATABASE={DATABASE_NAME};
                    Trusted_Connection=yes;
                """

        try:
            conn = odbc.connect(connection_string)
            cursor = conn.cursor()

            # Wstaw dane do tabeli Area
            self.insert_data(self.area_data, insert_area_table, cursor, conn)

            # Wstaw dane do tabeli Crime
            self.insert_data(self.crime_code_data, insert_crime_table, cursor, conn)

            # Wstaw dane do tabeli Victim
            self.insert_data(self.victim_data, insert_victim_table, cursor, conn)

            # Wstaw dane do tabeli Permis
            self.insert_data(self.premise_data, insert_permis_table, cursor, conn)

            # Wstaw dane do tabeli Weapon
            self.insert_data(self.weapon_data, insert_weapon_table, cursor, conn)

            # Wstaw dane do tabeli Status
            self.insert_data(self.status_data, insert_status_table, cursor, conn)

            # Wstaw dane do tabeli CrimeRegister
            self.insert_data(self.crime_register_data, insert_crime_register_table, cursor, conn)

            print("Dodano dane do wszystkich tabel.")

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

            print(f"Dodano dane do tabeli.")

        except pyodbc.Error as e:
            print(f"Wystąpił błąd podczas dodawania danych do tabeli: {e}")

    def insert(self, count: int):
        load_dotenv()
        DRIVER_NAME = os.getenv("DRIVER_NAME")
        SERVER_NAME = os.getenv("SERVER_NAME")
        DATABASE_NAME = os.getenv("DATABASE_NAME")
        connection_string = f"""
                            DRIVER={{{DRIVER_NAME}}};
                            SERVER={SERVER_NAME};
                            DATABASE={DATABASE_NAME};
                            Trusted_Connection=yes;
                        """

        try:
            conn = odbc.connect(connection_string)
            cursor = conn.cursor()

            cursor.execute("SELECT MAX(ID) FROM CrimeRegister")
            max_id = cursor.fetchone()[0]

            if max_id is None:
                max_id = 0

            new_ids = list(range(max_id + 1, max_id + count + 1))

            df = self.crime_register_data.head(count).copy()
            df['id'] = new_ids

            print(df.head(count))
            # Wstaw dane do tabeli CrimeRegister
            self.insert_data(df, insert_crime_register_table, cursor, conn)

            print("Dodano dane do wszystkich tabel.")

        except pyodbc.Error as e:
            print(f"Wystąpił błąd: {e}")

        finally:
            if conn:
                conn.close()


