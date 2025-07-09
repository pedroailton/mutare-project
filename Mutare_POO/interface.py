import customtkinter

class Interface():
    def __init__(self):

        self.janela = customtkinter.CTk()

        self.janela._set_appearance_mode('System')
        self.janela.title('Mutare')
        self.janela.geometry('950x700') # A mesma dimensão determinada no design do Figma
        self.janela.resizable(width = False, height = False)

        self.botao_tela_1 = customtkinter.CTkButton(master = self.janela, text = 'Cadastro', command = self.tela_cadastro).place(x = 400, y = 300)

        self.janela.mainloop()

    
    # Tela Inicial (para Iniciar)
    def tela_cadastro(self):
        self.tela_1 = customtkinter.CTkToplevel(self.janela, fg_color= '#181818')
        self.tela_1.title('Cadastro Mutare')
        self.tela_1.geometry('950x700')
        
interface = Interface()
interface.tela_inicial()