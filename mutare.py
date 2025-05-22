from colorama import init, Fore 
import sys
import os
import time
import bcrypt
from datetime import datetime
import re
import sqlite3 

init(autoreset=True)

# Conexão com o SQLite
conn = sqlite3.connect('Mutare.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Email TEXT UNIQUE NOT NULL,
        senha TEXT NOT NULL
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS habits (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        created_at DATE NOT NULL,
        frequency TEXT,
        motivation TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS habit_progress (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        habit_id INTEGER NOT NULL,
        date DATE NOT NULL,
        status TEXT NOT NULL,
        FOREIGN KEY (habit_id) REFERENCES habits(id) ON DELETE CASCADE
    )
''')

conn.commit()

# Verifica domínio do e-mail
def email_valido(email):
    '''Define os domínios de E-mail válidos para o cadastro no Mutare.
    '''
    return email.endswith('@gmail.com') or email.endswith('@ufrpe.br')

# Validação da senha
def validar_senha(senha):
    '''Valida uma senha de acordo com critérios de comprimento e presença de número.
    A senha deve ter entre 4 e 8 caracteres e conter pelo menos um número.
    Args:
        senha (str): A senha a ser validada.
    Returns:
        str: Uma mensagem indicando se a senha é válida ou qual critério não foi atendido.'''
    
    comprimento_minimo = 4
    comprimento_maximo = 8

    if len(senha) < comprimento_minimo:
        return f"A senha deve ter pelo menos {comprimento_minimo} caracteres."
    elif len(senha) > comprimento_maximo:
        return f"A senha não pode ter mais que {comprimento_maximo} caracteres."
    elif not any(char.isdigit() for char in senha):
        return "A senha deve conter pelo menos um número."
    else:
        return "válida"

#Função senha de asteriscos 
if os.name == 'nt':
    import msvcrt
else:
    import tty
    import termios
def input_senha_asteriscos(prompt='Senha: '):
    '''Lê a senha do usuário ocultando os caracteres com asteriscos (*).
    Funciona em sistemas Windows e Unix. Suporte para backspace e interrupção com Ctrl+C.
    Args:
        prompt (str): Texto exibido antes da digitação. Padrão é 'Senha: '.
    Returns:
        str: A senha digitada pelo usuário.'''
    
    print(prompt, end='', flush=True)
    senha = ''
    
    if os.name == 'nt':
        while True:
            char = msvcrt.getch()
            if char in(b'\r', b'\n'):
                print()
                break
            elif char == b'\x08':
                if len(senha)>0:
                    senha = senha[:-1]
                    print('\b \b', end='', flush=True)
            elif char == b'\x03':
                raise KeyboardInterrupt
            else:
                try:
                    char_dec = char.decode('utf-8')
                    senha += char_dec
                    print(Fore.YELLOW + '*', end='', flush=True)
                except UnicodeDecodeError:
                    pass
    else:
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            while True:
                char = sys.stdin.read(1)
                if char in ('\r', '\n'):
                    print()
                    break
                elif char == '\x7f':
                    if len(senha)>0:
                        senha = senha[:-1]
                        print('\b \b', end='', flush=True)
                elif char == '\x03':
                    raise KeyboardInterrupt
                else:
                    senha += char
                    print(Fore.YELLOW + '*', end='', flush=True)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return senha

#Limpar tela
def limpar_tela():
    '''Limpa o terminal, independente do sistema operacional.
    Usa 'cls' no Windows e 'clear' no Linux/MacOS.'''
    os.system('cls' if os.name == 'nt' else 'clear')

#Tela de Menu de login ou cadastro
def menu_log_cad():
    '''Exibe um menu do sistema Mutare com opções de login e cadastro.
    Direciona o usuário para a tela de login ou cadastro conforme a escolha.
    Em caso de entrada inválida, exibe uma mensagem de erro e recarrega o menu.'''

    limpar_tela()
    print(Fore.WHITE + '\n=== Bem-vindo ao Mutare! ===')
    print(Fore.WHITE + 'Escolha uma opção')
    print(Fore.CYAN + '[1] Login')
    print(Fore.CYAN + '[2] Cadastro')

    escolha = input(Fore.YELLOW + 'Digite o número da opção: ')

    if escolha == '1':
        tela_login()
    elif escolha == '2':
        tela_cadastro()
    else:
        print(Fore.RED + 'Insira uma opção válida.')
        time.sleep(2) #Retém a mensagem por 2 segundos, a fim de que o leitor consiga lê-la.
        limpar_tela()
        menu_log_cad()

#Tela de cadastro
def tela_cadastro():
    '''Solicita e valida e-mail e senha, cadastra novo usuário no banco e redireciona para login.'''
    while True:
        limpar_tela()
        print(Fore.WHITE + '\n' + '='*40)
        print(' '*16 + 'CADASTRO')
        print('='*40)

        #Validação do e-mail
        Email = input(Fore.YELLOW + 'Seu E-mail: ').strip()
        if ' ' in Email or not email_valido(Email.lower()):
            print(Fore.RED + 'E-mail inválido. Use apenas domínios @gmail.com ou @ufrpe.br e não utilize espaços.')
            time.sleep(4)
            continue

        #Validação da senha
        while True:
            nova_senha = input_senha_asteriscos(Fore.YELLOW + 'Nova senha: ') 
            resultado = validar_senha(nova_senha)
            if resultado != "válida":
                print(Fore.RED + resultado)
                time.sleep(2)
                continue

            confirmar_senha = input_senha_asteriscos(Fore.YELLOW + 'Confirme a senha: ')
            if nova_senha != confirmar_senha:
                print(Fore.RED + 'As senhas não coincidem. Tente novamente.')
                time.sleep(2)
                continue

            break 

        try:
            hash_senha = bcrypt.hashpw(nova_senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            cursor.execute('INSERT INTO usuarios (Email, senha) VALUES (?, ?)', (Email, hash_senha))
            conn.commit()
            print(Fore.GREEN + f'\n{Email} cadastrado com sucesso!')
            time.sleep(2)
            tela_login()
            return
        except sqlite3.IntegrityError:
            print(Fore.RED + 'Usuário já cadastrado. Tente novamente com outro e-mail.')
            time.sleep(4)

#Tela de login
def tela_login():
    '''Solicita e-mail e senha, verifica credenciais no banco de dados e exibe mensagem de sucesso ou erro.'''

    limpar_tela()
    print(Fore.WHITE + '='*40)
    print(' '*17 + 'LOGIN')
    print('='*40)

    Email = input(Fore.YELLOW + 'Seu E-mail: ')
    senha = input_senha_asteriscos(Fore.YELLOW + 'Senha: ') 

    cursor.execute('SELECT senha FROM usuarios WHERE Email = ?', (Email,))
    resultado = cursor.fetchone()

    print(Fore.BLUE + '\nVerificando...\n')
    time.sleep(1)

    if resultado:
        senha_hash = resultado[0]
        if isinstance(senha_hash, str):
            senha_hash = senha_hash.encode('utf-8')
        
        if bcrypt.checkpw(senha.encode('utf-8'), senha_hash):
            print(Fore.GREEN + f'Bem vindo(a), {Email}!')
            time.sleep(2)
            menu_principal(Email)
            return
        else:
            print(Fore.RED + 'E-mail ou senha incorretos.')
    else:
        print(Fore.RED + 'E-mail ou senha incorretos.')

    time.sleep(2)
    tela_login()

#Menu principal
def menu_principal(Email):
    """
    Exibe o menu principal do programa Mutare e gerencia a navegação entre as opções.
    """
    while True:
        limpar_tela()
        print(Fore.WHITE + '=' * 40)
        print('      === BEM-VINDO AO MUTARE! ===')
        print('=' * 40)
        print(Fore.CYAN + '[1] Menu Hábitos')
        print(Fore.CYAN + '[2] Mascote')
        print(Fore.CYAN + '[3] Configurações')
        print(Fore.CYAN + '[4] Fechar Programa')
        escolha = input(Fore.YELLOW + 'Digite sua escolha: ').strip()

        if escolha == '1':
            menu_habitos()
        elif escolha == '2':
            mascote()
        elif escolha == '3':
            configuracoes(Email)
        elif escolha == '4':
            print(Fore.GREEN + "Encerrando programa...")
            time.sleep(1)
            break
        else:
            print(Fore.RED + 'Dígito inválido. Digite novamente.')
            time.sleep(2)
            limpar_tela()

#Menu de controle de hábitos
def menu_habitos():
    
    while True:
        limpar_tela()
        print(Fore.WHITE + '=' * 20)
        print('      HÁBITOS')
        print('=' * 20)
        print(Fore.CYAN + '[1] Inserir hábito')
        print(Fore.CYAN + '[2] Visualizar progresso')
        print(Fore.CYAN + '[3] Editar hábito')
        print(Fore.CYAN + '[4] Deletar hábito')
        print(Fore.CYAN + '[5] Voltar')
        escolha = input(Fore.YELLOW + 'Digite sua escolha: ').strip()

        if escolha == '1':
            inserir_habito()
        elif escolha == '2':
            progresso()
        elif escolha == '3':
            editar_habito()
        elif escolha == '4':
            deletar_habito()
        elif escolha == '5':
            menu_principal()
        else:
            print(Fore.RED + 'Digito inválido. Digite novamente.')
            time.sleep(2)
            limpar_tela()

#Configurações(RUD)
def buscar_conta(Email):
    cursor.execute('SELECT Email, senha FROM usuarios WHERE Email = ?', (Email,))
    return cursor.fetchone()

def configuracoes(Email):
    while True:
        limpar_tela()
        print(Fore.WHITE + '=' * 30) 
        print('        CONFIGURAÇÕES') 
        print('=' * 30)
        print(Fore.CYAN + '[1] Visualizar conta')
        print(Fore.CYAN + '[2] Sair da conta')
        print(Fore.CYAN + '[3] Voltar')
        escolha = input('Digite sua escolha: ').strip()

        if escolha == '1':
            visualizar_conta(Email)
        elif escolha == '2':
            print(Fore.BLUE + 'Saindo da conta...') 
            time.sleep(2)
            break
        elif escolha == '3':
            menu_principal()
        else:
            print('Digito inválido. Digite novamente.')   

def visualizar_conta(Email):
    limpar_tela()
    conta = buscar_conta(Email)
    if not conta:
        print(Fore.RED + 'Conta não encontrada.')
        return
    
    print('-'*20)
    print(f"INFORMAÇÕES DA CONTA\nEmail: {conta[0]}\nSenha: {'*' * 8}")
    print('-'*20)

    while True:
        print('\n[1] Atualizar senha')
        print(Fore.RED + '[2] Excluir conta')
        print('[3] Voltar')
        escolha = input('Digite sua escolha: ').strip()

        if escolha == '1':
            atualizar_senha(Email)
        elif escolha == '2':
            excluir_conta(Email)
        elif escolha == '3':
            break
        else:
            print('Digito inválido. Digite novamente.')

def atualizar_senha(Email):
    limpar_tela()
    conta = buscar_conta(Email)
    if not conta:
        print(Fore.RED + 'Conta não encontrada.')
        return

    senha_atual = input_senha_asteriscos('Confirme sua senha atual: ').strip().encode('utf-8') 

    senha_hash = conta[1].encode('utf-8') if isinstance(conta[1], str) else conta[1]

    if not bcrypt.checkpw(senha_atual, senha_hash):
        print(Fore.RED + 'Senha incorreta.')
        limpar_tela()
        return

    while True:
        nova_senha = input_senha_asteriscos("Digite sua nova senha (4-8 caracteres, ao menos uma letra e um número): ").strip()
        
        if validar_senha(nova_senha):
            nova_senha_hash = bcrypt.hashpw(nova_senha.encode('utf-8'), bcrypt.gensalt())
            
            cursor.execute('UPDATE usuarios SET senha = ? WHERE email = ?', (nova_senha_hash, Email))
            conn.commit()
            print(Fore.GREEN + "Senha atualizada com sucesso!")
            break
        else:
            print(Fore.RED + "Senha inválida. Tente novamente.")

def excluir_conta(Email):
    limpar_tela()
    conta = buscar_conta(Email)
    if not conta:
        print(Fore.RED + "Conta não encontrada.")
        return

    confirmacao = input("Tem certeza que quer excluir sua conta? (1 - Sim / 2 - Não): ")
    if confirmacao != "1":
        print(Fore.YELLOW + "Exclusão cancelada.")
        return

    senha = input_senha_asteriscos("Confirme sua senha: ").strip().encode('utf-8')
    
    senha_hash = conta[1] if isinstance(conta[1], bytes) else conta[1].encode('utf-8')
    
    if not bcrypt.checkpw(senha, senha_hash):
        print(Fore.RED + "Senha incorreta. Processo de exclusão interrompido.")
        time.sleep(1)
        limpar_tela()
        return

    confirmacao_final = input("Ao excluir sua conta, perderá acesso a todo o sistema. Deseja mesmo excluir? (1 - Sim / 2 - Não): ")
    if confirmacao_final != "1":
        print(Fore.YELLOW + "Exclusão cancelada.")
        time.sleep(1)
        limpar_tela()
        return

    try:
        cursor.execute('DELETE FROM usuarios WHERE email = ?', (Email,))
        conn.commit()
        print(Fore.GREEN + "Conta excluída com sucesso.")
    except Exception as e:
        print(Fore.RED + f"Erro ao excluir conta: {e}")
        conn.rollback()

#Hábitos
def inserir_habito():
    limpar_tela()
    nome = input("Nome do novo hábito (máx. 50 caracteres, sem caracteres especiais): ").strip()
    
    if not nome:
        print("O nome do hábito não pode ser vazio.\n")
        return

    if len(nome) > 50:
        print("O nome do hábito deve ter no máximo 50 caracteres.\n")
        return

    if not re.match(r'^[A-Za-z0-9 ]+$', nome):
        print("O nome do hábito deve conter apenas letras, números e espaços.\n")
        return

    frequencia = input("Frequência desejada (Ex.: Diário, Semanal, etc.): ").strip()
    
    if not frequencia:
        print("A frequência é obrigatória.\n")
        return

    motivacao = None
    resposta = input("Deseja adicionar uma motivação? (s/n): ").strip().lower()
    if resposta == 's':
        motivacao = input("Motivação (máx. 200 caracteres): ").strip()
        if len(motivacao) > 200:
            print("A motivação deve ter no máximo 200 caracteres.\n")
            return

    data = datetime.now().date()

    cursor.execute(
    "INSERT INTO habits (name, created_at, frequency, motivation) VALUES (?, ?, ?, ?)", 
    (nome, data, frequencia, motivacao)
    )
    conn.commit()

    print(f"Hábito '{nome}' adicionado com sucesso em {data}!\n")
    time.sleep(2)

#Execução    
if __name__ == '__main__':
    try:
        menu_log_cad()
    finally:
        cursor.close()
        conn.close()