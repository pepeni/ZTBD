import psycopg2
from psycopg2 import OperationalError

from options import POSTGRES_HOST, POSTGRES_PORT, POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB
from TableScripts.postgresTables import area_table, crime_table, victim_table, permis_table, weapon_table, status_table, crime_register_table


def postgresInit():
    try:
        connection = psycopg2.connect(
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
            host=POSTGRES_HOST,
            port=POSTGRES_PORT,
            database=POSTGRES_DB
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


if __name__ == "__main__":
    postgresInit()
