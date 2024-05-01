import psycopg2 as pg
import psycopg2.pool
from datetime import datetime

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

            # Check if the view exists
            db_cursor.execute(f"""
            SELECT EXISTS (
                SELECT 1
                FROM   information_schema.views 
                WHERE  table_schema = 'public'
                AND    table_name   = '{self.view_name}'
            );
            """)

            view_exists = db_cursor.fetchone()[0]

            # If the view does not exist, create it
            if not view_exists:
                query = f"""
                CREATE VIEW {self.view_name} AS
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


    def sell_product(self, cod_cliente: int, nome_produto: str, quantidade: int, forma_pagamento: str):
        try:
            connection = self.connection_pool.getconn()
            db_cursor = connection.cursor()

            #Verificar o estoque do produto com base no nome
            db_cursor.execute("SELECT cod_produto, estoque, valor FROM produtos WHERE nome = %s", (nome_produto,))
            produto = db_cursor.fetchone()
            if produto is None:
                print(f"Produto '{nome_produto}' não encontrado.")
                return False
            
            cod_produto, estoque, valor = produto
            
            #Verify for enough stock
            if estoque < quantidade:
                print(f"Estoque insuficiente para o produto '{nome_produto}'.")
                return False

            #Check client info for discounts
            db_cursor.execute("SELECT is_flamengo, one_piece_fan, from_sousa FROM clientes WHERE cod_client = %s", (cod_cliente,))
            cliente = db_cursor.fetchone()
            if cliente is None:
                print("Cliente não encontrado.")
                return False

            #Discount calc
            desconto = 0
            if cliente[0]:  #isFlamengo
                desconto += 0.05
            if cliente[1]:  #onePieceFan
                desconto += 0.05
            if cliente[2]:  #fromSousa
                desconto += 0.05
            
            #Final price calc
            preco_final = valor * (1 - desconto)

            #Stock update
            novo_estoque = estoque - quantidade
            db_cursor.execute("UPDATE produtos SET estoque = %s WHERE cod_produto = %s", (novo_estoque, cod_produto))

            #Register purchase on 'compras' table
            data_compra = datetime.now().date()
            db_cursor.execute("""
                INSERT INTO compras (cod_cliente, cod_vendedor, cod_produto, quantidade, data_compra, forma_pagamento, desconto_aplicado, status_pagamento)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (cod_cliente, self.cod_vendedor, cod_produto, quantidade, data_compra, forma_pagamento, desconto, 'pendente'))

            connection.commit()
            print(f"Compra realizada com sucesso pelo cliente {cod_cliente} para o produto '{nome_produto}'.")
            return True

        except Exception as e:
            print(f"Erro ao efetuar compra: {e}")
            return False
        finally:
            db_cursor.close()
            self.connection_pool.putconn(connection)


    def verificar_produtos_com_estoque_baixo(self, limiar_estoque: int = 5):
            try:
                connection = self.connection_pool.getconn()
                db_cursor = connection.cursor()

                #Consulta para encontrar produtos com estoque abaixo do limiar especificado
                query = "SELECT * FROM produtos WHERE estoque < %s"
                db_cursor.execute(query, (limiar_estoque,))

                #Obter a lista de produtos com estoque baixo
                produtos = db_cursor.fetchall()

                #Retornar a lista de produtos encontrados
                return produtos

            except Exception as e:
                print(f"Erro ao verificar produtos com estoque baixo: {e}")
                return []
            finally:
                db_cursor.close()
                self.connection_pool.putconn(connection)


    def gerar_relatorio_vendas_mensal(self, data_inicio: str, data_fim: str):
        try:
            connection = self.connection_pool.getconn()
            db_cursor = connection.cursor()

            # Converter datas para o formato de data
            data_inicio = data_inicio.split('/')
            data_inicio = f"{data_inicio[2]}-{data_inicio[1]}-{data_inicio[0]}"

            data_fim = data_fim.split('/')
            data_fim = f"{data_fim[2]}-{data_fim[1]}-{data_fim[0]}"

            # Chamar a stored procedure gerar_relatorio_vendas_mensal
            db_cursor.execute("CALL gerar_relatorio_vendas_mensal(%s, %s)", (data_inicio, data_fim))

            # Recuperar os resultados
            rows = db_cursor.fetchall()

            # Processar os resultados e retorná-los
            resultados = []
            for row in rows:
                resultados.append({
                    "cod_vendedor": row[0],
                    "nome": row[1],
                    "quantidade_total": row[2],
                    "valor_total": row[3]
                })

            return resultados

        except Exception as e:
            print(f"Erro ao gerar relatório de vendas mensal: {e}")
            return []
        finally:
            db_cursor.close()
            self.connection_pool.putconn(connection)