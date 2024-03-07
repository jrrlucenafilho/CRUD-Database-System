from classes.produto import Produto

class CRUD:
    @staticmethod
    def criar_produto():
        Produto.criar_produto() #TODO: Checar se faz static msm

    @staticmethod
    def listar_produtos():
        Produto.listar_produtos()

    @staticmethod
    def atualizar_produto():
        Produto.atualizar_produto()

    @staticmethod
    def deletar_produto():
        Produto.deletar_produto()

    @staticmethod
    def buscar_por_nome(nome):
        Produto.buscar_por_nome(nome)

    @staticmethod
    def gerar_relatorio_estoque():
        Produto.gerar_relatorio_estoque()
