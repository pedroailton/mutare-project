from datetime import datetime, date
import time
from util import Util
from colorama import Fore

class Recomendacao:
    def __init__(self, db):
        self.db = db

    def inserirHabitoRecomendacao(self, habito_recomendado): # Definir hábito recomendado com base em lista
                
        Util.limparTela()

        self.nome = habito_recomendado # Única diferença do método inserir_habito()
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
            start_date = input('Data de início (AAAA-MM-DD): ').strip()
            datetime.strptime(start_date, '%Y-%m-%d')
            end_date = input('Data de término (AAAA-MM-DD): ').strip()
            datetime.strptime(end_date, '%Y-%m-%d')
            if end_date < start_date:
                print(Fore.RED + 'Data de término anterior à de início.')
                return
        except ValueError:
            print(Fore.RED + 'Data inválida.')
            return

        self.db.execute('''
            INSERT INTO habits (name, created_at, start_date, end_date, frequency, motivation)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (self.nome, date.today(), start_date, end_date, self.frequencia, self.motivacao))

        print(Fore.GREEN + f"Hábito recomendado '{self.nome}' adicionado com sucesso!")
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
                    
        while True:
            Util.limparTela()

            print('Cuidar do planeta começa com pequenas atitudes.\nCada gesto sustentável — mesmo que simples — é uma escolha consciente por um futuro melhor.\nQuando você diz “sim” a um hábito ecológico, você diz “não” ao desperdício, à poluição e ao desrespeito com a natureza.\nA sustentabilidade é construída no cotidiano — e depende de você.')

            nomes_habitos_sustentaveis = ['Comprar uma planta para cuidar', 'Reduzir tempo de banho', 'Evitar uso de copos descartáveis']

            # Menu adaptado para futuras alterações na lista nomes_habitos_sustentaveis
            for n in list(range(len(nomes_habitos_sustentaveis))):
                print(f'[{int(n) + 1}] Adicionar o hábito {nomes_habitos_sustentaveis[n]}\n') # indicação de um dígito para cada recomendação da lista
            print(f'[{len(nomes_habitos_sustentaveis) + 1}] Voltar') # indicação do dígito para voltar

            escolha = str(input(Fore.YELLOW + "Escolha uma opção: ")).strip()

            # Verificação do item escolhido
            n = 0
            while n in list(range(len(nomes_habitos_sustentaveis))):
                if escolha == str(int(n) + 1):
                    self.inserirHabitoRecomendacao(self, nomes_habitos_sustentaveis[n])
                    break
                elif escolha == str(len(nomes_habitos_sustentaveis)):
                    print(Fore.CYAN + "Voltando ao Menu de Recomendações...")
                    time.sleep(1)
                    break
                elif escolha == str(len(nomes_habitos_sustentaveis) + 1):
                    print(Fore.RED + "Opção inválida. Tente novamente")
                    time.sleep(1)
                    break
                n = n + 1


    def habitosSaudaveis(self):
                
        while True:
            Util.limparTela()
            print('Seu corpo é sua base e sua mente é seu motor.\nInvestir em hábitos saudáveis é uma forma de honrar o presente e proteger o seu futuro.\nDormir bem, se alimentar com equilíbrio, se movimentar: tudo isso transforma sua energia, seu humor e sua disposição.\nSeu bem-estar é sua principal ferramenta para viver com mais plenitude.')

            nomes_habitos_saudaveis = ['Dormir no mínimo 7 horas na noite anterior', 'Beber ao menos 2 litros de água', 'Caminhar']

            for n in list(range(len(nomes_habitos_saudaveis))):
                print(f'[{int(n) + 1}] Adicionar o hábito {nomes_habitos_saudaveis[n]}\n') # indicação de um dígito para cada recomendação da lista
            print(f'[{len(nomes_habitos_saudaveis) + 1}] Voltar') # indicação do dígito para voltar

            escolha = str(input(Fore.YELLOW + "Escolha uma opção: ")).strip()

            # Verificação do item escolhido
            n = 0
            while n in list(range(len(nomes_habitos_saudaveis))):
                if escolha == str(n + 1):
                    self.inserirHabitoRecomendacao(self, nomes_habitos_saudaveis[n])
                    break
                elif escolha == str(len(nomes_habitos_saudaveis)):
                    print(Fore.CYAN + "Voltando ao Menu de Recomendações...")
                    time.sleep(1)
                    break
                elif escolha == str(len(nomes_habitos_saudaveis) + 1):
                    print(Fore.RED + "Opção inválida. Tente novamente")
                    time.sleep(1)
                    break
                n = n + 1

    def habitosCriativos(self):

        while True:
            Util.limparTela()

            print('A criatividade é a ponte entre o que você sente e o que você expressa, sua essência.\nQuando você cultiva hábitos criativos, você alimenta sua autenticidade, sua curiosidade e sua capacidade de enxergar o mundo de forma única.\nCriar é uma forma de autoconhecimento e liberdade.\nUm minuto de imaginação ativa pode iluminar o seu dia inteiro. Você deveria investir nesses hábitos.')

            nomes_habitos_criativos = ['Desenhar', 'Tocar violão', 'Ler um livro' 'Sair sozinho', 'Escrever em um diário']

            for n in list(range(len(nomes_habitos_criativos))):
                print(f'[{int(n) + 1}] Adicionar o hábito {nomes_habitos_criativos[n]}\n') # indicação de um dígito para cada recomendação da lista
            print(f'[{len(nomes_habitos_criativos) + 1}] Voltar') # indicação do dígito para voltar

            escolha = str(input(Fore.YELLOW + "Escolha uma opção: ")).strip()

            # Verificação do item escolhido
            n = 0
            while n in list(range(len(nomes_habitos_criativos))):
                if escolha == str(n + 1):
                    self.inserirHabitoRecomendacao(self, nomes_habitos_criativos[n])
                    break
                elif escolha == str(len(nomes_habitos_criativos)):
                    print(Fore.CYAN + "Voltando ao Menu de Recomendações...")
                    time.sleep(1)
                    break
                elif escolha == str(len(nomes_habitos_criativos) + 1):
                    print(Fore.RED + "Opção inválida. Tente novamente")
                    time.sleep(1)
                    break
                n = n + 1     