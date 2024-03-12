from classes.DB_Manager import DB_Manager
import tkinter as tk
from tkinter import ttk

class CRUD:
    def __init__(self):
        self.db_manager = DB_Manager()

    def menu(self):
        print("\n===== Menu =====")
        print("1. Cadastrar Produto")
        print("2. Listar Produtos")
        print("3. Buscar Produto por Nome")
        print("4. Atualizar Produto")
        print("5. Deletar Produto")
        print("6. Gerar Relatório de Estoque")
        print("7. Sair")


    def criar_tabela(self, nome:str, colunas:int, info_colunas:list[tuple[str, str]]):
        self.db_manager.add_table(nome, colunas, info_colunas)


    def tabela_existe(self, nome :str):
        return self.db_manager.table_exists(nome)


    def criar_produto(self):
        nome = input("Digite o nome do produto: ")
        valor = float(input("Digite o valor do produto: "))
        estoque = int(input("Digite quantos produtos existem no estoque: "))

        # Check if product already exists (by name)
        if self.db_manager.product_exists_by_name(nome) is True:
            print("Produto já cadastrado.")
            opcao_edit = input("Deseja atualizar o produto existente? (s/n): ")
            if opcao_edit.lower() == 's':
                self.db_manager.edit_product_by_name(nome, 'valor', valor)  # Updates based on input
                self.db_manager.edit_product_by_name(nome, 'estoque', estoque)
                print("Produto atualizado com sucesso!")
            return
        else:
            self.db_manager.insert_product(nome, valor, estoque)
            print("Produto cadastrado com sucesso!")


    def listar_produtos(self):
        rows_list = self.db_manager.list_products()     #TODO: Print this with tkinter later

        # First check if table is empty
        if self.db_manager.is_table_empty('produtos') is True:
            print("Não há produtos cadastrados.")
            return False

        # Now print the rows (tkinter later)
        print("Código | Nome | Valor | Estoque")
        for row in rows_list:
            print(f"{row[0]} | {row[1]} | R$ {row[2]:.2f} | {row[3]}")


    def atualizar_produto(self):
        searched_name = input("Digite o nome do produto que deseja atualizar: ")

        # Check if product exists first
        if self.db_manager.product_exists_by_name(searched_name) is False:
            print("Produto a atualizar não encontrado.")
            return False

        # Ask for prompt on what to update      # TODO Change to buttons with tkinter later
        print("\n===== Menu =====")
        print("1. Nome")
        print("2. Valor")
        print("3. Estoque")
        opcao_atualizar = int(input("Digite a opcao desejada: "))

        if opcao_atualizar == 1:
            novo_nome = input("Digite o novo nome do produto: ")

            # Check if there's already a product with new_name
            if self.db_manager.product_exists_by_name(novo_nome) is True:
                print("Já existe um produto com este nome.")
                return False

            self.db_manager.edit_product_by_name(searched_name, 'nome', novo_nome)
        elif opcao_atualizar == 2:
            novo_valor = float(input("Digite o novo valor do produto: "))
            self.db_manager.edit_product_by_name(searched_name, 'valor', novo_valor)
        elif opcao_atualizar == 3:
            novo_estoque = int(input("Digite o novo valor do estoque: "))
            self.db_manager.edit_product_by_name(searched_name, 'estoque', novo_estoque)
        else:
            print("Opção inválida")
            return False 
        print("Produto atualizado com sucesso!")



    def deletar_produto(self):
        to_be_deleted_prod_name = input("Digite o nome do produto que deseja excluir: ")

        # Check if product exists first
        if self.db_manager.product_exists_by_name(to_be_deleted_prod_name) is False:
            print("Produto não encontrado.")
            return False

        self.db_manager.remove_product_by_name(to_be_deleted_prod_name)
        print("Produto excluído com sucesso!")



    def buscar_por_nome(self):
        searched_name = input("Digite o nome do produto que deseja buscar: ")

        # Exists check
        row = self.db_manager.search_product_by_name(searched_name)

        # Search and print
        if row is False:
            print("Produto pesquisado não encontrado.")
            return False

        print(f"Código | Nome | Valor | Estoque")
        print(f"{row[0]} | {row[1]} | R$ {row[2]:.2f} | {row[3]}")


    def gerar_relatorio_estoque(self):
        # Check if table is empty
        if self.db_manager.is_table_empty('produtos') is True:
            print("Não há produtos cadastrados.")
            return False

        # Print the rows (tkinter later)
        rows_list = self.db_manager.list_products()
        print("Relatório de Estoque:")
        print("Nome | Estoque")

        for row in rows_list:
            print(f"{row[1]} | {row[3]}")
