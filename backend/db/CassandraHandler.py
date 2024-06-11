import os

import pandas as pd
import numpy as np
from cassandra import ConsistencyLevel
from cassandra.cluster import Cluster
from cassandra.query import BatchStatement
from dotenv import load_dotenv
from datetime import datetime

from backend.TableScripts.cassandraTables import crimeRegister, insert_query_crime_register, orderBySelectTable, \
    complicatedSelectTable, insert_query_order_by_select, insert_query_complicated_select
from backend.crimedatapreprocessing.CrimeDataProcessor import CrimeDataProcessor
from backend.db.DbHandler import DbHandler


class CassandraHandler(DbHandler):
    def __init__(self, crime_data_processor: CrimeDataProcessor) -> None:
        super().__init__(crime_data_processor)
        self.crime_register_data = self.all_data[
            ['id', 'Area', 'Area name', 'Crime code', 'Crime code desc', 'Victim age', 'Victim sex', 'Victim descent', 'Premise code', 'Premise desc', 'Weapon used code', 'Weapon used desc', 'Status', 'Status Desc', 'Date', 'Location',
             'Latitude', 'Longitude']]
        self.crime_register_data = self.crime_register_data.dropna(subset=self.crime_register_data.columns[0])
        replacement_value = 0
        self.crime_register_data['Area'] = self.crime_register_data['Area'].fillna(replacement_value).astype(int)
        self.crime_register_data['Crime code'] = self.crime_register_data['Crime code'].fillna(replacement_value).astype(int)
        self.crime_register_data['Premise code'] = self.crime_register_data['Premise code'].fillna(replacement_value).astype(int)
        self.crime_register_data['Weapon used code'] = self.crime_register_data['Weapon used code'].fillna(replacement_value).astype(int)
        self.crime_register_data = self.crime_register_data.fillna('')
        self.crime_register_data = self.crime_register_data.replace(np.nan, None)
        self.init_database()

    def init_database(self) -> None:
        try:
            load_dotenv()
            self.CASSANDRA_HOST = os.getenv("CASSANDRA_HOST")
            self.CASSANDRA_PORT = os.getenv("CASSANDRA_PORT")

            cluster = Cluster([self.CASSANDRA_HOST], port=self.CASSANDRA_PORT)
            session = cluster.connect()
            self.keyspace = 'ztbd'

            keyspaces = session.execute("SELECT * FROM system_schema.keyspaces WHERE keyspace_name = %s", (self.keyspace,))
            if not list(keyspaces):
                # Tworzenie nowej przestrzeni kluczy, jeśli nie istnieje
                session.execute("CREATE KEYSPACE IF NOT EXISTS %s WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1}" % self.keyspace)
            session.set_keyspace(self.keyspace)

            session.execute(crimeRegister)
            session.execute(orderBySelectTable)
            session.execute(complicatedSelectTable)

        except Exception as e:
            print(f"Błąd: {e}")

        finally:
            if cluster:
                cluster.shutdown()

    def insert(self, count: int) -> None:
        try:
            cluster = Cluster([self.CASSANDRA_HOST], port=self.CASSANDRA_PORT)
            session = cluster.connect()
            session.set_keyspace(self.keyspace)

            insert_row = session.prepare(insert_query_crime_register)
            batch = BatchStatement(consistency_level=ConsistencyLevel.QUORUM)
            i = 0
            for row in self.crime_register_data.head(count).itertuples(index=False):
                if i % 100 == 0:
                    session.execute(batch)
                    batch = BatchStatement(consistency_level=ConsistencyLevel.QUORUM)
                    i = 0
                batch.add(insert_row, row)
                i += 1
            session.execute(batch)
            print("Udało się dodać dane")

            count_query = "SELECT COUNT(*) FROM CrimeRegister"
            result = session.execute(count_query)
            for row in result:
                print(f"Liczba rekordów: {row[0]}")

        except Exception as e:
            print(f"Błąd: {e}")

        finally:
            if cluster:
                cluster.shutdown()

    def insert_all(self) -> None:
        try:
            cluster = Cluster([self.CASSANDRA_HOST], port=self.CASSANDRA_PORT)
            session = cluster.connect()
            session.set_keyspace(self.keyspace)

            insert_row = session.prepare(insert_query_crime_register)
            batch = BatchStatement(consistency_level=ConsistencyLevel.QUORUM)
            i=0
            for row in self.crime_register_data.itertuples(index=False):
                if i % 100 == 0:
                    session.execute(batch)
                    batch = BatchStatement(consistency_level=ConsistencyLevel.QUORUM)
                    i = 0
                batch.add(insert_row, row)
                i+=1
            session.execute(batch)
            print("Udało się dodać dane")

            count_query = "SELECT COUNT(*) FROM CrimeRegister"
            result = session.execute(count_query)
            for row in result:
                print(f"Liczba rekordów: {row[0]}")

        except Exception as e:
            print(f"Błąd: {e}")

        finally:
            if cluster:
                cluster.shutdown()

    def insert_all_order_by_table(self) -> None:
        try:
            cluster = Cluster([self.CASSANDRA_HOST], port=self.CASSANDRA_PORT)
            session = cluster.connect()
            session.set_keyspace(self.keyspace)

            insert_row = session.prepare(insert_query_order_by_select)
            batch = BatchStatement(consistency_level=ConsistencyLevel.QUORUM)
            i = 0
            for row in self.crime_register_data.itertuples(index=False):
                if i % 100 == 0:
                    session.execute(batch)
                    batch = BatchStatement(consistency_level=ConsistencyLevel.QUORUM)
                    i = 0
                batch.add(insert_row, row)
                i += 1
            session.execute(batch)
            print("Udało się dodać dane")

        except Exception as e:
            print(f"Błąd: {e}")

        finally:
            if cluster:
                cluster.shutdown()

    def insert_all_complicated_order(self) -> None:
        try:
            cluster = Cluster([self.CASSANDRA_HOST], port=self.CASSANDRA_PORT)
            session = cluster.connect()
            session.set_keyspace(self.keyspace)

            insert_row = session.prepare(insert_query_complicated_select)
            batch = BatchStatement(consistency_level=ConsistencyLevel.QUORUM)
            i = 0
            for row in self.crime_register_data.itertuples(index=False):
                if i % 100 == 0:
                    session.execute(batch)
                    batch = BatchStatement(consistency_level=ConsistencyLevel.QUORUM)
                    i = 0
                batch.add(insert_row, row)
                i += 1
            session.execute(batch)
            print("Udało się dodać dane")

        except Exception as e:
            print(f"Błąd: {e}")

        finally:
            if cluster:
                cluster.shutdown()

    def update(self, count: int) -> None:
        try:
            cluster = Cluster([self.CASSANDRA_HOST], port=self.CASSANDRA_PORT)
            session = cluster.connect()
            session.set_keyspace(self.keyspace)

            max_id_query = f"""SELECT ID FROM CrimeRegister LIMIT {count};"""
            result = session.execute(max_id_query)
            ids = [row[0] for row in result]
            print(ids)

            update_row = session.prepare(f"""
                                    UPDATE ztbd.CrimeRegister
                                    SET LAT = 12.555, AREA_ID = 1
                                    WHERE ID = ?
                                """)
            batch = BatchStatement(consistency_level=ConsistencyLevel.QUORUM)
            i = 0
            j=0
            for id in ids:
                if i % 100 == 0:
                    session.execute(batch)
                    batch = BatchStatement(consistency_level=ConsistencyLevel.QUORUM)
                    i = 0
                batch.add(update_row, [id])
                i += 1
                j+=1
            session.execute(batch)

            print("Aktualizacja zakończona.")

        except Exception as e:
            print(f"Błąd: {e}")

        finally:
            if cluster:
                cluster.shutdown()

    def delete(self, count: int) -> None:
        try:
            cluster = Cluster([self.CASSANDRA_HOST], port=self.CASSANDRA_PORT)
            session = cluster.connect()
            session.set_keyspace(self.keyspace)

            # Pobierz odpowiednią liczbę ID do usunięcia
            id_query = f"SELECT ID FROM ztbd.CrimeRegister LIMIT {count}"
            result = session.execute(id_query)
            ids_to_delete = [row[0] for row in result]

            delete_row = session.prepare(f"DELETE FROM ztbd.CrimeRegister WHERE ID = ?")
            batch = BatchStatement(consistency_level=ConsistencyLevel.QUORUM)
            i = 0
            for id in ids_to_delete:
                if i % 100 == 0:
                    session.execute(batch)
                    batch = BatchStatement(consistency_level=ConsistencyLevel.QUORUM)
                    i = 0
                batch.add(delete_row, [id])
                i += 1
            session.execute(batch)

            print("Usunięto dane.")

        except Exception as e:
            print(f"Błąd: {e}")

        finally:
            if cluster:
                cluster.shutdown()

    def delete_all(self) -> None:
        try:
            cluster = Cluster([self.CASSANDRA_HOST], port=self.CASSANDRA_PORT)
            session = cluster.connect()
            session.set_keyspace(self.keyspace)

            # Usuwanie wszystkich danych z tabeli
            truncate_query = "TRUNCATE CrimeRegister"
            session.execute(truncate_query)
            print("Wszystkie dane zostały usunięte z tabeli CrimeRegister.")

        except Exception as e:
            print(f"Błąd: {e}")

        finally:
            if cluster:
                cluster.shutdown()

    def select_template(self, select_text: str) -> None:
        try:
            cluster = Cluster([self.CASSANDRA_HOST], port=self.CASSANDRA_PORT)
            session = cluster.connect()
            session.set_keyspace(self.keyspace)

            session.execute(select_text)

        except Exception as e:
            print(f"Błąd: {e}")

        finally:
            if cluster:
                cluster.shutdown()

    def select(self, count: int) -> None:
        self.select_template(f"SELECT * FROM CrimeRegister LIMIT {count} ALLOW FILTERING;")

    def where_select(self, count: int) -> None:
        self.select_template(f"SELECT * FROM CrimeRegister WHERE area_id = 1 LIMIT {count} ALLOW FILTERING;")

    def join_select(self, count: int) -> None:
        self.select_template(f"""
                SELECT * FROM CrimeRegister WHERE STATUS_DESC = 'Invest Cont' LIMIT {count} ALLOW FILTERING;
            """)

    def where_and_order_by_select(self, count: int) -> None:
        self.select_template(f"""
            SELECT * 
            FROM ztbd.OrderBySelectTable
            WHERE AREA_NAME = 'Central'
            LIMIT {count}
            ALLOW FILTERING;
        """)

    def complicated_select(self, count: int) -> None:
        self.select_template(f"""
            SELECT *
            FROM ztbd.ComplicatedSelectTable
            WHERE AREA_NAME = 'Central' AND WEAPON_DESC = 'RIFLE'
            LIMIT {count}
            ALLOW FILTERING;
        """)

