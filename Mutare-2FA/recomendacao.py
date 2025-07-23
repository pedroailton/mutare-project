from datetime import datetime, date
import time
from util import Util
from colorama import Fore

class Recomendacao:
    def __init__(self, db, email):
        self.db = db
        self.email = email

    def inserirHabitoRecomendacao(self, habito_recomendado):       
        Util.limparTela()

        self.nome = habito_recomendado
        print(f'Nome: {self.nome}')

        self.frequencia = input('Frequência (Diária, Semanal ou Mensal): ').strip().capitalize()
        if self.frequencia not in ['Diária', 'Semanal', 'Mensal']:
            print(Fore.RED + 'Frequência inválida. Tente novamente')
            time.sleep(2)
            return

        self.motivacao = input('Motivação (opcional, até 200 caracteres): ').strip()
        if self.motivacao and len(self.motivacao) > 200:
            print(Fore.RED + 'Motivação muito longa.')
            time.sleep(2)
            return

        try:
            start_date = input('Data de início (DD/MM/AAAA): ').strip()
            end_date = input('Data de término (DD/MM/AAAA): ').strip()

            start_date_dt = datetime.strptime(start_date, '%d/%m/%Y')
            end_date_dt = datetime.strptime(end_date, '%d/%m/%Y')

            if end_date_dt < start_date_dt:
                print(Fore.RED + 'Data de término anterior à de início.')
                time.sleep(2)
                return

        except ValueError:
            print(Fore.RED + 'Data inválida.')
            time.sleep(2)
            return

        try:
            self.db.execute('''
                INSERT INTO habitos (nome, criado_em, data_inicial, data_final, frequencia, motivacao, email)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (self.nome, date.today(), start_date, end_date, self.frequencia, self.motivacao, self.email))
  
            print(Fore.GREEN + f"Hábito recomendado '{self.nome}' adicionado com sucesso!")
            time.sleep(2)

        except Exception as e:
            print(Fore.RED + f"Erro ao adicionar hábito: {e}")
            time.sleep(2)

    def mostrarRecomendacao(self):
        while True:
            Util.limparTela()
            print(Fore.CYAN + f"\n=== HÁBITOS RECOMENDADOS ===")
            print("[1] Hábitos Sustentáveis")
            print("[2] Hábitos Saudáveis")
            print("[3] Hábitos Criativos")
            print("[4] Voltar")

            escolha = input(Fore.YELLOW + "Escolha uma opção: ").strip()
            if escolha == '1':
                self.habitosSustentaveis()
            elif escolha == '2':
                self.habitosSaudaveis()
            elif escolha == '3':
                self.habitosCriativos()
            elif escolha == '4':
                print("Voltando ao menu de hábitos...")
                time.sleep(1)
                break
            else:
                print(Fore.RED + "Opção inválida. Tente novamente")
                time.sleep(1)

    def habitosSustentaveis(self):
        nomes = ['Comprar uma planta para cuidar', 'Reduzir tempo de banho', 'Evitar uso de copos descartáveis']
        while True:
            Util.limparTela()
            print('Cuidar do planeta começa com pequenas atitudes.\n')

            for i, nome in enumerate(nomes, 1):
                print(f'[{i}] Adicionar o hábito {nome}\n')
            print(f'[{len(nomes) + 1}] Voltar')

            escolha = input(Fore.YELLOW + "Escolha uma opção: ").strip()
            if escolha.isdigit() and 1 <= int(escolha) <= len(nomes):
                self.inserirHabitoRecomendacao(nomes[int(escolha) - 1])
                break
            elif escolha == str(len(nomes) + 1):
                print(Fore.CYAN + "Voltando ao Menu de Recomendações...")
                time.sleep(1)
                break
            else:
                print(Fore.RED + "Opção inválida. Tente novamente")
                time.sleep(1)

    def habitosSaudaveis(self):
        nomes = ['Dormir no mínimo 7 horas na noite anterior', 'Beber ao menos 2 litros de água', 'Caminhar']
        while True:
            Util.limparTela()
            print('Seu corpo é sua base e sua mente é seu motor.\n')

            for i, nome in enumerate(nomes, 1):
                print(f'[{i}] Adicionar o hábito {nome}\n')
            print(f'[{len(nomes) + 1}] Voltar')

            escolha = input(Fore.YELLOW + "Escolha uma opção: ").strip()
            if escolha.isdigit() and 1 <= int(escolha) <= len(nomes):
                self.inserirHabitoRecomendacao(nomes[int(escolha) - 1])
                break
            elif escolha == str(len(nomes) + 1):
                print(Fore.CYAN + "Voltando ao Menu de Recomendações...")
                time.sleep(1)
                break
            else:
                print(Fore.RED + "Opção inválida. Tente novamente")
                time.sleep(1)

    def habitosCriativos(self):
        nomes = ['Desenhar', 'Tocar violão', 'Ler um livro', 'Sair sozinho', 'Escrever em um diário']  # corrigido: vírgula faltando

        while True:
            Util.limparTela()
            print('A criatividade é a ponte entre o que você sente e o que você expressa.\n')

            for i, nome in enumerate(nomes, 1):
                print(f'[{i}] Adicionar o hábito {nome}\n')
            print(f'[{len(nomes) + 1}] Voltar')

            escolha = input(Fore.YELLOW + "Escolha uma opção: ").strip()
            if escolha.isdigit() and 1 <= int(escolha) <= len(nomes):
                self.inserirHabitoRecomendacao(nomes[int(escolha) - 1])
                break
            elif escolha == str(len(nomes) + 1):
                print(Fore.CYAN + "Voltando ao Menu de Recomendações...")
                time.sleep(1)
                break
            else:
                print(Fore.RED + "Opção inválida. Tente novamente")
                time.sleep(1)
