import sqlite3
from module.banco import conectar

# Função para verificar se o usuário é admin
def verificar_permissao_admin(usuario_atual):
    try:
        with conectar() as conexao:
            cursor = conexao.cursor()
            cursor.execute('''
                SELECT tipo_usuario FROM usuario WHERE usuario = ?
            ''', (usuario_atual,))
            tipo_usuario = cursor.fetchone()
            if tipo_usuario and tipo_usuario[0] == 'admin':
                return True
            else:
                return False
    except sqlite3.Error as e:
        print(f"[ERRO] Falha ao verificar permissões do usuário: {e}")
        return False

# Função para deletar usuário
def deletar_usuario(usuario_atual, usuario_para_deletar):
    if not verificar_permissao_admin(usuario_atual):
        print("[ERRO] Permissão negada. Somente administradores podem excluir usuários.")
        return
    
    try:
        with conectar() as conexao:
            cursor = conexao.cursor()
            cursor.execute('''
                DELETE FROM usuario WHERE usuario = ?
            ''', (usuario_para_deletar,))
            conexao.commit()
            print(f"[INFO] Usuário '{usuario_para_deletar}' excluído com sucesso.")
    except sqlite3.Error as e:
        print(f"[ERRO] Falha ao excluir o usuário: {e}")