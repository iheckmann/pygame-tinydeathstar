#Evidências de Uso de Inteligência Artificial

Esse documento registra os principais prompts utilizados durante o desenvolvimento do projeto e como as orientações obtidas foram adaptadas pela equipe.

---

## Registro de Prompts e Aplicações

### 1. Estruturação de Catálogos e Dados Repetitivos
* **Objetivo:** Organizar todos os cenários já carregados por categoria (*Residential*, *Food*, *Service*, *Recreation* e *Retail*), associando produtos, estoques máximos e tempos de preparo, além de automatizar o carregamento de ícones (`Icon_*.png`).
* **Prompt utilizado:**
  > *"Tenho todos os meus cenários carregados nas pastas por categoria e os ícones no formato `Icon_Nome_Do_Item.png`. Como posso estruturar um catálogo em dicionário e carregar os ícones automaticamente sem precisar mapear um por um?"*
* **Como foi aplicado:** Criação do dicionário `CATALOGO_ANDARES` e da função auxiliar `carregar_icone_produto()`, conectando os arquivos gráficos já existentes no projeto à construção dinâmica de novos andares.

---

### 2. Cálculos de Pixels, Layout e Desenho Procedural (UI)
* **Objetivo:** Ajustar dimensões de painéis, alinhar elementos na tela (`800x600`), evitar vazamento de textos nas caixas e desenhar detalhes visuais com primitivas gráficas.
* **Prompt utilizado:**
  > *"Como ajustar a altura do painel azul para não sobrar espaço vazio embaixo, evitar que os textos saiam das caixas, desenhar moedas e relógios minimalistas e fazer o botão X mudar de cor no hover e no clique?"*
* **Como foi aplicado:** Redimensionamento dos `pygame.Rect` dos painéis (`406px` de altura), criação da fonte secundária `fonte_painel` para textos internos e implementação das funções `desenhar_moeda_mini()` e `desenhar_botao_fechar()`.

---

### 3. Sistema de Moradores, Atributos e Contratação
* **Objetivo:** Permitir clicar em um andar residencial, visualizar a ficha do *Bitizen* (emprego atual, emprego dos sonhos e barras de habilidades) e contratá-lo em estabelecimentos abertos.
* **Prompt utilizado:**
  > *"Como fazer com que ao clicar no andar residencial apareça a lista de moradores, e ao clicar em um bitizen abra a ficha dele com habilidades coerentes ao emprego dos sonhos e botão para escolher onde trabalhar?"*
* **Como foi aplicado:** Implementação do fluxo de estados entre painéis (`andar_aberto` --> `morador_selecionado` --> `escolhendo_emprego`) e da função `gerar_dream_job_e_skills()` para vincular a maior habilidade à categoria do *Dream Job*.

---

### 4. Rolagem Vertical da Torre (`scroll_y`) e Elevador Automático
* **Objetivo:** Permitir a construção de múltiplos andares acima do limite inicial da tela com rolagem via *trackpad*/mouse, acompanhando o movimento do elevador e retornando-o automaticamente ao térreo após o desembarque.
* **Prompt utilizado:**
  > *"Como implementar o scroll vertical da torre para construir mais andares além do topo da tela e fazer o elevador descer automaticamente para o Andar 1 depois que o passageiro desembarca?"*
* **Como foi aplicado:** Adição da variável de deslocamento `scroll_y` integrada ao evento `pygame.MOUSEWHEEL`, ajuste das coordenadas de clique/renderização da torre e controle de estado `voltando_elevador` no loop de movimento.

---

### 5. Depuração Pontual de Eventos e Estados
* **Objetivo:** Corrigir conflitos de ordem de cliques (`MOUSEBUTTONDOWN`), loop de desembarque no térreo e sincronização de idiomas (`PT`/`EN`).
* **Prompt utilizado:**
  > *"Quando clico para escolher o local de trabalho do morador o clique não registra, e quando o elevador desembarca no Andar 1 ele fica gerando passageiros sem parar. Onde está o conflito na ordem dos eventos?"*
