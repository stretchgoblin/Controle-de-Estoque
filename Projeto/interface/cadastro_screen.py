import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from module.usuario import cadastrar_usuario  # Importando a função de cadastro de usuário
from interface.admin_screen import abrir_menu_admin

def abrir_tela_cadastro():
    # Criando a janela de cadastro
    cadastro_window = tk.Toplevel()
    cadastro_window.title("Cadastrar Novo Usuário")
    cadastro_window.geometry("600x300")  # Tamanho desejado para a janela
    cadastro_window.resizable(True, True)  # Impede redimensionamento da janela

    # Definindo o layout da janela de cadastro com o uso de um Frame
    frame = tk.Frame(cadastro_window)
    frame.pack(padx=20, pady=20, fill='both', expand=True)  # O fill='both' e expand=True garantem que o frame ocupe toda a janela

    # Nome de Usuário
    tk.Label(frame, text="Nome de Usuário").grid(row=0, column=0, pady=5, sticky='w')
    entry_nome_usuario = tk.Entry(frame)
    entry_nome_usuario.grid(row=0, column=1, pady=5, sticky='ew')  # Expande para preencher a linha

    # Senha
    tk.Label(frame, text="Senha").grid(row=1, column=0, pady=5, sticky='w')
    entry_senha = tk.Entry(frame, show="*")  # Campo de senha
    entry_senha.grid(row=1, column=1, pady=5, sticky='ew')  # Expande para preencher a linha

    # Tipo de Usuário
    tk.Label(frame, text="Tipo de Usuário").grid(row=2, column=0, pady=5, sticky='w')
    tipo_usuario_var = tk.StringVar(value='usuario')  # Valor padrão é 'usuario'
    
    # Criando os Radiobuttons para escolher o tipo de usuário
    usuario_rb = tk.Radiobutton(frame, text="Usuário", variable=tipo_usuario_var, value='usuario')
    usuario_rb.grid(row=2, column=1, sticky='w', padx=10)

    admin_rb = tk.Radiobutton(frame, text="Administrador", variable=tipo_usuario_var, value='admin')
    admin_rb.grid(row=3, column=1, sticky='w', padx=10)

    # Função chamada ao clicar em "Cadastrar Novo Usuário"
    def salvar_novo_usuario():
        nome_usuario = entry_nome_usuario.get().strip()  # Remove espaços extras
        senha_usuario = entry_senha.get().strip()  # Remove espaços extras
        tipo_usuario = tipo_usuario_var.get()  # Pega o tipo de usuário selecionado

        # Verificar se os campos não estão vazios
        if not nome_usuario or not senha_usuario:
            messagebox.showerror("Erro", "Nome de usuário e senha são obrigatórios.")
            return

        # Mapeia 'usuario' para 'comum' antes de salvar
        if tipo_usuario == 'usuario':
            tipo_usuario = 'comum'
        
        try:
            # Chama a função de cadastro do model para registrar o novo usuário
            cadastrar_usuario(nome_usuario, senha_usuario, tipo_usuario)
            messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")

            # Limpar os campos após o cadastro bem-sucedido
            entry_nome_usuario.delete(0, tk.END)
            entry_senha.delete(0, tk.END)
            tipo_usuario_var.set('usuario')  # Resetar o tipo de usuário para 'usuario'

            # Fechar a janela de cadastro
            cadastro_window.destroy()
        
        except Exception as e:  # Captura qualquer erro que ocorra durante o processo
            messagebox.showerror("Erro", f"Erro ao cadastrar usuário: {e}")

    # Botão de cadastro
    botao_cadastrar = ttk.Button(cadastro_window, text="Cadastrar", command=salvar_novo_usuario)
    botao_cadastrar.pack(pady=20)

    cadastro_window.mainloop()