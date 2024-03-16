from DB_Manager import DB_Manager
import tkinter as tk
from tkinter import ttk

class CRUD:
    def __init__(self):
        self.db_manager = DB_Manager()

        #GUI Stuff
        self.root = tk.Tk()
        self.root.title("Loja de Revendas Jequiti")
        self.root.geometry("1280x400")
        self.tree = ttk.Treeview(self.root)

        self.title_label = tk.Label(self.root, text="Loja de Revendas Jequiti", font=("Arial", 20))
        self.title_label.grid(row=0, column=0, columnspan=2, padx=20, pady=20)

        #Labels for each attribute
        self.name_label = tk.Label(self.root, text="Nome", font=("Arial Bold", 15))
        self.price_label = tk.Label(self.root, text="Preço", font=("Arial Bold", 15))
        self.quantity_label = tk.Label(self.root, text="Estoque", font=("Arial Bold", 15))

        #Settign up their spots in the grid
        self.name_label.grid(row=2, column=0, padx=10, pady=10)
        self.price_label.grid(row=3, column=0, padx=10, pady=10)
        self.quantity_label.grid(row=4, column=0, padx=10, pady=10)

        #Entries for each attribute
        self.name_entry = tk.Entry(self.root, font=("Arial Bold", 15), width=25, bd=5)
        self.price_entry = tk.Entry(self.root, font=("Arial Bold", 15), width=25, bd=5)
        self.quantity_entry = tk.Entry(self.root, font=("Arial Bold", 15), width=25, bd=5)

        #Gridding the entries
        self.name_entry.grid(row=2, column=1, columnspan=3, padx=5, pady=5)
        self.price_entry.grid(row=3, column=1, columnspan=3, padx=5, pady=5)
        self.quantity_entry.grid(row=4, column=1, columnspan=3, padx=5, pady=5)

        #Button widgets
        self.create_button = tk.Button(self.root,   #TODO: Fix this button's size
                                       text="Adicionar",
                                       font=("Arial", 15),
                                       width=7, padx=5, pady=5, bd=3,
                                       bg="#0099ff",
                                       command=lambda: self.insert_data_UI())
        self.create_button.grid(row=5, column=1, columnspan=1, sticky='ew')

        self.delete_button = tk.Button(self.root, 
                                       text="Deletar",
                                       font=("Arial", 15),
                                       width=7, padx=10, pady=5, bd=3,
                                       bg="#0099ff",
                                       command=lambda: self.delete_data_UI())
        self.delete_button.grid(row=5, column=2, columnspan=1, padx=10, pady=5, sticky='ew')

        self.update_button = tk.Button(self.root,
                                       text="Atualizar",
                                       font=("Arial", 15),
                                       width=7, padx=10, pady=5, bd=3,
                                       bg="#0099ff")
        self.update_button.grid(row=5, column=3, columnspan=1, padx=10, pady=5, sticky='ew')

        self.list_button = tk.Button(self.root,
                                        text="Listar",
                                        font=("Arial", 15),
                                        width=7, padx=10, pady=5, bd=3,
                                        bg="#0099ff",
                                        command=lambda: self.update_treeview())
        self.list_button.grid(row=5, column=4, columnspan=1, padx=10, pady=5, sticky='ew')

        self.list_one_product_button = tk.Button(self.root,
                                                text="Buscar",
                                                font=("Arial", 15),
                                                width=7, padx=10, pady=5, bd=3,
                                                bg="#0099ff",
                                                command=lambda: self.buscar_por_nome()) #TODO: Change this into a new TopLevel window
        self.list_one_product_button.grid(row=5, column=5, columnspan=1, padx=10, pady=5, sticky='ew')

        #Treeview widget
        self.style = ttk.Style()
        self.style.configure("Treeview.Heading", font=("Arial Bold", 15))

        #Setting uo cols
        self.tree["columns"] = ("Cod. Produto", "Nome", "Preço", "Estoque") 
        self.tree.column("#0", width=0, stretch=tk.NO)
        self.tree.column("Cod. Produto", anchor=tk.W, width=150)
        self.tree.column("Nome", anchor=tk.W, width=250)
        self.tree.column("Preço", anchor=tk.W, width=100)
        self.tree.column("Estoque", anchor=tk.W, width=100)

        #Setting up headings
        self.tree.heading("Cod. Produto", text="Cod. Produto", anchor=tk.W)
        self.tree.heading("Nome", text="Nome", anchor=tk.W)
        self.tree.heading("Preço", text="Preço", anchor=tk.W)
        self.tree.heading("Estoque", text="Estoque", anchor=tk.W)

        #Config actual grid
        self.tree.tag_configure("orow", background="white", font=("Arial bold", 15))
        self.tree.grid(row=1, column=5, columnspan=4, rowspan=5, padx=10, pady=10)


    '''def menu(self):
        print("\n===== Menu =====")
        print("1. Cadastrar Produto")
        print("2. Listar Produtos")
        print("3. Buscar Produto por Nome")
        print("4. Atualizar Produto")
        print("5. Deletar Produto")
        print("6. Gerar Relatório de Estoque")
        print("7. Sair")'''


    '''Database Handling'''
    def criar_tabela(self, nome:str, colunas:int, info_colunas:list[tuple[str, str]]):
        self.db_manager.add_table(nome, colunas, info_colunas)


    def tabela_existe(self, nome :str):
        return self.db_manager.table_exists(nome)


    def database_existe(self, nome :str):
        return self.db_manager.database_exists(nome)


    def criar_produto(self):
        nome = input("Digite o nome do produto: ")
        valor = float(input("Digite o valor do produto: "))
        estoque = int(input("Digite quantos produtos existem no estoque: "))

        #Check if product already exists (by name)
        if self.db_manager.product_exists_by_name(nome) is True:
            print("Produto já cadastrado.")
            opcao_edit = input("Deseja atualizar o produto existente? (s/n): ")
            if opcao_edit.lower() == 's':
                self.db_manager.edit_product_by_name(nome, 'valor', valor)  #Updates based on input
                self.db_manager.edit_product_by_name(nome, 'estoque', estoque)
                print("Produto atualizado com sucesso!")
            return
        else:
            self.db_manager.insert_product(nome, valor, estoque)
            print("Produto cadastrado com sucesso!")


    def listar_produtos(self):
        rows_list = self.db_manager.list_products()     #TODO: Print this with tkinter later

        #First check if table is empty
        if self.db_manager.is_table_empty('produtos') is True:
            print("Não há produtos cadastrados.")
            return False

        #Now print the rows (tkinter later)
        print("Código | Nome | Valor | Estoque")
        for row in rows_list:
            print(f"{row[0]} | {row[1]} | R$ {row[2]:.2f} | {row[3]}")


    def atualizar_produto(self):
        searched_name = input("Digite o nome do produto que deseja atualizar: ")

        #Check if product exists first
        if self.db_manager.product_exists_by_name(searched_name) is False:
            print("Produto a atualizar não encontrado.")
            return False

        #Ask for prompt on what to update      #TODO Change to buttons with tkinter later
        print("\n===== Menu =====")
        print("1. Nome")
        print("2. Valor")
        print("3. Estoque")
        opcao_atualizar = int(input("Digite a opcao desejada: "))

        if opcao_atualizar == 1:
            novo_nome = input("Digite o novo nome do produto: ")

            #Check if there's already a product with new_name
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

        #Check if product exists first
        if self.db_manager.product_exists_by_name(to_be_deleted_prod_name) is False:
            print("Produto não encontrado.")
            return False

        self.db_manager.remove_product_by_name(to_be_deleted_prod_name)
        print("Produto excluído com sucesso!")



    def buscar_por_nome(self):
        searched_name = input("Digite o nome do produto que deseja buscar: ")

        #Exists check
        row = self.db_manager.search_product_by_name(searched_name)

        #Search and print
        if row is False:
            print("Produto pesquisado não encontrado.")
            return False

        print(f"Código | Nome | Valor | Estoque")
        print(f"{row[0]} | {row[1]} | R$ {row[2]:.2f} | {row[3]}")


    def gerar_relatorio_estoque(self):
        #Check if table is empty
        if self.db_manager.is_table_empty('produtos') is True:
            print("Não há produtos cadastrados.")
            return False

        #Print the rows (tkinter later)
        rows_list = self.db_manager.list_products()
        print("Relatório de Estoque:")
        print("Nome | Estoque")

        for row in rows_list:
            print(f"{row[1]} | {row[3]}")


    '''UI Handling'''
    def reverse_tuples(self, tuples):
        return tuples[::-1]


    def show_warning(self, message):
        #Create a new window
        warning_window = tk.Toplevel(self.root)

        #Create a label with the warning message
        warning_label = tk.Label(warning_window, text=message)
        warning_label.pack()

        #Create a button to close the window
        close_button = tk.Button(warning_window, text="Close", command=warning_window.destroy)
        close_button.pack()


    #Version that'll accpet yes or no for updating on a whim
    def show_warning_options(self, message, nome, valor, estoque):
        #Create a new window
        warning_window = tk.Toplevel(self.root)

        #Create a label with the warning message
        warning_label = tk.Label(warning_window, text=message)
        warning_label.pack()

        #Create a 'Yes' button
        yes_button = tk.Button(warning_window, text="Yes",
                               command=lambda: [self.db_manager.edit_product_by_name(nome, 'valor', valor),
                                                self.db_manager.edit_product_by_name(nome, 'estoque', estoque),
                                                self.update_treeview(),
                                                warning_window.destroy(),
                                                self.show_confirmation("Produto atualizado com sucesso!")])
        yes_button.pack()

        #Create a 'No' button
        no_button = tk.Button(warning_window, text="No", 
                              command=lambda: [self.show_confirmation("Operação cancelada."),
                                               warning_window.destroy()])
        no_button.pack()


    def show_confirmation(self, message):
        #Create a new window
        confirmation_window = tk.Toplevel(self.root)

        #Create a label with the confirmation message
        confirmation_label = tk.Label(confirmation_window, text=message)
        confirmation_label.pack()

        #Create a button to close the window
        close_button = tk.Button(confirmation_window, text="Close", command=confirmation_window.destroy)
        close_button.pack()


    def update_treeview(self):
        for tuple in self.tree.get_children():
            self.tree.delete(tuple)

        for tuple in self.reverse_tuples(self.db_manager.list_products()):
            self.tree.insert("", 0, values=tuple)


    def insert_data_UI(self):
        nome = str(self.name_entry.get())
        valor = float(self.price_entry.get())
        estoque = int(self.quantity_entry.get())

        #TODO: maybe do is-empty-checks here (for name mainly), teahcer said these won't matter

        #Check if product already exists (by name)
        if self.db_manager.product_exists_by_name(nome) is True:
            self.show_warning_options("Produto já cadastrado. Deseja inserir os novos dados?", nome, valor, estoque)
            return
        else:
            self.db_manager.insert_product(nome, valor, estoque)
            self.show_confirmation("Produto cadastrado com sucesso!")

        #Updating treeview
        self.update_treeview()


    def delete_data_UI(self):
        #Create a new window
        delete_window = tk.Toplevel(self.root)

        #Create a label
        label = tk.Label(delete_window, text="Nome do Produto a ser deletado:")
        label.pack()

        #Create an entry widget
        entry = tk.Entry(delete_window)
        entry.pack()

        #Create a 'Delete' button
        delete_button = tk.Button(delete_window, text="Delete",
                                  command=lambda: [[self.show_warning("Produto não encontrado."),
                                                    delete_window.destroy()]
                                                    if not self.db_manager.product_exists_by_name(entry.get()) 
                                                    else 
                                                    [self.db_manager.remove_product_by_name(entry.get()),
                                                    self.update_treeview(),
                                                    delete_window.destroy(),
                                                    self.show_confirmation("Produto deletado com sucesso!")]])
        
        delete_button.pack()

        #Create a 'Cancel' button
        cancel_button = tk.Button(delete_window, text="Cancel", command=delete_window.destroy)
        cancel_button.pack()


if __name__ == "__main__":
    crud = CRUD()
    crud.root.mainloop()