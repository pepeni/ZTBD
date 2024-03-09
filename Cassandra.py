from cassandra.cluster import Cluster
from options import HOST, PORT

cluster = Cluster([HOST], port=PORT)
session = cluster.connect("store")

rows = session.execute('SELECT * FROM shopping_cart;')

for row in rows:
    print(row)