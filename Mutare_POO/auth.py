import time
import bcrypt
from colorama import Fore
from util import Util
from database import Database
import sqlite3 

class Auth:
    def __init__(self, db: Database):
        self.db = db

    def cadastrarUsuario(self):
        while True:
            Util.limparTela()
            print(Fore.WHITE + '\n=== CADASTRO DE USUÁRIO ===')
            email = input(Fore.YELLOW + 'Digite seu e-mail: ').strip()

            if not Util.emailValido(email):
                print(Fore.RED + 'E-mail inválido. Use @gmail.com ou @ufrpe.br')
                time.sleep(2)
                continue

            # Verifica se o e-mail já está cadastrado
            resultado = self.db.execute('SELECT 1 FROM usuarios WHERE Email = ?', (email,))
            if resultado.fetchone():
                print(Fore.RED + 'Este e-mail já está cadastrado. Tente outro.')
                time.sleep(2)
                continue

            senha = Util.inputSenhaAsteriscos('Digite a senha: ').strip()
            confirmacao = Util.inputSenhaAsteriscos('Confirme a senha: ').strip()

            validacao = Util.validarSenha(senha)
            if validacao != "válida":
                print(Fore.RED + validacao)
                time.sleep(2)
                continue

            if senha != confirmacao:
                print(Fore.RED + 'As senhas não coincidem.')
                time.sleep(2)
                continue

            try:
                hash_senha = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                self.db.execute('INSERT INTO usuarios (Email, senha) VALUES (?, ?)', (email, hash_senha))
                self.db.conn.commit()
                print(Fore.GREEN + 'Usuário cadastrado com sucesso!')
                time.sleep(2)
                return
            except sqlite3.IntegrityError as e:
                if 'UNIQUE constraint' in str(e):
                    print(Fore.RED + 'Erro: este e-mail já está em uso.')
                else:
                    print(Fore.RED + 'Erro ao cadastrar. Tente novamente.')
                time.sleep(2)
            except Exception as e:
                print(Fore.RED + 'Erro inesperado ao cadastrar usuário.')
                print(Fore.RED + str(e))  # opcional: útil para debug
                time.sleep(2)

    def loginUsuario(self):
        tentativas = 0
        while tentativas < 3:
            Util.limparTela()
            print(Fore.WHITE + '\n=== LOGIN ===')
            email = input(Fore.YELLOW + 'Digite seu e-mail: ').strip()
            senha = Util.inputSenhaAsteriscos('Digite a senha: ').strip()

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

    