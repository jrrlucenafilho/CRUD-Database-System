import psycopg2 as pg
import psycopg2.pool

#All methodes have try/except blocks to handle errors while connecting to the database
#Filling errors are checked in the UI
class Client:
    def __init__(self):
        #Initialize the connection pool for better connection management
        self.connection_pool = pg.pool.SimpleConnectionPool(
            1, 10, user='postgres', password='postgres', dbname='loja_de_revendas_jequiti'
        )
        #Define table and view names
        self.table_name = "clientes"
        self.view_name = "cliente_data_view"
        #Create clients table and data view
        self._create_clients_table()
        self._create_client_data_view()

        #Client attributes
        self.cod_client = None
        self.cpf = None
        self.nome = None
        self.data_nascimento = None

    def _create_clients_table(self):
        try:
            connection = self.connection_pool.getconn()
            db_cursor = connection.cursor()
            #Create clients table if it doesn't exist
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

            #Check if the view exists
            db_cursor.execute(f"""
            SELECT EXISTS (
                SELECT 1
                FROM   information_schema.views 
                WHERE  table_schema = 'public'
                AND    table_name   = '{self.view_name}'
            );
            """)

            view_exists = db_cursor.fetchone()[0]

            #If the view does not exist, create it
            """
            View used to return only essential data to the client
            when the client requests a listing of their data 
            """
            if not view_exists:
                query = f"""
                CREATE VIEW {self.view_name} AS
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
            #Responsible for registering a new client to the database
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
            #Remove a client from the database by CPF
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
            #Retrieve a list of all clients from the view
            #Expected to be used by a sales manager
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
            #Search for a client by CPF
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
            #Check if login credentials are valid
            #If valid, client is logged in
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
            #Retrieve client data by email
            #Expected to be used by a logged in client so he can view his data
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

    def client_exists(self, cod_client: int):
        try:
            connection = self.connection_pool.getconn()
            db_cursor = connection.cursor()
            #Check if a client exists by cod_client
            query = f"SELECT * FROM {self.table_name} WHERE cod_client = %s"
            db_cursor.execute(query, (cod_client,))
            row = db_cursor.fetchone()
            return row is not None
        except Exception as e:
            print(f"Error while checking if client exists: {e}")
            return False
        finally:
            db_cursor.close()
            self.connection_pool.putconn(connection)


    def client_has_enough_money(self, cod_client: int, amount_bought: int, price_per_unit: float):
        try:
            connection = self.connection_pool.getconn()
            db_cursor = connection.cursor()
            #Check if client has enough money for a purchase
            query = f"SELECT saldo FROM {self.table_name} WHERE cod_client = %s"
            db_cursor.execute(query, (cod_client,))
            row = db_cursor.fetchone()
            return row[0] >= amount_bought * price_per_unit
        except Exception as e:
            print(f"Error while checking if client has enough money: {e}")
            return False
        finally:
            db_cursor.close()
            self.connection_pool.putconn(connection)