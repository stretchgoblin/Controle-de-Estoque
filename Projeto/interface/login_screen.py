import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from interface.principal_screen import abrir_tela_principal
from interface.admin_screen import abrir_menu_admin
from module.usuario import verificar_login, obter_tipo_usuario
from interface.cadastro_screen import abrir_tela_cadastro

def abrir_tela_login():
    janela_login = tk.Tk()
    janela_login.title("Tela de Login")

    def login():
        usuario = entry_usuario.get()
        senha = entry_senha.get()

        if verificar_login(usuario, senha):
            # Após o login, obtemos o tipo de usuário
            tipo_usuario = obter_tipo_usuario(usuario)
            print(f"Tipo de usuário: {tipo_usuario}")  # Para depuração
            
            janela_login.destroy()  # Fecha a tela de login
            
            if tipo_usuario == "admin":
                print("Abrindo menu do admin...")  # Depuração
                abrir_menu_admin(usuario)  # Chama a tela administrativa
            else:
                print("Abrindo tela principal...")  # Depuração
                abrir_tela_principal(usuario)  # Passa 'usuario' como argumento, não 'usuario_atual'
        else:
            messagebox.showerror("Erro de Login", "Nome de usuário ou senha incorretos.")

    # Criar a janela de login
    janela_login.geometry("600x300")

    # Labels e Entradas
    label_usuario = ttk.Label(janela_login, text="Usuário:")
    label_usuario.pack(pady=10)
    entry_usuario = ttk.Entry(janela_login)
    entry_usuario.pack(pady=5)

    label_senha = ttk.Label(janela_login, text="Senha:")
    label_senha.pack(pady=10)
    entry_senha = ttk.Entry(janela_login, show="*")
    entry_senha.pack(pady=5)

    # Botões
    botao_login = ttk.Button(janela_login, text="Entrar", command=login)
    botao_login.pack(pady=20)

    # Adiciona botão de cadastro
    botao_cadastro = tk.Button(janela_login, text="Cadastrar Novo Usuário", command=abrir_tela_cadastro)
    botao_cadastro.pack(pady=10)

    janela_login.mainloop()
