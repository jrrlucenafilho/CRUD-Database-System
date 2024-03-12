from classes.CRUD import CRUD

def main():
    crud_manager = CRUD()

    if crud_manager.tabela_existe('produtos') is False:
        crud_manager.criar_tabela('produtos', 4, [("nome", "str"), ("valor", "float"), ("estoque", "int")])

    while True:
        crud_manager.menu()
        opcao = input("Digite a opção desejada: ")
        if opcao == "1":
            crud_manager.criar_produto()
        elif opcao == "2":
            crud_manager.listar_produtos()
        elif opcao == "3":
            crud_manager.buscar_por_nome()
        elif opcao == "4":
            crud_manager.atualizar_produto()
        elif opcao == "5":
            crud_manager.deletar_produto()
        elif opcao == "6":
            crud_manager.gerar_relatorio_estoque()
        elif opcao == "7":
            print("Saindo...")
            break
        else:
            print("Opção inválida. Por favor, escolha uma opção válida.")

if __name__ == "__main__":
    main()
