from util import Util
from gamificacao import Gamificacao
from colorama import Fore
import bcrypt
import time

class Config:
    def __init__(self, db, main, auth):
        self.db = db
        self.main = main  
        self.auth = auth

    def buscarConta(self, email):
        '''Busca a conta atual no banco de dados.'''
        resultado = self.db.execute('SELECT Email, senha FROM usuarios WHERE Email = ?', (email,))
        return resultado.fetchone()

    def menuConfiguracoes(self, email, game):
        '''Exibe o menu de configurações.'''
        while True:
            Util.limparTela()
            print(Fore.WHITE + '=' * 30) 
            print('        CONFIGURAÇÕES') 
            print('=' * 30)
            print(Fore.CYAN + '[1] Visualizar conta')
            print(Fore.CYAN + '[2] Sair da conta')
            print(Fore.CYAN + '[3] Voltar')
            escolha = input('Digite sua escolha: ').strip()

            if escolha == '1':
                self.visualizarConta(email, game)
            elif escolha == '2':
                print(Fore.BLUE + 'Saindo da conta...') 
                time.sleep(2)
                self.main.menuInicial()
            elif escolha == '3':
                return
            else:
                print(Fore.RED + 'Dígito inválido. Digite novamente.')

    def visualizarConta(self, email, game):
        '''Exibe dados da conta e as opções de atualização/exclusão.'''
        Util.limparTela()
        conta = self.buscarConta(email)
        nivel = game.atualizarXP()
        
        if not conta:
            print(Fore.RED + 'Conta não encontrada.')
            return
        
        print('-'*20)
        print(f"INFORMAÇÕES DA CONTA\nEmail: {conta[0]}\nSenha: {'*' * 8}\nNível: {nivel}")
        print('-'*20)

        while True:
            print('\n[1] Atualizar senha')
            print(Fore.RED + '[2] Excluir conta')
            print('[3] Voltar')
            escolha = input('Digite sua escolha: ').strip()

            if escolha == '1':
                self.atualizarSenha(email)
            elif escolha == '2':
                self.excluirConta(email)
            elif escolha == '3':
                return
            else:
                print(Fore.RED + 'Dígito inválido. Digite novamente.')

    def atualizarSenha(self, email):
        '''Atualiza a senha do usuário.'''
        conta = self.buscarConta(email)
        if not conta:
            print(Fore.RED + 'Conta não encontrada.')
            return

        senha_atual = Util.inputSenhaAsteriscos('Confirme sua senha atual: ').strip().encode('utf-8')
        senha_hash = conta[1].encode('utf-8') if isinstance(conta[1], str) else conta[1]

        if not bcrypt.checkpw(senha_atual, senha_hash):
            print(Fore.RED + 'Senha incorreta.')
            time.sleep(2)
            return

        while True:
            nova_senha = Util.inputSenhaAsteriscos('Digite sua nova senha (4-8 caracteres, ao menos uma letra maiúscula e um número): ').strip()
            if Util.validarSenha(nova_senha) == "válida":
                nova_hash = bcrypt.hashpw(nova_senha.encode('utf-8'), bcrypt.gensalt())
                self.db.execute('UPDATE usuarios SET senha = ? WHERE Email = ?', (nova_hash, email))
                self.db.conn.commit()
                print(Fore.GREEN + 'Senha atualizada com sucesso!')
                time.sleep(2)
                return
            else:
                print(Fore.RED + 'Senha inválida. Tente novamente.')

    def excluirConta(self, email):
        '''Exclui a conta do usuário.'''
        conta = self.buscarConta(email)
        if not conta:
            print(Fore.RED + 'Conta não encontrada.')
            return

        senha = Util.inputSenhaAsteriscos('Confirme sua senha: ').strip().encode('utf-8')
        senha_hash = conta[1] if isinstance(conta[1], bytes) else conta[1].encode('utf-8')

        if not bcrypt.checkpw(senha, senha_hash):
            print(Fore.RED + 'Senha incorreta. Processo cancelado.')
            time.sleep(1)
            return

        confirmacao = input(Fore.YELLOW + 'Deseja mesmo excluir a conta? (s/n): ').lower()
        if confirmacao == 's':
            self.db.execute('DELETE FROM usuarios WHERE Email = ?', (email,))
            self.db.conn.commit()
            print(Fore.GREEN + 'Conta excluída com sucesso.')
            time.sleep(1)
            self.main.menuInicial(self.auth)
        else:
            print('Operação cancelada.')
