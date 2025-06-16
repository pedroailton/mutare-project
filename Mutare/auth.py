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
