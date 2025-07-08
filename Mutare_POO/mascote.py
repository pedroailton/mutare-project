from colorama import Fore
from datetime import datetime
from util import Util

class Mascote:
    def __init__(self, db):
        self.db = db

    def exibir(self):
        Util.limparTela()
        print("\n=== Seu mascote motivacional ===\n")

        lista_status = self.db.execute("SELECT status FROM habito_progresso").fetchall()
        feitos = sum(1 for s in lista_status if s[0] == 'Feito')
        total = len(lista_status)

        desempenho_percentual = (feitos / total * 100) if total > 0 else None

        if desempenho_percentual is None:
            estado = "esperando"
        elif desempenho_percentual >= 80:
            estado = "otimo"
        elif desempenho_percentual >= 60:
            estado = "bom"
        elif desempenho_percentual >= 40:
            estado = "fraco"
        else:
            estado = "ruim"

        mensagens = {
            "otimo": (r"\n\(^_^)/", "Você é incrível!!!"),
            "bom": (r"\n(^_^)", "É isso aí, tá arrasando!!"),
            "fraco": (r"\n(._.)", "Bora melhorar!"),
            "ruim": (r"\n(T_T)", "Lembre-se do seu porquê, não desista agora."),
            "esperando": (r"\n(o_o)", "Comece a registrar seu progresso!")
        }

        rosto, mensagem = mensagens[estado]
        print(Fore.YELLOW + rosto)
        print(Fore.CYAN + mensagem)

        input("\nPressione Enter para voltar ao menu.")
