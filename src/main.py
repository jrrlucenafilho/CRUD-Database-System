from classes.CRUD import CRUD

'''
Programa assume "user=postgres password=postgres" como credenciais do banco de dados
E 'loja_de_revendas_jequiti' como nome do BD
    
'''

def main():
    crud_manager = CRUD()

    if crud_manager.database_existe('loja_de_revendas_jequiti') is False:
        crud_manager.db_manager.create_database()

    if crud_manager.tabela_existe('produtos') is False:
        crud_manager.criar_tabela('produtos', 4, [("nome", "str"), ("valor", "float"), ("estoque", "int")])

    crud_manager.get_root().mainloop()

if __name__ == "__main__":
    main()
