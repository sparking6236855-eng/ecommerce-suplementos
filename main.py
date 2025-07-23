from modules.produtos import (
    cadastrar_produto,
    listar_produtos,
    editar_produto,
    remover_produto,
    pesquisar_produto
)

from modules.pedidos import (
    adicionar_ao_carrinho,
    finalizar_pedido,
    visualizar_pedidos
)

from database.init_db import iniciar_banco

def menu():
    iniciar_banco()  # cria as tabelas no banco se não existirem

    while True:
        print("\n=== E-COMMERCE DE SUPLEMENTOS ===")
        print("1) Cadastrar produto")
        print("2) Listar produtos")
        print("3) Editar produto")
        print("4) Remover produto")
        print("5) Pesquisar produto")
        print("6) Adicionar ao carrinho")
        print("7) Finalizar pedido")
        print("8) Ver pedidos")
        print("9) Sair")
        op = input("Escolha: ").strip()

        opcoes = {
            "1": cadastrar_produto,
            "2": listar_produtos,
            "3": editar_produto,
            "4": remover_produto,
            "5": pesquisar_produto,
            "6": adicionar_ao_carrinho,
            "7": finalizar_pedido,
            "8": visualizar_pedidos
        }

        if op == "9":
            print("🔚 Encerrando sistema...")
            break
        elif op in opcoes:
            opcoes[op]()
        else:
            print("❌ Opção inválida.\n")

if __name__ == "__main__":
    menu()