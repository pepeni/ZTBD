import os

import psycopg2
from dotenv import load_dotenv
from psycopg2 import OperationalError

from backend.TableScripts.postgresTables import area_table, crime_table, victim_table, permis_table, weapon_table, status_table, crime_register_table
from backend.crimedatapreprocessing.CrimeDataProcessor import CrimeDataProcessor
from backend.db.DbHandler import DbHandler


class PostgreSqlHandler(DbHandler):
    def __init__(self, crime_data_processor: CrimeDataProcessor):
        super().__init__(crime_data_processor)
        self.init_database()

    def init_database(self):
        try:
            load_dotenv()
            connection = psycopg2.connect(
                user=os.environ["POSTGRES_USER"],
                password=os.environ["POSTGRES_PASSWORD"],
                host=os.environ["POSTGRES_HOST"],
                port=os.environ["POSTGRES_PORT"],
                database=os.environ["POSTGRES_DB"]
            )

            cursor = connection.cursor()

            # Sprawdzam, czy istnieją tabele
            list_of_tables = {'area': area_table, 'crime': crime_table, 'victim': victim_table, 'permis': permis_table, 'weapon': weapon_table, 'status': status_table, 'crime_register': crime_register_table}
            for table_name, table_script in list_of_tables.items():
                cursor.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_name = %s", (table_name,))
                # Jeśli tabela istnieje
                if cursor.fetchone()[0] == 1:
                    print("Tabela", table_name, "istnieje.")
                # Jeśli tabela nie istnieje, dodaję ją
                else:
                    print("Dodaję tabelę", table_name)
                    cursor.execute(table_script)

            connection.commit()

        except OperationalError as e:
            print(f"Błąd: {e}")

        finally:
            if connection:
                connection.close()

    def insert(self, count: int):
        pass

    def insert_all(self):
        pass

    def update(self, count: int):
        pass

    def delete(self, count: int):
        pass

    def delete_all(self):
        pass