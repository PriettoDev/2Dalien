2Dalien: Laboratório de Alta Qualidade em Software

Status: encerrado. Este repositório foi usado como projeto prático da primeira parte da disciplina e não recebe mais atualizações. Ele fica preservado como registro do que foi estudado e aplicado.

Repositório de estudos da disciplina Alta Qualidade em Software (AQS), do curso de Engenharia da Computação da Universidade SENAI CIMATEC, ministrada pelo Prof. Dr. Leonardo da Cruz.

O ponto de partida foi o Game2D_Alien, um jogo 2D open source em Python/Pygame no estilo Alien Invasion: o jogador controla uma nave na parte inferior da tela e atira em uma frota de alienígenas. O jogo em si nunca foi o objetivo. Ele serviu de laboratório para aplicar, aula após aula, práticas de qualidade de software sobre um código real que começou monolítico.

A pergunta central que guiou o trabalho foi:

Não basta o código funcionar. Ele é legível, modular, testável, versionado e manutenível?

Sumário
Estrutura do projeto
O que foi estudado e aplicado
1. Análise estática e tipagem
2. Git, GitHub e Git Flow
3. Princípios SOLID e modularização
4. Testes automatizados com Pytest
5. Dublês de teste: stubs e mocks
6. Relatórios e cobertura de testes
Defeitos encontrados e corrigidos
Lições de ambiente e ferramentas
Como executar
Dívida técnica conhecida
Tecnologias
Licença
Estrutura do projeto
2Dalien/
├── images/                          # Sprites do jogo (ex.: ship.bmp)
├── src/
│   ├── alien_invasion_refactored.py # Classe principal: coordena o jogo
│   ├── alien.py                     # Alienígena
│   ├── fast_alien.py                # Variação de alienígena (extensão, OCP)
│   ├── bullet.py                    # Projétil
│   ├── bullet_manager.py            # Gerenciamento dos projéteis
│   ├── fleet_manager.py             # Criação e atualização da frota
│   ├── game_events.py               # Tratamento de eventos de entrada
│   ├── game_renderer.py             # Desenho dos elementos na tela
│   ├── settings.py                  # Configurações do jogo
│   ├── ship.py                      # Nave do jogador
│   └── desconto.py                  # Exemplo didático (SOLID e testes)
├── tests/
│   ├── doubles.py                   # Dublês de teste reutilizáveis (stubs)
│   ├── test_desconto.py             # Assert, fixture e parametrize
│   ├── test_doubles.py              # Stub e mock aplicados ao Pedido
│   └── test_ship.py                 # Stub e mock aplicados à nave
├── pytest.ini                       # Configuração do Pytest
├── requiriments.txt                 # Dependências do projeto
├── .gitignore
├── LICENSE
└── README.md
O que foi estudado e aplicado
1. Análise estática e tipagem

Problema: muitos erros podem ser detectados sem executar o programa, apenas lendo o código: tipos incompatíveis, imports não usados, violações de estilo.

O que foi feito:

Ruff: linter e verificador de estilo (PEP 8), usado para apontar problemas de padronização.
Mypy: verificador de tipos estáticos, aplicado sobre o código com type hints.
MonkeyType: ferramenta que observa o programa em execução e sugere type hints a partir dos tipos realmente usados. É útil para tipar código legado. O banco gerado (monkeytype.sqlite3) é um artefato local e foi incluído no .gitignore.

Aprendizado: Python continua sendo dinamicamente tipado. Os type hints não mudam o comportamento em tempo de execução, mas permitem que ferramentas encontrem erros antes de o código rodar. E um alerta de ferramenta é um sinal para investigar, não uma verdade absoluta.

2. Git, GitHub e Git Flow

Problema: sem um fluxo organizado, o histórico vira uma sequência de "alteração", "teste", "aula", e fica impossível entender o que mudou e por quê.

Modelo de branches adotado (Git Flow):

main     ──●─────────────────────────────●──────   versões estáveis
            \                           /
develop      ●──●──●──●──●──●──●──●──●─●─────────  integração contínua do trabalho
              \       /  \             /
