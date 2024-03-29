import psycopg2 as pg
from classes.Table import Table

class DB_Manager:
    def __init__(self):
        self.connection = None
        self.db_cursor = None
        self.db_name = str
        self.db_creation_query = str
        self.db_tables = [Table]


    #cols_info is a list that holds tuples with (name_of_column, data_type_of_column) for each column in the table
    #Size of cols_info must be equal (table_columns - 1), cause cod_prod is self generated by the db, so no need to have info for it
    #For now, acceptable data types: int, str, float
    def add_table(self, table_name:str, columns:int, cols_info:list[tuple[str, str]]):
        #Connection stuff
        self.connection = pg.connect("user=postgres password=postgres dbname=loja_de_revendas_jequiti")
        self.db_cursor = self.connection.cursor()

        #Table obj creation, attributing it to db_tables list for tracking (only be useful later w/ more tables)
        self.db_tables.append(Table(table_name, columns, cols_info))

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
        self.db_cursor.execute(query)
        self.connection.commit()


    def drop_table(self, table_name:str):
        #Connecting
        self.connection = pg.connect("user=postgres password=postgres dbname=loja_de_revendas_jequiti")
        self.db_cursor = self.connection.cursor()

        #Drop table query
        query = f"DROP TABLE {table_name}"

        self.db_cursor.execute(query)
        self.connection.commit()

    '''Insertion funcs'''
    def insert_product(self, nome:str, valor:float, estoque:int):
        #Connecting
        self.connection = pg.connect("user=postgres password=postgres dbname=loja_de_revendas_jequiti")
        self.db_cursor = self.connection.cursor()

        #First check the table to see if there's a product with the same name or code (will be done outside)

        #Insert product query
        query = f"INSERT INTO produtos (nome, valor, estoque) VALUES ('{nome}', {valor}, {estoque})"

        self.db_cursor.execute(query)
        self.connection.commit()

    '''Utility funcs for insertion / removal'''
    def product_exists_by_name(self, name:str):
        #Connecting
        self.connection = pg.connect("user=postgres password=postgres dbname=loja_de_revendas_jequiti")
        self.db_cursor = self.connection.cursor()

        #Create a cursor object
        self.db_cursor = self.connection.cursor()

        #Execute a SQL SELECT statement
        self.db_cursor.execute(f"""
            SELECT * FROM produtos
            WHERE nome = '{name}'
        """)

        #Fetch one row
        row = self.db_cursor.fetchone()
        #TODO: Add try_except blocks to handle closing (and closse connections duh)
        #If a row was fetched, the product exists
        return row is not None

    def product_exists_by_code(self, code:int):
        #Connecting
        self.connection = pg.connect("user=postgres password=postgres dbname=loja_de_revendas_jequiti")
        self.db_cursor = self.connection.cursor()

        #Create a cursor object
        self.db_cursor = self.connection.cursor()

        #Execute a SQL SELECT statement
        self.db_cursor.execute(f"""
            SELECT * FROM produtos
            WHERE cod_produto = {code}
        """)

        #Fetch one row
        row = self.db_cursor.fetchone()

        #If a row was fetched, the product exists
        return row is not None

    '''Removal funcs'''
    def remove_product_by_code(self, cod_produto:int):
        #Connecting
        self.connection = pg.connect("user=postgres password=postgres dbname=loja_de_revendas_jequiti")
        self.db_cursor = self.connection.cursor()

        #Remove product query
        query = f"DELETE FROM produtos WHERE cod_produto = {cod_produto}"

        self.db_cursor.execute(query)
        self.connection.commit()

    def remove_product_by_name(self, nome:str):
        #Connecting
        self.connection = pg.connect("user=postgres password=postgres dbname=loja_de_revendas_jequiti")
        self.db_cursor = self.connection.cursor()

        #Warn if product with this name does not exist
        if not self.product_exists_by_name(nome):
            print("Produto a ser removido não encontrado")
            return

        #Remove product query
        query = f"DELETE FROM produtos WHERE nome = '{nome}'"

        self.db_cursor.execute(query)
        self.connection.commit()

    '''List products func'''
    #Returns a list with all table rows (list of tuples)
    def list_products(self):
        #Connecting
        self.connection = pg.connect("user=postgres password=postgres dbname=loja_de_revendas_jequiti")
        self.db_cursor = self.connection.cursor()

        #List products query
        query = "SELECT * FROM produtos"

        self.db_cursor.execute(query)
        rows = self.db_cursor.fetchall()

        return rows

    def search_product_by_name(self, nome:str):
        #Connecting
        self.connection = pg.connect("user=postgres password=postgres dbname=loja_de_revendas_jequiti")
        self.db_cursor = self.connection.cursor()

        #Check if product exists
        if not self.product_exists_by_name(nome):
            return False

        #Search product query
        query = f"SELECT * FROM produtos WHERE nome = '{nome}'"

        self.db_cursor.execute(query)
        rows = self.db_cursor.fetchall()

        return rows[0]

    '''Editing rows funcs'''
    #edit_choice should be one of the following: "cod_produto", "nome", "valor", "estoque"
    #Special care when editing "cod_produto", as it's the primary key
    #Taking advantage of python's dynamic typing to allow for any type of new_attribute
    #Allows for one change at a time
    def edit_product_by_name(self, nome:str, edit_choice:str, new_attribute):
        #Connecting
        self.connection = pg.connect("user=postgres password=postgres dbname=loja_de_revendas_jequiti")
        self.db_cursor = self.connection.cursor()

        #Check if it exists first
        if self.product_exists_by_name(nome) is False:
            return False

        #Edit attribute based on edit_choice
        if edit_choice == "cod_produto":
            #Check if new code already exists
            if self.product_exists_by_code(new_attribute):
                return False

            self.edit_product_code_by_name(nome, new_attribute)
            return

        if edit_choice == "nome":
            #Check if new name already exists in db
            if self.product_exists_by_name(new_attribute):
                return False

            self.edit_product_name_by_name(nome, new_attribute)
            return

        if edit_choice == "valor":
            self.edit_product_value_by_name(nome, new_attribute)
            return

        if edit_choice == "estoque":
            self.edit_product_stock_by_name(nome, new_attribute)
            return

    '''Utility funcs for editing rows'''
    def edit_product_code_by_name(self, nome:str, new_code:int):
        query = f"UPDATE produtos SET cod_produto = {new_code} WHERE nome = '{nome}'"

        self.db_cursor.execute(query)
        self.connection.commit()

    def edit_product_name_by_name(self, nome:str, new_name:str):
        query = f"UPDATE produtos SET nome = '{new_name}' WHERE nome = '{nome}'"

        self.db_cursor.execute(query)
        self.connection.commit()

    def edit_product_value_by_name(self, nome:str, new_value:float):
        query = f"UPDATE produtos SET valor = {new_value} WHERE nome = '{nome}'"

        self.db_cursor.execute(query)
        self.connection.commit()

    def edit_product_stock_by_name(self, nome:str, new_stock:int):
        query = f"UPDATE produtos SET estoque = {new_stock} WHERE nome = '{nome}'"

        self.db_cursor.execute(query)
        self.connection.commit()

    #Check if table is empty, returning true if so
    def is_table_empty(self, table_name):
        #Connecting
        self.connection = pg.connect("user=postgres password=postgres dbname=loja_de_revendas_jequiti")
        self.db_cursor = self.connection.cursor()

        #Query to check if table is empty
        query = f"SELECT 1 FROM {table_name} LIMIT 1"

        self.db_cursor.execute(query)
        result = self.db_cursor.fetchone()

        #If fetchone() didn't return any rows, the table is empty
        return result is None

    def table_exists(self, table_name):
        #Connecting
        self.connection = pg.connect("user=postgres password=postgres dbname=loja_de_revendas_jequiti")
        self.db_cursor = self.connection.cursor()

        #Query to check if table exists
        query = f"""
        SELECT EXISTS (
            SELECT FROM information_schema.tables 
            WHERE  table_name   = '{table_name}'
        );
        """

        self.db_cursor.execute(query)
        exists = self.db_cursor.fetchone()[0]

        return exists