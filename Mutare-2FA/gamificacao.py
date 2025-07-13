from datetime import date, datetime
from util import Util
from colorama import Fore
import time

class Gamificacao:
    def __init__(self, db):
        self.db = db
        self.nivel_atual = 0

    def calcularProgresso(self):
        Util.limparTela()
        print("\n=== Progresso dos hábitos ===")

        habitos = self.db.execute("SELECT id, nome, data_inicial, data_final, frequencia FROM habitos").fetchall()
        if not habitos:
            print("Nenhum hábito encontrado.")
            time.sleep(1)
            return

        for habito in habitos:
            id_habito, nome, inicio, fim, freq = habito
            inicio = datetime.strptime(inicio, '%d/%m/%Y').date()
            fim = datetime.strptime(fim, '%d/%m/%Y').date()
            hoje = date.today()

            if freq == 'Diária':
                total = (fim - inicio).days + 1
            elif freq == 'Semanal':
                total = ((fim - inicio).days // 7) + 1
            elif freq == 'Mensal':
                total = ((fim.year - inicio.year) * 12 + fim.month - inicio.month) + 1
            else:
                print(f"Frequência desconhecida para {nome}.")
                continue

            feitos = self.db.execute(
                "SELECT COUNT(*) FROM habito_progresso WHERE id_habito = ?",
                (id_habito,)
            ).fetchone()[0]

            porcentagem = (feitos / total) * 100 if total else 0
            barra = '🟩' * int(porcentagem / 10) + '⬜' * (10 - int(porcentagem / 10))

            print(f"\n{nome} ({freq}) | {inicio} a {fim}")
            print(f"Progresso: {barra} {porcentagem:.2f}% ({feitos}/{total})")

            if input("Marcar progresso? (s/n): ").strip().lower() == 's':
                data = input("Data (DD/MM/AAAA), ou Enter para hoje: ").strip()
                if not data:
                    data = hoje.strftime('%d/%m/%Y')

                try:
                    datetime.strptime(data, '%d/%m/%Y') 
                    # verifica se já existe registro para esse hábito nessa data
                    ja_existe = self.db.execute(
                        "SELECT 1 FROM habito_progresso WHERE id_habito = ? AND data = ?",
                        (id_habito, data)
                    ).fetchone()

                    if ja_existe:
                        print(Fore.YELLOW + "Progresso já registrado para essa data.")
                    else:
                        self.db.execute(
                            "INSERT INTO habito_progresso (id_habito, data) VALUES (?, ?)",
                            (id_habito, data)
                        )
                        print(Fore.GREEN + "Progresso registrado!")
                except ValueError:
                    print(Fore.RED + "Data inválida.")
                except Exception as e:
                    print(Fore.RED + f"Erro ao registrar progresso: {e}")

        input("\nPressione Enter para continuar...")
    
    
    def atualizarXP(self):
        """
        Algoritmo de xp:
            Preenchimento único de hábito (diário, semanal,mensal): 1 ponto, 2 pontos e 3 pontos, respectivamente;
            Meta de feitos: de 20 em 20 (20, 40, 60, ...): 5 pontos;
            Para subir de nível: 5 pontos.
        """
        total_pontos = 0
        pontos = 0
        meta = 20

        habitos = self.db.execute("SELECT id, frequencia FROM habitos").fetchall()
        
        try:
            # Verificação de 'feitos' em cada hábito registrado no banco de dados
            for id_habito, frequencia in habitos:
                feitos = self.db.execute(
                        "SELECT COUNT(*) FROM habito_progresso WHERE id_habito = ?",
                        (id_habito,)
                    ).fetchone()[0]
                
                # Registro de pontos por tipo de frequência
                if frequencia == 'Diária':
                    pontos = feitos * 1
                elif frequencia == 'Semanal':
                    pontos = feitos * 2
                elif frequencia == 'Mensal':
                    pontos = feitos * 3

                # Contadores
                total_pontos += pontos 
                total_feitos += feitos

            # Pontos por meta batida
            total_pontos += (total_feitos // meta) * 5

            # Subir de nível
            novo_nivel = total_pontos // 5
            self.nivel_atual = novo_nivel

        # Caso não haja hábitos registrados, não faça nenhuma operação
        except:
            pass

        finally:
            return self.nivel_atual
    