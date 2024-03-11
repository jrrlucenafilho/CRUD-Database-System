import psycopg2 as pg

class Table:
    def __init__(self, table_name: str, table_columns: int, cols_info: list[tuple[str, str]]):
        self.table_name = table_name
        self.table_columns = table_columns
        self.column_info = cols_info    #holds tuples with {name_of_column, data_type_of_column} for each column, in order