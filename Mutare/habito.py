import time
import re
from datetime import datetime, date
from colorama import Fore
from util import Util

class Habito:
    def __init__(self, db):
        self.db = db

    def inserirHabito(self, email):
        Util.limparTela()
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
            data_inicial_str = input('Data de início (DD/MM/AAAA): ').strip()
            data_inicial = datetime.strptime(data_inicial_str, '%d/%m/%Y').date()

            data_final_str = input('Data de término (DD/MM/AAAA): ').strip()
            data_final = datetime.strptime(data_final_str, '%d/%m/%Y').date()

            if data_final < data_inicial:
                print(Fore.RED + 'Data de término anterior à de início.')
                time.sleep(2)
                return
        except ValueError:
            print(Fore.RED + 'Data inválida.')
            time.sleep(2)
            return

        try:
            self.db.execute('''
                INSERT INTO habitos (Email, nome, criado_em, data_inicial, data_final, frequencia, motivacao)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                email,
                nome,
                date.today().strftime('%d/%m/%Y'),
                data_inicial.strftime('%d/%m/%Y'),
                data_final.strftime('%d/%m/%Y'),
                frequencia,
                motivacao
            ))

            print(Fore.GREEN + f"Hábito '{nome}' adicionado com sucesso!")
        except Exception as e:
            print(Fore.RED + f"Erro ao adicionar hábito: {e}")

        time.sleep(2)

    def listarHabitos(self):
        resultados = self.db.execute("SELECT id, nome, frequencia, motivacao FROM habitos").fetchall()
        if not resultados:
            return []

        for h in resultados:
            print(f"ID: {h[0]} | Nome: {h[1]} | Frequência: {h[2]} | Motivação: {h[3]}")
        return resultados

    def editarHabito(self):
        habitos = self.listarHabitos()
        if not habitos:
            print('Nenhum hábito encontrado.')
            time.sleep(1)
            return

        try:
            habit_id = int(input("ID do hábito a editar: "))
        except ValueError:
            print("ID inválido.")
            return

        dados = self.db.execute("SELECT nome, frequencia, motivacao FROM habitos WHERE id = ?", (habit_id,)).fetchone()
        if not dados:
            print("Nenhum hábito encontrado.")
            return

        novo_nome = input(f"Novo nome ({dados[0]}): ").strip() or dados[0]
        nova_freq = input(f"Nova frequência ({dados[1]}): ").strip() or dados[1]
        nova_motiv = input(f"Nova motivação ({dados[2]}): ").strip() or dados[2]

        self.db.execute('''
            UPDATE habitos SET nome = ?, frequencia = ?, motivacao = ? WHERE id = ?
        ''', (novo_nome, nova_freq, nova_motiv, habit_id))

        print(Fore.GREEN + f"Hábito {habit_id} atualizado.")
        time.sleep(2)

    def deletarHabito(self):
        habitos = self.listarHabitos()
        if not habitos:
            print("Nenhum hábito encontrado.")
            time.sleep(1)
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

        self.db.execute("DELETE FROM habitos WHERE id = ?", (habit_id,))
        print(Fore.GREEN + "Hábito deletado.")
        time.sleep(2)

    