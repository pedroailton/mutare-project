from util import Util

class Game():
    def progresso(self):
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
                    datetime.strptime(data, '%d/%m/%Y')  # valida o formato
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
    
    '''
    def atualizar_xp(self):
        """
        Algoritmo de xp:
            Preenchimento único de hábito (diário, semanal,mensal): 1 ponto, 2 pontos e 3 pontos, respectivamente
            Meta de preenchimentos: de 20 em 20 (20, 40, 60, ...): 5 pontos
            Pontos para subir de nível: 5
        """
        Utils.limpar_tela()

        pontos = quantidade de preenchimentos de hábitos presente no banco de dados (db)

        # Subir de nível
        if pontos >= nivel_atual + 5
            nivel_atual += 1
    '''