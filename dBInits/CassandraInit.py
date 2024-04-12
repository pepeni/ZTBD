from cassandra.cluster import Cluster
from options import CASSANDRA_HOST, CASSANDRA_PORT
from TableScripts.cassandraTables import crimeRegister

def cassandraInit():

    try:
        cluster = Cluster([CASSANDRA_HOST], port=CASSANDRA_PORT)
        session = cluster.connect()
        keyspace = 'ztbd'

        keyspaces = session.execute("SELECT * FROM system_schema.keyspaces WHERE keyspace_name = %s", (keyspace,))
        if not keyspaces:
            # Tworzenie nowej przestrzeni kluczy, jeśli nie istnieje
            session.execute("CREATE KEYSPACE IF NOT EXISTS %s WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1}" % keyspace)
        session.set_keyspace(keyspace)

        session.execute(crimeRegister)

        #ToDo Dodać wartości do tabeli, jeśli ich jeszcze nie ma

    except Exception as e:
        print(f"Błąd: {e}")

    finally:
        if cluster:
            cluster.shutdown()

if __name__ == "__main__":
    cassandraInit()