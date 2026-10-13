# Castle Defenders

## Integrantes do grupo

- Álvaro Barbosa Ferreira Silva
- Enzo Gentil Xavier Barroso
- Rafael Gomes Antunes De Oliveira
- João Mario Paes de Abreu

## Estrutura do projeto

- `main.py`: ponto de entrada da aplicação.
- `src/`: código-fonte principal do jogo (loop, regras, sprites e dados).
- `assets/`: imagens, fontes e sons.
- `data/`: arquivos persistentes (recorde/ranking).
- `tests/`: testes unitários com `pytest`.
- `docs/`: documentação do projeto, incluindo proposta inicial.

## Descrição do jogo

> O jogo consiste em defender uma torre de inimigos, juntar moedas ao derrotá-los e gastá-las em melhorias. A partida termina quando a vida da torre chega em 0.

## Objetivo do jogador


> Para avançar no jogo o jogador deve derrotar os chefões que aparecem periodicamente, o que aumenta o nível de dificuldade. O objetivo é chegar na maior dificuldade possível.

## Regras do jogo

- O jogador ataca no local onde clica com o mouse.
- Cada inimigo aumenta a quantidade de moedas ao derrotado.
- Inimigos atacam a torre e tiram sua vida ao entrar em contato com ela.
- O inimigo "Cultista" ataca a torre periodicamente e não para até ser derrotado.
- O inimigo "Coxinha" começa a surgir a partir do nível 3 e explode ao chegar na torre, causando alto dano e se auto-derrotando.
- Os bosses são versões dos inimigos maiores e mais fortes que aparecem a cada 30 segundos. Ao derrotar um boss, a vida da torre se cura um pouco, o jogador recebe moedas a mais o nível de dificuldade aumenta.
- A cada aumento no nível de dificuldade os inimigos ficam mais rápidos, causam mais dano e tem mais vida.
- Com as moedas acumuladas ao derrotar inimigos e bosses, podem ser feitas melhorias de: dano do ataque, raio do ataque, vida da torre e o desbloqueio de uma habilidade de fazer "combos" (cada clique que acerta um inimigo acumula combo e aumenta o dano, errar um clique reseta o combo para 0).
- Quando a vida da torre chega a 0, o jogador deve recomeçar do início do nível em que estava ou pode escolher começar um novo jogo.

## Controles

- Posição do cursor para determinar o local de ataque.
- Botão esquerdo do mouse para atacar.
- Tecla U para abrir o menu de melhorias.

## Como executar o projeto

### 1. Clonar o repositório

```bash
git clone https://github.com/rafaelgomes77oliveira-ux/Pygame-Castle-Defenders
cd Pygame-Castle-Defenders
pip install -r requirements.txt
python main.py
```

## Como executar os testes

```bash
python -m pytest
```

## Checklist mínimo para entrega

- Preencher este README com nome final, descrição real, regras e controles do jogo.
- Atualizar `docs/proposta.MD` com a proposta do grupo.
- Garantir que o jogo executa com `python main.py`.
- Garantir que os testes passam com `pytest`.

## Observações para os alunos

- Mantenham o código organizado em módulos pequenos e com responsabilidade clara.
- Comentem partes importantes da lógica, principalmente regras do jogo.
- Registrem decisões técnicas no README do grupo ao longo do desenvolvimento.
