import tkinter as tk
from tkinter import ttk, messagebox
from module.peca import consultar_pecas, cadastrar_peca, atualizar_peca, excluir_peca
from module.admin import verificar_permissao_admin, deletar_usuario

def abrir_tela_principal(usuario_atual):
    # Criando a janela principal
    janela_principal = tk.Tk()
    janela_principal.title("Tela Principal - Gerenciamento de Peças")
    
    # Verifica se o usuário é administrador
    is_admin = verificar_permissao_admin(usuario_atual)

    # Configuração de estilo para a Treeview
    style = ttk.Style()
    style.configure("Treeview", font=("Arial", 10))
    style.configure("Treeview.Heading", font=("Arial", 12, "bold"))

    def carregar_pecas():
        for item in tree.get_children():
            tree.delete(item)
        pecas = consultar_pecas()
        for peca in pecas:
            tree.insert("", "end", values=(peca[0], peca[1], peca[2], peca[3], peca[4]))

    def adicionar_peca():
        def salvar_nova_peca():
            nome = entry_nome.get()
            tipo = entry_tipo.get()
            try:
                quantidade = int(entry_quantidade.get())
                preco = float(entry_preco.get())
                if not nome or not tipo or quantidade <= 0 or preco <= 0:
                    messagebox.showerror("Erro", "Preencha todos os campos corretamente.")
                    return
                cadastrar_peca(nome, tipo, quantidade, preco)
                messagebox.showinfo("Sucesso", "Peça cadastrada com sucesso!")
                adicionar_peca_window.destroy()
                carregar_pecas()
            except ValueError:
                messagebox.showerror("Erro", "Preencha todos os campos corretamente.")

        adicionar_peca_window = tk.Toplevel(janela_principal)
        adicionar_peca_window.title("Adicionar Nova Peça")
        tk.Label(adicionar_peca_window, text="Nome da Peça").pack(pady=5)
        entry_nome = tk.Entry(adicionar_peca_window)
        entry_nome.pack(pady=5)
        tk.Label(adicionar_peca_window, text="Tipo da Peça").pack(pady=5)
        entry_tipo = tk.Entry(adicionar_peca_window)
        entry_tipo.pack(pady=5)
        tk.Label(adicionar_peca_window, text="Quantidade").pack(pady=5)
        entry_quantidade = tk.Entry(adicionar_peca_window)
        entry_quantidade.pack(pady=5)
        tk.Label(adicionar_peca_window, text="Preço").pack(pady=5)
        entry_preco = tk.Entry(adicionar_peca_window)
        entry_preco.pack(pady=5)
        tk.Button(adicionar_peca_window, text="Salvar", command=salvar_nova_peca).pack(pady=10)

    def editar_peca():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showerror("Erro", "Selecione uma peça para editar.")
            return
        peca_id = int(tree.item(selected_item, "values")[0])
        def salvar_edicao_peca():
            novo_nome = entry_nome.get()
            novo_tipo = entry_tipo.get()
            try:
                nova_quantidade = int(entry_quantidade.get())
                novo_preco = float(entry_preco.get())
                if not novo_nome or not novo_tipo or nova_quantidade <= 0 or novo_preco <= 0:
                    messagebox.showerror("Erro", "Preencha todos os campos corretamente.")
                    return
                atualizar_peca(peca_id, novo_nome, novo_tipo, nova_quantidade, novo_preco)
                messagebox.showinfo("Sucesso", "Peça atualizada com sucesso!")
                editar_peca_window.destroy()
                carregar_pecas()
            except ValueError:
                messagebox.showerror("Erro", "Preencha todos os campos corretamente.")
        editar_peca_window = tk.Toplevel(janela_principal)
        editar_peca_window.title("Editar Peça")
        tk.Label(editar_peca_window, text="Nome da Peça").pack(pady=5)
        entry_nome = tk.Entry(editar_peca_window)
        entry_nome.pack(pady=5)
        tk.Label(editar_peca_window, text="Tipo da Peça").pack(pady=5)
        entry_tipo = tk.Entry(editar_peca_window)
        entry_tipo.pack(pady=5)
        tk.Label(editar_peca_window, text="Quantidade").pack(pady=5)
        entry_quantidade = tk.Entry(editar_peca_window)
        entry_quantidade.pack(pady=5)
        tk.Label(editar_peca_window, text="Preço").pack(pady=5)
        entry_preco = tk.Entry(editar_peca_window)
        entry_preco.pack(pady=5)
        pecas = consultar_pecas()
        peca = next(p for p in pecas if p[0] == peca_id)
        entry_nome.insert(0, peca[1])
        entry_tipo.insert(0, peca[2])
        entry_quantidade.insert(0, peca[3])
        entry_preco.insert(0, peca[4])
        tk.Button(editar_peca_window, text="Salvar", command=salvar_edicao_peca).pack(pady=10)

    def excluir_peca_ui():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showerror("Erro", "Selecione uma peça para excluir.")
            return
        peca_id = int(tree.item(selected_item, "values")[0])
        excluir_peca(peca_id)
        messagebox.showinfo("Sucesso", "Peça excluída com sucesso!")
        carregar_pecas()

    def excluir_usuario_ui():
        # Função para excluir usuário apenas para administradores
        def excluir_usuario():
            usuario_para_deletar = entrada_usuario.get()
            if not usuario_para_deletar:
                messagebox.showwarning("Atenção", "Por favor, insira o nome de um usuário.")
                return
            confirmar = messagebox.askyesno("Confirmação", f"Tem certeza de que deseja excluir o usuário '{usuario_para_deletar}'?")
            if confirmar:
                sucesso = deletar_usuario(usuario_atual, usuario_para_deletar)
                if sucesso:
                    messagebox.showinfo("Sucesso", f"O usuário '{usuario_para_deletar}' foi excluído com sucesso!")
                    entrada_usuario.delete(0, tk.END)
                else:
                    messagebox.showerror("Erro", f"Não foi possível excluir o usuário '{usuario_para_deletar}'.")
            else:
                messagebox.showinfo("Cancelado", "A exclusão foi cancelada.")

        # Janela para excluir usuário
        excluir_usuario_window = tk.Toplevel(janela_principal)
        excluir_usuario_window.title("Excluir Usuário")
        tk.Label(excluir_usuario_window, text="Nome do Usuário para excluir:").pack(pady=10)
        entrada_usuario = tk.Entry(excluir_usuario_window)
        entrada_usuario.pack(pady=5)
        tk.Button(excluir_usuario_window, text="Excluir Usuário", command=excluir_usuario).pack(pady=10)

    # Criando a Treeview para exibir as peças
    tree = ttk.Treeview(janela_principal, columns=("ID", "Nome", "Tipo", "Quantidade", "Preço"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Nome", text="Nome")
    tree.heading("Tipo", text="Tipo")
    tree.heading("Quantidade", text="Quantidade")
    tree.heading("Preço", text="Preço")
    tree.pack(pady=10, fill="both", expand=True)

    # Botões para usuários comuns
    tk.Button(janela_principal, text="Adicionar Peça", command=adicionar_peca).pack(side="left", padx=10)
    tk.Button(janela_principal, text="Editar Peça", command=editar_peca).pack(side="left", padx=10)
    tk.Button(janela_principal, text="Excluir Peça", command=excluir_peca_ui).pack(side="left", padx=10)

    # Botões exclusivos para administradores
    if is_admin:
        tk.Button(janela_principal, text="Excluir Usuário", command=excluir_usuario_ui).pack(side="left", padx=10)

    # Carregar as peças na inicialização
    carregar_pecas()

    # Iniciar a interface
    janela_principal.mainloop()