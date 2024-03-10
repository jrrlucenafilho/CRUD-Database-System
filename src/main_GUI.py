import tkinter as tk
from produto import ProdutoGUI  

def abrir_janela_produto():
    root = tk.Tk()
    app = ProdutoGUI(root)
    root.mainloop()

def main():
    root = tk.Tk()
    root.title("Menu Principal")

    largura_janela = 600
    altura_janela = 400
    largura_tela = root.winfo_screenwidth()
    altura_tela = root.winfo_screenheight()
    x = (largura_tela - largura_janela) // 2
    y = (altura_tela - altura_janela) // 2
    root.geometry(f"{largura_janela}x{altura_janela}+{x}+{y}")

    menu_principal = tk.Menu(root)
    root.config(menu=menu_principal)

    menu_produto = tk.Menu(menu_principal)
    menu_principal.add_cascade(label="Produto", menu=menu_produto)
    menu_produto.add_command(label="Abrir Janela", command=abrir_janela_produto)

    root.mainloop()

if __name__ == "__main__":
    main()
