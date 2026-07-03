import urllib.request
import os
from banco import salvar_imagem

def baixar_imagens_teste(quantidade=5):
    print(f"Iniciando o download de {quantidade} imagens aleatórias...")
    
    for i in range(1, quantidade + 1):
        nome_arquivo = f"teste_aleatorio_{i}.jpg"
        # Pega o caminho completo da imagem
        caminho_completo = os.path.abspath(nome_arquivo)
        
        print(f"Baixando {nome_arquivo}...")
        
        # Site gera imagens aleatórias(500x350)
        url = "https://picsum.photos/500/350"
        
        try:
            # Faz o download e salva o arquivo na pasta
            urllib.request.urlretrieve(url, nome_arquivo)
            
            # Já insere direto no seu banco de dados
            salvar_imagem(nome_arquivo, caminho_completo, descricao=f"Imagem gerada automaticamente - Teste {i}")
        except Exception as e:
            print(f"Erro ao baixar a imagem {i}: {e}")

    print("\n✅ Pronto! Imagens baixadas e cadastradas no banco com sucesso.")
    print("vitor doa o cu")

#função para baixar 5 imagens
baixar_imagens_teste(5)