# Tiny Death Star

## Membros do grupo

- Isabel Heckmann
- José Eduardo Terras Mello
- Maria Luíza Tebaldi Franco

## Descrição do projeto

Este projeto é uma versão inspirada no jogo **Star Wars: Tiny Death Star**, criado para o trabalho de Pygame da disciplina de Design de Software
O Tiny Death Star original era baseado no jogo **Tiny Tower**, lançado pela NimbleBit em 2011. No Tiny Tower, o objetivo é construir andares em uma torre, receber moradores e administrar os negócios. Em 2013, a NimbleBit trabalhou com a Disney para criar uma versão com o tema de Star Wars, trocando a torre pela Estrela da Morte e incluindo personagens da saga.

O "Star Wars: Tiny Death Star" original foi lançado em novembro de 2013. Em outubro de 2014, a Disney retirou o jogo das lojas digitais, como a App Store e o Google Play. Os motivos divulgados foram ligados à decisão da empresa de seguir o universo de Star Wars em outra direção.

Essa versão em Pygame é um projeto feito pelo grupo e não é uma cópia oficial do jogo original. Nós usamos a ideia como inspiração e criamos uma versão mais simples, com menu, elevador, personagens, andares comerciais e sistema de moedas.

No jogo, o jogador pode construir novos andares e levar visitantes até o andar indicado pelo balão acima do elevador. Quando o visitante chega ao destino correto, ele passa a circular pelo andar e pode consumir produtos. A partir daí, o jogador recebe créditos. A versão atual também possui um andar comercial com Blue Milk, Womp Rat Stew e Dustcrepe.

Recursos presentes no projeto:

- Menu principal com opções para iniciar, ver as instruções, mudar as configurações e sair;
- Som de fundo e opção para ligar ou desligar o som;
- Português e inglês;
- Elevador controlado pelo mouse ou pelas setas do teclado;
- Personagens conhecidos e inspirados em Star Wars;
- Construção de novos andares;
- Andar comercial com produtos e estoque;
- Andar residencial;
- Moedas e Imperial Bux;
- Animação dos personagens.

## Tecnologias utilizadas

- Python;
- Pygame ou Pygame Community Edition;
- Imagens, fontes e áudio da pasta `tiny-death-star`.

## Instalação

É necessário ter o Python instalado no computador. Depois, abra o terminal na pasta do projeto e instale o Pygame Community Edition:

```powershell
python -m pip install pygame-ce
```

Caso prefira, também pode ser usada a versão padrão do Pygame:

```powershell
python -m pip install pygame
```

## Como executar

Para abrir o jogo no Windows, abra o terminal na pasta do projeto e execute:

```powershell
python pygame-tinydeathstar.py
```

Para abrir o jogo em inglês:

```powershell
python .\pygame-tinydeathstar.py --en
```

Caso não seja usada a opção `--en`, o jogo começa em português.

## Controles

- **Mouse:** navegar no menu, clicar nos botões e nos andares;
- **Seta para cima:** subir o elevador;
- **Seta para baixo:** descer o elevador;
- **M:** ativar ou desativar o som;
- **Fechar a janela:** encerrar o jogo.

Na tela do jogo, clique em `ADD LEVEL` para construir um andar, desde que haja moedas suficientes. Para controlar o andar comercial, clique nele e faça os pedidos ou use o Imperial Bux para acelerar a produção. Cada visitante mostra o número do andar de destino em um balão acima do elevador.

## Vídeo de apresentação

Vídeo curto mostrando o jogo funcionando:

https://youtu.be/KWjUATp5dRs


## Referências sobre os jogos originais

- [Página sobre o Tiny Tower](https://en.wikipedia.org/wiki/Tiny_Tower)
- [Página sobre o Star Wars: Tiny Death Star](https://en.wikipedia.org/wiki/Star_Wars:_Tiny_Death_Star)
- [Anúncio do jogo pelo IGN](https://www.ign.com/articles/2013/10/04/tiny-death-star-announced)
- [Notícia de lançamento pelo GameSpot](https://www.gamespot.com/articles/star-wars-tiny-death-star-is-available-now-for-free/1100-6416041/)
- [Cobertura do anúncio pela Variety](https://variety.com/2013/digital/news/disney-lucasarts-to-launch-star-wars-tiny-death-star-with-tiny-tower-creator-nimblebit-1200694453/)
- [Uma versão inspirada no jogo original no itch.io](https://ammoled.itch.io/tds64)

## Uso de Inteligência Artificial

A Inteligência Artificial foi utilizada como ferramenta de apoio técnico para acelerar etapas repetitivas e ajustes visuais, enquanto a arquitetura, as regras de negócio e a implementação principal foram conduzidas pela equipe:

- *Estruturação de catálogos e dados:* Organização de dicionários extensos em Python para associar os cenários carregados dos PNGs às suas respectivas categorias (Residential, Food, Service, Recreation e Retail), produtos, estoques máximos e tempos de preparo.
- *Coordenadas e layout de interface (UI):* Definição de posições em pixels, dimensões de componentes (pygame.Rect), escalonamento de sprites e cálculos de rolagem vertical (scroll_y).
- *Desenho procedural no Pygame:* Criação de funções auxiliares com primitivas gráficas (pygame.draw) para botões interativos, barras de habilidades, ícones minimalistas e indicadores de estoque.
- *Depuração pontual:* Apoio na revisão de indentação, ordenação de eventos de clique (MOUSEBUTTONDOWN) e controle de estados entre telas e painéis.