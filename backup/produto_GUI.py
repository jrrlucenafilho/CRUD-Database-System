import tkinter as tk
from tkinter import messagebox, simpledialog

class ProdutoGUI:
    __codigo_produto = 0
    __produtos_cadastrados = []

    def __init__(self, master):
        self.master = master
        self.master.title("Cadastro de Produtos")
        self.master.geometry("800x600")

        self.frame = tk.Frame(self.master)
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.frame, bg="white")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scroll_y = tk.Scrollbar(self.frame, orient="vertical", command=self.canvas.yview)
        self.scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.configure(yscrollcommand=self.scroll_y.set)

        self.table_frame = tk.Frame(self.canvas, bg="white")
        self.table_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.table_frame, anchor="nw")

        self.labels = ["Código", "Nome", "Valor", "Estoque"]
        column_widths = [10, 30, 15, 10]

        for i, (label, width) in enumerate(zip(self.labels, column_widths)):
            lbl = tk.Label(self.table_frame, text=label, font=("Arial", 10, "bold"), bg="white", relief=tk.RIDGE)
            lbl.grid(row=0, column=i, sticky="nsew", padx=2, pady=2)
            self.table_frame.grid_columnconfigure(i, minsize=width) 

        self.row_counter = 1

        self.button_cadastrar = tk.Button(self.master, text="Cadastrar", command=self.cadastrar_produto)
        self.button_cadastrar.pack(pady=5)

        self.button_listar = tk.Button(self.master, text="Listar Produtos", command=self.listar_produtos)
        self.button_listar.pack(pady=5) 

        self.button_atualizar = tk.Button(self.master, text="Atualizar Produto", command=self.atualizar_produto)
        self.button_atualizar.pack(pady=5) 

        self.button_deletar = tk.Button(self.master, text="Deletar Produto", command=self.deletar_produto)
        self.button_deletar.pack(pady=5) 

        self.button_buscar = tk.Button(self.master, text="Buscar Produto", command=self.buscar_por_nome)
        self.button_buscar.pack(pady=5)

        self.button_relatorio = tk.Button(self.master, text="Gerar Relatório de Estoque", command=self.gerar_relatorio_estoque)
        self.button_relatorio.pack(pady=5) 

    def cadastrar_produto(self):
        nome = simpledialog.askstring("Nome do Produto", "Digite o nome do produto:")
        if not nome:
            messagebox.showerror("Erro", "Nome do produto não pode ser vazio.")
            return

        valor_str = simpledialog.askstring("Valor do Produto", "Digite o valor do produto:")
        if not valor_str:
            messagebox.showerror("Erro", "Valor do produto não pode ser vazio.")
            return
        try:
            valor = float(valor_str)
        except ValueError:
            messagebox.showerror("Erro", "Valor do produto deve ser um número.")
            return

        estoque_str = simpledialog.askstring("Estoque", "Digite a quantidade em estoque:")
        if not estoque_str:
            messagebox.showerror("Erro", "Estoque não pode ser vazio.")
            return
        try:
            estoque = int(estoque_str)
        except ValueError:
            messagebox.showerror("Erro", "Estoque deve ser um número inteiro.")
            return

        for produto in ProdutoGUI.__produtos_cadastrados:
            if produto['Nome'].lower() == nome.lower():
                messagebox.showerror("Erro", "Produto já cadastrado.")
                return

        produto = {'Código': self.__formatar_codigo(ProdutoGUI.__codigo_produto), 'Nome': nome, 'Valor': valor, 'Estoque': estoque}
        ProdutoGUI.__codigo_produto += 1
        ProdutoGUI.__produtos_cadastrados.append(produto)

        messagebox.showinfo("Cadastro de Produto", "Produto cadastrado com sucesso!")
        self.listar_produtos() 

    def __formatar_codigo(self, codigo):
        return f"{codigo:05d}"

    def listar_produtos(self):
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        for i, label in enumerate(self.labels):
            lbl = tk.Label(self.table_frame, text=label, font=("Arial", 10, "bold"), bg="white", relief=tk.RIDGE)
            lbl.grid(row=0, column=i, sticky="nsew", padx=2, pady=2)

        self.row_counter = 1

        if not ProdutoGUI.__produtos_cadastrados:
            for i in range(0):
                for j in range(len(self.labels)):
                    lbl = tk.Label(self.table_frame, text="", font=("Arial", 10), bg="white", relief=tk.RIDGE)
                    lbl.grid(row=self.row_counter, column=j, sticky="nsew", padx=2, pady=2)
                self.row_counter += 1
        else:
            for produto in ProdutoGUI.__produtos_cadastrados:
                for i, key in enumerate(self.labels):
                    value = produto[key]
                    lbl = tk.Label(self.table_frame, text=value, font=("Arial", 10), bg="white", relief=tk.RIDGE)
                    lbl.grid(row=self.row_counter, column=i, sticky="nsew", padx=2, pady=2)
                self.row_counter += 1

    def atualizar_produto(self):
        nome = simpledialog.askstring("Buscar Produto", "Digite o nome do produto que deseja atualizar:")
        if nome is None:
            return

        for produto in ProdutoGUI.__produtos_cadastrados:
            if produto['Nome'].lower() == nome.lower():
                novo_nome = simpledialog.askstring("Novo Nome", "Digite o novo nome do produto:", initialvalue=produto['Nome'])
                if novo_nome is None:
                    return
                novo_valor_str = simpledialog.askstring("Novo Valor", "Digite o novo valor do produto:", initialvalue=produto['Valor'])
                if not novo_valor_str:
                    messagebox.showerror("Erro", "Valor do produto não pode ser vazio.")
                    return
                try:
                    novo_valor = float(novo_valor_str)
                except ValueError:
                    messagebox.showerror("Erro", "Valor do produto deve ser um número.")
                    return

                novo_estoque_str = simpledialog.askstring("Novo Estoque", "Digite o novo valor do estoque:", initialvalue=produto['Estoque'])
                if not novo_estoque_str:
                    messagebox.showerror("Erro", "Estoque não pode ser vazio.")
                    return
                try:
                    novo_estoque = int(novo_estoque_str)
                except ValueError:
                    messagebox.showerror("Erro", "Estoque deve ser um número inteiro.")
                    return

                produto['Nome'] = novo_nome
                produto['Valor'] = novo_valor
                produto['Estoque'] = novo_estoque
                messagebox.showinfo("Atualizar Produto", "Produto atualizado com sucesso!")
                self.listar_produtos() 
                return
        messagebox.showerror("Erro", "Produto não encontrado.")

    def deletar_produto(self):
        nome = simpledialog.askstring("Buscar Produto", "Digite o nome do produto que deseja excluir:")
        if nome is None:
            return

        for produto in ProdutoGUI.__produtos_cadastrados:
            if produto['Nome'].lower() == nome.lower():
                ProdutoGUI.__produtos_cadastrados.remove(produto)
                messagebox.showinfo("Deletar Produto", "Produto excluído com sucesso!")
                self.listar_produtos() 
                return
        messagebox.showerror("Erro", "Produto não encontrado.")

    def buscar_por_nome(self):
        nome = simpledialog.askstring("Buscar Produto", "Digite o nome do produto:")
        if nome is None:
            return

        for produto in ProdutoGUI.__produtos_cadastrados:
            if produto['Nome'].lower() == nome.lower():
                messagebox.showinfo("Buscar Produto", f"Produto encontrado: Código: {produto['Código']}, Nome: {produto['Nome']}, Valor: R${produto['Valor']:.2f}, Estoque: {produto['Estoque']}")
                return
        messagebox.showerror("Erro", "Produto não encontrado.")

    def gerar_relatorio_estoque(self):
        if not ProdutoGUI.__produtos_cadastrados:
            messagebox.showinfo("Relatório de Estoque", "Não há produtos cadastrados.")
        else:
            relatorio = "Relatório de Estoque:\n"
            for produto in ProdutoGUI.__produtos_cadastrados:
                relatorio += f"Nome: {produto['Nome']}, Estoque: {produto['Estoque']}\n"
            messagebox.showinfo("Relatório de Estoque", relatorio)

def main():
    root = tk.Tk()
    app = ProdutoGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
