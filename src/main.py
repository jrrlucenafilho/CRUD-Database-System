from classes.CRUD_Manager import CRUD_Manager
import psycopg2 as pg
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

'''
Program assumes "user=postgres password=postgres" as db credentials
And 'loja_de_revendas_jequiti' as db name
'''
# Exists-check and creation funcs for db and tables
def database_exists(db_name):
    #Connecting to the default database
    connection = pg.connect("user=postgres password=postgres")
    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    db_cursor = connection.cursor()

    #Query to check if database exists
    query = f"""
    SELECT EXISTS (
        SELECT datname FROM pg_catalog.pg_database 
        WHERE datname = '{db_name}'
    );
    """

    db_cursor.execute(query)
    exists = db_cursor.fetchone()[0]

    return exists


def init_database():
    connection = pg.connect("user=postgres password=postgres")
    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    #Setting up db
    db_cursor = connection.cursor()
    db_name = "loja_de_revendas_jequiti"

    if not database_exists(db_name):
        db_creation_query = f"CREATE DATABASE {db_name}"
        db_cursor.execute(db_creation_query)


def table_exists(table_name):
    connection = pg.connect("user=postgres password=postgres dbname=loja_de_revendas_jequiti")
    db_cursor = connection.cursor()

    #Query to check if table exists
    query = f"""
    SELECT EXISTS (
        SELECT FROM information_schema.tables 
        WHERE  table_name   = '{table_name}'
    );
    """

    db_cursor.execute(query)
    exists = db_cursor.fetchone()[0]

    return exists


def init_table(table_name:str, columns:int, cols_info:list[tuple[str, str]]):
    connection = pg.connect("user=postgres password=postgres dbname=loja_de_revendas_jequiti")
    db_cursor = connection.cursor()

    #Create table query with proper variable number of collumns in PostgreSQL db
    query = f"CREATE TABLE {table_name} ("
    query += "cod_produto SERIAL PRIMARY KEY, " #cod_produto is prim key auto generated by db

    for i in range(columns-1):
        #Correcting 'str' to 'VARCHAR(255)' for PostgreSQL to understand
        if cols_info[i][1] == "str":
            cols_info[i] = (cols_info[i][0], "VARCHAR(255)")

        query += f"{cols_info[i][0]} {cols_info[i][1]}, "
    query = query[:-2] + ")"

    #Execute query
    db_cursor.execute(query)
    connection.commit()


def main():
    #DB exists check
    if database_exists('loja_de_revendas_jequiti') is False:
        init_database()

    #Table exists check
    if table_exists('produtos') is False:
        init_table('produtos', 4, [("nome", "str"), ("valor", "float"), ("estoque", "int")])

    crud_manager = CRUD_Manager()
    crud_manager.get_root().mainloop()

if __name__ == "__main__":
    main()
