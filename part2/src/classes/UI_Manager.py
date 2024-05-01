from classes.DB_Manager import DB_Manager
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class UI_Manager:
    def __init__(self):
        self.db_manager = DB_Manager()
        self.search_product_tuple = None

        #GUI Stuff
        self.root = tk.Tk()
        self.root.title("Loja de Revendas Jequiti")
        self.root.geometry("840x570")

        #Title Frame
        title_frame = tk.Frame(self.root)
        title_frame.pack(side=tk.TOP, fill=tk.BOTH, padx=10, pady=10)

        #Title Label
        self.title_label = tk.Label(title_frame, text="Loja de Revendas Jequiti", font=("Arial", 20))
        self.title_label.grid(row=0, column=1, columnspan=2, padx=(260, 30), pady=20)

        #Main Frame
        main_frame = tk.Frame(self.root)
        main_frame.pack(side=tk.TOP, fill=tk.BOTH, padx=280, pady=90)

        #Labels Frame
        labels_frame = tk.Frame(main_frame)
        labels_frame.pack(side=tk.TOP, fill=tk.BOTH, padx=10, pady=10)

        self.seller_title = tk.Label(labels_frame, text="Cadastrar", font=("Arial", 15))
        self.seller_title.grid(row=0, column=0, padx=10, pady=(10, 110))

        self.client_title = tk.Label(labels_frame, text="Login", font=("Arial", 15))
        self.client_title.grid(row=0, column=1, padx=10, pady=(10, 110))

        #Button widgets
        self.seller_button_1 = tk.Button(labels_frame,
                                        text="Vendedor",
                                        font=("Arial", 15),
                                        width=7, padx=5, pady=5, bd=3,
                                        bg="#0099ff",
                                        command=lambda: self.transaction_UI())
        self.seller_button_1.grid(row=1, column=1, padx=10, pady=10)

        self.client_button_1 = tk.Button(labels_frame,
                                        text="Cliente",
                                        font=("Arial", 15),
                                        width=7, padx=5, pady=5, bd=3,
                                        bg="#0099ff",
                                        command=lambda: self.register_client_UI())
        self.client_button_1.grid(row=0, column=0, padx=10, pady=10)

        self.seller_button_2 = tk.Button(labels_frame,
                                        text="Vendedor",
                                        font=("Arial", 15),
                                        width=7, padx=5, pady=5, bd=3,
                                        bg="#0099ff",
                                        command=lambda: self.register_seller_UI())
        self.seller_button_2.grid(row=1, column=0, padx=10, pady=10)

        self.client_button_2 = tk.Button(labels_frame,
                                        text="Cliente",
                                        font=("Arial", 15),
                                        width=7, padx=5, pady=5, bd=3,
                                        bg="#0099ff",
                                        command=lambda: self.placeholder())
        self.client_button_2.grid(row=0, column=1, padx=10, pady=10)

        #Navigation button widget
        self.new_button = tk.Button(main_frame,
                                    text="Navegar",
                                    font=("Arial", 15),
                                    width=7, padx=5, pady=5, bd=3,
                                    bg="#0099ff",
                                    command=lambda: self.navigate_stock_UI())
        self.new_button.pack(side=tk.TOP, padx=(10, 20), pady=10)


    def get_root(self):
        return self.root


    def get_db_manager(self):
        return self.db_manager


    '''Database Handling'''
    def criar_tabela(self, nome:str, colunas:int, info_colunas:list[tuple[str, str]]):
        self.db_manager.add_table(nome, colunas, info_colunas)


    def tabela_existe(self, nome :str):
        return self.db_manager.table_exists(nome)


    def database_existe(self, nome :str):
        return self.db_manager.database_exists(nome)


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
        #Get the main window's position and dimensions
        main_window_x = self.root.winfo_x()
        main_window_y = self.root.winfo_y()
        main_window_width = self.root.winfo_width()
        main_window_height = self.root.winfo_height()

        #Calculate the position to center the Toplevel window within the main window
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

    '''Utility part 2'''
    #Converts date from 'dd/mm/yyyy' to 'yyyy-mm-dd'
    def convert_date_format(self, date):
        day, month, year = date.split('/')
        return f'{year}-{month}-{day}'


    def clean_cpf(self, cpf):
        return ''.join(filter(str.isdigit, cpf))


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
                                padx=10, pady=5, bd=3, bg="#0099ff",
                                command=lambda: self.update_product_by_name_UI('nome', treeview))

        value_button = tk.Button(edit_buttons_frame, text="Valor",
                                 padx=10, pady=5, bd=3, bg="#0099ff",
                                 command=lambda: self.update_product_by_name_UI('valor', treeview))

        quantity_button = tk.Button(edit_buttons_frame, text="Estoque",
                                    padx=10, pady=5, bd=3, bg="#0099ff",
                                    command=lambda: self.update_product_by_name_UI('estoque', treeview))

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


    def update_product_by_name_UI(self, attr_choice:str, update_window_treeview: ttk.Treeview):
        #Create a new window
        update_window = tk.Toplevel(self.root, padx=10, pady=10)
        update_window.geometry(self.popup_coords_calc(update_window))

        #Create a label
        label = tk.Label(update_window, text=f"Digite o novo {attr_choice} do produto:")
        label.pack(padx=10, pady=10)

        #Create an entry widget
        entry = tk.Entry(update_window)
        entry.pack(padx=10, pady=10)

        #Def funtion for button
        def on_update_button_click():
            if entry.get().strip() == '':
                self.show_warning("Nome não pode ser vazio.")
                return
            if not self.db_manager.product_exists_by_name(self.get_searched_product_tuple()[1]):
                self.show_warning("Produto não encontrado.")
                update_window.destroy()
                return
            if attr_choice == 'name' and self.db_manager.product_exists_by_name(entry.get()):
                self.show_warning("Produto já cadastrado.")
                return
            if not entry.get().isnumeric() and attr_choice == 'estoque':
                self.show_warning("Valor inválido.")
                return
            if not entry.get().replace('.', '').isnumeric() and attr_choice == 'valor':
                self.show_warning("Valor inválido.")
                return
            self.db_manager.edit_product_by_name(self.get_searched_product_tuple()[1], attr_choice, entry.get())
            self.update_treeview()  #Global treeview

            #Update TopLevel popup treeview
            update_window_treeview.delete(*update_window_treeview.get_children())
            update_window_treeview.insert("", 0, values=self.db_manager.search_product_by_name(self.get_searched_product_tuple()[1]))
            update_window.destroy()
            self.show_confirmation("Produto atualizado com sucesso!")

        #Create a button
        button = tk.Button(update_window, text="Atualizar",
                           padx=10, pady=5, bd=3, bg="#0099ff",
                           command=on_update_button_click)
        button.pack()


    '''Part 2 UI functions'''
    #Function to access all values in 'stock' table. And append the value from the "Stock" table at the end of each row
    #Finally putting it all in a treeview
    def navigate_stock_UI(self):
        #Create a new window
        stock_window = tk.Toplevel(self.root, padx=10, pady=10)
        stock_window.geometry(self.popup_coords_calc(stock_window))

        #Create a treeview
        self.tree = ttk.Treeview(stock_window, columns=('Cod. Produto', 'Nome', 'Preço', 'Fabricado em', 'Estoque'), show='headings')
        self.tree.heading('Cod. Produto', text='Cod. Produto')
        self.tree.heading('Nome', text='Nome')
        self.tree.heading('Preço', text='Preço')
        self.tree.heading('Fabricado em', text='Fabricado em')
        self.tree.heading('Estoque', text='Estoque')
        self.tree.pack(padx=10, pady=10)

        #Inserting the values
        for product in self.reverse_tuples(self.db_manager.list_products()):
            stock = self.db_manager.get_one_stock(product[0])  #assuming product[0] is the product code
            self.tree.insert("", 0, values=product + (stock,))

        #Create a button
        button = tk.Button(stock_window, text="Fechar",
                           padx=10, pady=5, bd=3, bg="#0099ff",
                           command=stock_window.destroy)
        button.pack()


    #Function that opens a new window for registering clients
    #Basically adding them to the clients table
    def register_client_UI(self):
        # Create a new window
        client_register_window = tk.Toplevel(self.root, padx=10, pady=10)
        client_register_window.geometry(self.popup_coords_calc(client_register_window))

        # Frame and Entry for cpf
        cpf_frame = tk.Frame(client_register_window)
        cpf_frame.pack(fill='x')
        tk.Label(cpf_frame, text="CPF: ").pack(side='left')
        self.cpf_entry = tk.Entry(cpf_frame)
        self.cpf_entry.pack(side='right', expand=True)

        # Frame and Entry for nome
        nome_frame = tk.Frame(client_register_window)
        nome_frame.pack(fill='x')
        tk.Label(nome_frame, text="Nome: ").pack(side='left')
        self.nome_entry = tk.Entry(nome_frame)
        self.nome_entry.pack(side='right', expand=True)

        # Frame and Entry for dataNascimento
        dataNascimento_frame = tk.Frame(client_register_window)
        dataNascimento_frame.pack(fill='x')
        tk.Label(dataNascimento_frame, text="Data de Nascimento: ").pack(side='left')
        self.dataNascimento_entry = tk.Entry(dataNascimento_frame)
        self.dataNascimento_entry.pack(side='right', expand=True)

        # Frame and Entry for email
        email_frame = tk.Frame(client_register_window)
        email_frame.pack(fill='x')
        tk.Label(email_frame, text="Email: ").pack(side='left')
        self.email_entry = tk.Entry(email_frame)
        self.email_entry.pack(side='right', expand=True)

        # Frame and Entry for senha
        senha_frame = tk.Frame(client_register_window)
        senha_frame.pack(fill='x')
        tk.Label(senha_frame, text="Senha: ").pack(side='left')
        self.senha_entry = tk.Entry(senha_frame, show="*")  # Password is censored with *
        self.senha_entry.pack(side='right', expand=True)

        # Checkbutton for isFlamengo
        self.isFlamengo_var = tk.IntVar()
        self.isFlamengo_check = tk.Checkbutton(client_register_window, text="Torcedor do Flamengo", variable=self.isFlamengo_var)
        self.isFlamengo_check.pack()

        # Checkbutton for onePieceFan
        self.onePieceFan_var = tk.IntVar()
        self.onePieceFan_check = tk.Checkbutton(client_register_window, text="Fã de One Piece", variable=self.onePieceFan_var)
        self.onePieceFan_check.pack()

        # Checkbutton for fromSousa
        self.fromSousa_var = tk.IntVar()
        self.fromSousa_check = tk.Checkbutton(client_register_window, text="Nascido(a) em Sousa", variable=self.fromSousa_var)
        self.fromSousa_check.pack()

        #Returns false if even jsut one is empty
        def check_empty_entries_on_client_login():
            return all([
                self.cpf_entry.get(),
                self.nome_entry.get(),
                self.dataNascimento_entry.get(),
                self.email_entry.get(),
                self.senha_entry.get()
        ])

        #Checks if any entry is empty
        def add_client_if_valid():
            if check_empty_entries_on_client_login():
                self.db_manager.client.add_client(
                    self.clean_cpf(self.cpf_entry.get()),
                    self.nome_entry.get(),
                    self.dataNascimento_entry.get(),
                    self.email_entry.get(),
                    self.senha_entry.get(),
                    bool(self.isFlamengo_var.get()),
                    bool(self.onePieceFan_var.get()),
                    bool(self.fromSousa_var.get()))
            else:
                self.show_warning("Preencha todos os campos")

        button = tk.Button(client_register_window, text="Cadastrar",
                        padx=10, pady=5, bd=3, bg="#0099ff",
                        command=lambda: add_client_if_valid())
        button.pack()

    def register_seller_UI(self):
            # Crie uma nova janela
            seller_register_window = tk.Toplevel(self.root, padx=10, pady=10)
            seller_register_window.geometry(self.popup_coords_calc(seller_register_window))

            # Frame e Entry para CPF
            cpf_frame = tk.Frame(seller_register_window)
            cpf_frame.pack(fill='x')
            tk.Label(cpf_frame, text="CPF: ").pack(side='left')
            cpf_entry = tk.Entry(cpf_frame)
            cpf_entry.pack(side='right', expand=True)

            # Frame e Entry para nome
            nome_frame = tk.Frame(seller_register_window)
            nome_frame.pack(fill='x')
            tk.Label(nome_frame, text="Nome: ").pack(side='left')
            nome_entry = tk.Entry(nome_frame)
            nome_entry.pack(side='right', expand=True)

            # Frame e Entry para dataNascimento
            dataNascimento_frame = tk.Frame(seller_register_window)
            dataNascimento_frame.pack(fill='x')
            tk.Label(dataNascimento_frame, text="Data de Nascimento: ").pack(side='left')
            dataNascimento_entry = tk.Entry(dataNascimento_frame)
            dataNascimento_entry.pack(side='right', expand=True)

            # Frame e Entry para email
            email_frame = tk.Frame(seller_register_window)
            email_frame.pack(fill='x')
            tk.Label(email_frame, text="Email: ").pack(side='left')
            email_entry = tk.Entry(email_frame)
            email_entry.pack(side='right', expand=True)

            # Frame e Entry para senha
            senha_frame = tk.Frame(seller_register_window)
            senha_frame.pack(fill='x')
            tk.Label(senha_frame, text="Senha: ").pack(side='left')
            senha_entry = tk.Entry(senha_frame, show="*")  # Senha é mascarada com *
            senha_entry.pack(side='right', expand=True)


            # Retorna False se pelo menos um estiver vazio
            def check_empty_entries_on_seller_login():
                return all([
                    cpf_entry.get(),
                    nome_entry.get(),
                    dataNascimento_entry.get(),
                    email_entry.get(),
                    senha_entry.get()
                ])

            # Verifica se algum campo está vazio
            def add_seller_if_valid():
                if check_empty_entries_on_seller_login():
                    # Chame a função para adicionar o vendedor
                    try:
                        self.db_manager.seller.add_seller(
                            cpf_entry.get(),
                            nome_entry.get(),
                            dataNascimento_entry.get(),
                            email_entry.get(),
                            senha_entry.get()
                        )
                        messagebox.showinfo("Sucesso", "Vendedor cadastrado com sucesso!")
                    except Exception as e:
                        messagebox.showerror("Erro", f"Erro ao cadastrar vendedor: {e}")
                else:
                    self.show_warning("Preencha todos os campos")

            button = tk.Button(seller_register_window, text="Cadastrar",
                            padx=10, pady=5, bd=3, bg="#0099ff",
                            command=add_seller_if_valid)
            button.pack()

    #UI for buying from client's view
    def transaction_UI(self):
        #Create a new window
        transaction_window = tk.Toplevel(self.root)
        transaction_window.title("Transação")

        #Create a Treeview widget
        tree = ttk.Treeview(transaction_window)
        tree["columns"] = ("produto", "estoque")
        tree.column("#0", width=0, stretch=tk.NO)
        tree.column("produto", anchor=tk.W, width=100)
        tree.column("estoque", anchor=tk.W, width=100)

        tree.heading("#0", text="", anchor=tk.W)
        tree.heading("produto", text="produto", anchor=tk.W)
        tree.heading("estoque", text="estoque", anchor=tk.W)

        #Add items to the Treeview
        for product in self.db_manager.produto.get_products():
            tree.insert(parent='', index='end', iid=product, text="", values=(product.name, product.stock))

        tree.pack()

        #Create a Sell button
        sell_button = tk.Button(transaction_window, text="Sell", padx=10, pady=5, bd=3, bg="#0099ff")
        sell_button.pack()