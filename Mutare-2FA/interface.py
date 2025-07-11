import customtkinter

class Interface():
    def __init__(self):

        self.janela = customtkinter.CTk()

        self.janela._set_appearance_mode('Dark')
        self.janela.title('Mutare')
        self.janela.geometry('950x700') # A mesma dimensão determinada no design do Figma
        self.janela.resizable(width = False, height = False)

        self.botao_janela_cadastro = customtkinter.CTkButton(master = self.janela, text = 'Cadastro', command = self.janela_cadastro).place(x = 400, y = 300)
        self.botao_janela_login = customtkinter.CTkButton(master = self.janela, text = 'Login', command = self.janela_login).place(x = 400, y = 350)

        # Quadrado verde da tela inicial (conferir Figma)
        frame1 = customtkinter.CTkFrame(master = self.janela, width = 902.5, height = 665).place(x = 30, y = 25)

        self.janela.mainloop()

    
    # Nova janela
    def janela_cadastro(self):
        self.tela_1 = customtkinter.CTkToplevel(self.janela, fg_color= '#181818')
        self.tela_1.title('Cadastro Mutare')
        self.tela_1.geometry('950x700')

    def janela_login(self):
        self.tela_2 = customtkinter.CTkToplevel(self.janela, fg_color= '#181818')
        self.tela_1.title('Login Mutare')
        self.tela_1.geometry('950x700')
    
        
interface = Interface()