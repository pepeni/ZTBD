from cassandra.cluster import Cluster

from backend.TableScripts.cassandraTables import crimeRegister
from backend.crimedatapreprocessing.CrimeDataProcessor import CrimeDataProcessor
from backend.db.DbHandler import DbHandler


class CassandraHandler(DbHandler):
    def __init__(self, crime_data_processor: CrimeDataProcessor):
        super().__init__(crime_data_processor)
        self.init_database()

    def init_database(self):
        pass
        # try:
        #     cluster = Cluster([CASSANDRA_HOST], port=CASSANDRA_PORT)
        #     session = cluster.connect()
        #     keyspace = 'ztbd'
        #
        #     keyspaces = session.execute("SELECT * FROM system_schema.keyspaces WHERE keyspace_name = %s", (keyspace,))
        #     if not keyspaces:
        #         # Tworzenie nowej przestrzeni kluczy, jeśli nie istnieje
        #         session.execute("CREATE KEYSPACE IF NOT EXISTS %s WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1}" % keyspace)
        #     session.set_keyspace(keyspace)
        #
        #     session.execute(crimeRegister)
        #
        #     #ToDo Dodać wartości do tabeli, jeśli ich jeszcze nie ma
        #
        # except Exception as e:
        #     print(f"Błąd: {e}")
        #
        # finally:
        #     if cluster:
        #         cluster.shutdown()

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
