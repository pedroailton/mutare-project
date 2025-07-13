from database import Database
from util import Util
from auth import Auth
from habito import Habito
from mascote import Mascote
from colorama import Fore
from configurações import Config
from gamificacao import Gamificacao
from recomendacao import Recomendacao
import main
import time


def menuPrincipal(email, db):
    habito = Habito(db)
    mascote = Mascote(db)
    auth = Auth(db)
    config = Config(db, main, auth)
    game = Gamificacao(db)
    rec = Recomendacao(db)

    while True:
        Util.limparTela()
        print(Fore.CYAN + f"\n=== BEM-VINDO AO MUTARE, {email}! ===")
        print("[1] Menu de Hábitos")
        print("[2] Ver Mascote")
        print("[3] Configurações")
        print("[4] Sair")

        escolha = input(Fore.YELLOW + "Escolha uma opção: ").strip()
        if escolha == '1':
            menuHabitos(email, habito, game, rec)
        elif escolha == '2':
            mascote.exibir()
        elif escolha == '3':
            config.menuConfiguracoes(email, game)
        elif escolha == '4':
            print("Saindo...")
            time.sleep(1)
            break
        else:
            print(Fore.RED + "Opção inválida.")
            time.sleep(1)


def menuHabitos(email, habito, game, rec):

    while True:
        Util.limparTela()
        print(Fore.BLUE + "\n=== MENU DE HÁBITOS ===")
        print("[1] Inserir hábito")
        print("[2] Editar hábito")
        print("[3] Deletar hábito")
        print("[4] Progresso")
        print("[5] Hábitos Recomendados")
        print("[6] Voltar")

        opcao = input(Fore.YELLOW + "Escolha uma opção: ").strip()
        if opcao == '1':
            habito.inserirHabito(email)
        elif opcao == '2':
            habito.editarHabito()
        elif opcao == '3':
            habito.deletarHabito()
        elif opcao == '4':
            game.progresso()
        elif opcao == '5':
            rec.mostrarRecomendacao()
        elif opcao == '6':
            break
        else:
            print(Fore.RED + "Opção inválida.")
            time.sleep(1)
            

def menuInicial(auth):
    while True:
        Util.limparTela()
        print(Fore.MAGENTA + "\n=== MUTARE - GERENCIAMENTO DE HÁBITOS ===")
        print("[1] Login")
        print("[2] Cadastro")
        print("[3] Sair")

        opcao = input(Fore.YELLOW + "Escolha uma opção: ").strip()
        if opcao == '1':
            email = auth.loginUsuario()
            if email:
                return email
        elif opcao == '2':
            auth.cadastrarUsuario()
        elif opcao == '3':
            print("Encerrando programa...")
            time.sleep(1)
            return None
        else:
            print(Fore.RED + "Opção inválida.")
            time.sleep(1)


if __name__ == '__main__':
    db = Database()
    auth = Auth(db)
    try:
        email = menuInicial(auth)
        if email:
            menuPrincipal(email, db)
    finally:
        db.close()
