import psycopg2 as pg
import psycopg2.pool

class Seller:
    def __init__(self):
        self.connection_pool = pg.pool.SimpleConnectionPool(
            1, 10, user='postgres', password='postgres', dbname='loja_de_revendas_jequiti'
        )
        self.table_name = "sellers"
        self.view_name = "seller_data_view"
        self._create_sellers_table()
        self._create_seller_data_view()

    def _create_sellers_table(self):
        try:
            connection = self.connection_pool.getconn()
            db_cursor = connection.cursor()
            query = f"""
            CREATE TABLE IF NOT EXISTS {self.table_name} (
                cod_vendedor SERIAL PRIMARY KEY,
                cpf VARCHAR(11) NOT NULL UNIQUE,
                nome VARCHAR(255) NOT NULL,
                data_nascimento DATE NOT NULL,
                email VARCHAR(255) NOT NULL,
                senha VARCHAR(255) NOT NULL
            )
            """
            db_cursor.execute(query)
            connection.commit()
        except Exception as e:
            print(f"Error while creating sellers table: {e}")
        finally:
            db_cursor.close()
            self.connection_pool.putconn(connection)

    def _create_seller_data_view(self):
        try:
            connection = self.connection_pool.getconn()
            db_cursor = connection.cursor()
            query = f"""
            CREATE VIEW IF NOT EXISTS {self.view_name} AS
            SELECT cod_vendedor, cpf, nome, data_nascimento, email
            FROM {self.table_name}
            """
            db_cursor.execute(query)
            connection.commit()
        except Exception as e:
            print(f"Error while creating seller data view: {e}")
        finally:
            db_cursor.close()
            self.connection_pool.putconn(connection)

    def add_seller(self, cpf: str, nome: str, data_nascimento: str, email: str, senha: str):
        try:
            connection = self.connection_pool.getconn()
            db_cursor = connection.cursor()
            query = f"""
            INSERT INTO {self.table_name} (cpf, nome, data_nascimento, email, senha)
            VALUES (%s, %s, %s, %s, %s)
            """
            db_cursor.execute(query, (cpf, nome, data_nascimento, email, senha))
            connection.commit()
        except Exception as e:
            print(f"Error while adding seller: {e}")
        finally:
            db_cursor.close()
            self.connection_pool.putconn(connection)

    def remove_seller_by_cpf(self, cpf: str):
        try:
            connection = self.connection_pool.getconn()
            db_cursor = connection.cursor()
            query = f"DELETE FROM {self.table_name} WHERE cpf = %s"
            db_cursor.execute(query, (cpf,))
            connection.commit()
        except Exception as e:
            print(f"Error while removing seller by CPF: {e}")
        finally:
            db_cursor.close()
            self.connection_pool.putconn(connection)

    def list_sellers(self):
        try:
            connection = self.connection_pool.getconn()
            db_cursor = connection.cursor()
            query = f"SELECT * FROM {self.view_name}"
            db_cursor.execute(query)
            rows = db_cursor.fetchall()
            return rows
        except Exception as e:
            print(f"Error while listing sellers: {e}")
            return []
        finally:
            db_cursor.close()
            self.connection_pool.putconn(connection)

    def search_seller_by_cpf(self, cpf: str):
        try:
            connection = self.connection_pool.getconn()
            db_cursor = connection.cursor()
            query = f"SELECT * FROM {self.table_name} WHERE cpf = %s"
            db_cursor.execute(query, (cpf,))
            rows = db_cursor.fetchall()
            return rows[0] if rows else False
        except Exception as e:
            print(f"Error while searching seller by CPF: {e}")
            return False
        finally:
            db_cursor.close()
            self.connection_pool.putconn(connection)

    def edit_seller(self, cpf: str, field_to_edit: str, new_value):
        try:
            connection = self.connection_pool.getconn()
            db_cursor = connection.cursor()
            if not self.search_seller_by_cpf(cpf):
                return False
            query = f"UPDATE {self.table_name} SET {field_to_edit} = %s WHERE cpf = %s"
            db_cursor.execute(query, (new_value, cpf))
            connection.commit()
        except Exception as e:
            print(f"Error while editing seller: {e}")
            return False
        finally:
            db_cursor.close()
            self.connection_pool.putconn(connection)

    def login(self, email: str, password: str):
        try:
            connection = self.connection_pool.getconn()
            db_cursor = connection.cursor()
            query = f"SELECT senha FROM {self.table_name} WHERE email = %s"
            db_cursor.execute(query, (email,))
            row = db_cursor.fetchone()
            return row and row[0] == password
        except Exception as e:
            print(f"Error while logging in: {e}")
            return False
        finally:
            db_cursor.close()
            self.connection_pool.putconn(connection)

    def get_seller_data(self, email: str):
        try:
            connection = self.connection_pool.getconn()
            db_cursor = connection.cursor()
            query = f"SELECT * FROM {self.view_name} WHERE email = %s"
            db_cursor.execute(query, (email,))
            row = db_cursor.fetchone()
            return row
        except Exception as e:
            print(f"Error while fetching seller data: {e}")
            return None
        finally:
            db_cursor.close()
            self.connection_pool.putconn(connection)

    def get_all_sellers_data(self):
        try:
            connection = self.connection_pool.getconn()
            db_cursor = connection.cursor()
            query = f"""
            SELECT cod_vendedor, nome, data_nascimento, email
            FROM {self.view_name}
            """
            db_cursor.execute(query)
            rows = db_cursor.fetchall()
            return rows
        except Exception as e:
            print(f"Error while fetching all sellers data: {e}")
            return []
        finally:
            db_cursor.close()
            self.connection_pool.putconn(connection)
