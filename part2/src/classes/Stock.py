import psycopg2 as pg

class Stock:
    def __init__(self):
        self.connection = pg.connect("user=postgres password=postgres dbname=loja_de_revendas_jequiti")
        self.connection.set_isolation_level(pg.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        self.cursor = self.connection.cursor()

    #This returns the entire table
    def get_stock(self):
        query = """
        SELECT * FROM estoque;
        """
        self.cursor.execute(query)
        stock = self.cursor.fetchall()

        return stock

    #This returns a single row from the table, based on the foreign key cod_produto
    def get_one_stock(self, cod_produto:int):
        query = f"""
        SELECT * FROM estoque WHERE cod_produto = {cod_produto};
        """
        self.cursor.execute(query)
        stock = self.cursor.fetchone()

        return stock[0]
