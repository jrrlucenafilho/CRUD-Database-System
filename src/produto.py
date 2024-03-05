from franquia import Franquia

class Produto(Franquia):
    __codigo_produto = 0
    __produtos_cadastrados = []

    def __init__(self, nome, valor, estoque):
        super().__init__(self.__formatar_codigo(Produto.__codigo_produto))
        
        self.__nome = nome
        self.__valor = valor
        self.__estoque = estoque
        Produto.__codigo_produto += 1
        Produto.__produtos_cadastrados.append(self)

    @staticmethod
    def __formatar_codigo(codigo):
        return f"{codigo:05d}"
    
    @staticmethod
    def criar_produto():
        nome = input("Digite o nome do produto: ")
        valor = float(input("Digite o valor do produto: "))
        estoque = int(input("Digite quantos produtos existem no estoque: "))
        
        for produto in Produto.__produtos_cadastrados:
            if produto._Produto__nome.lower() == nome.lower():
                print("Produto já cadastrado.")
                opcao = input("Deseja atualizar o produto existente? (s/n): ")
                if opcao.lower() == 's':
                    produto._Produto__valor = valor
                    produto._Produto__estoque = estoque
                    print("Produto atualizado com sucesso!")
                return
        
        produto = Produto(nome, valor, estoque)
        print("Produto cadastrado com sucesso!")

    @staticmethod
    def listar_produtos():
        if not Produto.__produtos_cadastrados:
            print("Não há produtos cadastrados.")
        else:
            print("Lista de produtos cadastrados:")
            for produto in Produto.__produtos_cadastrados:
                print(f"Código: {produto.cod_produto}, Nome: {produto._Produto__nome}, Valor: R${produto._Produto__valor:.2f}, Estoque: {produto._Produto__estoque}")

    @staticmethod
    def atualizar_produto():
        nome = input("Digite o nome do produto que deseja atualizar: ")
        for produto in Produto.__produtos_cadastrados:
            if produto._Produto__nome.lower() == nome.lower():
                print("\n===== Menu =====")
                print("1. Nome")
                print("2. Valor")
                print("3. Estoque")
                opcao = int(input("Digite a opcao desejada: "))
                if opcao == 1:
                    novo_nome = input("Digite o novo nome do produto: ")
                    produto._Produto__nome = novo_nome
                elif opcao == 2:
                    novo_valor = float(input("Digite o novo valor do produto: "))
                    produto._Produto__valor = novo_valor
                elif opcao == 3:
                    novo_estoque = int(input("Digite o novo valor do estoque: "))
                    produto._Produto__estoque = novo_estoque
                print("Produto atualizado com sucesso!")
                return
        print("Produto não encontrado.")

    @staticmethod
    def deletar_produto():
        nome = input("Digite o nome do produto que deseja excluir: ")
        for produto in Produto.__produtos_cadastrados:
            if produto._Produto__nome.lower() == nome.lower():
                Produto.__produtos_cadastrados.remove(produto)
                print("Produto excluído com sucesso!")
                return
        print("Produto não encontrado.")
    
    @staticmethod
    def buscar_por_nome(nome):
        for produto in Produto.__produtos_cadastrados:
            if produto._Produto__nome.lower() == nome.lower():
                print(f"Produto encontrado: Código: {produto.cod_produto}, Nome: {produto._Produto__nome}, Valor: R${produto._Produto__valor:.2f}, Estoque: {produto._Produto__estoque}")
                return
        print("Produto não encontrado.")

    @staticmethod
    def gerar_relatorio_estoque():
        if not Produto.__produtos_cadastrados:
            print("Não há produtos cadastrados.")
        else:
            print("Relatório de estoque:")
            for produto in Produto.__produtos_cadastrados:
                print(f"Nome: {produto._Produto__nome}, Estoque: {produto._Produto__estoque}")
