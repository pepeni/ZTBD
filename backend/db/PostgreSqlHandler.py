import os

import psycopg2
import numpy as np
from dotenv import load_dotenv
from pandas import DataFrame
from psycopg2 import OperationalError

from backend.TableScripts.postgresTables import area_table, crime_table, victim_table, permis_table, weapon_table, \
    status_table, crime_register_table, insert_area_query, insert_crime_query, \
    insert_victim_query, insert_permis_query, insert_weapon_query, insert_status_query, insert_crime_register_query
from backend.crimedatapreprocessing.CrimeDataProcessor import CrimeDataProcessor
from backend.db.DbHandler import DbHandler


class PostgreSqlHandler(DbHandler):
    def __init__(self, crime_data_processor: CrimeDataProcessor) -> None:
        super().__init__(crime_data_processor)

        load_dotenv()
        self.connection = psycopg2.connect(
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            host=os.getenv("POSTGRES_HOST"),
            port=os.getenv("POSTGRES_PORT"),
            database=os.getenv("POSTGRES_DB")
        )

        temporary_data = self.all_data
        temporary_data['Victim ID'] = range(1, len(temporary_data) + 1)
        temporary_data.drop(columns=['Victim age'], inplace=True)
        self.victim_data = self.victim_data.copy()
        self.victim_data.insert(0, 'Victim ID', list(range(1, len(self.all_data) + 1)))
        self.crime_register_data = temporary_data[
            ['id', 'Area', 'Crime code', 'Victim ID', 'Premise code', 'Weapon used code', 'Status', 'Date', 'Location',
             'Latitude', 'Longitude']]

        self.init_database()

    def init_database(self) -> None:
        try:
            cursor = self.connection.cursor()
            insert_all = False
            list_of_tables = {'area': area_table, 'crime': crime_table, 'victim': victim_table, 'permis': permis_table,
                              'weapon': weapon_table, 'status': status_table, 'crimeregister': crime_register_table}
            for table_name, table_script in list_of_tables.items():
                cursor.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_name = %s", (table_name,))
                if cursor.fetchone()[0] == 1:
                    pass
                else:
                    cursor.execute(table_script)
                    insert_all = True
            self.connection.commit()

            if insert_all:
                self.insert_data(self.area_data, insert_area_query)
                self.insert_data(self.crime_code_data, insert_crime_query)
                self.insert_data(self.victim_data, insert_victim_query)
                self.insert_data(self.premise_data, insert_permis_query)
                self.insert_data(self.weapon_data, insert_weapon_query)
                self.insert_data(self.status_data, insert_status_query)

        except OperationalError as e:
            print(f"Błąd: {e}")
        finally:
            cursor.close()

    def insert_data(self, df: DataFrame, insert_query: str) -> None:
        try:
            cursor = self.connection.cursor()
            df = df.dropna(subset=df.columns[0])
            df = df.replace(np.nan, None)

            for row in df.itertuples(index=False):
                cursor.execute(insert_query, row)
            self.connection.commit()

        except OperationalError as e:
            print(f"Wystąpił błąd podczas dodawania danych do tabeli: {e}")
        finally:
            cursor.close()

    def insert(self, count: int) -> None:
        try:
            df = self.crime_register_data.head(count).copy()
            self.insert_data(df, insert_crime_register_query)
        except OperationalError as e:
            print(f"Wystąpił błąd: {e}")

    def insert_all(self) -> None:
        try:
            self.insert_data(self.crime_register_data, insert_crime_register_query)
        except OperationalError as e:
            print(f"Wystąpił błąd: {e}")

    def update(self, count: int) -> None:
        try:
            cursor = self.connection.cursor()
            query = """
                        UPDATE crimeregister
                        SET lon = %s, area_id = %s
                        WHERE id IN (
                            SELECT id
                            FROM crimeregister
                            ORDER BY id DESC
                            LIMIT %s
                        )
                    """
            cursor.execute(query, (12.555, 1, count))
            self.connection.commit()
        except OperationalError as e:
            print(f"Wystąpił błąd: {e}")
        finally:
            cursor.close()

    def delete(self, count: int) -> None:
        try:
            cursor = self.connection.cursor()
            query = f"""
                        DELETE FROM crimeregister
                        WHERE id IN (
                            SELECT id
                            FROM crimeregister
                            ORDER BY id DESC
                            LIMIT {count}
                        )
                    """
            cursor.execute(query)
            self.connection.commit()
        except OperationalError as e:
            print(f"Wystąpił błąd: {e}")
        finally:
            cursor.close()

    def delete_all(self) -> None:
        try:
            cursor = self.connection.cursor()
            query = """DELETE FROM crimeregister;"""
            cursor.execute(query)
            self.connection.commit()
        except OperationalError as e:
            print(f"Wystąpił błąd: {e}")
        finally:
            cursor.close()

    def select_template(self, select_text: str) -> None:
        try:
            cursor = self.connection.cursor()
            cursor.execute(select_text)
            # records = cursor.fetchall()
        except OperationalError as e:
            print(f"Wystąpił błąd: {e}")
        finally:
            cursor.close()

    def select(self, count: int) -> None:
        self.select_template(f"SELECT * FROM crimeregister LIMIT {count};")

    def where_select(self, count: int) -> None:
        self.select_template(f"SELECT * FROM crimeregister WHERE area_id = 1 LIMIT {count};")

    def join_select(self, count: int) -> None:
        self.select_template(f"""
            SELECT c.*, s.status_desc 
            FROM crimeregister c 
            JOIN status s ON s.status_id = c.status_id 
            WHERE s.status_desc = 'Invest Cont'
            LIMIT {count};
        """)

    def where_and_order_by_select(self, count: int) -> None:
        self.select_template(f"""
            SELECT * 
            FROM crimeregister 
            WHERE area_id = 1
            ORDER BY date_occ DESC
            LIMIT {count};
        """)

    def complicated_select(self, count: int) -> None:
        self.select_template(f"""
            SELECT c.*, a.area_name, w.weapon_desc, v.vict_age
            FROM crimeregister c 
            JOIN area a ON a.area_id = c.area_id 
            JOIN weapon w ON w.weapon_id = c.weapon_id
            JOIN victim v ON v.victim_id = c.victim_id
            WHERE a.area_name = 'Central' AND w.weapon_desc = 'RIFLE'
            ORDER BY v.vict_age
            LIMIT {count};
        """)
