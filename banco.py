import sqlite3

import sqlite3

# Cria o banco de dados e a tabela de imagens, caso não existam
def criar_banco():
    with sqlite3.connect("banco.db") as conexao:
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

# Insere um novo registro de imagem no banco de dados
def salvar_imagem(nome, caminho, descricao=""):
    with sqlite3.connect("banco.db") as conexao:
        cursor = conexao.cursor()
        cursor.execute("""
            INSERT INTO imagens (nome_original, caminho, descricao)
            VALUES (?, ?, ?)
        """, (nome, caminho, descricao))
        conexao.commit()

# Retorna todos os registros de imagens ordenados por ID
def carregar_imagens():
    with sqlite3.connect("banco.db") as conexao:
        cursor = conexao.cursor()
        cursor.execute("""
            SELECT id, nome_original, caminho, descricao
            FROM imagens
            ORDER BY id
        """)
        return cursor.fetchall()

# Filtra imagens cujo nome ou descrição contenham o termo buscado
def buscar_imagens(termo):
    with sqlite3.connect("banco.db") as conexao:
        cursor = conexao.cursor()
        busca = f"%{termo}%"
        cursor.execute("""
            SELECT id, nome_original, caminho, descricao
            FROM imagens
            WHERE nome_original LIKE ? OR descricao LIKE ?
            ORDER BY id
        """, (busca, busca))
        return cursor.fetchall()

# Remove uma imagem do banco de dados com base no seu ID
def deletar_imagem(id_imagem):
    with sqlite3.connect("banco.db") as conexao:
        cursor = conexao.cursor()
        cursor.execute("DELETE FROM imagens WHERE id = ?", (id_imagem,))
        conexao.commit()