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

    #Check for stock availability
    def has_stock(self, cod_produto:int, quantidade:int):
        query = f"""
        SELECT quantidade FROM estoque WHERE cod_produto = {cod_produto};
        """
        self.cursor.execute(query)
        stock = self.cursor.fetchone()

        if stock[0] >= quantidade:
            return True
        else:
            return False

    #Decreate stock quantity by amount bought
    def update_stock(self, cod_produto:int, quantidade_comprada:int):
        query = f"""
        UPDATE estoque SET quantidade = quantidade - {quantidade_comprada} WHERE cod_produto = {cod_produto};
        """
        self.cursor.execute(query)


    '''Procedure for generating a monthly sales report'''
    def criar_stored_procedure_sales_report(self):
            try:
                connection = self.connection_pool.getconn()
                db_cursor = connection.cursor()

                #Instrução para criar a stored procedure com do report mensal
                procedure_sql = """
                CREATE OR REPLACE PROCEDURE gerar_relatorio_vendas_mensal(data_inicio DATE, data_fim DATE)
                LANGUAGE plpgsql AS $$
                DECLARE
                    vendedor RECORD;
                BEGIN
                    -- Selecionar vendas por vendedor no intervalo de datas especificado
                    FOR vendedor IN
                        SELECT s.cod_vendedor, s.nome, SUM(c.quantidade) AS quantidade_total, SUM(p.valor * c.quantidade) AS valor_total
                        FROM compras c
                        JOIN sellers s ON c.cod_vendedor = s.cod_vendedor
                        JOIN produtos p ON c.cod_produto = p.cod_produto
                        WHERE c.data_compra BETWEEN data_inicio AND data_fim
                        GROUP BY s.cod_vendedor, s.nome
                    LOOP
                        -- Inserir dados na tabela relatorio_mensal
                        EXECUTE 'INSERT INTO relatorio_mensal (cod_vendedor, nome, quantidade_total, valor_total) VALUES ($1, $2, $3, $4)'
                        USING vendedor.cod_vendedor, vendedor.nome, vendedor.quantidade_total, vendedor.valor_total;
                    END LOOP;
                END;
                $$;
                """

                db_cursor.execute(procedure_sql)
                connection.commit()

                print("report: Stored procedure criada com sucesso, dados de vendas mensais armazenados")
                return True

            except Exception as e:
                print(f"Erro ao criar stored procedure: {e}")
                return False
            finally:
                db_cursor.close()
                self.connection_pool.putconn(connection)