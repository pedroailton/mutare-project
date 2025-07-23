from colorama import Fore
from datetime import datetime
from util import Util

class Mascote:
    def __init__(self, db):
        self.db = db

    def exibir(self):
        Util.limparTela()
        print("\n=== Seu mascote motivacional ===\n")

        # Pega todos os registros de progresso
        registros = self.db.execute("SELECT id_habito FROM habito_progresso").fetchall()
        total_feitos = len(registros)

        # Calcula o total possível com base nos hábitos cadastrados
        habitos = self.db.execute("SELECT id, data_inicial, data_final, frequencia FROM habitos").fetchall()
        total_possivel = 0

        for id_habito, data_inicio, data_fim, frequencia in habitos:
            try:
                inicio = datetime.strptime(data_inicio, '%d/%m/%Y').date()
                fim = datetime.strptime(data_fim, '%d/%m/%Y').date()
            except ValueError:
                continue  # ignora se as datas estiverem mal formatadas

            if frequencia == 'Diária':
                total_possivel += (fim - inicio).days + 1
            elif frequencia == 'Semanal':
                total_possivel += ((fim - inicio).days // 7) + 1
            elif frequencia == 'Mensal':
                total_possivel += ((fim.year - inicio.year) * 12 + fim.month - inicio.month) + 1

        desempenho = (total_feitos / total_possivel * 100) if total_possivel > 0 else None

        # Define o estado do mascote
        if desempenho is None:
            estado = "esperando"
        elif desempenho >= 80:
            estado = "otimo"
        elif desempenho >= 60:
            estado = "bom"
        elif desempenho >= 40:
            estado = "fraco"
        else:
            estado = "ruim"

        # Rosto e mensagem do mascote
        mensagens = {
            "otimo": (r"\(^_^)/", "Você é incrível!!!"),
            "bom": (r"(^_^)", "É isso aí, tá arrasando!!"),
            "fraco": (r"(._.)", "Bora melhorar!"),
            "ruim": (r"(T_T)", "Lembre-se do seu porquê, não desista agora."),
            "esperando": (r"(o_o)", "Comece a registrar seu progresso!")
        }

        rosto, mensagem = mensagens[estado]
        print(Fore.YELLOW + rosto)
        print(Fore.CYAN + mensagem)

        input("\nPressione Enter para voltar ao menu.")
