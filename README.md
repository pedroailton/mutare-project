![Sem nome (500 x 500 px) (2)](https://github.com/user-attachments/assets/db754006-615e-483d-b495-2ba13c265d26)
# MUTARE Project 🐌

**Repositório MUTARE - PISI1 - Projetos Interdiciplinares de Sistemas da Informação 1**  
Desenvolvedores: [Laura Cordeiro](https://github.com/mlcordeiro) e [Pedro Ailton](https://github.com/pedroailton)  
Docente Responsável: [Cleyton Magalhães](https://github.com/cvanut)

Descrição do projeto:  
O Mutare é uma ferramenta segura de gerenciamento consciente de hábitos que busca trazer qualidade de vida, saúde e produtividade na atual era de estímulos incessantes advindos das comodidades das novas tecnologias, que desincentiva a prática de bons hábitos.  
A partir da poderosa psicologia do hábito (acertivamente tratada por Charles Duhigg em seu livro "O Poder do Hábito", inspiração para o nosso projeto), criamos um sistema digital capaz de fornecer assistência ao desenvolvimento de hábitos novos (que o sistema também poderá sugerir - como hábitos sustentáveis e cidadãos), correção de maus hábitos e acompanhamento dos hábitos desenvolvidos pelos usuários, junto de um sistema de recompensas, medição de desempenho e mascote.  
Esse é o Mutare.

## ENTREGAS
- [x] 1VA 28/05/25
- [ ] 2VA 23/07/25
- [ ] 3VA 30/07/25

## FLUXOGRAMAS DOS REQUISITOS FUNCIONAIS
Acesse clicando [aqui](https://drive.google.com/drive/folders/1aOAuCHuZ8fUJ0etgrPnZh6ARmnOMll4f?usp=sharing) (Google Drive)
## REQUISITOS FUNCIONAIS
###  1ª VA
RF001 - Menu Cadastro  
RF002 -  Cadastro de Conta do Usuário ("C" do CRUD)  
RF003 - Login  
RF004 - Senha Não Visível ao Digitar  
RF006 - Menu Principal  
RF007 - Configurações: "R", "U" e "D" do CRUD de Conta do Usuário  
RF008 - Menu Hábitos  
RF009 - Algoritmo de Desempenho do Usuário para Mascote  
RF009- Mascote  
RF010 - CRUD Hábitos  
  
 ### 2ª VA

RF011 - Sistema de Recompensas(XP) e Níveis  
RF012 - Interface Gráfica com CustomTKinter  
RF013 - Verificação em Duas Etapas por email  
RF014 - Recuperar Senha  
RF015 - Recomendações Inteligentes  

## PRINCIPAIS FUNÇÕES DO CÓDIGO

### Autenticação de Usuário

- `menu_log_cad()`: Menu inicial com opções de login e cadastro.
- `tela_cadastro()`: Cadastro de usuários com validação de e-mail e senha.
- `tela_login()`: Login seguro com verificação de credenciais e limite de tentativas.
- `email_valido(email)`: Verifica se o e-mail possui domínio permitido (`@gmail.com`, `@ufrpe.br`).
- `validar_senha(senha)`: Valida senhas com base em regras de segurança (mín. 1 número, 1 maiúscula).
- `input_senha_asteriscos()`: Entrada de senha com caracteres ocultos no terminal.

### Configurações da Conta

- `configuracoes(Email)`: Acessa as configurações da conta do usuário.
- `visualizar_conta(Email)`: Exibe informações da conta e permite alterações.
- `atualizar_senha(Email)`: Atualiza a senha com verificação da senha atual.
- `excluir_conta(Email)`: Exclui a conta após dupla confirmação.

### Gerenciamento de Hábitos

- `menu_habitos()`: Menu com opções de adicionar, editar, deletar ou visualizar hábitos.
- `inserir_habito()`: Adiciona um novo hábito com nome, frequência, motivação e datas.
- `listar_habitos(cursor)`: Lista todos os hábitos cadastrados.
- `editar_habito(cursor, conn)`: Edita um hábito existente.
- `deletar_habito(cursor, conn)`: Exclui um hábito com base no ID.

### Registro de Progresso

- `progresso()`: Exibe barra de progresso para cada hábito com base na frequência (Diária, Semanal, Mensal).
  - Permite adicionar registros conforme a frequência.
  - Garante que não sejam inseridos registros duplicados para o mesmo período.

### Mascote Motivacional

- `mascote()`: Mostra um mascote com mensagens motivacionais de acordo com o desempenho do usuário:
  - Desempenho excelente (≥ 80%)
  - Bom (60–79%)
  - Fraco (40–59%)
  - Ruim (< 40%)
  - Sem registros (início)

### Utilidades

- `limpar_tela()`: Limpa a tela do terminal conforme o sistema operacional.
- `buscar_conta(Email)`: Recupera dados da conta do usuário logado.


## TECNOLOGIAS UTILIZADAS

- Python 3.13.5
- SQLite 3
- Bibliotecas `bcrypt`,`colorama`,`datetime`, `os`, `time`, `re`, `msvcrt`

## BIBLIOTECAS

## INSTALAÇÃO NECESSÁRIA
 ```
 pip install colorama bcrypt
 ```
Utilizar esse comando na execução no terminal.
