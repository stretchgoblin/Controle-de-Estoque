import hashlib
import os
import sqlite3
from .banco import conectar

# Função para criptografar a senha com SHA-256 e um salt
def criptografar_senha(senha):
    salt = os.urandom(16)  # Gera um salt aleatório de 16 bytes
    senha_com_salt = salt + senha.encode('utf-8')  # Concatena o salt com a senha
    senha_criptografada = hashlib.sha256(senha_com_salt).hexdigest()  # Criptografa a senha com o salt
    return salt.hex(), senha_criptografada  # Retorna o salt e o hash da senha

# Função para verificar login
def verificar_login(usuario, senha):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT usuario, senha, salt FROM usuario WHERE usuario = ?", (usuario,))
    dados_usuario = cursor.fetchone()
    conexao.close()

    if dados_usuario:
        nome_usuario, senha_armazenada, salt_armazenado = dados_usuario
        salt_armazenado = bytes.fromhex(salt_armazenado)  # Converte o salt de volta para bytes
        senha_criptografada = hashlib.sha256(salt_armazenado + senha.encode('utf-8')).hexdigest()  # Criptografa a senha inserida
        if senha_armazenada == senha_criptografada:
            return True  # Login bem-sucedido
    return False

# Função para verificar o tipo de usuário (admin ou comum)
def obter_tipo_usuario(usuario):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT tipo_usuario FROM usuario WHERE usuario = ?", (usuario,))
    dados_usuario = cursor.fetchone()
    conexao.close()

    if dados_usuario:
        tipo_usuario = dados_usuario[0]
        return tipo_usuario  # Retorna 'admin' ou 'comum'
    return "comum"  # Se não encontrar, retorna 'comum'

# Função para cadastrar um novo usuário
def cadastrar_usuario(nome_usuario, senha_usuario, tipo_usuario='usuario'):
    salt, senha_criptografada = criptografar_senha(senha_usuario)
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("INSERT INTO usuario (usuario, senha, salt, tipo_usuario) VALUES (?, ?, ?, ?)", 
                   (nome_usuario, senha_criptografada, salt, tipo_usuario))
    conexao.commit()
    conexao.close()
    print(f"[INFO] Usuário '{nome_usuario}' cadastrado com sucesso.")