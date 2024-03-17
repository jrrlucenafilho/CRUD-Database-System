from DB_Manager import DB_Manager
import tkinter as tk
from tkinter import ttk

class CRUD:
    def __init__(self):
        self.db_manager = DB_Manager()
        self.search_product_tuple = None

        #GUI Stuff
        self.root = tk.Tk()
        self.root.title("Loja de Revendas Jequiti")
        self.root.geometry("840x570")
        self.tree = ttk.Treeview(self.root)

        self.title_label = tk.Label(self.root, text="Loja de Revendas Jequiti", font=("Arial", 20))
        self.title_label.grid(row=0, column=0, columnspan=2, padx=20, pady=20)

        #Labels for each attribute
        self.name_label = tk.Label(self.root, text="Nome", font=("Arial Bold", 15))
        self.price_label = tk.Label(self.root, text="Valor", font=("Arial Bold", 15))
        self.quantity_label = tk.Label(self.root, text="Estoque", font=("Arial Bold", 15))

        #Settign up their spots in the grid
        self.name_label.grid(row=2, column=0, padx=10, pady=10)
        self.price_label.grid(row=3, column=0, padx=10, pady=10)
        self.quantity_label.grid(row=4, column=0, padx=10, pady=10)

        #Entries for each attribute
        self.name_entry = tk.Entry(self.root, font=("Arial Bold", 15), width=25, bd=5)
        self.price_entry = tk.Entry(self.root, font=("Arial Bold", 15), width=15, bd=5)
        self.quantity_entry = tk.Entry(self.root, font=("Arial Bold", 15), width=15, bd=5)

        #Gridding the entries
        self.name_entry.grid(row=2, column=1, columnspan=3, padx=5, pady=5, sticky="w")
        self.price_entry.grid(row=3, column=1, columnspan=3, padx=5, pady=5, sticky="w")
        self.quantity_entry.grid(row=4, column=1, columnspan=3, padx=5, pady=5, sticky="w")

        #Buttons Frame
        buttons_frame = tk.Frame(self.root)

        #Button widgets
        self.create_button = tk.Button(buttons_frame,
                                       text="Adicionar",
                                       font=("Arial", 15),
                                       width=7, padx=5, pady=5, bd=3,
                                       bg="#0099ff",
                                       command=lambda: self.insert_product_UI())

        self.delete_button = tk.Button(buttons_frame, 
                                       text="Deletar",
                                       font=("Arial", 15),
                                       width=7, padx=10, pady=5, bd=3,
                                       bg="#0099ff",
                                       command=lambda: self.delete_product_UI())

        self.update_button = tk.Button(buttons_frame,
                                       text="Atualizar",
                                       font=("Arial", 15),
                                       width=7, padx=10, pady=5, bd=3,
                                       bg="#0099ff",
                                       command=lambda: self.update_product_UI())

        self.search_product_button = tk.Button(buttons_frame,
                                                text="Buscar",
                                                font=("Arial", 15),
                                                width=7, padx=10, pady=5, bd=3,
                                                bg="#0099ff",
                                                command=lambda: self.search_product_UI())

        self.list_button = tk.Button(buttons_frame,
                                        text="Listar",
                                        font=("Arial", 15),
                                        width=7, padx=10, pady=5, bd=3,
                                        bg="#0099ff",
                                        command=lambda: self.update_treeview())

        #Grid buttons into frame and frame into window
        self.create_button.grid(row=5, column=1, columnspan=1, pady=10, padx=5)
        self.delete_button.grid(row=5, column=2, columnspan=1, pady=10, padx=5)
        self.update_button.grid(row=5, column=3, columnspan=1, pady=10, padx=5)
        self.search_product_button.grid(row=5, column=4, columnspan=1, pady=10, padx=5)
        self.list_button.grid(row=5, column=5, columnspan=1, pady=10, padx=5)

        buttons_frame.grid(row=5, column=1, columnspan=4, pady=10, padx=10)

        #Treeview widget
        self.style = ttk.Style()
        self.style.configure("Treeview.Heading", font=("Arial Bold", 15))

        #Setting uo cols
        self.tree["columns"] = ("Cod. Produto", "Nome", "Valor", "Estoque") 
        self.tree.column("#0", width=0, stretch=tk.NO)
        self.tree.column("Cod. Produto", anchor=tk.W, width=150)
        self.tree.column("Nome", anchor=tk.W, width=250)
        self.tree.column("Valor", anchor=tk.W, width=100)
        self.tree.column("Estoque", anchor=tk.W, width=100)

        #Setting up headings
        self.tree.heading("Cod. Produto", text="Cod. Produto", anchor=tk.W)
        self.tree.heading("Nome", text="Nome", anchor=tk.W)
        self.tree.heading("Valor", text="Valor", anchor=tk.W)
        self.tree.heading("Estoque", text="Estoque", anchor=tk.W)

        #Config actual grid
        self.tree.tag_configure("orow", background="white", font=("Arial bold", 15))
        self.tree.grid(row=6, column=1, columnspan=4, rowspan=5, padx=10, pady=10)

        #Initial Listing
        self.update_treeview()


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
        rows_list = self.db_manager.list_products()

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

        #Ask for prompt on what to update
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


    '''CRUD UI utility functions'''
    def reverse_tuples(self, tuples):
        return tuples[::-1]


    def show_warning(self, message):
        #Create a new window
        warning_window = tk.Toplevel(self.root, padx=10, pady=10)
        warning_window.geometry(self.popup_coords_calc(warning_window))

        #Create a label with the warning message
        warning_label = tk.Label(warning_window, text=message)
        warning_label.pack()

        #Create a button to close the window
        close_button = tk.Button(warning_window, text="Fechar",
                                  padx=10, pady=5, bd=3, bg="#0099ff",
                                 command=warning_window.destroy)
        close_button.pack()


    #Version that'll accept yes or no for updating on a whim
    def show_warning_options(self, message, nome, valor, estoque):
        #Create a new window
        warning_window = tk.Toplevel(self.root, padx=10, pady=10)
        warning_window.geometry(self.popup_coords_calc(warning_window))

        #Create a label with the warning message
        warning_label = tk.Label(warning_window, text=message)
        warning_label.pack()

        #Display old values
        before_treeview = ttk.Treeview(warning_window, columns=('Nome', 'Valor', 'Estoque'), show='headings', height=1)
        before_treeview.heading('Nome', text='Nome')
        before_treeview.heading('Valor', text='Valor')
        before_treeview.heading('Estoque', text='Estoque')

        prod_info = self.db_manager.search_product_by_name(nome)

        before_treeview.insert("", 0, values=(prod_info[1], prod_info[2], prod_info[3]))
        before_treeview.pack(padx=10, pady=10)

        #Print Downward arrow
        arrow_label = tk.Label(warning_window, text="↓")
        arrow_label.pack()

        #Display current to-be-updated values
        after_treeview = ttk.Treeview(warning_window, columns=('Nome', 'Valor', 'Estoque'), show='headings', height=1)
        after_treeview.heading('Nome', text='Nome')
        after_treeview.heading('Valor', text='Valor')
        after_treeview.heading('Estoque', text='Estoque')

        #Inserting the values
        after_treeview.insert("", 0, values=(nome, valor, estoque))
        after_treeview.pack(padx=10, pady=10)

        #Create buttons frame
        buttons_frame = tk.Frame(warning_window)

        #'Yes' button
        yes_button = tk.Button(buttons_frame, text="Sim",
                               padx=10, pady=5, bd=3, bg="#0099ff",
                               command=lambda: [self.db_manager.edit_product_by_name(nome, 'valor', valor),
                                                self.db_manager.edit_product_by_name(nome, 'estoque', estoque),
                                                self.update_treeview(),
                                                warning_window.destroy(),
                                                self.show_confirmation("Produto atualizado com sucesso!")])

        #'No' button
        no_button = tk.Button(buttons_frame, text="Não",
                               padx=10, pady=5, bd=3, bg="#0099ff",
                              command=lambda: [self.show_confirmation("Operação cancelada."),
                                               warning_window.destroy()])

        yes_button.grid(row=0, column=0, padx=5, pady=5)
        no_button.grid(row=0, column=1, padx=5, pady=5)

        buttons_frame.pack()


    def show_confirmation(self, message):
        #Create a new window
        confirmation_window = tk.Toplevel(self.root, padx=10, pady=10)
        confirmation_window.geometry(self.popup_coords_calc(confirmation_window))

        #Create a label with the confirmation message
        confirmation_label = tk.Label(confirmation_window, text=message)
        confirmation_label.pack()

        #Create a button to close the window
        close_button = tk.Button(confirmation_window, text="Fechar",
                                 padx=10, pady=5, bd=3, bg="#0099ff",
                                 command=confirmation_window.destroy)
        close_button.pack()

    #Returns str that allows it to popup in the middle main window (roughly)
    def popup_coords_calc(self, topLevel: tk.Toplevel):
        # Get the main window's position and dimensions
        main_window_x = self.root.winfo_x()
        main_window_y = self.root.winfo_y()
        main_window_width = self.root.winfo_width()
        main_window_height = self.root.winfo_height()

        # Calculate the position to center the Toplevel window within the main window
        x = main_window_x + (main_window_width - topLevel.winfo_reqwidth()) / 2
        y = main_window_y + (main_window_height - topLevel.winfo_reqheight()) / 2

        return f'+{int(x)}+{int(y)}'


    def update_treeview(self):
        for tuple in self.tree.get_children():
            self.tree.delete(tuple)

        for tuple in self.reverse_tuples(self.db_manager.list_products()):
            self.tree.insert("", 0, values=tuple)


    def clear_entries(self):
        self.name_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)
        self.quantity_entry.delete(0, tk.END)


    def search_product(self, entry, treeview):
        if not self.db_manager.product_exists_by_name(entry.get()):
            self.show_warning("Produto não encontrado.")
            treeview.delete(*treeview.get_children())
            return False
        else:
            self.searched_product_tuple = self.db_manager.search_product_by_name(entry.get())
            treeview.insert("", 0, values=(self.searched_product_tuple[0], self.searched_product_tuple[1], self.searched_product_tuple[2], self.searched_product_tuple[3]))
            self.show_confirmation("Produto encontrado!")
            return True


    def get_searched_product_tuple(self):
        return self.searched_product_tuple


    def search_and_unhide_edit_buttons(self, entry, treeview, edit_buttons_frame):
        result = self.search_product(entry, treeview)
        edit_buttons_frame.pack()

        return result


    '''UI CRUD Functions'''
    def insert_product_UI(self):
        nome = str(self.name_entry.get())
        valor = str(self.price_entry.get())
        estoque = str(self.quantity_entry.get())

        if nome == "" or valor == "" or estoque == "":
            self.show_warning("Preencha todos os campos.")
            return

        #Post-check conversion
        valor = float(valor)
        estoque = int(estoque)

        #Check if product already exists (by name)
        if self.db_manager.product_exists_by_name(nome) is True:
            self.show_warning_options("Produto já cadastrado. Deseja inserir os novos dados?", nome, valor, estoque)
        else:
            self.db_manager.insert_product(nome, valor, estoque)
            self.show_confirmation("Produto cadastrado com sucesso!")
        self.clear_entries()

        #Updating treeview
        self.update_treeview()


    def delete_product_UI(self):
        #Create a new window
        delete_window = tk.Toplevel(self.root, padx=10, pady=10)
        delete_window.geometry(self.popup_coords_calc(delete_window))

        #Create a label
        label = tk.Label(delete_window, text="Nome do Produto a ser deletado:")
        label.pack()

        #Create an entry widget
        entry = tk.Entry(delete_window)
        entry.pack()

        #Create buttons frame
        buttons_frame = tk.Frame(delete_window)

        #Create a 'Delete' button
        delete_button = tk.Button(buttons_frame, text="Deletar",
                                  padx=10, pady=5, bd=3, bg="#0099ff",
                                  command=lambda: [[self.show_warning("Produto não encontrado."),
                                                    delete_window.destroy()]
                                                    if not self.db_manager.product_exists_by_name(entry.get()) 
                                                    else 
                                                    [self.db_manager.remove_product_by_name(entry.get()),
                                                    self.update_treeview(),
                                                    delete_window.destroy(),
                                                    self.show_confirmation("Produto deletado com sucesso!")]])

        #Create a 'Cancel' button
        cancel_button = tk.Button(buttons_frame, text="Cancelar",
                                  padx=10, pady=5, bd=3, bg="#0099ff",
                                  command=delete_window.destroy)

        delete_button.grid(row=0, column=0, padx=5, pady=5)
        cancel_button.grid(row=0, column=1, padx=5, pady=5)

        buttons_frame.pack()


    def search_product_UI(self):
        #Create a new window
        search_window = tk.Toplevel(self.root, padx=10, pady=10)
        search_window.geometry(self.popup_coords_calc(search_window))

        #Create a label
        label = tk.Label(search_window, text="Nome do Produto a ser buscado:")
        label.pack()

        #Create an entry widget
        entry = tk.Entry(search_window)
        entry.pack()

        #Create a teeview to show searched product's data
        treeview = ttk.Treeview(search_window, columns=('Cod. Produto','Nome', 'Valor', 'Estoque'), show='headings', height=1)
        treeview.heading('Cod. Produto', text='Cod. Produto')
        treeview.heading('Nome', text='Nome')
        treeview.heading('Valor', text='Valor')
        treeview.heading('Estoque', text='Estoque')
        treeview.pack(padx=10, pady=10)

        #Create a button
        button = tk.Button(search_window, text="Buscar",
                           padx=10, pady=5, bd=3, bg="#0099ff",
                           command=lambda: self.search_product(entry, treeview))

        button.pack()


    def update_product_UI(self):
        #First search for the product to be updated
        #Create a new window
        search_window = tk.Toplevel(self.root, padx=10, pady=10)
        search_window.geometry(self.popup_coords_calc(search_window))

        #Create a label
        label = tk.Label(search_window, text="Nome do Produto a ser atualizado:")
        label.pack()

        #Create an entry widget
        entry = tk.Entry(search_window)
        entry.pack()

        #Create a teeview to show searched product's data
        treeview = ttk.Treeview(search_window, columns=('Cod. Produto','Nome', 'Valor', 'Estoque'), show='headings', height=1)
        treeview.heading('Cod. Produto', text='Cod. Produto')
        treeview.heading('Nome', text='Nome')
        treeview.heading('Valor', text='Valor')
        treeview.heading('Estoque', text='Estoque')
        treeview.pack(padx=10, pady=10)

        #Make a frame for next buttons
        edit_buttons_frame = tk.Frame(search_window)
        edit_buttons_frame.pack_forget()

        #Make buttons for each edit attribute
        name_button = tk.Button(edit_buttons_frame, text="Nome",
                                padx=10, pady=5, bd=3, bg="#0099ff",    #TODO: Create another window for editing, for eachbutton
                                command=lambda: self.update_product_by_name_UI('nome'))

        value_button = tk.Button(edit_buttons_frame, text="Valor",
                                 padx=10, pady=5, bd=3, bg="#0099ff",
                                 command=lambda: self.update_product_by_name_UI('valor'))

        quantity_button = tk.Button(edit_buttons_frame, text="Estoque",
                                    padx=10, pady=5, bd=3, bg="#0099ff",
                                    command=lambda: self.update_product_by_name_UI('estoque'))

        #Label for prompt
        edit_label = tk.Label(edit_buttons_frame, text="Qual atributo atualizar?", font=("Arial Bold", 15))
        edit_label.grid(row=0, column=0, columnspan=3, padx=5, pady=5)

        name_button.grid(row=1, column=0, padx=5, pady=5)
        value_button.grid(row=1, column=1, padx=5, pady=5)
        quantity_button.grid(row=1, column=2, padx=5, pady=5)

        #Hide frame at first as there's no product to be updated yet
        edit_buttons_frame.pack_forget()

        #Create a button for searching
        button = tk.Button(search_window, text="Buscar",
                           padx=10, pady=5, bd=3, bg="#0099ff",
                           command=lambda: edit_buttons_frame.pack()
                           if self.search_and_unhide_edit_buttons(entry, treeview, edit_buttons_frame)
                           else edit_buttons_frame.pack_forget())
        button.pack()

    def update_product_by_name_UI(self, attr_choice:str):
        #Create a new window
        update_window = tk.Toplevel(self.root, padx=10, pady=10)
        update_window.geometry(self.popup_coords_calc(update_window))

        #Create a label
        label = tk.Label(update_window, text=f"Digite o novo {attr_choice} do produto:")
        label.pack(padx=10, pady=10)

        #Create an entry widget
        entry = tk.Entry(update_window)
        entry.pack(padx=10, pady=10)

        #Create a button
        button = tk.Button(update_window, text="Atualizar",
                           padx=10, pady=5, bd=3, bg="#0099ff",
                           command=lambda: [[self.show_warning("Produto não encontrado."),
                                                update_window.destroy()]
                                                if not self.db_manager.product_exists_by_name(self.get_searched_product_tuple()[1])
                                                else
                                                [self.show_warning("Valor inválido.") if not entry.get().isnumeric() and attr_choice == 'estoque'
                                                else
                                                [self.show_warning("Valor inválido.") if not entry.get().replace('.', '').isnumeric() and attr_choice == 'valor'
                                                else
                                                [self.show_warning("Produto já cadastrado.") if self.db_manager.product_exists_by_name(entry.get())
                                                else
                                                [self.db_manager.edit_product_by_name(self.get_searched_product_tuple()[1], attr_choice, entry.get()),
                                                self.update_treeview(),
                                                update_window.destroy(),
                                                self.show_confirmation("Produto atualizado com sucesso!")]]]]])
        button.pack()


if __name__ == "__main__":
    crud = CRUD()
    crud.root.mainloop()