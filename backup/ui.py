import psycopg2 as pg
from classes.CRUD import CRUD
from tkinter import *
from tkinter import ttk # ThemedTK

janela = Tk()
janela.title("Controle de Estoque")
janela.geometry("800x600")

# Criando um label com o título da interface
titulo = ttk.Label(janela, text="Controle de Estoque", font=("Arial", 24))
titulo.pack(pady=20)

# Criando um botão para criar um novo produto
botao_criar = ttk.Button(janela, text="Criar Produto", command=CRUD.criar_produto)
botao_criar.pack(pady=10)

# Criando um botão para listar os produtos cadastrados
botao_listar = ttk.Button(janela, text="Listar Produtos", command=CRUD.listar_produtos)
botao_listar.pack(pady=10)

# Criando um botão para atualizar um produto existente
botao_atualizar = ttk.Button(janela, text="Atualizar Produto", command=CRUD.atualizar_produto)
botao_atualizar.pack(pady=10)

# Criando um botão para deletar um produto existente
botao_deletar = ttk.Button(janela, text="Deletar Produto", command=CRUD.deletar_produto)
botao_deletar.pack(pady=10)

# Criando um botão para buscar um produto pelo nome
botao_buscar = ttk.Button(janela, text="Buscar Produto", command=CRUD.buscar_por_nome)
botao_buscar.pack(pady=10)

# Criando um botão para gerar um relatório de estoque
botao_relatorio = ttk.Button(janela, text="Gerar Relatório", command=CRUD.gerar_relatorio_estoque)
botao_relatorio.pack(pady=10)

# Criando uma tabela com quatro colunas
tabela = ttk.Treeview(janela, columns=("codigo", "nome", "valor", "estoque"), show="headings")
tabela.pack(pady=20)

# Definindo os nomes e os tamanhos das colunas
tabela.heading("codigo", text="Código")
tabela.column("codigo", width=100)
tabela.heading("nome", text="Nome")
tabela.column("nome", width=300)
tabela.heading("valor", text="Valor")
tabela.column("valor", width=100)
tabela.heading("estoque", text="Estoque")
tabela.column("estoque", width=100)

# Inserindo alguns dados de exemplo na tabela
tabela.insert("", "end", values=("001", "LeloPerfume", "100", "100"))
tabela.insert("", "end", values=("002", "RichardParfum", "150", "200"))
tabela.insert("", "end", values=("003", "Eau de Arthur", "200", "150"))

janela.mainloop()