import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

# Funções utilitárias para arquivos JSON
def carregar_dados(arquivo):
    if os.path.exists(arquivo):
        with open(arquivo, "r") as f:
            return json.load(f)
    return []

def salvar_dados(dados, arquivo):
    with open(arquivo, "w") as f:
        json.dump(dados, f, indent=4)

# Geradores de ID automático
def gerar_proximo_id(lista):
    if not lista:
        return "1"
    ids = [int(item['id']) for item in lista if 'id' in item]
    return str(max(ids) + 1)

def gerar_proximo_id_produto(produtos):
    if not produtos:
        return "p1"
    ids = [int(produto['id'][1:]) for produto in produtos if 'id' in produto and produto['id'].startswith('p')]
    return f"p{max(ids) + 1}"

# Dados principais
usuarios = carregar_dados("usuarios.json")
produtos = carregar_dados("produtos.json")
lista_compras = carregar_dados("lista_compras.json")

# Funções principais
def cadastrar_usuario():
    janela = tk.Toplevel(root)
    janela.title("Cadastrar Usuário")

    tk.Label(janela, text="Nome:").grid(row=0, column=0, padx=5, pady=5)
    entrada_nome = tk.Entry(janela)
    entrada_nome.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(janela, text="E-mail:").grid(row=1, column=0, padx=5, pady=5)
    entrada_email = tk.Entry(janela)
    entrada_email.grid(row=1, column=1, padx=5, pady=5)

    def salvar_usuario():
        nome = entrada_nome.get().strip()
        email = entrada_email.get().strip()
        if nome and email:
            novo_usuario = {
                "id": gerar_proximo_id(usuarios),
                "nome": nome,
                "email": email
            }
            usuarios.append(novo_usuario)
            salvar_dados(usuarios, "usuarios.json")
            messagebox.showinfo("Sucesso", "Usuário cadastrado!")
            janela.destroy()
        else:
            messagebox.showerror("Erro", "Preencha todos os campos!")

    tk.Button(janela, text="Salvar", command=salvar_usuario).grid(row=2, column=0, columnspan=2, pady=10)

def cadastrar_produto():
    janela = tk.Toplevel(root)
    janela.title("Cadastrar Produto")

    tk.Label(janela, text="Nome do Produto:").grid(row=0, column=0, padx=5, pady=5)
    entrada_nome = tk.Entry(janela)
    entrada_nome.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(janela, text="Categoria:").grid(row=1, column=0, padx=5, pady=5)
    categoria = ttk.Combobox(janela, values=["Alimentos", "Limpeza", "Higiene", "Outros"])
    categoria.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(janela, text="Preço:").grid(row=2, column=0, padx=5, pady=5)
    entrada_preco = tk.Entry(janela)
    entrada_preco.grid(row=2, column=1, padx=5, pady=5)

    def salvar_produto():
        nome = entrada_nome.get().strip()
        cat = categoria.get().strip()
        try:
            preco = float(entrada_preco.get().strip())
        except ValueError:
            preco = None
        if nome and cat and preco is not None:
            novo_produto = {
                "id": gerar_proximo_id_produto(produtos),
                "nome": nome,
                "categoria": cat,
                "preco": preco
            }
            produtos.append(novo_produto)
            salvar_dados(produtos, "produtos.json")
            messagebox.showinfo("Sucesso", "Produto cadastrado!")
            janela.destroy()
        else:
            messagebox.showerror("Erro", "Preencha todos os campos corretamente!")

    tk.Button(janela, text="Salvar", command=salvar_produto).grid(row=3, column=0, columnspan=2, pady=10)

