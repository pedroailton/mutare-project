import time
import bcrypt
from colorama import Fore
from util import Util
from database import Database
import sqlite3 
import smtplib
import random
import os
from datetime import datetime, timedelta 
from email.mime.text import MIMEText
from dotenv import load_dotenv

class Auth:
    def __init__(self, db: Database):
        self.db = db
        self._carregar_env()
        self.codigo = None
        self.hora_codigo = None

    def _carregar_env(self):
        load_dotenv(dotenv_path='2FA.env')
        self.email_remetente = os.getenv("EMAIL_REMETENTE")
        self.email_senha = os.getenv("EMAIL_SENHA")

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

            senha = Util.inputSenhaAsteriscos('Digite a senha (De 4-8 caracteres, pelo menos 1 número e 1 letra maiúscula): ').strip()
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
                from main import menuPrincipal  
                menuPrincipal(email, self.db) 
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
                    codigo = self.gerarCodigo()
                    if self.enviarCodigoAutenticacao(email, codigo):
                        for i in range(3):
                            digitado = input(Fore.CYAN + 'Digite o código de verificação enviado para seu e-mail: ').strip()
                            if self.codigoExpirado():
                                print(Fore.RED + '⏰ Código expirado.')
                                resposta = input(Fore.YELLOW + 'Deseja reenviar um novo código? (s/n): ').strip().lower()
                                if resposta == 's':
                                    self.gerarCodigo()
                                    if self.enviarCodigoAutenticacao(email, self.codigo):
                                        print(Fore.GREEN + '📧 Novo código enviado com sucesso.\n')
                                        time.sleep(1)
                                        continue  
                                    else:
                                        print(Fore.RED + '❌ Erro ao reenviar o código. Encerrando login.')
                                        time.sleep(2)
                                        return None
                                else:
                                    print(Fore.RED + '❌ Verificação cancelada.')
                                    time.sleep(2)
                                    return None
                            elif digitado == self.codigo:
                                print(Fore.GREEN + f'\n✅ Verificação concluída. Bem-vindo(a), {email}!')
                                time.sleep(2)
                                return email
                            else:
                                print(Fore.RED + '❌ Código incorreto.')
                                time.sleep(2)
                        print(Fore.RED + '\n❌ Muitas tentativas. Login bloqueado.')
                        time.sleep(2)
                        return None
                    else:
                        print(Fore.RED + '\n❌ Erro ao enviar o código de verificação.')
                        time.sleep(2)
                        return None
            print(Fore.RED + 'E-mail ou senha incorretos.')
            tentativas += 1
            resposta = input(Fore.YELLOW + 'Esqueceu sua senha? Deseja recuperar agora? (s/n): ').strip().lower()
            if resposta == 's':
                self.recuperarSenha()
                return None  
            time.sleep(2)
        return None

    # Autentiacação em Duas Etapas
    def gerarCodigo(self):
        self.codigo = str(random.randint(100000, 999999))
        self.hora_codigo = datetime.now()
        return self.codigo

    def codigoExpirado(self):
        if not self.hora_codigo:
            return True
        return datetime.now() > self.hora_codigo + timedelta(minutes=5)

    
    def enviarCodigoAutenticacao(self, destinatario, codigo):
        corpo = f'Seja bem vindo(a) à sua jornada Mutare! Seu código de verificação é: {codigo}'
        msg = MIMEText(corpo)
        msg['Subject'] = 'Código de Autenticação em Dois Fatores - Mutare'
        msg['From'] = self.email_remetente
        msg['To'] = destinatario

        try:
            with smtplib.SMTP('smtp.gmail.com', 587) as servidor:
                servidor.set_debuglevel(1)
                servidor.ehlo()
                servidor.starttls()
                servidor.login(self.email_remetente, self.email_senha)
                servidor.send_message(msg)
            print('✅ Código enviado com sucesso.')
            return True
        except Exception as erro:
            print(f"❌ Erro ao enviar e-mail: {erro}") 
            time.sleep(2)
            return False
        
    def recuperarSenha(self):
        Util.limparTela()
        print(Fore.WHITE + '\n=== RECUPERAÇÃO DE SENHA ===')
        email = input(Fore.YELLOW + 'Digite seu e-mail: ').strip()

        # Verifica se o e-mail está cadastrado
        resultado = self.db.execute('SELECT 1 FROM usuarios WHERE Email = ?', (email,)).fetchone()
        if not resultado:
            print(Fore.RED + 'E-mail não encontrado.')
            time.sleep(2)
            return

        # Gera e envia código
        codigo = self.gerarCodigo()
        if not self.enviarCodigoAutenticacao(email, codigo):
            print(Fore.RED + '❌ Falha ao enviar código. Tente novamente.')
            time.sleep(2)
            return

        print(Fore.GREEN + '📧 Código enviado. Verifique seu e-mail.')

        # Verificação do código
        for _ in range(3):
            digitado = input(Fore.YELLOW + 'Digite o código recebido: ').strip()
            if self.codigoExpirado():
                print(Fore.RED + '⏰ Código expirado. Tente novamente.')
                return
            if digitado == self.codigo:
                break
            else:
                print(Fore.RED + 'Código incorreto.')
        else:
            print(Fore.RED + '❌ Limite de tentativas atingido.')
            return

        # Redefinir senha
        nova = Util.inputSenhaAsteriscos('Nova senha(De 4-8 caracteres, pelo menos 1 número e 1 letra maiúscula): ').strip()
        confirmar = Util.inputSenhaAsteriscos('Confirme a nova senha: ').strip()

        if nova != confirmar:
            print(Fore.RED + 'As senhas não coincidem.')
            return

        validacao = Util.validarSenha(nova)
        if validacao != "válida":
            print(Fore.RED + validacao)
            return

        nova_hash = bcrypt.hashpw(nova.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        self.db.execute('UPDATE usuarios SET senha = ? WHERE Email = ?', (nova_hash, email))
        self.db.conn.commit()

        print(Fore.GREEN + '✅ Senha atualizada com sucesso!')
        time.sleep(2)
