from classes.UI_Manager import UI_Manager
import psycopg2 as pg
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2.pool import SimpleConnectionPool

'''
Program assumes "user=postgres password=postgres" as db credentials
And 'loja_de_revendas_jequiti' as db name
'''

# Exists-check and creation funcs for db and tables
def database_exists(db_name):
    #Connecting to the default database
    connection = pg.connect("user=postgres password=postgres")
    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    db_cursor = connection.cursor()

    #Query to check if database exists
    query = f"""
    SELECT EXISTS (
        SELECT datname FROM pg_catalog.pg_database 
        WHERE datname = '{db_name}'
    );
    """

    db_cursor.execute(query)
    exists = db_cursor.fetchone()[0]

    return exists


def init_database():
    connection = pg.connect("user=postgres password=postgres")
    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    #Setting up db
    db_cursor = connection.cursor()
    db_name = "loja_de_revendas_jequiti"

    if not database_exists(db_name):
        db_creation_query = f"CREATE DATABASE {db_name}"
        db_cursor.execute(db_creation_query)


def table_exists(table_name):
    connection = pg.connect("user=postgres password=postgres dbname=loja_de_revendas_jequiti")
    db_cursor = connection.cursor()

    #Query to check if table exists
    query = f"""
    SELECT EXISTS (
        SELECT FROM information_schema.tables 
        WHERE  table_name   = '{table_name}'
    );
    """

    db_cursor.execute(query)
    exists = db_cursor.fetchone()[0]

    return exists


def init_table(table_name:str, columns:int, cols_info:list[tuple[str, str]], primary_key:str=None, is_primary_also_foreign:bool=False, foreign_table:str=None):
    connection = pg.connect("user=postgres password=postgres dbname=loja_de_revendas_jequiti")
    db_cursor = connection.cursor()

    #Create table query with proper variable number of collumns in PostgreSQL db
    query = f"CREATE TABLE {table_name} ("

    #Only sets a primary
    if is_primary_also_foreign is False:
        query += f"{primary_key} SERIAL PRIMARY KEY, "  #All keys are codes, so all can be serial

    for i in range(columns-1):
        #Correcting 'str' to 'VARCHAR(255)' for PostgreSQL to understand
        if cols_info[i][1] == "str":
            cols_info[i] = (cols_info[i][0], "VARCHAR(255)")

        query += f"{cols_info[i][0]} {cols_info[i][1]}, "

    #Set foreign key as primary if the primary key is also foreign
    if is_primary_also_foreign is True:
        query += f"{primary_key} INTEGER PRIMARY KEY REFERENCES {foreign_table}({primary_key}), "
    query = query[:-2] + ")"

    db_cursor.execute(query)
    connection.commit()
    connection.close()


def set_foreign_key(table_name: str, foreign_key: str, foreign_table_name: str):
    connection = pg.connect("user=postgres password=postgres dbname=loja_de_revendas_jequiti")
    db_cursor = connection.cursor()

    query = f"ALTER TABLE {table_name} ADD FOREIGN KEY ({foreign_key}) REFERENCES {foreign_table_name}({foreign_key});"

    db_cursor.execute(query)
    connection.commit()
    connection.close()


#Inits monthly report table
def init_sales_report_table():
    try:
        connection = pg.connect("user=postgres password=postgres dbname=loja_de_revendas_jequiti")
        db_cursor = connection.cursor()

        # Create the relatorio_estoque table
        db_cursor.execute("""
            CREATE TABLE IF NOT EXISTS relatorio_estoque (
                cod_vendedor INT,
                nome VARCHAR(255),
                qtd_total INT,
                valor_total FLOAT,
                FOREIGN KEY (cod_vendedor) REFERENCES vendedor(cod_vendedor)
            )
        """)

        connection.commit()

    except Exception as e:
        print(f"Error creating table: {e}")

    finally:
        db_cursor.close()
        connection.close()


def setup_all_tables():
    #DB exists check
    if database_exists('loja_de_revendas_jequiti') is False:
        init_database()

    #Check for each table and create if they don't exist
    if table_exists('produtos') is False:
        init_table('produtos', 4, [('nomeProduto', 'str'), ('precoProduto', 'float'), ('fabricadoEm', 'str')],
                   'cod_produto', False)

    if table_exists('clientes') is False:
        init_table('clientes', 9, [('cpf', 'str'), ('nome', 'str'), ('data_nascimento', 'str'), ('email', 'str'),
                                   ('senha', 'str'), ('is_flamengo', 'bool'), ('one_piece_fan', 'bool'), ('from_sousa', 'bool')]
                   ,'cod_cliente', False)

    if table_exists('vendedor') is False:
        init_table('vendedor', 5, [('cpf', 'str'), ('nome', 'str'), ('dataNascimento', 'str'), ('email', 'str'), ('senha', 'str'),],
                   'cod_vendedor', False)

    if table_exists('pedido') is False:
        init_table('pedido', 5, [('cod_cliente','int'), ('cod_vendedor','int'), ('dataPedido', 'str'), ('dataEntrega', 'str'), ('tipoPagamento', 'str')],
                   'cod_pedido', False)

    if table_exists('pedido_item') is False:
        init_table('pedido_item', 4, [('cod_produto', 'int'), ('qtd_produto', 'int'), ('precoProduto', 'float')],
                   'cod_pedido', True, 'pedido')

    if table_exists('pagamento') is False:
        init_table('pagamento', 3, [('tipo_pagamento', 'float'), ('status_confirmacao', 'str')],
                   'cod_pedido', True, 'pedido')

    if table_exists('estoque') is False:
        init_table('estoque', 2, [('qtd_produto', 'int')],
                   'cod_produto', True, 'produtos')

    init_sales_report_table()

    #Now setting up foreign keys that aren't primary keys (and to which table they point to)
    set_foreign_key('pedido', 'cod_cliente', 'clientes')
    set_foreign_key('pedido', 'cod_vendedor', 'vendedor')
    set_foreign_key('pedido_item', 'cod_pedido', 'pedido')
    set_foreign_key('pagamento', 'cod_pedido', 'pedido')
    set_foreign_key('estoque', 'cod_produto', 'produtos')
    set_foreign_key('pedido_item', 'cod_produto', 'produtos')


def main():
    if database_exists('loja_de_revendas_jequiti') is False:
        init_database()

    #Table exists check and creation + setup
    setup_all_tables()

    crud_manager = UI_Manager()
    crud_manager.get_root().mainloop()


if __name__ == "__main__":
    main()