feature/...    ●──●──●    ●──●──●──●──●            uma branch por funcionalidade
Branch	Papel	Vida útil
main	Versão estável	Permanente
develop	Integração das funcionalidades	Permanente
feature/*	Uma funcionalidade ou aula (ex.: feature/applying-solid, feature/tests_units, feature/analise-estatica)	Apagada após o merge

Práticas exercitadas:

Modelo mental do Git: Working Directory → Staging Area → Repositório local → Repositório remoto.
Revisão antes de cada commit com git status, git diff e git diff --staged.
git add seletivo, arquivo por arquivo, em vez de git add . mecânico.
Staging parcial com git add -p, para separar duas mudanças de intenções diferentes no mesmo arquivo em commits distintos.
Commits atômicos e Conventional Commits (feat, fix, test, chore, refactor, style, docs).
Pull Request no GitHub (PR #1, da análise estática).
Merge fast-forward vs. merge com commit (--no-ff), e sincronização segura com --ff-only.
Resolução de conflitos de merge, lendo os dois lados e verificando com git show que nenhuma regra foi perdida.
Exclusão segura de branches integradas (git branch -d, local, e git push origin --delete, remoto).
Inspeção do histórico com git log --oneline --graph --all e git log A..B.
3. Princípios SOLID e modularização

Problema: o jogo começou com um arquivo único (alien_invasion.py) que concentrava eventos, desenho, frota, projéteis e colisões. Qualquer mudança arriscava quebrar partes não relacionadas, e testar uma parte isolada era praticamente impossível.

Evolução:

Código monolítico
      ↓  muitas responsabilidades numa só classe
Single Responsibility Principle (SRP)
      ↓  separação em módulos e classes coesos
alien_invasion_refactored.py + gerenciadores especializados
      ↓
Código modular, mais fácil de entender, alterar e testar
SRP (Responsabilidade Única): cada módulo passou a ter um motivo para mudar. Por exemplo: game_events.py trata entradas, game_renderer.py desenha, fleet_manager.py cuida da frota e bullet_manager.py cuida dos projéteis.
OCP (Aberto/Fechado): novos comportamentos são adicionados por extensão (como a variação fast_alien.py), sem modificar o código existente.
DIP (Inversão de Dependência), no exemplo desconto.py: a classe Pedido depende da abstração IDesconto (uma classe abstrata com abc.ABC) e recebe o desconto pelo construtor (injeção de dependência). Implementações concretas (DescontoNormal, DescontoVIP, DescontoPremium) podem ser trocadas sem alterar o Pedido.

Aprendizado: SOLID não é uma lista de regras a decorar. Cada princípio resolve um problema concreto de manutenção. E um código bem desenhado é, como consequência, mais fácil de testar, como as seções seguintes mostram.

4. Testes automatizados com Pytest

Problema: depois de uma refatoração, um bug pode surgir de forma imperceptível. Por exemplo, trocar valor * 0.1 por valor * 1 não gera nenhum erro, mas quebra a regra de negócio. Testes automatizados funcionam como um cinto de segurança do código.

Características de um bom teste unitário: rápido, determinístico, isolado e repetível.

Recursos aplicados:

Recurso	Para que serve	Onde
assert	Comparar resultado esperado com resultado obtido	test_desconto.py
@pytest.fixture	Preparar objetos e ambiente antes do teste, sem duplicação	test_desconto.py, test_ship.py
@pytest.mark.parametrize	Executar o mesmo teste com vários conjuntos de dados	test_desconto.py
pytest.ini	Configurar o Pytest (pythonpath = .)	raiz do projeto

Por que o pytest.ini? Por padrão, o Pytest adiciona ao sys.path a pasta do arquivo de teste (tests/), e não a raiz do projeto. Sem a linha pythonpath = ., o import from src.desconto import ... falha com ModuleNotFoundError.

Aprendizado sobre a saída do Pytest:

ERROR: o teste nem chegou a rodar (problema de import, coleta ou ambiente).
FAILED: o teste rodou e o assert encontrou um comportamento diferente do esperado.
5. Dublês de teste: stubs e mocks

Problema: classes dependem de outros componentes (banco de dados, APIs, a tela do Pygame). Usar as dependências reais deixa o teste lento, difícil de reproduzir e dependente de ambiente.

Dublês de teste substituem essas dependências durante o teste:

	Stub	Mock
Função	Devolve respostas controladas	Devolve respostas e registra como foi usado
Verifica	O resultado	A interação (se foi chamado, quantas vezes, com quais argumentos)
Exemplo no projeto	StubSemDesconto, StubSettings	mocker.Mock() (via pytest-mock)

Aplicações:

Pedido com stub: um desconto que sempre retorna 0 permite verificar que Pedido.total(100) == 100, isolando a lógica do Pedido.
Pedido com mock: além do resultado, verifica-se que calcular foi chamado uma única vez e com o argumento 100 (assert_called_once_with).
Ship com stub: StubSettings fixa a velocidade da nave, permitindo verificar exatamente quanto ela se moveu, sem depender do settings.py real.
Ship com mock: a tela do Pygame é substituída por um mock (com get_rect retornando um pygame.Rect real). Assim, o teste não abre nenhuma janela e verifica que blitme() chama screen.blit(ship.image, ship.rect).

Aprendizados:

Regra prática: se o método devolve um valor ou altera estado, verifique o resultado (stub). Se o efeito do método é chamar uma dependência, verifique a interação (mock).
O que define se um dublê é stub ou mock é como o teste o usa, e não a biblioteca que o criou.
A injeção de dependência (Pedido(desconto), Ship(screen, settings)) é o que torna essas substituições simples. Design e testabilidade andam juntos.
6. Relatórios e cobertura de testes
pytest-html: gera um relatório visual da execução (relatorio.html). A opção --self-contained-html embute o CSS no próprio arquivo.
Coverage.py: mede quais linhas do código foram executadas pelos testes.
# pragma: no cover: exclui da medição trechos que não fazem sentido testar, como o bloco if __name__ == "__main__":.
Relatórios gerados (relatorio.html, htmlcov/, .coverage) são artefatos e ficam no .gitignore.

Aprendizado: cobertura mede execução, não qualidade. Um teste sem assert pode atingir 100% de cobertura sem verificar nada. Além disso, sem --source=src, o relatório inclui os próprios arquivos de teste e ignora módulos que nunca foram importados, o que produz um número otimista demais. Cobertura serve para encontrar o que não está testado, não como troféu.

Defeitos encontrados e corrigidos

Os testes revelaram defeitos que estavam no histórico sem ninguém perceber:

Defeito	Como foi detectado	Correção
Criação duplicada de aliens em create_fleet	Execução do jogo	fix: remove criação duplicada de aliens no 'create_fleet'
class IDesconto(abc): herança de um módulo em vez de uma classe, gerando TypeError: module() takes at most 2 arguments	Coleta do Pytest (ao importar o arquivo)	abc → abc.ABC
Nome da classe DescontoVIP escrito errado	ImportError na coleta	Correção do nome
StubSettings usado nos testes, mas ausente em tests/doubles.py	Execução dos testes após o merge	Inclusão da classe no arquivo de dublês

A lição: testes obrigam o código a ser executado. Vários desses erros existiam porque aquele código simplesmente nunca tinha rodado.

Lições de ambiente e ferramentas

Nem todo problema é de código. Vários dos obstáculos enfrentados foram de ambiente, e diagnosticá-los seguiu sempre o fluxo sintoma → hipótese → evidência → correção → prevenção:

Sintoma	Causa	Lição
Fatal error in launcher ao rodar pip	O ambiente virtual foi criado em outro caminho e depois a pasta foi movida/renomeada	Ambientes virtuais não são portáteis: recrie-os a partir do arquivo de dependências e prefira python -m pip
A pasta não está vazia ao apagar o .venv	O OneDrive bloqueou a exclusão em massa e pediu confirmação	Pastas sincronizadas interagem com ferramentas de desenvolvimento
git diff exibindo Binary files differ para um .txt	O operador > do Windows PowerShell 5.1 grava em UTF-16, e o Git trata bytes nulos como binário	Verificar a codificação. Arquivos de texto devem ser UTF-8
Tamanho do arquivo diferente no disco e no repositório	core.autocrlf=true: o repositório guarda LF, o Windows usa CRLF	Entender a normalização de quebras de linha
Conflito no .gitignore ao integrar develop em main	As duas branches alteraram o mesmo trecho	Ler os dois lados, decidir e verificar com git show
Como executar

Pré-requisito: Python 3.11.

powershell
# 1. Criar e ativar o ambiente virtual (Windows / PowerShell)
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 2. Instalar as dependências
python -m pip install -r requiriments.txt

# 3. Executar o jogo (a partir da raiz do projeto)
python src/alien_invasion_refactored.py

O jogo deve ser executado a partir da raiz do repositório, porque as imagens são carregadas por caminho relativo (./images/...).

Testes:

powershell
pytest -v                                        # executa todos os testes
pytest --html=relatorio.html --self-contained-html   # relatório HTML
coverage run --source=src -m pytest              # coleta a cobertura do código de src/
coverage report -m                               # tabela com as linhas não cobertas
coverage html                                    # relatório navegável em htmlcov/
Dívida técnica conhecida

Pontos identificados e registrados conscientemente, que ficaram para trabalhos futuros:

Caminho da imagem da nave relativo ao diretório de execução (./images/ship.bmp). O ideal seria montá-lo a partir do arquivo com pathlib (Path(__file__).resolve().parent.parent / "images"), tornando o jogo e os testes independentes do diretório atual.
Cobertura incompleta da nave: faltam testes do movimento para a esquerda e do limite da tela.
.gitignore com regras duplicadas (htmlcov/htmlcov/, .sqlite3/*.sqlite3, variações de relatorio.html).
Detalhes de estilo: falta de linha em branco final e espaçamento PEP 8 em tests/doubles.py, e o nome de teste test_desconto__vip_100.
Nome do arquivo de dependências: requiriments.txt deveria ser requirements.txt, o nome padrão esperado por ferramentas.
Comentários históricos no código (por exemplo, em ship.py), cujo contexto pertence às mensagens de commit, e não ao código-fonte.
Tecnologias
Ferramenta	Versão	Uso
Python	3.11	Linguagem
pygame	2.6.1	Motor do jogo
pytest	9.1.1	Testes automatizados
pytest-mock	(ver requiriments.txt)	Mocks via fixture mocker
pytest-html	(ver requiriments.txt)	Relatório HTML dos testes
coverage	(ver requiriments.txt)	Cobertura de testes
mypy	2.3.0	Verificação estática de tipos
ruff	0.16.2	Linter / estilo
MonkeyType	23.3.0	Geração de type hints a partir da execução
Git + GitHub	—	Versionamento, Git Flow e Pull Requests
Licença

Distribuído sob a licença MIT. Veja o arquivo LICENSE.

Desenvolvido por Prietto (@PriettoDev) como parte da disciplina Alta Qualidade em Software, Universidade SENAI CIMATEC.
