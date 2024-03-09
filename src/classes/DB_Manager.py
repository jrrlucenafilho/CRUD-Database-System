import psycopg2 as pg
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from Table import Table

class DB_Manager:
    def __init__(self):
        self.connection = None
        self.db_cursor = None
        self.db_name = str
        self.db_creation_query = str
        self.db_tables = [Table]

    def create_database(self):
        # Conneting to PostgreSQL
        self.connection = pg.connect("user=postgres password=postgres")
        self.connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

        # Setting up db
        self.db_cursor = self.connection.cursor()
        self.db_name = "loja_de_revendas_jequiti"
        self.db_creation_query = f"CREATE DATABASE {self.db_name}"
        self.db_cursor.execute(self.db_creation_query)

    # cols_info is a list that holds tuples with (name_of_column, data_type_of_column) for each column in the table
    # Size of cols_info must be equal to table_columns, ofc
    # For now, acceptable data types: int, str, float
    def add_table(self, table_name:str, columns:int, rows:int, cols_info:list[tuple[str, str]]):
        # Connection stuff
        self.connection = pg.connect("user=postgres password=postgres dbname=loja_de_revendas_jequiti")
        self.db_cursor = self.connection.cursor()

        # Table obj creation, attributing it to db_tables list for tracking
        self.db_tables.append(Table(table_name, columns, rows, cols_info))

        # Create table query with proper variable number of collumns in PostgreSQL db
        query = f"CREATE TABLE {table_name} ("

        for i in range(columns):
            # Correcting 'str' to 'VARCHAR(255)' for PostgreSQL to understand
            if cols_info[i][1] == "str":
                cols_info[i] = (cols_info[i][0], "VARCHAR(255)")

            query += f"{cols_info[i][0]} {cols_info[i][1]}, "
        query = query[:-2] + ")"

        # Execute query
        self.db_cursor.execute(query)
        self.connection.commit()

    def drop_table(self, table_name:str):
        # Connecting
        self.connection = pg.connect("user=postgres password=postgres dbname=loja_de_revendas_jequiti")
        self.db_cursor = self.connection.cursor()

        # Drop table query
        query = f"DROP TABLE {table_name}"

        self.db_cursor.execute(query)
        self.connection.commit()


# for testing
if __name__ == "__main__":
    db_manager = DB_Manager()
    #db_manager.add_table("produto", 4, 0, [("cod_produto", "int"), ("nome", "str"), ("preco", "float"), ("estoque", "int")])
    db_manager.drop_table("produto")