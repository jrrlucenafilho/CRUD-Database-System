from crud import CRUD

def menu():
    print("\n===== Menu =====")
    print("1. Cadastrar Produto")
    print("2. Listar Produtos")
    print("3. Buscar Produto por Nome")
    print("4. Atualizar Produto")
    print("5. Deletar Produto")
    print("6. Gerar Relatório de Estoque")
    print("7. Sair")

def main():
    while True:
        menu()
        opcao = input("Digite a opção desejada: ")
        if opcao == "1":
            CRUD.criar_produto()
        elif opcao == "2":
            CRUD.listar_produtos()
        elif opcao == "3":
            nome = input("Digite o nome do produto que deseja buscar: ")
            CRUD.buscar_por_nome(nome)
        elif opcao == "4":
            CRUD.atualizar_produto()
        elif opcao == "5":
            CRUD.deletar_produto()
        elif opcao == "6":
            CRUD.gerar_relatorio_estoque()
        elif opcao == "7":
            print("Saindo...")
            break
        else:
            print("Opção inválida. Por favor, escolha uma opção válida.")

if __name__ == "__main__":
    main()
