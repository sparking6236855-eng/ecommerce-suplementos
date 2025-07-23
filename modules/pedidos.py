from database.connection import conectar

def adicionar_ao_carrinho():
    con = conectar()
    cur = con.cursor()

    produto_id = input("ID do produto: ")
    quantidade = int(input("Quantidade: "))

    cur.execute("SELECT preco FROM produtos WHERE id = ?", (produto_id,))
    produto = cur.fetchone()

    if not produto:
        print("❌ Produto não encontrado.")
        con.close()
        return

    preco = produto[0]
    subtotal = preco * quantidade

    cur.execute("""
        INSERT INTO itens_pedido (pedido_id, produto_id, quantidade, subtotal)
        VALUES (NULL, ?, ?, ?)
    """, (produto_id, quantidade, subtotal))

    con.commit()
    con.close()
    print("✅ Item adicionado ao carrinho!\n")


def finalizar_pedido():
    con = conectar()
    cur = con.cursor()

    cur.execute("""
        SELECT produto_id, quantidade, subtotal FROM itens_pedido
        WHERE pedido_id IS NULL
    """)
    itens = cur.fetchall()

    if not itens:
        print("🛒 Carrinho vazio.\n")
        con.close()
        return

    total = sum(item[2] for item in itens)

    from datetime import datetime
    data = datetime.now().strftime("%d/%m/%Y %H:%M")

    cur.execute("INSERT INTO pedidos (data, total) VALUES (?, ?)", (data, total))
    pedido_id = cur.lastrowid

    for produto_id, quantidade, subtotal in itens:
        cur.execute("""
            UPDATE itens_pedido
            SET pedido_id = ?
            WHERE produto_id = ? AND pedido_id IS NULL
        """, (pedido_id, produto_id))

        cur.execute("""
            UPDATE produtos
            SET estoque = estoque - ?
            WHERE id = ?
        """, (quantidade, produto_id))

    con.commit()
    con.close()
    print(f"✅ Pedido finalizado! Total: R${total:.2f}\n")


def visualizar_pedidos():
    con = conectar()
    cur = con.cursor()

    cur.execute("SELECT id, data, total FROM pedidos ORDER BY id DESC")
    pedidos = cur.fetchall()

    if not pedidos:
        print("🗂️ Nenhum pedido registrado.\n")
        con.close()
        return

    for pid, data, total in pedidos:
        print(f"\n🧾 Pedido #{pid} | {data} | Total: R${total:.2f}")
        cur.execute("""
            SELECT produto_id, quantidade, subtotal FROM itens_pedido
            WHERE pedido_id = ?
        """, (pid,))
        itens = cur.fetchall()
        for prod_id, qtd, sub in itens:
            cur.execute("SELECT nome FROM produtos WHERE id = ?", (prod_id,))
            nome = cur.fetchone()[0]
            print(f" - {nome} x{qtd} → R${sub:.2f}")

    con.close()
    print()