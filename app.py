import os
import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk 
from PIL import Image, ImageTk

# Importa as funções do módulo de banco de dados
from banco import criar_banco, salvar_imagem, carregar_imagens, buscar_imagens, deletar_imagem

# Configuração da paleta de cores (Tema Escuro Corporativo)
COR_FUNDO = "#121212"
COR_PAINEL = "#1E1E1E"
COR_BORDA = "#333337"
COR_TEXTO = "#FFFFFF"
COR_TEXTO_SECUNDARIO = "#A0A0AB"
COR_BOTAO = "#0066CC"
COR_BOTAO_HOVER = "#0052A3"  
COR_BOTAO_SECUNDARIO = "#2D2D30"
COR_BOTAO_SEC_HOVER = "#3E3E42"
COR_BOTAO_PERIGO = "#D9534F"
COR_BOTAO_PERIGO_HOVER = "#C9302C"

# Configuração das fontes
FONTE_TITULO = ("Segoe UI", 24, "bold")
FONTE_TEXTO = ("Segoe UI", 14)
FONTE_PEQUENA = ("Segoe UI", 12)

class GerenciadorImagensApp:
    def __init__(self, janela):
        self.janela = janela
        self.janela.title("SFS - Dashboard de Gestão")
        self.janela.geometry("950x800")
        
        # Aplica o tema escuro
        ctk.set_appearance_mode("dark")
        self.janela.configure(fg_color=COR_FUNDO)

        # Inicializa o banco de dados e carrega os dados
        criar_banco()
        self.imagens = carregar_imagens()
        self.indice_atual = 0

        # Constrói a interface e exibe a primeira imagem
        self.configurar_interface()
        self.atualizar_visualizacao()

    # Função auxiliar para padronizar a criação de botões
    def criar_botao(self, pai, texto, comando, cor_fundo=COR_BOTAO, cor_hover=COR_BOTAO_HOVER, cor_texto="#FFFFFF"):
        return ctk.CTkButton(
            pai, text=texto, command=comando,
            fg_color=cor_fundo, hover_color=cor_hover, text_color=cor_texto,
            font=FONTE_TEXTO, corner_radius=6, cursor="hand2", 
            border_width=0, height=40
        )

    def configurar_interface(self):
        # 1. Cabeçalho
        self.frame_topo = ctk.CTkFrame(self.janela, fg_color=COR_PAINEL, corner_radius=0)
        self.frame_topo.pack(fill="x", ipadx=20, ipady=15)

        self.label_logo = tk.Label(self.frame_topo, bg=COR_PAINEL)
        self.label_logo.pack(side="left", padx=20)
        self.carregar_logo()

        self.titulo = ctk.CTkLabel(self.frame_topo, text="Smart Floor Solutions", font=FONTE_TITULO, text_color=COR_TEXTO)
        self.titulo.pack(side="left", pady=10)

        # 2. Barra de pesquisa
        self.frame_pesquisa = ctk.CTkFrame(self.janela, fg_color=COR_FUNDO)
        self.frame_pesquisa.pack(pady=20, fill="x", padx=40)

        self.entry_pesquisa = ctk.CTkEntry(
            self.frame_pesquisa, font=FONTE_TEXTO, fg_color=COR_PAINEL, 
            text_color=COR_TEXTO, corner_radius=6, border_width=1, border_color=COR_BORDA,
            placeholder_text="Pesquisar por nome ou descrição...", placeholder_text_color=COR_TEXTO_SECUNDARIO
        )
        self.entry_pesquisa.pack(side="left", fill="x", expand=True, padx=(0, 10), ipady=5)
        self.entry_pesquisa.bind("<Return>", lambda event: self.realizar_pesquisa())

        self.btn_pesquisar = self.criar_botao(self.frame_pesquisa, "Pesquisar", self.realizar_pesquisa)
        self.btn_pesquisar.pack(side="left", padx=5)

        self.btn_limpar = self.criar_botao(self.frame_pesquisa, "Limpar", self.limpar_pesquisa, cor_fundo=COR_BOTAO_SECUNDARIO, cor_hover=COR_BOTAO_SEC_HOVER, cor_texto=COR_TEXTO)
        self.btn_limpar.pack(side="left", padx=5)

        # 3. Área de exibição da imagem
        self.frame_visualizacao = ctk.CTkFrame(self.janela, fg_color=COR_PAINEL, corner_radius=10, border_width=1, border_color=COR_BORDA)
        self.frame_visualizacao.pack(pady=10, padx=40, expand=True, fill="both")

        self.label_imagem = tk.Label(self.frame_visualizacao, text="Nenhum registo selecionado", font=FONTE_TEXTO, bg=COR_PAINEL, fg=COR_TEXTO_SECUNDARIO)
        self.label_imagem.pack(pady=(30, 10), expand=True)

        self.frame_info = ctk.CTkFrame(self.frame_visualizacao, fg_color="transparent")
        self.frame_info.pack(fill="x", side="bottom", pady=15)

        self.label_nome = ctk.CTkLabel(self.frame_info, text="", font=("Segoe UI", 16, "bold"), text_color=COR_TEXTO)
        self.label_nome.pack()

        self.label_contador = ctk.CTkLabel(self.frame_info, text="0 / 0", font=FONTE_PEQUENA, text_color=COR_TEXTO_SECUNDARIO)
        self.label_contador.pack()

        # 4. Botões de ação
        self.frame_botoes = ctk.CTkFrame(self.janela, fg_color=COR_FUNDO)
        self.frame_botoes.pack(pady=20)

        self.btn_anterior = self.criar_botao(self.frame_botoes, "◀ Anterior", self.imagem_anterior, cor_fundo=COR_BOTAO_SECUNDARIO, cor_hover=COR_BOTAO_SEC_HOVER, cor_texto=COR_TEXTO)
        self.btn_anterior.grid(row=0, column=0, padx=10)

        self.btn_adicionar = self.criar_botao(self.frame_botoes, "Adicionar Novo Registo", self.adicionar_imagem)
        self.btn_adicionar.grid(row=0, column=1, padx=10)

        self.btn_remover = self.criar_botao(self.frame_botoes, "Eliminar", self.remover_imagem, cor_fundo=COR_BOTAO_PERIGO, cor_hover=COR_BOTAO_PERIGO_HOVER)
        self.btn_remover.grid(row=0, column=2, padx=10)

        self.btn_proximo = self.criar_botao(self.frame_botoes, "Próxima ▶", self.proxima_imagem, cor_fundo=COR_BOTAO_SECUNDARIO, cor_hover=COR_BOTAO_SEC_HOVER, cor_texto=COR_TEXTO)
        self.btn_proximo.grid(row=0, column=3, padx=10)

    # Carrega a logo da empresa, caso o arquivo exista
    def carregar_logo(self):
        caminho_logo = "logo.png"
        if os.path.exists(caminho_logo):
            try:
                img = Image.open(caminho_logo)
                img.thumbnail((50, 50)) 
                self.img_logo_tk = ImageTk.PhotoImage(img)
                self.label_logo.config(image=self.img_logo_tk)
            except Exception:
                self.label_logo.config(text="[Logo]", fg=COR_TEXTO_SECUNDARIO)
        else:
            self.label_logo.config(text="[SFS]", font=("Segoe UI", 12, "bold"), fg=COR_BOTAO)

    # Executa a busca baseada no texto inserido
    def realizar_pesquisa(self):
        termo = self.entry_pesquisa.get().strip()
        if termo:
            self.imagens = buscar_imagens(termo)
            self.indice_atual = 0
            self.atualizar_visualizacao()
        else:
            self.limpar_pesquisa()

    # Restaura a lista completa de imagens
    def limpar_pesquisa(self):
        self.entry_pesquisa.delete(0, tk.END)
        self.imagens = carregar_imagens()
        self.indice_atual = 0
        self.atualizar_visualizacao()

    # Atualiza a interface com a imagem correspondente ao índice atual
    def atualizar_visualizacao(self):
        if not self.imagens:
            self.label_imagem.config(image="", text="Sem registos.")
            self.label_nome.configure(text="")
            self.label_contador.configure(text="0 / 0")
            return

        _, nome, caminho, _ = self.imagens[self.indice_atual]

        self.label_nome.configure(text=nome)
        self.label_contador.configure(text=f"Registo {self.indice_atual + 1} de {len(self.imagens)}")

        try:
            img_original = Image.open(caminho)
            img_original.thumbnail((600, 450)) 
            img_tk = ImageTk.PhotoImage(img_original)
            
            # Mantém a referência da imagem na memória
            self.label_imagem.config(image=img_tk, text="")
            self.label_imagem.image = img_tk 
        except Exception:
            self.label_imagem.config(image="", text="⚠️ Erro ao abrir arquivo.")

    # Permite selecionar uma imagem do sistema e salva no banco de dados
    def adicionar_imagem(self):
        arquivo = filedialog.askopenfilename(
            title="Selecionar Ficheiro de Imagem",
            filetypes=[("Imagens", "*.jpg *.jpeg *.png *.webp")]
        )

        if not arquivo:
            return

        nome = os.path.basename(arquivo)
        salvar_imagem(nome, arquivo, descricao="Adicionado via painel")

        self.limpar_pesquisa()
        self.indice_atual = len(self.imagens) - 1
        self.atualizar_visualizacao()

    # Remove a imagem atual após confirmação do usuário
    def remover_imagem(self):
        if not self.imagens:
            return
            
        id_imagem, nome, _, _ = self.imagens[self.indice_atual]
        
        confirmacao = messagebox.askyesno(
            "Confirmar Exclusão", 
            f"Deseja excluir permanentemente '{nome}'?"
        )
        
        if confirmacao:
            deletar_imagem(id_imagem)
            self.limpar_pesquisa()
            
            if self.indice_atual >= len(self.imagens):
                self.indice_atual = max(0, len(self.imagens) - 1)
            self.atualizar_visualizacao()

    # Avança para a próxima imagem na lista
    def proxima_imagem(self):
        if self.imagens and self.indice_atual < len(self.imagens) - 1:
            self.indice_atual += 1
            self.atualizar_visualizacao()

    # Retrocede para a imagem anterior na lista
    def imagem_anterior(self):
        if self.imagens and self.indice_atual > 0:
            self.indice_atual -= 1
            self.atualizar_visualizacao()

# Ponto de entrada da aplicação
if __name__ == "__main__":
    root = ctk.CTk()
    app = GerenciadorImagensApp(root)
    root.mainloop()