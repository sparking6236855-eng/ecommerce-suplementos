import sqlite3

con = sqlite3.connect("suplementos.db")
cur = con.cursor()

def cadastrar_produto():
    nome = input("Nome do suplemento: ")
    preco = float(input("Preço (R$): "))
    estoque = int(input("Estoque inicial: "))
    cur.execute("INSERT INTO produtos (nome, preco, estoque) VALUES (?, ?, ?)", (nome, preco, estoque))
    con.commit()
    print("✅ Produto cadastrado!\n")

def listar_produtos():
    cur.execute("SELECT * FROM produtos")
    rows = cur.fetchall()
    if not rows:
        print("📂 Não há produtos cadastrados.\n")
        return
    for id_, nome, preco, est in rows:
        print(f"ID {id_:<3} | {nome:<15} | R${preco:>7.2f} | Estoque: {est}")
    print()

def editar_produto():
    listar_produtos()
    pid = input("ID do produto para editar: ").strip()
    cur.execute("SELECT * FROM produtos WHERE id = ?", (pid,))
    p = cur.fetchone()
    if not p:
        print("❌ Produto não encontrado.\n")
        return
    novo_nome = input(f"Novo nome [{p[1]}]: ") or p[1]
    novo_preco = input(f"Novo preço [{p[2]:.2f}]: ") or p[2]
    novo_estoque = input(f"Novo estoque [{p[3]}]: ") or p[3]
    cur.execute("UPDATE produtos SET nome=?, preco=?, estoque=? WHERE id=?", (novo_nome, float(novo_preco), int(novo_estoque), pid))
    con.commit()
    print("✅ Produto atualizado!\n")

def remover_produto():
    listar_produtos()
    pid = input("ID do produto para remover: ").strip()
    cur.execute("SELECT nome FROM produtos WHERE id = ?", (pid,))
    p = cur.fetchone()
    if not p:
        print("❌ Produto não encontrado.\n")
        return
    if input(f"Remover '{p[0]}'? (s/n): ").lower() == "s":
        cur.execute("DELETE FROM produtos WHERE id = ?", (pid,))
        con.commit()
        print("✅ Produto removido!\n")
    else:
        print("🚫 Cancelado.\n")

def pesquisar_produto():
    termo = input("Buscar por nome: ").strip()
    cur.execute("SELECT * FROM produtos WHERE nome LIKE ?", (f"%{termo}%",))
    res = cur.fetchall()
    if not res:
        print("😕 Nenhum produto encontrado.\n")
        return
    for id_, nome, preco, est in res:
        print(f"ID {id_} | {nome} | R${preco:.2f} | Estoque: {est}")