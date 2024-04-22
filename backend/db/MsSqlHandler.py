import pyodbc as odbc

from backend.TableScripts.msSqlTables import area_table, crime_table, victim_table, permis_table, weapon_table, \
    status_table, crime_register_table
from backend.crimedatapreprocessing.CrimeDataProcessor import CrimeDataProcessor
from backend.db.DbHandler import DbHandler
from dotenv import load_dotenv
import os

class MsSqlHandler(DbHandler):
    def __init__(self, crime_data_processor: CrimeDataProcessor):
        super().__init__(crime_data_processor)
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
                    # TODO Dodać rekordy
                    conn.commit()
        except odbc.Error as e:
            print(f"Błąd: {e}")

        finally:
            if conn:
                conn.close()

    def insert(self, count: int):
        pass
