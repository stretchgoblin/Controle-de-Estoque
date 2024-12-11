import sqlite3

def conectar(caminho='estoque.db'):
    try:
        conexao = sqlite3.connect(caminho)
        print(f"[INFO] Conectando ao banco de dados em {caminho}.")
        return conexao
    except sqlite3.Error as e:
        print(f"[ERRO] Falha ao conectar ao banco de dados: {e}")
        raise

def criar_tabela_pecas():
    try:
        with conectar() as conexao:
            cursor = conexao.cursor()  # Criando o cursor aqui
            print("[INFO] Criando a tabela pecas, se não existir.")
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS pecas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    tipo TEXT NOT NULL,
                    quantidade INTEGER NOT NULL,  -- Alterado para INTEGER
                    preco REAL NOT NULL  -- Alterado para REAL
                )
            ''')
            conexao.commit()
            print("[INFO] Tabela 'pecas' criada com sucesso.")
            cursor.execute("PRAGMA table_info(pecas);")
            tabela_info = cursor.fetchall()
            if tabela_info:
                print("[INFO] A tabela 'pecas' existe com as colunas:", tabela_info)
            else:
                print("[ERRO] A tabela 'pecas' não foi criada corretamente.")
    except sqlite3.Error as e:
        print(f"[ERRO] Falha ao criar a tabela 'pecas': {e}")
        raise

def criar_tabela_usuario():
    try:
        with conectar() as conexao:
            cursor = conexao.cursor()  # Criando o cursor aqui
            print("[INFO] Criando a tabela 'usuario', se não existir.")
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS usuario (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    usuario TEXT NOT NULL UNIQUE,
                    senha TEXT NOT NULL,
                    salt TEXT NOT NULL,
                    tipo_usuario TEXT CHECK(tipo_usuario IN ('comum', 'admin')) NOT NULL
                )
            ''')
            conexao.commit()
            print("[INFO] Tabela 'usuario' criada/verificada com sucesso.")
            cursor.execute("PRAGMA table_info(usuario);")
            tabela_info = cursor.fetchall()
            if tabela_info:
                print("[INFO] A tabela 'usuario' existe com as colunas:", tabela_info)
            else:
                print("[ERRO] A tabela 'usuario' não foi criada corretamente.")
    except sqlite3.Error as e:
        print(f"[ERRO] Falha ao criar a tabela 'usuario': {e}")
        raise

def listar_tabelas():
    try:
        with conectar() as conexao:
            cursor = conexao.cursor()  # Criando o cursor aqui
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tabelas = cursor.fetchall()
            print("[INFO] Tabelas no banco de dados:", tabelas)
    except sqlite3.Error as e:
        print(f"[ERRO] Falha ao listar as tabelas: {e}")

def inserir_peca(nome, tipo, quantidade, preco):
    try:
        if not nome or not tipo or quantidade <= 0 or preco <= 0:
            print("[ERRO] Dados inválidos para inserção!")
            return
        
        with conectar() as conexao:
            cursor = conexao.cursor()  # Criando o cursor aqui
            cursor.execute('''
                INSERT INTO pecas (nome, tipo, quantidade, preco)
                VALUES (?, ?, ?, ?)
            ''', (nome, tipo, quantidade, preco))
            conexao.commit()
            print(f"[INFO] Peça '{nome}' adicionada com sucesso!")
    except sqlite3.Error as e:
        print(f"[ERRO] Falha ao inserir a peça: {e}")

def consultar_pecas(nome=None, tipo=None):
    try:
        with conectar() as conexao:
            cursor = conexao.cursor()  # Criando o cursor aqui
            query = "SELECT * FROM pecas WHERE 1=1"
            params = []
            
            if nome:
                query += " AND nome LIKE ?"
                params.append(f"%{nome}%")
            if tipo:
                query += " AND tipo LIKE ?"
                params.append(f"%{tipo}%")
            
            cursor.execute(query, params)
            pecas = cursor.fetchall()
            if pecas:
                print("[INFO] Peças encontradas:", pecas)
            else:
                print("[INFO] Nenhuma peça encontrada.")
            return pecas
    except sqlite3.Error as e:
        print(f"[ERRO] Falha ao consultar as peças: {e}")
        return []

if __name__ == "__main__":
    # Criar/verificar tabelas
    criar_tabela_usuario()  # Cria a tabela 'usuario'
    criar_tabela_pecas()  # Cria a tabela 'pecas'

    # Verificar se as tabelas foram criadas corretamente
    listar_tabelas()  # Exibe as tabelas no banco de dados