* **Como foi aplicado:** Reordenação da cadeia `if / elif` no tratamento de cliques (priorizando subpainéis ativos antes dos painéis base) e inclusão de travas de estado (`ja_moveu_elevador` e `elevador_y < 425.0`) no desembarque.

---

### 6. Bloqueio de Andares Fechados (`CLOSED`) e Validação de Estoque
* **Objetivo:** Impedir que visitantes do elevador peçam para ir a estabelecimentos sem funcionários e bloquear encomendas de produtos enquanto o andar estiver fechado.
* **Prompt utilizado:**
  > *"Mesmo com o andar marcado como `CLOSED`, ainda é possível clicar para estocar itens e os passageiros continuam pedindo esse andar no elevador. Como bloquear essas ações até que um morador seja contratado?"*
* **Como foi aplicado:** Criação da função `sortear_andar_aberto()` para filtrar estabelecimentos com `0` trabalhadores no sorteio de destino e adição de trava visual e funcional (`HIRE WORKER FIRST`) nos cartões sem funcionário.

---

### 7. Cálculo Dinâmico de Habilidade Total (`Total Skill`) e Rank
* **Objetivo:** Substituir os valores fixos do rodapé dos estabelecimentos pela soma real das habilidades dos trabalhadores contratados na categoria correspondente.
* **Prompt utilizado:**
  > *"Como calcular o `Total Skill` dinamicamente no rodapé do painel comercial com base na habilidade específica de cada bitizen contratado naquela categoria?"*
* **Como foi aplicado:** Uso de expressão geradora `sum(t["skills"][cat] for t in andar_sel["trabalhadores"])` vinculada à categoria do andar (`food`, `service`, `recreation`, `retail`).

---

### 8. Menu de Seleção de Categoria ao Construir Novo Andar (`ADD LEVEL`)
* **Objetivo:** Permitir que o jogador escolha qual tipo de andar deseja construir (*Residential*, *Food*, *Service*, *Recreation* ou *Retail*) ao clicar em `ADD LEVEL`, sorteando uma opção ainda não construída.
* **Prompt utilizado:**
  > *"Ao clicar em `ADD LEVEL`, quero que abra um painel para eu escolher qual categoria de andar construir, sorteando um andar daquela categoria que ainda não esteja na minha torre."*
* **Como foi aplicado:** Implementação do estado `escolhendo_novo_andar`, renderização dos 5 botões coloridos por categoria (`OPCOES_CONSTRUCAO`) e filtro de andares inéditos antes da adição à lista `andares`.

---

### 9. Suporte Bilíngue Dinâmico (`PT` / `EN`) na Interface do Jogo
* **Objetivo:** Garantir que todos os textos internos dos painéis, botões de estoque, fichas de moradores e avisos de status acompanhem o idioma escolhido nas configurações.
* **Prompt utilizado:**
  > *"Os textos dentro dos painéis do jogo ficaram fixos em português. Como fazer toda a interface dos andares e fichas obedecerem à variável `LINGUAGEM` (`pt` ou `en`)?"*
* **Como foi aplicado:** Criação do dicionário `UI_JOGO` mapeando todas as chaves de texto em português e inglês, consumido dinamicamente na renderização dos painéis (`ui = UI_JOGO[LINGUAGEM]`).

---

### 10. Controle de Fluxo e Descongestionamento de Visitantes nos Andares
* **Objetivo:** Evitar acúmulo excessivo de sprites nos andares ao longo do tempo, mantendo apenas os moradores fixos e fazendo visitantes temporários irem embora após passearem.
* **Prompt utilizado:**
  > *"Os personagens estão acumulando nos andares e deixando o cenário congestionado. Como fazer com que visitantes que não moram no andar caminhem por alguns segundos e depois saiam pelo elevador?"*
* **Como foi aplicado:** Adição das propriedades `morador_aqui` e `tempo_vida` nos objetos de `clientes_no_andar`, alternando o estado para `"saindo"` quando o contador expira.

