import time
import re
from datetime import datetime, date
from colorama import Fore

from utils import Utils

class Habit:
    def __init__(self, db):
        self.db = db

    def inserir_habito(self):
        Utils.limpar_tela()
        nome = input('Nome do hábito (até 50 caracteres): ').strip()

        if not nome or len(nome) > 50 or not re.match(r'^[A-Za-z0-9 ]+$', nome):
            print(Fore.RED + 'Nome inválido. Use apenas letras, números e espaços.')
            time.sleep(2)
            return

        frequencia = input('Frequência (Diária, Semanal ou Mensal): ').strip().capitalize()
        if frequencia not in ['Diária', 'Semanal', 'Mensal']:
            print(Fore.RED + 'Frequência inválida.')
            time.sleep(2)
            return

        motivacao = input('Motivação (opcional, até 200 caracteres): ').strip()
        if motivacao and len(motivacao) > 200:
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
        ''', (nome, date.today(), start_date, end_date, frequencia, motivacao))

        print(Fore.GREEN + f"Hábito '{nome}' adicionado com sucesso!")
        time.sleep(2)

    def listar_habitos(self):
        resultados = self.db.execute("SELECT id, name, frequency, motivation FROM habits").fetchall()
        if not resultados:
            print("Nenhum hábito encontrado.")
            return []

        for h in resultados:
            print(f"ID: {h[0]} | Nome: {h[1]} | Frequência: {h[2]} | Motivação: {h[3]}")
        return resultados

    def editar_habito(self):
        habitos = self.listar_habitos()
        if not habitos:
            return

        try:
            habit_id = int(input("ID do hábito a editar: "))
        except ValueError:
            print("ID inválido.")
            return

        dados = self.db.execute("SELECT name, frequency, motivation FROM habits WHERE id = ?", (habit_id,)).fetchone()
        if not dados:
            print("Hábito não encontrado.")
            return

        novo_nome = input(f"Novo nome ({dados[0]}): ").strip() or dados[0]
        nova_freq = input(f"Nova frequência ({dados[1]}): ").strip() or dados[1]
        nova_motiv = input(f"Nova motivação ({dados[2]}): ").strip() or dados[2]

        self.db.execute('''
            UPDATE habits SET name = ?, frequency = ?, motivation = ? WHERE id = ?
        ''', (novo_nome, nova_freq, nova_motiv, habit_id))

        print(Fore.GREEN + f"Hábito {habit_id} atualizado.")
        time.sleep(2)

    def deletar_habito(self):
        habitos = self.listar_habitos()
        if not habitos:
            return

        try:
            habit_id = int(input("ID do hábito a deletar: "))
        except ValueError:
            print("ID inválido.")
            return

        confirm = input("Tem certeza que deseja deletar? (s/n): ").lower()
        if confirm != 's':
            print("Operação cancelada.")
            return

        self.db.execute("DELETE FROM habits WHERE id = ?", (habit_id,))
        print(Fore.GREEN + "Hábito deletado.")
        time.sleep(2)

    def progresso(self):
        Utils.limpar_tela()
        print("\n=== Progresso dos hábitos ===")

        habitos = self.db.execute("SELECT id, name, start_date, end_date, frequency FROM habits").fetchall()
        if not habitos:
            print("Nenhum hábito encontrado.")
            time.sleep(2)
            return

        for habito in habitos:
            habit_id, name, start, end, freq = habito
            start = datetime.strptime(start, '%Y-%m-%d').date()
            end = datetime.strptime(end, '%Y-%m-%d').date()
            today = date.today()

            if freq == 'Diária':
                total = (end - start).days + 1
            elif freq == 'Semanal':
                total = ((end - start).days // 7) + 1
            elif freq == 'Mensal':
                total = ((end.year - start.year) * 12 + end.month - start.month) + 1
            else:
                print(f"Frequência desconhecida para {name}.")
                continue

            feitos = self.db.execute("SELECT COUNT(*) FROM habit_progress WHERE habit_id = ?", (habit_id,)).fetchone()[0]
            porcentagem = (feitos / total) * 100 if total else 0
            barra = '🟩' * int(porcentagem/10) + '⬜' * (10 - int(porcentagem/10))

            print(f"\n{name} ({freq}) | {start} a {end}")
            print(f"Progresso: {barra} {porcentagem:.2f}% ({feitos}/{total})")

            if input("Marcar progresso? (s/n): ").strip().lower() == 's':
                data = input("Data (YYYY-MM-DD), ou Enter para hoje: ").strip() or today.isoformat()
                status = input("Status (Feito/Não feito): ").strip().capitalize()

                try:
                    datetime.strptime(data, '%Y-%m-%d')
                    self.db.execute('''INSERT INTO habit_progress (habit_id, date, status) VALUES (?, ?, ?)''',
                                    (habit_id, data, status))
                    print(Fore.GREEN + "Progresso registrado!")
                except:
                    print(Fore.RED + "Erro ao registrar progresso.")

        input("\nPressione Enter para continuar...")
