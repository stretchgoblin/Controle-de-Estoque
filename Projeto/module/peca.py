from .banco import conectar

def cadastrar_peca(nome, tipo, quantidade, preco):
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute(''' 
            INSERT INTO pecas (nome, tipo, quantidade, preco)
            VALUES (?, ?, ?, ?)
        ''', (nome, tipo, quantidade, preco))
        conexao.commit()
    except Exception as e:
        print(f"[ERRO] Falha ao cadastrar peça: {e}")
    finally:
        conexao.close()

def consultar_pecas():
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM pecas")
        pecas = cursor.fetchall()
        return pecas
    except Exception as e:
        print(f"[ERRO] Falha ao consultar peças: {e}")
        return []
    finally:
        conexao.close()

def atualizar_peca(id_peca, novo_nome, novo_tipo, nova_quantidade, novo_preco):
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute(''' 
            UPDATE pecas
            SET nome = ?, tipo = ?, quantidade = ?, preco = ?
            WHERE id = ?
        ''', (novo_nome, novo_tipo, nova_quantidade, novo_preco, id_peca))
        conexao.commit()
    except Exception as e:
        print(f"[ERRO] Falha ao atualizar peça: {e}")
    finally:
        conexao.close()

def excluir_peca(id_peca):
    try:
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute('DELETE FROM pecas WHERE id = ?', (id_peca,))
        conexao.commit()
    except Exception as e:
        print(f"[ERRO] Falha ao excluir peça: {e}")
    finally:
        conexao.close()