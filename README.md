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
RF012 - Verificação em Duas Etapas por email  
RF013 - Recuperar Senha  
RF014 - Recomendações Inteligentes  

## PRINCIPAIS FUNÇÕES DO CÓDIGO

### Autenticação de Usuário

- `menuInicial(auth)`: Menu inicial com opções de login e cadastro.
- `cadastrarUsuario(self)`: Cadastro de usuários com validação de e-mail e senha.
- `loginUsuario(self)`: Login seguro com verificação de credenciais e limite de tentativas.
- `enviarCodigoAutenticacao(self, destinatario, codigo)`: Envia um código para a autenticação em dois fatores e recuperação de senha.
- `recuperarSenha(self)`: Realiza o processo de recuperação de senha.

### Configurações da Conta

- `menuconfiguracoes(self, email, game)`: Acessa as configurações da conta do usuário.
- `visualizarConta(self, email, game)`: Exibe informações da conta e permite alterações.
- `atualizarSenha(self, email)`: Atualiza a senha com verificação da senha atual.
- `excluirConta(self, email)`: Exclui a conta após dupla confirmação.
- `buscarConta(self, email)`: Recupera dados da conta do usuário logado.

### Gerenciamento de Hábitos

- `menuHabitos(email, habito, game, rec)`: Menu com opções de adicionar, editar, deletar ou visualizar hábitos.
- `inserirHabito(self, email)`: Adiciona um novo hábito com nome, frequência, motivação e datas.
- `listarHabitos(self)`: Lista todos os hábitos cadastrados.
- `editarHabito(self)`: Edita um hábito existente.
- `deletarHabito(self)`: Exclui um hábito com base no ID.

### Gameficação

- `calcularProgresso(self)`: Exibe barra de progresso para cada hábito com base na frequência (Diária, Semanal, Mensal).
  - Permite adicionar registros conforme a frequência.
  - Garante que não sejam inseridos registros duplicados para o mesmo período.
- `atualizarPontos(self)`: Atualiza os pontos de XP.
  
### Mascote Motivacional

- `exibir(self)`: Mostra um mascote com mensagens motivacionais de acordo com o desempenho do usuário:
  - Desempenho excelente (≥ 80%)
  - Bom (60–79%)
  - Fraco (40–59%)
  - Ruim (< 40%)
  - Sem registros (início)

### Utilidades

- `limparTela()`: Limpa a tela do terminal conforme o sistema operacional.
- `emailValido(email)`: Verifica se o e-mail possui domínio permitido (`@gmail.com`, `@ufrpe.br`).
- `validarSenha(senha)`: Valida senhas com base em regras de segurança (mín. 1 número, 1 maiúscula).
- `inputSenhaAsteriscos()`: Entrada de senha com caracteres ocultos no terminal.


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
