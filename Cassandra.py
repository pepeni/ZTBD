from cassandra.cluster import Cluster
from options import CASSANDRA_HOST, CASSANDRA_PORT

cluster = Cluster([CASSANDRA_HOST], port=CASSANDRA_PORT)
session = cluster.connect()

keyspace = 'ztbd'

keyspaces = session.execute("SELECT * FROM system_schema.keyspaces WHERE keyspace_name = %s", (keyspace,))
if not keyspaces:
    # Tworzenie nowej przestrzeni kluczy, jeśli nie istnieje
    session.execute("CREATE KEYSPACE IF NOT EXISTS %s WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1}" % keyspace)
session.set_keyspace(keyspace)

create_table_query = """
    CREATE TABLE IF NOT EXISTS users (
        user_id TEXT PRIMARY KEY,
        username TEXT,
        email TEXT,
        age INT
    );
"""
session.execute(create_table_query)

insert_user_query = """
    INSERT INTO users (user_id, username, email, age)
    VALUES (%s, %s, %s, %s)
"""

user_id = 'jan_kowalski2'  # Ciąg znaków jako klucz główny
username = 'Jan Kowalski2'
email = 'jan.kowalski@examplee.com'
age = 31

# Wykonanie zapytania wstawiania
session.execute(insert_user_query, (user_id, username, email, age))

rows = session.execute('SELECT * FROM users;')

for row in rows:
    print(row)

cluster.shutdown()