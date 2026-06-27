import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

from banco import (
    criar_banco,
    salvar_imagem,
    carregar_imagens
)


# Cria o banco caso não exista
criar_banco()


# Lista que armazenará as imagens carregadas
imagens = carregar_imagens()

indice_atual = 0


def atualizar_visualizacao():
    global imagens
    global indice_atual

    if not imagens:
        label_nome.config(text="Nenhuma imagem cadastrada")
        label_contador.config(text="0 de 0")
        return

    _, nome, caminho = imagens[indice_atual]

    label_nome.config(text=nome)

    label_contador.config(
        text=f"{indice_atual + 1} de {len(imagens)}"
    )


def adicionar_imagem():
    global imagens
    global indice_atual

    arquivo = filedialog.askopenfilename(
        title="Selecione uma imagem",
        filetypes=[
            ("Imagens", "*.jpg *.jpeg *.png *.webp")
        ]
    )

    if not arquivo:
        return

    nome = os.path.basename(arquivo)

    salvar_imagem(nome, arquivo)

    imagens = carregar_imagens()

    indice_atual = len(imagens) - 1

    atualizar_visualizacao()


def proxima_imagem():
    global indice_atual

    if not imagens:
        return

    if indice_atual < len(imagens) - 1:
        indice_atual += 1

    atualizar_visualizacao()


def imagem_anterior():
    global indice_atual

    if not imagens:
        return

    if indice_atual > 0:
        indice_atual -= 1

    atualizar_visualizacao()


janela = tk.Tk()

janela.title("Gerenciador de Imagens")

janela.geometry("700x400")


titulo = ttk.Label(
    janela,
    text="Gerenciador de Imagens",
    font=("Arial", 18)
)

titulo.pack(pady=20)


frame_visualizacao = ttk.Frame(janela)

frame_visualizacao.pack(pady=20)


label_nome = ttk.Label(
    frame_visualizacao,
    text="Nenhuma imagem cadastrada",
    font=("Arial", 14)
)

label_nome.pack()


label_contador = ttk.Label(
    frame_visualizacao,
    text="0 de 0",
    font=("Arial", 10)
)

label_contador.pack(pady=10)


frame_botoes = ttk.Frame(janela)

frame_botoes.pack(pady=20)


botao_anterior = ttk.Button(
    frame_botoes,
    text="◀ Anterior",
    command=imagem_anterior
)

botao_anterior.grid(
    row=0,
    column=0,
    padx=10
)


botao_adicionar = ttk.Button(
    frame_botoes,
    text="Adicionar Imagem",
    command=adicionar_imagem
)

botao_adicionar.grid(
    row=0,
    column=1,
    padx=10
)


botao_proximo = ttk.Button(
    frame_botoes,
    text="Próxima ▶",
    command=proxima_imagem
)

botao_proximo.grid(
    row=0,
    column=2,
    padx=10
)


atualizar_visualizacao()

janela.mainloop()