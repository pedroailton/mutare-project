import os
from colorama import init, Fore

init(autoreset=True)

class Util:
    @staticmethod
    def limparTela():
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def emailValido(email):
        return email.endswith('@gmail.com') or email.endswith('@ufrpe.br')

    @staticmethod
    def validarSenha(senha):
        if len(senha) < 4:
            return "A senha deve ter pelo menos 4 caracteres."
        if len(senha) > 8:
            return "A senha não pode ter mais que 8 caracteres."
        if not any(char.isdigit() for char in senha):
            return "A senha deve conter pelo menos um número."
        if not any(char.isupper() for char in senha):
            return "A senha deve conter pelo menos uma letra maiúscula."
        return "válida"

    @staticmethod
    def inputSenhaAsteriscos(prompt='Senha: '):
        senha = ''
        print(prompt, end='', flush=True)
        if os.name == 'nt':
            import msvcrt
            while True:
                char = msvcrt.getch()
                if char in (b'\r', b'\n'):
                    print()
                    break
                elif char == b'\x08':
                    if len(senha) > 0:
                        senha = senha[:-1]
                        print('\b \b', end='', flush=True)
                elif char == b'\x03':
                    raise KeyboardInterrupt
                else:
                    try:
                        senha += char.decode('utf-8')
                        print(Fore.YELLOW + '*', end='', flush=True)
                    except UnicodeDecodeError:
                        pass
        else:
            senha = input()
        return senha
