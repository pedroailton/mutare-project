import customtkinter
from tkinter import *
from tkinter import font
from PIL import Image, ImageTk

class Interface():
    def __init__(self):

        self.janela = customtkinter.CTk()
        self.janela._set_appearance_mode('Dark')
        self.janela.title('Mutare')
        self.janela.geometry('950x700') # A mesma dimensão determinada no design do Figma
        self.janela.resizable(width = False, height = False)

        self.botao_janela_cadastro = customtkinter.CTkButton(
            master = self.janela, 
            text = 'Cadastro', 
            command = self.janelaCadastro
            )
        self.botao_janela_cadastro.place(x = 400, y = 300)
        
        self.botao_janela_login = customtkinter.CTkButton(
            master = self.janela, 
            text = 'Login', 
            command = self.janelaLogin)
        self.botao_janela_login.place(x = 400, y = 350)

        # Quadrado verde da tela inicial (conferir Figma)
        frame1 = customtkinter.CTkFrame(
            master=self.janela,
            width=897,
            height=668,
            fg_color='#D1FF00',
            corner_radius=34,
            bg_color='#242424'
        )
        frame1.place(x=26, y=0)

        # Logo
        self.carregarImagemTransparente(
            caminho_imagem='./imagens/logob.png',
            posicao_x=309,
            posicao_y=22,
            tamanho=(332, 332),
            cor_fundo='#D1FF00'
        )

        # Titulo
        self.carregarImagemTransparente(
            caminho_imagem='./imagens/titulo.png',
            posicao_x=385,  
            posicao_y=354,  
            tamanho=(180, 35),  
            cor_fundo='#D1FF00'
        )

        # Subtitulo
        self.carregarImagemTransparente(
            caminho_imagem='./imagens/subtitulo.png',
            posicao_x=420,
            posicao_y=418,
            tamanho=(114, 20),
            cor_fundo='#D1FF00'
        )

        # Copyright
        customtkinter.CTkLabel(
            self.janela, 
            text='© 2025 MUTARE. Todos os direitos reservados.',
            bg_color='#242424',
            text_color='#FFFFFF',
            font=customtkinter.CTkFont(size=15)
            ).place(x=597, y=674)

        self.janela.mainloop()
    
    def carregarImagemTransparente(self, caminho_imagem, posicao_x, posicao_y, tamanho, cor_fundo):
        """Método para carregar imagens PNG com transparência"""
        try:
            # Carregar e processar a imagem
            imagem_original = Image.open(caminho_imagem).convert('RGBA')
            
            # Redimensionar se necessário
            if imagem_original.size != tamanho:
                imagem_redimensionada = imagem_original.resize(tamanho, Image.LANCZOS)
            else:
                imagem_redimensionada = imagem_original
            
            # Converter para formato Tkinter
            imagem_tk = ImageTk.PhotoImage(imagem_redimensionada)
            
            # Criar Canvas para exibição com transparência
            canvas = Canvas(
                self.janela,
                width=tamanho[0],
                height=tamanho[1],
                bg=cor_fundo,
                highlightthickness=0,
                bd=0
            )
            canvas.place(x=posicao_x, y=posicao_y)
            canvas.create_image(0, 0, image=imagem_tk, anchor='nw')
            
            # Manter referência para evitar problemas de garbage collection
            nome_referencia = f"imagem_tk_{posicao_x}_{posicao_y}"
            setattr(self, nome_referencia, imagem_tk)
            
        except FileNotFoundError:
            print(f"Erro: Arquivo de imagem não encontrado - {caminho_imagem}")
            # Exibir aviso se a imagem não for encontrada
            label_aviso = customtkinter.CTkLabel(
                self.janela,
                text=f"Imagem faltando: {caminho_imagem}",
                text_color='red'
            )
            label_aviso.place(x=posicao_x, y=posicao_y)

    # Nova janela
    def janelaCadastro(self):
        self.tela_1 = customtkinter.CTkToplevel(self.janela, fg_color= '#181818')
        self.tela_1.title('Cadastro Mutare')
        self.tela_1.geometry('950x700')

    def janelaLogin(self):
        self.tela_2 = customtkinter.CTkToplevel(self.janela, fg_color= '#181818')
        self.tela_2.title('Login Mutare')
        self.tela_2.geometry('950x700')
    
        
interface = Interface()