def adicionar_item_lista():
    janela = tk.Toplevel(root)
    janela.title("Adicionar Item à Lista")

    tk.Label(janela, text="Usuário:").grid(row=0, column=0, padx=5, pady=5)
    usuarios_combo = ttk.Combobox(janela, values=[f"{u['id']} - {u['nome']}" for u in usuarios])
    usuarios_combo.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(janela, text="Produto:").grid(row=1, column=0, padx=5, pady=5)
    produtos_combo = ttk.Combobox(janela, values=[f"{p['id']} - {p['nome']}" for p in produtos])
    produtos_combo.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(janela, text="Quantidade:").grid(row=2, column=0, padx=5, pady=5)
    entrada_qtd = tk.Entry(janela)
    entrada_qtd.grid(row=2, column=1, padx=5, pady=5)

    tk.Label(janela, text="Prioridade:").grid(row=3, column=0, padx=5, pady=5)
    prioridade_combo = ttk.Combobox(janela, values=["baixa", "média", "alta"])
    prioridade_combo.grid(row=3, column=1, padx=5, pady=5)

    def salvar_item():
        usuario_sel = usuarios_combo.get().split(" - ")[0]
        produto_sel = produtos_combo.get().split(" - ")[0]
        try:
            qtd = int(entrada_qtd.get().strip())
        except ValueError:
            qtd = None
        prioridade = prioridade_combo.get().strip()

        if usuario_sel and produto_sel and qtd is not None and prioridade:
            novo_item = {
                "id_usuario": usuario_sel,
                "id_produto": produto_sel,
                "quantidade": qtd,
                "prioridade": prioridade,
                "status": "a comprar",
                "data_adicionado": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            lista_compras.append(novo_item)
            salvar_dados(lista_compras, "lista_compras.json")
            messagebox.showinfo("Sucesso", "Item adicionado à lista!")
            janela.destroy()
        else:
            messagebox.showerror("Erro", "Preencha todos os campos corretamente!")

    tk.Button(janela, text="Salvar", command=salvar_item).grid(row=4, column=0, columnspan=2, pady=10)

def ver_lista_compras():
    janela = tk.Toplevel(root)
    janela.title("Lista de Compras")

    tree = ttk.Treeview(janela, columns=("Usuário", "Produto", "Qtd", "Prioridade", "Status", "Data"), show="headings")
    tree.heading("Usuário", text="Usuário")
    tree.heading("Produto", text="Produto")
    tree.heading("Qtd", text="Qtd")
    tree.heading("Prioridade", text="Prioridade")
    tree.heading("Status", text="Status")
    tree.heading("Data", text="Data")
    tree.grid(row=0, column=0, padx=5, pady=5)

    for item in lista_compras:
        usuario = next((u['nome'] for u in usuarios if u['id'] == item['id_usuario']), "Desconhecido")
        produto = next((p['nome'] for p in produtos if p['id'] == item['id_produto']), "Desconhecido")
        tree.insert("", "end", values=(usuario, produto, item['quantidade'], item['prioridade'], item['status'], item['data_adicionado']))

    def excluir_selecionado():
        selecionado = tree.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um item!")
            return
        idx = tree.index(selecionado[0])
        lista_compras.pop(idx)
        salvar_dados(lista_compras, "lista_compras.json")
        tree.delete(selecionado[0])
        messagebox.showinfo("Sucesso", "Item removido!")

    tk.Button(janela, text="Excluir Selecionado", command=excluir_selecionado).grid(row=1, column=0, pady=10)

# Interface principal
root = tk.Tk()
root.title("Lista de Compras - Sistema Familiar")
root.geometry("400x300")

tk.Label(root, text="Gerenciamento de Lista de Compras", font=("Arial", 14, "bold")).pack(pady=10)

tk.Button(root, text="Cadastrar Usuário", width=25, command=cadastrar_usuario).pack(pady=5)
tk.Button(root, text="Cadastrar Produto", width=25, command=cadastrar_produto).pack(pady=5)
tk.Button(root, text="Adicionar Item à Lista", width=25, command=adicionar_item_lista).pack(pady=5)
tk.Button(root, text="Ver Lista de Compras", width=25, command=ver_lista_compras).pack(pady=5)

root.mainloop()
