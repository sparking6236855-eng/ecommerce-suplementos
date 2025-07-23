import sqlite3
from datetime import datetime

con = sqlite3.connect("suplementos.db")
cur = con.cursor()

carrinho = []

def adicionar_ao_carrinho():
    from produtos import listar_produtos
    listar_produtos()
    pid = input("ID do produto: ").strip()
    qtd = int(input("Quantidade: "))
    cur.execute("SELECT estoque FROM produtos WHERE id = ?", (pid,))
    row = cur.fetchone()
    if row and row[0] >= qtd:
        carrinho.append((int(pid), qtd))
        print("✅ Adicionado ao carrinho!\n")
    else:
        print("❌ Estoque insuficiente ou produto inválido.\n")

def finalizar_pedido():
    if not carrinho:
        print("🛒 Carrinho vazio.\n")
        return
    total = 0
    for pid, qtd in carrinho:
        cur.execute("SELECT preco FROM produtos WHERE id = ?", (pid,))
        total += cur.fetchone()[0] * qtd
    data = datetime.now().strftime("%Y-%m-%d %H:%M")
    cur.execute("INSERT INTO pedidos (data, total) VALUES (?, ?)", (data, total))
    pedido_id = cur.lastrowid
    for pid, qtd in carrinho:
        cur.execute("SELECT preco FROM produtos WHERE id = ?", (pid,))
        preco = cur.fetchone()[0]
        subtotal = preco * qtd
        cur.execute("INSERT INTO itens_pedido (pedido_id, produto_id, quantidade, subtotal) VALUES (?, ?, ?, ?)", (pedido_id, pid, qtd, subtotal))
        cur.execute("UPDATE produtos SET estoque = estoque - ? WHERE id = ?", (qtd, pid))
    con.commit()
    carrinho.clear()
    print(f"✅ Pedido #{pedido_id} finalizado! Total R${total:.2f}\n")

def visualizar_pedidos():
    cur.execute("SELECT * FROM pedidos ORDER BY data DESC")
    pedidos = cur.fetchall()
    if not pedidos:
        print("📭 Nenhum pedido registrado.\n")
        return
    for pid, data, total in pedidos:
        print(f"\n🧾 Pedido #{pid} | {data} | Total: R${total:.2f}")
        cur.execute("""
            SELECT p.nome, ip.quantidade, ip.subtotal
            FROM itens_pedido ip
            JOIN produtos p ON p.id = ip.produto_id
            WHERE ip.pedido_id = ?
        """, (pid,))
        for nome, qtd, sub in cur.fetchall():
            print(f"  - {nome} x{qtd} → R${sub:.2f}")
    print()