from database import Database
from util import Utils
from auth import Auth
from habito import Habit
from mascote import Mascot
from colorama import Fore
import time

# Ainda é preciso ter certeza dos objetos ligados ao usuário

def menu_principal(email, db):
    habit = Habit(db)
    mascot = Mascot(db)

    while True:
        Utils.limpar_tela()
        print(Fore.CYAN + f"\n=== BEM-VINDO AO MUTARE, {email}! ===")
        print("[1] Menu de Hábitos")
        print("[2] Ver Mascote")
        print("[3] Sair")

        escolha = input(Fore.YELLOW + "Escolha uma opção: ").strip()
        if escolha == '1':
            menu_habitos(habit)
        elif escolha == '2':
            mascot.exibir()
        elif escolha == '3':
            print("Saindo...")
            time.sleep(1)
            break
        else:
            print(Fore.RED + "Opção inválida.")
            time.sleep(1)


def menu_habitos(habit):
    while True:
        Utils.limpar_tela()
        print(Fore.BLUE + "\n=== MENU DE HÁBITOS ===")
        print("[1] Inserir hábito")
        print("[2] Editar hábito")
        print("[3] Deletar hábito")
        print("[4] Progresso")
        print("[5] Hábitos Recomendados")
        print("[6] Voltar")

        opcao = input(Fore.YELLOW + "Escolha uma opção: ").strip()
        if opcao == '1':
            habit.inserir_habito()
        elif opcao == '2':
            habit.editar_habito()
        elif opcao == '3':
            habit.deletar_habito()
        elif opcao == '4':
            habit.progresso()
        elif opcao == '5':
            habit.recomendacao()
        elif opcao == '6': 
            break
        else:
            print(Fore.RED + "Opção inválida.")
            time.sleep(1)


def menu_inicial(auth):
    while True:
        Utils.limpar_tela()
        print(Fore.MAGENTA + "\n=== MUTARE - GERENCIAMENTO DE HÁBITOS ===")
        print("[1] Login")
        print("[2] Cadastro")
        print("[3] Sair")

        opcao = input(Fore.YELLOW + "Escolha uma opção: ").strip()
        if opcao == '1':
            email = auth.login_usuario()
            if email:
                return email
        elif opcao == '2':
            auth.cadastrar_usuario()
        elif opcao == '3':
            print("Encerrando programa...")
            time.sleep(1)
            return None
        else:
            print(Fore.RED + "Opção inválida.")
            time.sleep(1)


if __name__ == '__main__':
    db = Database('data/Mutare.db') # Objeto do database
    auth = Auth(db) # Objeto do authorizate com database
    try:
        email = menu_inicial(auth)
        if email:
            menu_principal(email, db)
    finally:
        db.close()
