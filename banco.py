import sqlite3


def criar_banco():
    conexao = sqlite3.connect("banco.db")
    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS imagens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_original TEXT NOT NULL,
            caminho TEXT NOT NULL,
            descricao TEXT,
            data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conexao.commit()
    conexao.close()


def salvar_imagem(nome, caminho):
    conexao = sqlite3.connect("banco.db")
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO imagens (
            nome_original,
            caminho
        )
        VALUES (?, ?)
    """, (nome, caminho))

    conexao.commit()
    conexao.close()


def carregar_imagens():
    conexao = sqlite3.connect("banco.db")
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT id, nome_original, caminho
        FROM imagens
        ORDER BY id
    """)

    imagens = cursor.fetchall()

    conexao.close()

    return imagens