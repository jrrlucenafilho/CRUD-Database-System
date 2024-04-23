import psycopg2 as pg
import psycopg2.pool
from Table import Table

class Client:
    def __init__(self):
        self.connection_pool = pg.pool.SimpleConnectionPool(
            1, 10, user='postgres', password='postgres', dbname='loja_de_revendas_jequiti'
        )
        self.table_name = "clients"
        self.view_name = "client_data_view"
        self._create_clients_table()
        self._create_client_data_view()

    def _create_clients_table(self):
        try:
            connection = self.connection_pool.getconn()
            db_cursor = connection.cursor()
            query = f"""
            CREATE TABLE IF NOT EXISTS {self.table_name} (
                cod_client SERIAL PRIMARY KEY,
                cpf VARCHAR(11) NOT NULL UNIQUE,
                nome VARCHAR(255) NOT NULL,
                data_nascimento DATE NOT NULL,
                email VARCHAR(255) NOT NULL,
                senha VARCHAR(255) NOT NULL,
                is_flamengo BOOLEAN NOT NULL,
                one_piece_fan BOOLEAN NOT NULL,
                from_sousa BOOLEAN NOT NULL
            )
            """
            db_cursor.execute(query)
            connection.commit()
        except Exception as e:
            print(f"Error while creating clients table: {e}")
        finally:
            db_cursor.close()
            self.connection_pool.putconn(connection)

    def _create_client_data_view(self):
        try:
            connection = self.connection_pool.getconn()
            db_cursor = connection.cursor()
            query = f"""
            CREATE VIEW IF NOT EXISTS {self.view_name} AS
            SELECT nome, data_nascimento, email, senha, is_flamengo, one_piece_fan, from_sousa
            FROM {self.table_name}
            """
            db_cursor.execute(query)
            connection.commit()
        except Exception as e:
            print(f"Error while creating client data view: {e}")
        finally:
            db_cursor.close()
            self.connection_pool.putconn(connection)

    def add_client(self, cpf: str, nome: str, data_nascimento: str, email: str, senha: str, is_flamengo: bool, one_piece_fan: bool, from_sousa: bool):
        try:
            connection = self.connection_pool.getconn()
            db_cursor = connection.cursor()
            query = f"""
            INSERT INTO {self.table_name} (cpf, nome, data_nascimento, email, senha, is_flamengo, one_piece_fan, from_sousa)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            db_cursor.execute(query, (cpf, nome, data_nascimento, email, senha, is_flamengo, one_piece_fan, from_sousa))
            connection.commit()
        except Exception as e:
            print(f"Error while adding client: {e}")
        finally:
            db_cursor.close()
            self.connection_pool.putconn(connection)

    def remove_client_by_cpf(self, cpf: str):
        try:
            connection = self.connection_pool.getconn()
            db_cursor = connection.cursor()
            query = f"DELETE FROM {self.table_name} WHERE cpf = %s"
            db_cursor.execute(query, (cpf,))
            connection.commit()
        except Exception as e:
            print(f"Error while removing client by CPF: {e}")
        finally:
            db_cursor.close()
            self.connection_pool.putconn(connection)

    def list_clients(self):
        try:
            connection = self.connection_pool.getconn()
            db_cursor = connection.cursor()
            query = f"SELECT * FROM {self.view_name}"
            db_cursor.execute(query)
            rows = db_cursor.fetchall()
            return rows
        except Exception as e:
            print(f"Error while listing clients: {e}")
            return []
        finally:
            db_cursor.close()
            self.connection_pool.putconn(connection)

    def search_client_by_cpf(self, cpf: str):
        try:
            connection = self.connection_pool.getconn()
            db_cursor = connection.cursor()
            query = f"SELECT * FROM {self.table_name} WHERE cpf = %s"
            db_cursor.execute(query, (cpf,))
            rows = db_cursor.fetchall()
            return rows[0] if rows else False
        except Exception as e:
            print(f"Error while searching client by CPF: {e}")
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

            if row and row[0] == password:
                return True
            else:
                return False
        except Exception as e:
            print(f"Error while logging in: {e}")
            return False
        finally:
            db_cursor.close()
            self.connection_pool.putconn(connection)

    def get_client_data(self, email: str):
        try:
            connection = self.connection_pool.getconn()
            db_cursor = connection.cursor()
            query = f"SELECT * FROM {self.view_name} WHERE email = %s"
            db_cursor.execute(query, (email,))
            row = db_cursor.fetchone()
            return row
        except Exception as e:
            print(f"Error while fetching client data: {e}")
            return None
        finally:
            db_cursor.close()
            self.connection_pool.putconn(connection)
