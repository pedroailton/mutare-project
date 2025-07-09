import time
import bcrypt
from colorama import Fore
from utils import Utils
from database import Database

class Auth:
    def __init__(self, db: Database):
        self.db = db

    def cadastrar_usuario(self):
        while True:
            Utils.limpar_tela()
            print(Fore.WHITE + '\n=== CADASTRO DE USUÁRIO ===')
            email = input(Fore.YELLOW + 'Digite seu e-mail: ').strip()
            if not Utils.email_valido(email):
                print(Fore.RED + 'E-mail inválido. Use @gmail.com ou @ufrpe.br')
                time.sleep(2)
                continue

            senha = Utils.input_senha_asteriscos('Digite a senha: ').strip()
            confirmacao = Utils.input_senha_asteriscos('Confirme a senha: ').strip()

            validacao = Utils.validar_senha(senha)
            if validacao != "válida":
                print(Fore.RED + validacao)
                time.sleep(2)
                continue

            if senha != confirmacao:
                print(Fore.RED + 'As senhas não coincidem.')
                time.sleep(2)
                continue

            try:
                senha_hash = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                self.db.execute('INSERT INTO usuarios (Email, senha) VALUES (?, ?)', (email, senha_hash))
                print(Fore.GREEN + 'Usuário cadastrado com sucesso!')
                time.sleep(2)
                return
            except Exception as e:
                print(Fore.RED + f'Erro: {e}')
                time.sleep(2)

    def login_usuario(self):
        tentativas = 0
        while tentativas < 3:
            Utils.limpar_tela()
            print(Fore.WHITE + '\n=== LOGIN ===')
            email = input(Fore.YELLOW + 'Digite seu e-mail: ').strip()
            senha = Utils.input_senha_asteriscos('Digite a senha: ').strip()

            resultado = self.db.execute('SELECT senha FROM usuarios WHERE Email = ?', (email,)).fetchone()

            if resultado:
                senha_hash = resultado[0]
                if isinstance(senha_hash, str):
                    senha_hash = senha_hash.encode('utf-8')
                if bcrypt.checkpw(senha.encode('utf-8'), senha_hash):
                    print(Fore.GREEN + f'Bem-vindo(a), {email}!')
                    time.sleep(2)
                    return email

            print(Fore.RED + 'E-mail ou senha incorretos.')
            tentativas += 1
            time.sleep(2)
        return None

    def atualizar_senha(self):
        email = input(Fore.YELLOW + "Digite seu email: ").strip()
        senha_antiga = Utils.input_senha("Digite sua senha atual: ").strip()
        
        if not self.db.verificar_credenciais(email, senha_antiga):
            print(Fore.RED + "Email ou senha incorretos.")
            return
    
        nova_senha = Utils.input_senha("Digite a nova senha: ").strip()
        if not nova_senha:
            print(Fore.RED + "Nova senha inválida.")
            return
    
        self.db.cursor.execute("UPDATE usuarios SET senha = ? WHERE Email = ?", (nova_senha, email))
        self.db.conn.commit()
        print(Fore.GREEN + "Senha atualizada com sucesso.")

    def excluir_conta(self):
        email = input(Fore.YELLOW + "Digite seu e-mail: ").strip()
        senha = Utils.input_senha("Digite sua senha: ").strip()
    
        if not self.db.verificar_credenciais(email, senha):
            print(Fore.RED + "Credenciais inválidas.")
            return
    
        confirmacao = input(Fore.RED + "Tem certeza que deseja excluir sua conta? (s/n): ").lower()
        if confirmacao == 's':
            self.db.cursor.execute("DELETE FROM usuarios WHERE Email = ?", (email,))
            self.db.conn.commit()
            print(Fore.GREEN + "Conta excluída com sucesso.")
        else:
            print("Operação cancelada.")
