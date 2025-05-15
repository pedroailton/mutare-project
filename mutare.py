from colorama import init, Fore 
import sys
import os
import time
import sqlite3 

init(autoreset=True)

# Conexão com o SQLite
conn = sqlite3.connect('Mutare.db')
cursor = conn.cursor()

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
        time.sleep(2)
        limpar_tela()
        menu_log_cad()

#Tela de cadastro
def tela_cadastro():
    '''Solicita e valida e-mail e senha, cadastra novo usuário no banco e redireciona para login.'''
    limpar_tela()
    print(Fore.WHITE + '\n' + '='*40)
    print(' '*16 + 'CADASTRO')
    print('='*40)

    Email = input(Fore.YELLOW + 'Seu E-mail: ').strip()
    if ' ' in Email or not email_valido(Email.lower()):
        print(Fore.RED + 'E-mail inválido. Use apenas domínios @gmail.com ou @ufrpe.br e não utilize espaços.')
        time.sleep(4)
        tela_cadastro() 
        return
        
    while True:
        nova_senha = input_senha_asteriscos(Fore.YELLOW + 'Nova senha: ') 
        resultado = validar_senha(nova_senha)
        if resultado == "válida":
            break
        else:
            print(Fore.RED + resultado)
            time.sleep(2)
    
    try:
        cursor.execute('INSERT INTO usuarios (Email, senha) VALUES (?, ?)', (Email, nova_senha))
        conn.commit()
        print(Fore.GREEN + f'\n{Email} cadastrado com sucesso!')
    except sqlite3.IntegrityError:
        print(Fore.RED + 'Usuário já cadastrado. Escolha outro.')
        time.sleep(4)
        tela_cadastro()
    time.sleep(2)
    tela_login()

#Tela de login
def tela_login():
    '''Solicita e-mail e senha, verifica credenciais no banco e exibe mensagem de sucesso ou erro.'''

    limpar_tela()
    print(Fore.WHITE + '='*40)
    print(Fore.WHITE + ' '*17 + 'LOGIN')
    print('='*40)
    
    Email = input(Fore.YELLOW + 'Seu E-mail: ')
    senha = input_senha_asteriscos(Fore.YELLOW + 'Senha: ') 

    cursor.execute('SELECT * FROM usuarios WHERE Email = ? AND senha = ?', (Email, senha))
    resultado = cursor.fetchone()

    print(Fore.BLUE + '\nVerificando...\n')

    if resultado:
        print(Fore.GREEN + f'Bem vindo(a), {Email}!')
    else:
        print(Fore.RED + 'E-mail ou senha incorretos.')
    time.sleep(2)
    menu_principal()

def menu_principal():
    while True:
        limpar_tela()
        print(Fore.WHITE + '=' * 40)
        print(Fore.WHITE + '      === BEM-VINDO AO MUTARE! ===')
        print(Fore.WHITE + '=' * 40)
        print(Fore.CYAN + '1. Menu Hábitos')
        print(Fore.CYAN + '2. Mascote')
        print(Fore.CYAN + '3. Configurações')
        print(Fore.CYAN + '4. Fechar Programa')
        escolha = input(Fore.YELLOW + 'Digite sua escolha: ').strip()

#Execução    
if __name__ == '__main__':
    try:
        menu_log_cad()
    finally:
        cursor.close()
        conn.close()