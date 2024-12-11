import sqlite3

def conectar(caminho='estoque.db'):
    try:
        conexao = sqlite3.connect(caminho)
        print(f"[INFO] Conexão estabelecida com o banco de dados '{caminho}'.")
        return conexao
    except sqlite3.Error as e:
        print(f"[ERRO] Não foi possível conectar ao banco de dados: {e}")
        return None