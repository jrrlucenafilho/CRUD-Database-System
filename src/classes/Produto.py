import psycopg2 as pg
import psycopg2.pool
from classes.Table import Table

class DB_Manager:
    def __init__(self):
        self.connection_pool = pg.pool.SimpleConnectionPool(
            1, 10, user='postgres', password='postgres', dbname='loja_de_revendas_jequiti'
        )
        self.db_tables = [Table]

    def add_table(self, table_name: str, columns: int, cols_info: list[tuple[str, str]]):
        try:
            connection = self.connection_pool.getconn()
            db_cursor = connection.cursor()
            cols_info.append(('fabricadoEm', 'VARCHAR(30)'))
            query = f"CREATE TABLE IF NOT EXISTS {table_name} (cod_produto SERIAL PRIMARY KEY, "
            for col_name, col_type in cols_info:
                if col_type == "str":
                    col_type = "VARCHAR(255)"
                query += f"{col_name} {col_type}, "
            query = query[:-2] + ")"
            db_cursor.execute(query)
            connection.commit()
            self.db_tables.append(Table(table_name, columns, cols_info))
        except Exception as e:
            print(f"Error while adding table: {e}")
        finally:
            if connection:
                db_cursor.close()
                self.connection_pool.putconn(connection)

    def drop_table(self, table_name: str):
        try:
            connection = self.connection_pool.getconn()
            db_cursor = connection.cursor()
            query = f"DROP TABLE IF EXISTS {table_name}"
            db_cursor.execute(query)
            connection.commit()
        except Exception as e:
            print(f"Error while dropping table: {e}")
        finally:
            if connection:
                db_cursor.close()
                self.connection_pool.putconn(connection)

    def insert_product(self, nome: str, valor: float, estoque: int, fabricadoEm: str):
        try:
            connection = self.connection_pool.getconn()
            db_cursor = connection.cursor()
            query = f"INSERT INTO produtos (nome, valor, estoque, fabricadoEm) VALUES (%s, %s, %s, %s)"
            db_cursor.execute(query, (nome, valor, estoque, fabricadoEm))
            connection.commit()
        except Exception as e:
            print(f"Error while inserting product: {e}")
        finally:
            if connection:
                db_cursor.close()
                self.connection_pool.putconn(connection)

    def product_exists_by_name(self, name: str):
        try:
            connection = self.connection_pool.getconn()
            db_cursor = connection.cursor()
            db_cursor.execute(f"SELECT * FROM produtos WHERE nome = '{name}'")
            row = db_cursor.fetchone()
            return row is not None
        except Exception as e:
            print(f"Error while checking product existence by name: {e}")
            return False
        finally:
            db_cursor.close()
            self.connection_pool.putconn(connection)

    def product_exists_by_code(self, code: int):
        try:
            connection = self.connection_pool.getconn()
            db_cursor = connection.cursor()
            db_cursor.execute(f"SELECT * FROM produtos WHERE cod_produto = {code}")
            row = db_cursor.fetchone()
            return row is not None
        except Exception as e:
            print(f"Error while checking product existence by code: {e}")
            return False
        finally:
            db_cursor.close()
            self.connection_pool.putconn(connection)

    def remove_product_by_code(self, cod_produto: int):
        try:
            connection = self.connection_pool.getconn()
            db_cursor = connection.cursor()
            query = f"DELETE FROM produtos WHERE cod_produto = {cod_produto}"
            db_cursor.execute(query)
            connection.commit()
        except Exception as e:
            print(f"Error while removing product by code: {e}")
        finally:
            db_cursor.close()
            self.connection_pool.putconn(connection)

    def remove_product_by_name(self, nome: str):
        try:
            connection = self.connection_pool.getconn()
            db_cursor = connection.cursor()
            if not self.product_exists_by_name(nome):
                return
            query = f"DELETE FROM produtos WHERE nome = '{nome}'"
            db_cursor.execute(query)
            connection.commit()
        except Exception as e:
            print(f"Error while removing product by name: {e}")
        finally:
            db_cursor.close()
            self.connection_pool.putconn(connection)

    def list_products(self):
        try:
            connection = self.connection_pool.getconn()
            db_cursor = connection.cursor()
            query = "SELECT * FROM produtos"
            db_cursor.execute(query)
            rows = db_cursor.fetchall()
            return rows
        except Exception as e:
            print(f"Error while listing products: {e}")
            return []
        finally:
            db_cursor.close()
            self.connection_pool.putconn(connection)

    def search_product_by_name(self, nome: str):
        try:
            connection = self.connection_pool.getconn()
            db_cursor = connection.cursor()
            if not self.product_exists_by_name(nome):
                return False
            query = f"SELECT * FROM produtos WHERE nome = '{nome}'"
            db_cursor.execute(query)
            rows = db_cursor.fetchall()
            return rows[0] if rows else False
        except Exception as e:
            print(f"Error while searching product by name: {e}")
            return False
        finally:
            db_cursor.close()
            self.connection_pool.putconn(connection)

    def edit_product_by_name(self, nome: str, edit_choice: str, new_attribute):
        try:
            connection = self.connection_pool.getconn()
            db_cursor = connection.cursor()
            if self.product_exists_by_name(nome) is False:
                return False
            if edit_choice == "cod_produto":
                if self.product_exists_by_code(new_attribute):
                    return False
                self.edit_product_code_by_name(nome, new_attribute)
                return
            if edit_choice == "nome":
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
        except Exception as e:
            print(f"Error while editing product by name: {e}")
        finally:
            db_cursor.close()
            self.connection_pool.putconn(connection)

    def edit_product_code_by_name(self, nome: str, new_code: int):
        try:
            connection = self.connection_pool.getconn()
            db_cursor = connection.cursor()
            query = f"UPDATE produtos SET cod_produto = {new_code} WHERE nome = '{nome}'"
            db_cursor.execute(query)
            connection.commit()
        except Exception as e:
            print(f"Error while editing product code by name: {e}")
        finally:
            db_cursor.close()
            self.connection_pool.putconn(connection)

    def edit_product_name_by_name(self, nome: str, new_name: str):
        try:
            connection = self.connection_pool.getconn()
            db_cursor = connection.cursor()
            query = f"UPDATE produtos SET nome = '{new_name}' WHERE nome = '{nome}'"
            db_cursor.execute(query)
            connection.commit()
        except Exception as e:
            print(f"Error while editing product name by name: {e}")
        finally:
            db_cursor.close()
            self.connection_pool.putconn(connection)

    def edit_product_value_by_name(self, nome: str, new_value: float):
        try:
            connection = self.connection_pool.getconn()
            db_cursor = connection.cursor()
            query = f"UPDATE produtos SET valor = {new_value} WHERE nome = '{nome}'"
            db_cursor.execute(query)
            connection.commit()
        except Exception as e:
            print(f"Error while editing product value by name: {e}")
        finally:
            db_cursor.close()
            self.connection_pool.putconn(connection)

    def edit_product_stock_by_name(self, nome: str, new_stock: int):
        try:
            connection = self.connection_pool.getconn()
            db_cursor = connection.cursor()
            query = f"UPDATE produtos SET estoque = {new_stock} WHERE nome = '{nome}'"
            db_cursor.execute(query)
            connection.commit()
        except Exception as e:
            print(f"Error while editing product stock by name: {e}")
        finally:
            db_cursor.close()
            self.connection_pool.putconn(connection)

    def is_table_empty(self, table_name):
        try:
            connection = self.connection_pool.getconn()
            db_cursor = connection.cursor()
            query = f"SELECT 1 FROM {table_name} LIMIT 1"
            db_cursor.execute(query)
            result = db_cursor.fetchone()
            return result is None
        except Exception as e:
            print(f"Error while checking if table is empty: {e}")
            return True
        finally:
            db_cursor.close()
            self.connection_pool.putconn(connection)

    def table_exists(self, table_name):
        try:
            connection = self.connection_pool.getconn()
            db_cursor = connection.cursor()
            query = f"""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = '{table_name}'
            );
            """
            db_cursor.execute(query)
            exists = db_cursor.fetchone()[0]
            return exists
        except Exception as e:
            print(f"Error while checking if table exists: {e}")
            return False
        finally:
            db_cursor.close()
            self.connection_pool.putconn(connection)
