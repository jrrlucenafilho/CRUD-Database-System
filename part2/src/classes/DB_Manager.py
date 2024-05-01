import psycopg2 as pg
from classes.Client import Client
from classes.Seller import Seller
from classes.Product import Product
from classes.Stock import Stock


class DB_Manager:
    def __init__(self):
        self.connection = None
        self.db_cursor = None
        self.db_name = str
        self.db_creation_query = str

        #Instances of each
        self.stock = Stock()
        self.client = Client()
        self.seller = Seller()
        self.produto = Product()


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


    '''Getters from tables'''
    def get_stock(self):
        return self.stock.get_stock()

    def get_one_stock(self, cod_produto:int):
        return self.stock.get_one_stock(cod_produto)

    def get_products(self):
        return self.produto.get_products()


    '''Logging in functions'''
    def validate_client_login(self, email:str, senha:str):
        return self.client.login(email, senha)

    def validate_seller_login(self, email:str, senha:str):
        return self.seller.login(email, senha)


    '''Registering functions'''
    def register_client(self, nome:str, email:str, senha:str, cpf:str, data_nascimento:str):
        #Check if client already exists first
        if self.client.search_client_by_cpf(cpf):
            return False

        self.client.add_client(nome, email, senha, cpf, data_nascimento)

        return True


    def register_seller(self, nome:str, email:str, senha:str, cpf:str, data_nascimento:str):
        #Check if seller already exists first
        if self.seller.search_seller_by_cpf(cpf):
            return False

        self.seller.add_seller(nome, email, senha, cpf, data_nascimento)

        return True


    '''Purchase functions'''
    def purchase_product(self, cod_produto:int, cod_cliente:int, quantidade:int, forma_pagamento:str):
        #Check if product exists
        if not self.product_exists_by_code(cod_produto):
            return False

        #Check if there's enough stock
        if not self.stock.has_stock(cod_produto, quantidade):
            return False

        #Check if client exists
        if not self.client.client_exists(cod_cliente):
            return False

        #Check if client has enough money
        if not self.client.has_enough_money(cod_cliente, cod_produto, quantidade):
            return False

        #Effective purchase
        self.seller.sell_product(cod_cliente, cod_produto, quantidade, forma_pagamento)
        self.stock.purchase_product(cod_produto, quantidade)
        self.client.purchase_product(cod_cliente, cod_produto, quantidade)

        return True