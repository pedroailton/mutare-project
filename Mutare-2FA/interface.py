import auth
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

        # Janela inicial 
        self.frame_inicial = customtkinter.CTkFrame(
            master=self.janela,
            width=897,
            height=668,
            fg_color='#D1FF00',
            corner_radius=34,
            bg_color='#242424'
        )
        self.frame_inicial.place(x=26, y=0)

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
            font=('Roboto', 15)
            ).place(x=597, y=675)

            # Botão login
        self.botao_janela_login = customtkinter.CTkButton(
            master = self.janela, 
            text = 'Login',
            fg_color='#181818',
            text_color='#FFFFFF',
            corner_radius=25,
            width=237,
            height=45,
            bg_color='#D1FF00',
            font=('Arial', 20, 'bold'),
            command = self.mostrarJanelaLogin
            )
        self.botao_janela_login.place(x = 356, y = 487)

            # Botão cadastro
        self.botao_janela_cadastro = customtkinter.CTkButton(
            master = self.janela, 
            text = 'Cadastro', 
            fg_color='#181818',
            text_color='#FFFFFF',
            corner_radius=25,
            width=237,
            height=45,
            bg_color='#D1FF00',
            font=('Arial', 20, 'bold'),
            command = self.mostrarJanelaCadastro)
        self.botao_janela_cadastro.place(x = 357, y = 553)

        self.janela.mainloop()
    
    def carregarImagemTransparente(self, caminho_imagem, posicao_x, posicao_y, tamanho, cor_fundo, master=None):
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
                master,
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

    def voltarParaInicial(self):
        self.frame_login.place_forget()
        self.frame_cadastro.place_forget()
        self.frame_inicial.place(x=26, y=0)

    def mostrarJanelaLogin(self):
        self.frame_inicial.place_forget()
        if hasattr(self, 'frame_cadastro'):
            self.frame_cadastro.place_forget()
        self.frame_login = customtkinter.CTkFrame(
            master=self.janela,
            width=950,
            height=700,
            fg_color='#242424',   
            bg_color='#242424'    
        ).place(x=0, y=0)
        
        # Lateral
        self.carregarImagemTransparente(
            caminho_imagem='./imagens/lateral.png',
            posicao_x=0,
            posicao_y=0,
            tamanho=(437, 700),
            cor_fundo='#242424'
        )

        # Textos
        self.carregarImagemTransparente(
            caminho_imagem='./imagens/logintexto.png',
            posicao_x=632,
            posicao_y=101,
            tamanho=(130, 50),
            cor_fundo='#242424'
        )

        self.carregarImagemTransparente(
            caminho_imagem='./imagens/logintexto2.png',
            posicao_x=580,
            posicao_y=160,
            tamanho=(248, 19),
            cor_fundo='#242424'
        )

        self.carregarImagemTransparente(
            caminho_imagem='./imagens/logintexto3.png',
            posicao_x=527,
            posicao_y=232,
            tamanho=(171, 18),
            cor_fundo='#242424'
        )

        entrada_email = customtkinter.CTkEntry(
            master=self.janela,
            placeholder_text="exemplo@ufrpe.br",
            width=355,
            height=36,
            corner_radius=57,
            font=("Arial", 16),
            text_color="#1E1E1E",
            placeholder_text_color="#707070",  # cinza claro
            fg_color="#FFFFFF",  # fundo escuro da caixa
            border_width=2,
            bg_color='#242424'
        )
        entrada_email.place(x=515, y=265)

        self.carregarImagemTransparente(
            caminho_imagem='./imagens/logintexto4.png',
            posicao_x=527,
            posicao_y=326,
            tamanho=(68, 17),
            cor_fundo='#242424'
        )           

        entrada_senha = customtkinter.CTkEntry(
            master=self.janela,
            placeholder_text="Exemplo123",
            width=355,
            height=36,
            corner_radius=57,
            font=("Arial", 16),
            text_color="#1E1E1E",
            placeholder_text_color="#707070",  # cinza claro
            fg_color="#FFFFFF",  # fundo escuro da caixa
            border_width=2,
            bg_color='#242424'
        )
        entrada_senha.place(x=515, y=358)

        self.botao_entrar = customtkinter.CTkButton(
            master=self.janela,  
            text="Entrar",
            fg_color="#D1FF00",
            bg_color='#242424',            # cor de fundo do botão
            text_color="#181818",          # cor do texto
            font=("Arial", 20, "bold"),
            width=107,
            height=45,
            corner_radius=57,
            command=self.autenticacao 
        )
        self.botao_entrar.place(x=640, y=430)  

        self.botao_voltar_login = customtkinter.CTkButton(
            master=self.frame_login,
            text="Voltar",
            fg_color="#D1FF00",
            bg_color="#242424",
            text_color="#181818",
            font=("Arial", 16, "bold"),
            corner_radius=20,
            width=100,
            height=35,
           # command=
        )
        self.botao_voltar_login.place(x=30, y=30)  


    def autenticacao(self):
        self.frame_2fa = customtkinter.CTkToplevel(self.janela)
        self.frame_2fa.title('Autenticação em Dois Fatores')
        self.frame_2fa.geometry("500x300")
        self.frame_2fa.configure(fg_color='#242424')
        self.frame_2fa.lift()
        self.frame_2fa.focus_force()
        self.frame_2fa.grab_set()
        self.frame_2fa.resizable(width = False, height = False)

        self.carregarImagemTransparente(
        caminho_imagem="./imagens/2fatexto1.png",  
        posicao_x=77,
        posicao_y=40,
        tamanho=(350, 25),
        cor_fundo="#242424",
        master=self.frame_2fa
    )
        self.carregarImagemTransparente(
        caminho_imagem="./imagens/2fatexto2.png",  
        posicao_x=80,
        posicao_y=100,
        tamanho=(340, 20),
        cor_fundo="#242424",
        master=self.frame_2fa
    )
        entrada_codigo = customtkinter.CTkEntry(
            master=self.frame_2fa,
            placeholder_text="123456",
            width=300,
            height=36,
            corner_radius=57,
            font=("Arial", 16),
            text_color="#1E1E1E",
            placeholder_text_color="#707070",  # cinza claro
            fg_color="#FFFFFF",  # fundo escuro da caixa
            border_width=2,
            bg_color='#242424'
        )
        entrada_codigo.place(x=100,y=150)

        self.botao_confirmar = customtkinter.CTkButton(
            master=self.frame_2fa,  
            text="Confirmar",
            fg_color="#D1FF00",
            bg_color='#242424',            # cor de fundo do botão
            text_color="#181818",          # cor do texto
            font=("Arial", 20, "bold"),
            width=107,
            height=45,
            corner_radius=57,
            #command= 
        )
        self.botao_confirmar.place(x=180, y=210)  
        
    def mostrarJanelaCadastro(self):
        self.frame_inicial.place_forget()
        if hasattr(self, 'frame_cadastro'):
            self.frame_cadastro.place_forget()
        self.frame_cadastro = customtkinter.CTkFrame(
            master=self.janela,
            width=950,
            height=700,
            fg_color='#242424',   
            bg_color='#242424'    
        ).place(x=0, y=0)

        # Lateral
        self.carregarImagemTransparente(
            caminho_imagem='./imagens/lateral.png',
            posicao_x=0,
            posicao_y=0,
            tamanho=(437, 700),
            cor_fundo='#242424'
        )

        self.carregarImagemTransparente(
            caminho_imagem='./imagens/cadastrotexto1.png',
            posicao_x=605,
            posicao_y=101,
            tamanho=(190, 39),
            cor_fundo='#242424'
        )

        self.carregarImagemTransparente(
            caminho_imagem='./imagens/cadastrotexto2.png',
            posicao_x=593,
            posicao_y=160,
            tamanho=(209, 19),
            cor_fundo='#242424'
        )

        self.carregarImagemTransparente(
            caminho_imagem='./imagens/logintexto3.png',
            posicao_x=527,
            posicao_y=232,
            tamanho=(171, 18),
            cor_fundo='#242424'
        )     

        entrada_email = customtkinter.CTkEntry(
            master=self.janela,
            placeholder_text="exemplo@ufrpe.br",
            width=355,
            height=36,
            corner_radius=57,
            font=("Arial", 16),
            text_color="#1E1E1E",
            placeholder_text_color="#707070",  # cinza claro
            fg_color="#FFFFFF",  # fundo escuro da caixa
            border_width=2,
            bg_color='#242424'
        )
        entrada_email.place(x=515, y=265)   

        self.carregarImagemTransparente(
            caminho_imagem='./imagens/logintexto4.png',
            posicao_x=527,
            posicao_y=326,
            tamanho=(68, 17),
            cor_fundo='#242424'
        )           
        
        entrada_senha = customtkinter.CTkEntry(
            master=self.janela,
            placeholder_text="Exemplo123",
            width=355,
            height=36,
            corner_radius=57,
            font=("Arial", 16),
            text_color="#1E1E1E",
            placeholder_text_color="#707070",  # cinza claro
            fg_color="#FFFFFF",  # fundo escuro da caixa
            border_width=2,
            bg_color='#242424'
        )
        entrada_senha.place(x=515, y=358)

        self.carregarImagemTransparente(
            caminho_imagem='./imagens/css.png',
            posicao_x=527,
            posicao_y=420,
            tamanho=(203, 18),
            cor_fundo='#242424'
        )     

        entrada_senha = customtkinter.CTkEntry(
            master=self.janela,
            placeholder_text="Exemplo123",
            width=355,
            height=36,
            corner_radius=57,
            font=("Arial", 16),
            text_color="#1E1E1E",
            placeholder_text_color="#707070",  # cinza claro
            fg_color="#FFFFFF",  # fundo escuro da caixa
            border_width=2,
            bg_color='#242424'
        )
        entrada_senha.place(x=515, y=451)  

        self.carregarImagemTransparente(
            caminho_imagem='./imagens/reqsen.png',
            posicao_x=522,
            posicao_y=527,
            tamanho=(350, 120),
            cor_fundo='#242424'
        )     
    
        self.botao_seguir = customtkinter.CTkButton(
            master=self.janela,  
            text="➜",
            fg_color="#D1FF00",
            bg_color='#242424',           
            text_color="#181818",          
            font=("Arial", 22, "bold"),
            width=30,
            height=28,
            corner_radius=57,
            command=self.mostrarJanelaLogin
        )
        self.botao_seguir.place(x=877, y=454)



interface = Interface()