import tkinter as tk
from tkinter import messagebox
from module.admin import verificar_permissao_admin, deletar_usuario

def abrir_menu_admin(usuario_atual):
    # Verifica se o tipo de usuário é 'admin' utilizando a função verificar_admin
    if not verificar_permissao_admin(usuario_atual):  # Função que verifica se o usuário é admin
        messagebox.showerror("Erro", "Acesso negado! Apenas administradores podem acessar esta seção.")
        return

    # Criando a janela do menu administrativo
    janela_admin = tk.Toplevel()
    janela_admin.title("Menu Administrativo")
    janela_admin.geometry("400x300")

    def excluir_usuario():
        # Verifica se a janela e os widgets ainda existem
        if not janela_admin.winfo_exists():
            messagebox.showerror("Erro", "A janela administrativa foi fechada.")
            return
        
        if not entrada_usuario.winfo_exists():
            messagebox.showerror("Erro", "O campo de entrada não está disponível.")
            return

        usuario_para_deletar = entrada_usuario.get()
        if not usuario_para_deletar:
            messagebox.showwarning("Atenção", "Por favor, insira o nome de um usuário.")
            return

        confirmar = messagebox.askyesno("Confirmação", f"Tem certeza de que deseja excluir o usuário '{usuario_para_deletar}'?")
        if confirmar:
            sucesso = deletar_usuario(usuario_atual, usuario_para_deletar)
            if sucesso:
                messagebox.showinfo("Sucesso", f"O usuário '{usuario_para_deletar}' foi excluído com sucesso!")
                entrada_usuario.delete(0, tk.END)  # Limpa o campo de entrada
            else:
                messagebox.showerror("Erro", f"Não foi possível excluir o usuário '{usuario_para_deletar}'.")
        else:
            messagebox.showinfo("Cancelado", "A exclusão foi cancelada.")

    def sair():
        janela_admin.destroy()

    # Título do menu
    label_titulo = tk.Label(janela_admin, text="Menu Administrativo", font=("Arial", 16))
    label_titulo.pack(pady=10)

    # Entrada para o nome do usuário a ser excluído
    label_usuario = tk.Label(janela_admin, text="Usuário para excluir:", font=("Arial", 12))
    label_usuario.pack(pady=5)
    entrada_usuario = tk.Entry(janela_admin, font=("Arial", 12), width=30)
    entrada_usuario.pack(pady=5)

    # Botão para excluir usuário
    botao_excluir = tk.Button(janela_admin, text="Excluir Usuário", font=("Arial", 12), bg="red", fg="white", command=excluir_usuario)
    botao_excluir.pack(pady=10)

    # Botão para sair
    botao_sair = tk.Button(janela_admin, text="Sair", font=("Arial", 12), command=sair)
    botao_sair.pack(pady=10)

    janela_admin.mainloop()
