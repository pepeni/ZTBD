import pyodbc as odbc
from options import DRIVER_NAME, SERVER_NAME, DATABASE_NAME
from TableScripts.msSqlTables import area_table, crime_table, victim_table, permis_table, weapon_table, status_table, crime_register_table


def msSqlInit():
    # uid=<username>;
    # pwd=<password>;
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

        list_of_table_name = {'Area': area_table, 'Crime': crime_table, 'Victim': victim_table, 'Permis': permis_table, 'Weapon': weapon_table, 'Status': status_table, 'CrimeRegister': crime_register_table}
        for i in list_of_table_name.keys():
            cursor.execute("SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = ?", (i,))

            # Jeśli tabela istnieje
            if cursor.fetchone()[0] == 1:
                print("Tabela", i, "istnieje.")

            # Jeśli tabela nie istnieje, dodaje ją
            else:
                print("Dodaję tabelę", i)
                cursor.execute(list_of_table_name[i])
                # TODO Dodać rekordy
                conn.commit()



    except odbc.Error as e:
        print(f"Błąd: {e}")

    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    msSqlInit()