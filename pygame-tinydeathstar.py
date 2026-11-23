import os
import sys
import random
import pygame

pygame.init()
pygame.mixer.init()

#Setup
#LÍNGUAGEM: português ou inglês. O padrão é português.
LINGUAGEM = "en" if "--en" in sys.argv else "pt"  #ou "inglês"

#CORES (obtidas de: https://inventwithpython.com/blog/complete-list-tkinter-colors-valid-and-tested.html)
PRETO = (0, 0, 0)  #Preto
BRANCO = (255, 255, 255)  #Branco
AMARELO_TITULO = (255, 215, 0)  #Amarelo para o texto inicial ("TINY DEATH STAR")
GALAXIA_COR = (10, 10, 25)  #Azul escuro do espaço
DEATH_STAR_CINZA = (160, 160, 160)  #Cinza para a Estrela da Morte
TRENCH_CINZA = (110, 110, 110)  #Cinza mais escuro para o trench
DISH_CINZA = (130, 130, 130)  #Cinza para o prato do superlaser (olho da Estrela da Morte) 
TIE_CINZA = (170, 175, 185) #Cinza tie fighter
TIE_ESCURO = (70, 75, 85) #Escuro tie fighter 

#JANELA:
JANELA_LARGURA = 800
JANELA_ALTURA = 600
screen = pygame.display.set_mode((JANELA_LARGURA, JANELA_ALTURA))
pygame.display.set_caption("Tiny Death Star")  #Título da janela

#MÚSICA DE FUNDO:
pygame.mixer.music.load("tiny-death-star/music/Tiny-Death-Star_Main-Star-Wars-Theme.mp3")
pygame.mixer.music.play(-1)  #Reproduzir em loop (pygame.mixer.music.stop() para parar a música)

#FONTES:
fonte_titulo = pygame.font.Font("tiny-death-star/fontes/star_jedi/starjedi/Starjedi.ttf", 75)

#fonte cheia junto com a oca
fonte_sw_cheia = pygame.font.Font("tiny-death-star/fontes/star_jedi/starjedi/Starjedi.ttf", 26)
fonte_sw_oca = pygame.font.Font("tiny-death-star/fontes/star_jedi/starjedi/Starjhol.ttf", 26)

caixa_rect = pygame.Rect(225, 115, 350, 255)

def criar_logo_sw(texto): #ajuda de IA
    fundo = fonte_sw_cheia.render(texto, False, (18, 20, 30))
    frente = fonte_sw_oca.render(texto, False, AMARELO_TITULO)

    w, h = fundo.get_size()
    surf = pygame.Surface((w + 6, h + 6), pygame.SRCALPHA)
    for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2), (-2, -2), (2, 2), (-2, 2), (2, -2)]:
        surf.blit(fundo, (3 + dx, 3 + dy))
    surf.blit(fundo, (3, 3))
    surf.blit(frente, (3, 3))
    return surf

txt_star = criar_logo_sw("star")
txt_wars = criar_logo_sw("wars")

star_rect = txt_star.get_rect(midleft=(caixa_rect.left + 20, caixa_rect.top - 11))
wars_rect = txt_wars.get_rect(midright=(caixa_rect.right - 20, caixa_rect.bottom + 6))


def pixelar_surface(surf, fator=4):
    w, h = surf.get_size()
    peq = pygame.transform.scale(surf, (max(1, w // fator), max(1, h // fator)))
    return pygame.transform.scale(peq, (w, h))

def renderizar_texto_pixelado(texto, fonte, cor_frente, cor_sombra, fator=4):
    frente = pixelar_surface(fonte.render(texto, False, cor_frente), fator)
    sombra = pixelar_surface(fonte.render(texto, False, cor_sombra), fator)
    borda = pixelar_surface(fonte.render(texto, False, (15, 15, 25)), fator)

    final = pygame.Surface((frente.get_width() + 12, frente.get_height() + 14), pygame.SRCALPHA)
    for dx, dy in [(-4, 0), (4, 0), (0, -4), (0, 4), (-4, 6), (4, 6), (0, 10)]:
        final.blit(borda, (4 + dx, 4 + dy))
    final.blit(sombra, (4, 9))
    final.blit(frente, (4, 4))
    return final

#Desenhar death star (ajuda de IA para desenhar o Death Star pixelado)
def criar_death_star(raio=36, bloco=6):
    tam = (raio * 2 + 1) * bloco
    surf = pygame.Surface((tam, tam), pygame.SRCALPHA)
    centro = raio * bloco

    C_BRILHO = (195, 198, 205)
    C_CLARO  = (155, 158, 166)
    C_MEDIO  = (110, 114, 122)
    C_ESCURO = (65, 68, 76)
    C_SOMBRA = (32, 35, 44)

    prato_x, prato_y = -13, -14

    
    for y in range(-raio, raio + 1):
        for x in range(-raio, raio + 1):
            dist = (x**2 + y**2) ** 0.5
            if dist <= raio:
                dist_luz = ((x + 16)**2 + (y + 16)**2) ** 0.5

                if dist > raio - 1.5 or dist_luz > 52:
                    cor = C_SOMBRA
                elif dist_luz > 40:
                    cor = C_ESCURO
                elif dist_luz > 27:
                    cor = C_MEDIO
                elif dist_luz > 14:
                    cor = C_CLARO
                else:
                    cor = C_BRILHO

                if y in (-24, -15, -7, 8, 16, 25) and cor != C_SOMBRA:
                    cor = C_ESCURO if cor in (C_MEDIO, C_CLARO) else C_MEDIO

                if y in (0, 1):
                    cor = C_SOMBRA

                dist_prato = ((x - prato_x)**2 + (y - prato_y)**2) ** 0.5
                if dist_prato <= 9.5:
                    if dist_prato > 8:
                        cor = C_SOMBRA
                    elif dist_prato > 2.5:
                        cor = C_ESCURO
                    else:
                        cor = C_MEDIO

                if (x, y) in [(-22, 5), (-16, 12), (-25, -4), (6, -20), (-8, 20)]:
                    cor = BRANCO

                rect = pygame.Rect(centro + x * bloco, centro + y * bloco, bloco, bloco)
                pygame.draw.rect(surf, cor, rect)
    return surf

death_star_img = criar_death_star(raio=36, bloco=6)
death_star_rect = death_star_img.get_rect(center=(400, 230))

#Título Principal ("tiny", "death", "star")
titulo = [
    (renderizar_texto_pixelado("tiny", fonte_titulo, (255, 220, 40), (175, 70, 0), fator=4), 102),
    (renderizar_texto_pixelado("death", fonte_titulo, (255, 220, 40), (195, 110, 0), fator=4), 172),
    (renderizar_texto_pixelado("star", fonte_titulo, (255, 220, 40), (195, 110, 0), fator=4), 242)
]

#BOTÕES (para o menu principal):
tela_atual = "menu"  #ou "menu", "como_jogar", "configuracoes", "jogo"
botao_voltar = pygame.Rect(300, 480, 200, 38)

#FONTES
fonte_botao = pygame.font.Font("tiny-death-star/fontes/star_jedi/starjedi/Starjedi.ttf", 14)
fonte_titulo_painel = pygame.font.Font("tiny-death-star/fontes/star_jedi/starjedi/Starjedi.ttf", 26)
fonte_instrucoes = pygame.font.SysFont("avenir", 20, bold=True)
fonte_painel = pygame.font.SysFont("avenir", 14, bold=True)


#som
som_ativo = True 

TEXTOS = {
    "pt": {
        "iniciar": "i n i c i a r",
        "como_jogar": "c o m o   j o g a r",
        "configuracoes": "c o n f i g u r a ç õ e s",
        "sair": "s a i r",
        "voltar": "v o l t a r",
        "som_on": "s o m :   l i g a d o   ( m )",
        "som_off": "s o m :   m u d o   ( m )",
        "idioma": "i d i o m a :   p o r t u g u ê s",
        "titulo_como": "c o m o   j o g a r",
        "regras": [
            "1. Construa novos andares na Estrela da Morte.",
            "2. Use o elevador para levar visitantes ao andar certo.",
            "3. Colete créditos para expandir o Império!",
            "Atalho rápido: aperte M para mutar o som."
        ],
        "fechado": "fechado",
        "contratar": "+ vaga",
        "contratar_antes": "CONTRATAR ANTES",
        "encomendar": "ENCOMENDAR",
        "finalizar_bux": "1 BUX P/ TERMINAR",
        "estocado": "ESTOCADO",
        "habilidade": "Habilidade Total",
        "emprego": "EMPREGO:",
        "desempregado": "DESEMPREGADO",
        "emp_atual": "Emprego Atual:",
        "emp_sonho": "Emprego dos Sonhos:",
        "botao_emprego": "EMPREGO",
        "botao_expulsar": "EXPULSAR",
        "escolher_local": "ESCOLHA O LOCAL DE TRABALHO"
    },
    "en": {
        "iniciar": "s t a r t",
        "como_jogar": "h o w   t o   p l a y",
        "configuracoes": "s e t t i n g s",
        "sair": "q u i t",
        "voltar": "b a c k",
        "som_on": "s o u n d :   o n   ( m )",
        "som_off": "s o u n d :   m u t e d   ( m )",
        "idioma": "l a n g u a g e :   e n g l i s h",
        "titulo_como": "h o w   t o   p l a y",
        "regras": [
            "1. Build new floors inside the Death Star.",
            "2. Use the elevator to take visitors to their floor.",
            "3. Collect credits to expand the Empire!",
            "Quick shortcut: press M to mute sound."
        ],
        "fechado": "closed",
        "contratar": "+ hire",
        "contratar_antes": "HIRE WORKER FIRST",
        "encomendar": "PLACE ORDER",
        "finalizar_bux": "1 BUX TO FINISH",
        "estocado": "STOCKED",
        "habilidade": "Total Skill",
        "emprego": "JOB:",
        "desempregado": "UNEMPLOYED",
        "emp_atual": "Current Job:",
        "emp_sonho": "Dream Job:",
        "botao_emprego": "JOB",
        "botao_expulsar": "EVICT",
        "escolher_local": "SELECT WORKPLACE"
    }
    
}

NOMES_STAR_WARS = ["Rugor Medon", "Jango Nu", "Rom Ollie", "Adas Pavan", "Tyber Colton", "Kaye Tharen", "Dax Antilles", "Vek Solis"]
morador_selecionado = None   #Guarda o morador clicado para abrir a ficha respectiva dele
escolhendo_emprego = False   #True quando clicar em JOB na ficha do morador

botao_som = pygame.Rect(210, 230, 380, 42)
botao_idioma = pygame.Rect(210, 290, 380, 42)

def alternar_som():
    global som_ativo
    som_ativo = not som_ativo
    if som_ativo:
        pygame.mixer.music.unpause()
    else:
        pygame.mixer.music.pause()

botoes_menu = [
    ("iniciar", pygame.Rect(280, 410, 240, 36)),
    ("como_jogar", pygame.Rect(280, 454, 240, 36)),
    ("configuracoes", pygame.Rect(280, 498, 240, 36)),
    ("sair", pygame.Rect(280, 542, 240, 36))
]

def carregar_personagem(caminho, escala=2):
    img = pygame.image.load(caminho).convert_alpha()
    
    # Recorta as sobras transparentes em volta para o pé encostar certinho no chão
    rect_recorte = img.get_bounding_rect()
    img = img.subsurface(rect_recorte).copy()

    w, h = img.get_size()
    return pygame.transform.scale(img, (w * escala, h * escala))


#PERSONAGENS
#rebels
luke = carregar_personagem("tiny-death-star/characters/men-of-the-rebellion/Luke_Skywalker.png", escala = 2)
leia = carregar_personagem("tiny-death-star/characters/ladies-of-the-rebellion/Leia_Organa_Rebel.png", escala = 2)
han_solo = carregar_personagem("tiny-death-star/characters/men-of-the-rebellion/Han_Solo.png", escala = 2)
chewbacca = carregar_personagem("tiny-death-star/characters/rebel-heroes/Chewbacca.png", escala=2)

#droids
c3po = carregar_personagem("tiny-death-star/characters/droids/C-3PO.png", escala = 1.8)
r2d2 = carregar_personagem("tiny-death-star/characters/droids/R2-D2.png", escala = 1.8)

#imperial
vader = carregar_personagem("tiny-death-star/characters/the-force/Darth_Vader.png", escala=1.8)
stormtrooper = carregar_personagem("tiny-death-star/characters/troops/Stormtrooper.png", escala=2)
palpatine = carregar_personagem("tiny-death-star/characters/the-force/Emperor_Palpatine.png", escala=1.8)
tarkin = carregar_personagem("tiny-death-star/characters/limited-edition/Grand_Moff_Tarkin.png", escala=2)
greedo = carregar_personagem("tiny-death-star/characters/bounty-hunters/Greedo.png", escala=1.6)
guard = carregar_personagem("tiny-death-star/characters/troops/Royal_Gaurd.png", escala=1.7)

#ESTRELAS (fundo):
estrelas = []
for _ in range(150):
    x = random.randint(0, 800)
    y = random.randint(0, 515) #para no chão cinza (y = 520)
    tam = random.choice([2,3])
    brilho = random.randint(120,255)
    estrelas.append([x, y, tam, brilho])

#NAVES (fundo):
def tie_fighter(tam_px=3):
    surf = pygame.Surface((9 * tam_px, 7 * tam_px), pygame.SRCALPHA)
    #asas + cabine
    for x in (0, 8):
        pygame.draw.rect(surf, TIE_CINZA, (x * tam_px, 0, tam_px, 7 * tam_px))
    pygame.draw.rect(surf, TIE_CINZA, (tam_px, 3 * tam_px, 7 * tam_px, tam_px))
    pygame.draw.rect(surf, TIE_CINZA, (3 * tam_px, 2 * tam_px, 3 * tam_px, 3 * tam_px))
    pygame.draw.rect(surf, TIE_ESCURO, (4 * tam_px, 3 * tam_px, tam_px, tam_px))
    return surf

def x_wing(tam_px=3):
    surf = pygame.Surface((11 * tam_px, 7 * tam_px), pygame.SRCALPHA)
    branco = (230, 230, 235)
    vermelho = (220, 60, 60)
    #corpo + nariz + asas
    pygame.draw.rect(surf, branco, (2 * tam_px, 3 * tam_px, 8 * tam_px, tam_px))
    pygame.draw.rect(surf, vermelho, (4 * tam_px, 3 * tam_px, 2 * tam_px, tam_px))
    pygame.draw.rect(surf, branco, (1 * tam_px, 1 * tam_px, 4 * tam_px, tam_px))
    pygame.draw.rect(surf, branco, (1 * tam_px, 5 * tam_px, 4 * tam_px, tam_px))
    pygame.draw.rect(surf, vermelho, (0, 1 * tam_px, tam_px, tam_px))
    pygame.draw.rect(surf, vermelho, (0, 5 * tam_px, tam_px, tam_px))
    return surf

tie_img = tie_fighter(tam_px=3)
xwing_img = x_wing(tam_px=3)
#lista de naves: [imagem, pos_x, pos_y, velocidade]
naves = [
    [tie_img, 100, 90, 1.3],
    [xwing_img, -120, 320, 1.5],
    [tie_img, 650, 390, 1.2],
]

#botões elevador (ajuda de IA)
#P0 do elevador (parado no Andar 1 - Arrivals) + retângulos dos botões
elevador_y = 425.0
elevador_vel = 3.5
botao_cima_rect = pygame.Rect(190, 508, 46, 44)
botao_baixo_rect = pygame.Rect(242, 508, 46, 44)

def desenhar_seta_elevador(superficie, rect, direcao, pressionado=False):
    #Moldura externa metálica cinza
    pygame.draw.rect(superficie, (35, 42, 52), rect, border_radius=6)
    pygame.draw.rect(superficie, (130, 145, 165), rect, width=3, border_radius=6)

    #Interior azul (escurece um pouco quando estiver segurando o clique)
    interno = rect.inflate(-10, -10)
    cor_azul = (25, 75, 130) if pressionado else (35, 105, 175)
    cor_borda_azul = (65, 145, 220) if pressionado else (95, 180, 250)
    pygame.draw.rect(superficie, cor_azul, interno, border_radius=4)
    pygame.draw.rect(superficie, cor_borda_azul, interno, width=2, border_radius=4)

    #Seta pixelada azul claro no centro + 2 tracinhos (igual à imagem!)
    cx, cy = interno.centerx, interno.centery
    cor_seta = (145, 215, 255)
    desloc = 2 if pressionado else 0  #Afunda 2px ao clicar

    if direcao == "cima":
        pontos = [(cx, cy - 12 + desloc), (cx - 12, cy + desloc), (cx + 12, cy + desloc)]
        pygame.draw.polygon(superficie, cor_seta, pontos)
        pygame.draw.rect(superficie, cor_seta, (cx - 6, cy + 3 + desloc, 12, 3))
        pygame.draw.rect(superficie, cor_seta, (cx - 6, cy + 8 + desloc, 12, 3))
    else:
        pontos = [(cx, cy + 12 + desloc), (cx - 12, cy + desloc), (cx + 12, cy + desloc)]
        pygame.draw.polygon(superficie, cor_seta, pontos)
        pygame.draw.rect(superficie, cor_seta, (cx - 6, cy - 6 + desloc, 12, 3))
        pygame.draw.rect(superficie, cor_seta, (cx - 6, cy - 11 + desloc, 12, 3))


#COMIDA (andares)
def carregar_cenario(caminho, largura=366, altura=121):
    img = pygame.image.load(caminho).convert_alpha()
    return pygame.transform.scale(img, (largura, altura))

cenario_mos_espa = carregar_cenario("tiny-death-star/food/Mos_Espa_Cafe.png")
#Arrivals
cenario_arrivals = carregar_cenario("tiny-death-star/scenes/Blast_Doors.png")

#Elevador:
elevador_img = pygame.image.load("tiny-death-star/elevator/Standard_Elevator.png").convert_alpha()
elevador_img = pygame.transform.scale(elevador_img, (54, 80))

moedas = 100
bux = 10

#lista com personagens
lista_passageiros = [
    (carregar_personagem("tiny-death-star/characters/men-of-the-rebellion/Luke_Skywalker.png", escala=0.6), True),
    (carregar_personagem("tiny-death-star/characters/ladies-of-the-rebellion/Leia_Organa_Rebel.png", escala=0.6), True),
    (carregar_personagem("tiny-death-star/characters/men-of-the-rebellion/Han_Solo.png", escala=0.6), True),
    (carregar_personagem("tiny-death-star/characters/droids/C-3PO.png", escala=0.6), True),
    (carregar_personagem("tiny-death-star/characters/bounty-hunters/Greedo.png", escala=0.6), False),
    (carregar_personagem("tiny-death-star/characters/rebel-heroes/Chewbacca.png", escala = 0.6), True),
    (carregar_personagem("tiny-death-star/characters/rebel-heroes/Admiral_Ackbar.png", escala = 0.6), True),
    (carregar_personagem("tiny-death-star/characters/rebel-heroes/Wicket.png", escala = 0.6), True),
    (carregar_personagem("tiny-death-star/characters/rebel-heroes/Nien_Nunb.png", escala = 0.6), True),
    (carregar_personagem("tiny-death-star/characters/bounty-hunters/Boba_Fett.png", escala = 0.6), False),
    (carregar_personagem("tiny-death-star/characters/troops/Stormtrooper.png", escala = 0.6), False),
    (carregar_personagem("tiny-death-star/characters/troops/AT-AT_Pilot.png", escala = 0.6), False),
    (carregar_personagem("tiny-death-star/characters/troops/Imperial_Gunner.png", escala = 0.6), False),
    (carregar_personagem("tiny-death-star/characters/troops/Shadowtrooper.png", escala = 0.6), False),
    (carregar_personagem("tiny-death-star/characters/troops/Snowtrooper.png", escala = 0.6), False),
    (carregar_personagem("tiny-death-star/characters/troops/Swamptrooper.png", escala = 0.6), False),
    (carregar_personagem("tiny-death-star/characters/troops/TIE_Pilot.png", escala = 0.6), False),
]

tem_passageiro = True
ja_moveu_elevador = False  #Evita errar antes mesmo de começar a subir
clientes_no_andar = []     #Lista dos personagens caminhando e comprando nos andares

#para não repetir passageiros que já estão nos andares
def sortear_passageiro_unico():
    sprites_em_uso = [c["sprite"] for c in clientes_no_andar]
    disponiveis = [p for p in lista_passageiros if p not in sprites_em_uso]
    # Se todos os personagens da lista já estiverem nos andares, libera todos de novo
    if not disponiveis:
        disponiveis = lista_passageiros
    return random.choice(disponiveis)

def sortear_andar_aberto():
    abertos = []
    for i, a in enumerate(andares):
        #Só sorteia o andar se NÃO for um comercial fechado (0 trabalhadores)
        if not (a.get("tipo") == "comercial" and len(a["trabalhadores"]) == 0):
            abertos.append(i + 1)
    return random.choice(abertos) if abertos else 1


passageiro_atual, passageiro_olha_dir = sortear_passageiro_unico()

custo_andar = 100

def carregar_icone_seguro(caminho, cor_reserva, tamanho=(40, 40)):
    if os.path.exists(caminho):
        img = pygame.image.load(caminho).convert_alpha()
        return pygame.transform.scale(img, tamanho)
    #desenha um ícone provisório caso o arquivo ainda não esteja na pasta
    surf = pygame.Surface(tamanho, pygame.SRCALPHA)
    pygame.draw.rect(surf, cor_reserva, (4, 4, tamanho[0] - 8, tamanho[1] - 8), border_radius=8)
    pygame.draw.rect(surf, BRANCO, (4, 4, tamanho[0] - 8, tamanho[1] - 8), width=2, border_radius=8)
    return surf

ico_blue_milk = carregar_icone_seguro("tiny-death-star/food/Icon_Blue_Milk.png", (70, 175, 235))
ico_womp_stew = carregar_icone_seguro("tiny-death-star/food/Icon_Womp_Rat_Stew.png", (195, 110, 60))
ico_dustcrepe = carregar_icone_seguro("tiny-death-star/food/Icon_Dustcrepe.png", (225, 185, 75))

andar_aberto = None  # Índice do andar clicado (ou None se nenhum estiver aberto)

#Lista dos andares já construídos na torre
andares = [
    {"nome": "arrivals", "tipo": "saguao", "cenario": cenario_arrivals, "cor_titulo": BRANCO},
    {
        "nome": "mos espa cafe",
        "tipo": "comercial",
        "categoria": "food",
        "rank": 1,
        "cenario": cenario_mos_espa,
        "cor_titulo": (130, 235, 110),
        "trabalhadores": [],  #Máximo de 3 funcionários (1 por produto)
        "produtos": [
            {"nome": "blue milk", "icone": ico_blue_milk, "estoque": 0, "max": 10, "tempo": 0, "duracao": 180},
            {"nome": "womp rat stew", "icone": ico_womp_stew, "estoque": 0, "max": 100, "tempo": 0, "duracao": 360},
            {"nome": "dustcrepe", "icone": ico_dustcrepe, "estoque": 0, "max": 300, "tempo": 0, "duracao": 600},
        ]
    },
]

novos_andares_disponiveis = [
    {
        "nome": "christophsis apts",
        "tipo": "residencial",
        "cenario": cenario_arrivals,  #Troque pelo PNG residencial quando quiser
        "cor_titulo": (130, 200, 255),
        "moradores": []  #Máximo de 5 bitizens morando aqui!
    },
]


andar_destino = sortear_andar_aberto()

#Verifica clique nos botoes azuis ou setas do teclado(cima/baixo) para subir/descender o elevador
clicando = pygame.mouse.get_pressed()
teclas = pygame.key.get_pressed()

#moedas
def desenhar_moeda_mini(superficie, cx, cy):
    #Moeda circular com borda dourada escura e detalhe interno
    pygame.draw.circle(superficie, (180, 120, 0), (cx, cy), 7)
    pygame.draw.circle(superficie, (255, 215, 0), (cx, cy), 6)
    pygame.draw.line(superficie, (255, 248, 180), (cx, cy - 3), (cx, cy + 3), 2)

def desenhar_botao_fechar(superficie, rect, mouse_pos):
    hover = rect.collidepoint(mouse_pos)
    clicando = hover and pygame.mouse.get_pressed()
    cor_fundo = (145, 25, 25) if clicando else ((235, 65, 65) if hover else (195, 45, 45))
    cor_borda = (255, 200, 200) if hover else (255, 130, 130)
    desloc_y = 2 if clicando else 0

    r = rect.move(0, desloc_y)
    pygame.draw.rect(superficie, cor_fundo, r, border_radius=6)
    pygame.draw.rect(superficie, cor_borda, r, width=2, border_radius=6)
    txt_x = fonte_painel.render("X", True, BRANCO)
    superficie.blit(txt_x, txt_x.get_rect(center=r.center))

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 








# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
#LOOP PRINCIPAL DO JOGO:
clock = pygame.time.Clock() #para remover sensação de engasgo/bugs

game = True
while game:
    clock.tick(60) #60 fps
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False

        #M muta/desmuta em qualquer tela
        if event.type == pygame.KEYDOWN and event.key == pygame.K_m:
            alternar_som()

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if tela_atual == "menu":
                for chave, rect in botoes_menu:
                    if rect.collidepoint(mouse_pos):
                        if chave == "iniciar":
                            tela_atual = "jogo"
                        elif chave == "como_jogar":
                            tela_atual = "como_jogar"
                        elif chave == "configuracoes":
                            tela_atual = "configuracoes"
                        elif chave == "sair":
                            game = False


            elif tela_atual == "configuracoes":
                if botao_som.collidepoint(mouse_pos):
                    alternar_som()
                elif botao_idioma.collidepoint(mouse_pos):
                    LINGUAGEM = "en" if LINGUAGEM == "pt" else "pt"
                elif botao_voltar.collidepoint(mouse_pos):
                    tela_atual = "menu"


            elif tela_atual == "como_jogar":
                if botao_voltar.collidepoint(mouse_pos):
                    tela_atual = "menu"


            elif tela_atual == "jogo":
                #TELA A: ESCOLHENDO O LOCAL DE TRABALHO (após clicar em JOB na ficha)
                if escolhendo_emprego and morador_selecionado is not None:
                    if pygame.Rect(548, 412, 54, 34).collidepoint(mouse_pos):
                        escolhendo_emprego = False
                    else:
                        comerciais = [a for a in andares if a.get("tipo") == "comercial" and len(a["trabalhadores"]) < 3]
                        for idx, c in enumerate(comerciais):
                            botao_loc = pygame.Rect(210, 130 + idx * 75, 380, 62)
                            if botao_loc.collidepoint(mouse_pos):
                                #Remove do emprego anterior se já trabalhava em outro lugar
                                for a in andares:
                                    if a.get("tipo") == "comercial" and morador_selecionado in a["trabalhadores"]:
                                        a["trabalhadores"].remove(morador_selecionado)
                                morador_selecionado["emprego"] = c["nome"]
                                c["trabalhadores"].append(morador_selecionado)
                                escolhendo_emprego = False
                                morador_selecionado = None
                                break

                #TELA B: FICHA DO BITIZEN (Current Job, Dream Job, Skills, JOB, EVICT)
                elif morador_selecionado is not None:
                    if pygame.Rect(548, 412, 54, 34).collidepoint(mouse_pos):
                        morador_selecionado = None
                    #Botão JOB (abrir lista de empregos)
                    elif pygame.Rect(275, 395, 115, 55).collidepoint(mouse_pos):
                        escolhendo_emprego = True
                    #Botão EVICT (expulsar morador)
                    elif pygame.Rect(410, 395, 115, 55).collidepoint(mouse_pos):
                        for a in andares:
                            if a.get("tipo") == "comercial" and morador_selecionado in a["trabalhadores"]:
                                a["trabalhadores"].remove(morador_selecionado)
                            if a.get("tipo") == "residencial" and morador_selecionado in a["moradores"]:
                                a["moradores"].remove(morador_selecionado)
                        morador_selecionado = None

                #TELA C: PAINEL DE UM ANDAR ABERTO (Comercial ou Residencial)
                elif andar_aberto is not None:
                    andar_sel = andares[andar_aberto]
                    if pygame.Rect(548, 412, 54, 34).collidepoint(mouse_pos):
                        andar_aberto = None

                    #Se clicou em um ANDAR RESIDENCIAL -> abre a ficha do morador clicado
                    elif andar_sel.get("tipo") == "residencial":
                        for idx, m in enumerate(andar_sel["moradores"]):
                            card_m = pygame.Rect(202, 102 + idx * 60, 396, 54)
                            if card_m.collidepoint(mouse_pos):
                                morador_selecionado = m
                                break

                    #Se clicou em um ANDAR COMERCIAL -> encomenda produto (se houver funcionário)
                    elif andar_sel.get("tipo") == "comercial":
                        trabs = andar_sel["trabalhadores"]
                        for idx, prod in enumerate(andar_sel["produtos"]):
                            card_dir = pygame.Rect(280, 104 + idx * 102, 322, 92)
                            if card_dir.collidepoint(mouse_pos) and idx < len(trabs):
                                if prod["estoque"] == 0 and prod["tempo"] == 0:
                                    prod["tempo"] = prod["duracao"]
                                elif prod["tempo"] > 0 and bux >= 1:
                                    bux -= 1
                                    prod["tempo"] = 0
                                    prod["estoque"] = prod["max"]

                #TELA D: CLIQUES NORMAIS NA TORRE
                else:
                    if pygame.Rect(515, 558, 95, 34).collidepoint(mouse_pos):
                        tela_atual = "menu"

                    y_topo_torre = 505 - len(andares) * 145
                    botao_add_rect = pygame.Rect(315, y_topo_torre - 80, 170, 52)
                    if botao_add_rect.collidepoint(mouse_pos):
                        if moedas >= custo_andar and len(novos_andares_disponiveis) > 0:
                            moedas -= custo_andar
                            andares.append(novos_andares_disponiveis.pop(0))
                            custo_andar += 100

                    #Clicar em qualquer andar Comercial OU Residencial abre o painel dele!
                    for i, andar in enumerate(andares):
                        y_topo = 505 - (i + 1) * 145
                        rect_andar = pygame.Rect(248, y_topo, 366, 145)
                        if rect_andar.collidepoint(mouse_pos) and andar.get("tipo") in ("comercial", "residencial"):
                            andar_aberto = i

                



    screen.fill(GALAXIA_COR) #Preencher o fundo com a cor do espaço

    for estrela in estrelas:
        if random.random() < 0.03: #3% de chance por frame de mudar o brilho, efeito != estático (sugestão de IA)
            estrela[3]
        b = estrela[3]
        pygame.draw.rect(screen, (b, b, b), (estrela[0], estrela[1], estrela[2], estrela[2]))
    

    if tela_atual == "menu":
        for nave in naves:
            nave[1] += nave[3] #soma v no eixo x
            if nave[1] > 820: #quando sai pela direita, volta pela esquerda
                nave[1] = -60
                nave[2] = random.randint(40, 460)
            screen.blit(nave[0], (nave[1], nave[2]))


        screen.blit(death_star_img, death_star_rect)  #Desenhar Death Star
    
        #Contorno do título "TINY DEATH STAR"
        pygame.draw.rect(screen, (255, 165, 0), caixa_rect, width=6, border_radius=15)
        pygame.draw.rect(screen, AMARELO_TITULO, caixa_rect.inflate(-4, -4), width=3, border_radius=14)
        screen.blit(txt_star, star_rect)
        screen.blit(txt_wars, wars_rect)

        for img, y in titulo:
            screen.blit(img, (400 - img.get_width() // 2, y))

        #Chão e personagens na base
        pygame.draw.rect(screen, (40, 45, 60), (0, 520, 800, 80))
        screen.blit(stormtrooper, (665, 400))
        screen.blit(greedo, (748, 435))
        screen.blit(tarkin, (600, 415))
        screen.blit(guard, (695, 483))
        screen.blit(palpatine, (615, 440))
        screen.blit(vader, (525, 445))

        screen.blit(leia, (10, 395))
        screen.blit(han_solo, (118, 400))
        screen.blit(r2d2, (120, 510))
        screen.blit(c3po, (75, 465))
        screen.blit(luke, (185, 452))
        screen.blit(chewbacca, (-8, 465))


        #botões do menu principal
        for chave, rect in botoes_menu:
            hover = rect.collidepoint(mouse_pos)
            cor_fundo = (55, 62, 85) if hover else (25, 28, 42)
            cor_borda = (255, 255, 130) if hover else AMARELO_TITULO

            pygame.draw.rect(screen, cor_fundo, rect, border_radius=8)
            pygame.draw.rect(screen, cor_borda, rect, width=2, border_radius=8)

            texto_traduzido = TEXTOS[LINGUAGEM][chave]
            txt = fonte_botao.render(texto_traduzido, False, cor_borda)
            screen.blit(txt, txt.get_rect(center=(rect.centerx, rect.centery - 2)))


    elif tela_atual == "como_jogar": #ajuda de IA com tamanhos
        painel = pygame.Rect(70, 100, 660, 340)
        pygame.draw.rect(screen, (25, 28, 42), painel, border_radius=14)
        pygame.draw.rect(screen, AMARELO_TITULO, painel, width=3, border_radius=14)

        #linha divisória abaixo do título do painel
        pygame.draw.line(screen, AMARELO_TITULO, (100, 175), (700, 175), 2)

        titulo_tela = fonte_titulo_painel.render(TEXTOS[LINGUAGEM]["titulo_como"], False, AMARELO_TITULO)
        screen.blit(titulo_tela, titulo_tela.get_rect(center=(400, 142)))

        for i, linha in enumerate(TEXTOS[LINGUAGEM]["regras"]):
            cor_linha = (255, 235, 130) if i == 3 else BRANCO
            txt_regra = fonte_instrucoes.render(linha, True, cor_linha)
            screen.blit(txt_regra, (105, 205 + i * 48))

    elif tela_atual == "configuracoes":
        painel = pygame.Rect(160, 140, 480, 280)
        pygame.draw.rect(screen, (25, 28, 42), painel, border_radius=14)
        pygame.draw.rect(screen, AMARELO_TITULO, painel, width=3, border_radius=14)

        chave_som = "som_on" if som_ativo else "som_off"
        for texto_botao, rect in ([(TEXTOS[LINGUAGEM][chave_som], botao_som), (TEXTOS[LINGUAGEM]["idioma"], botao_idioma)]):
            hover = rect.collidepoint(mouse_pos)
            cor_fundo = (55, 62, 85) if hover else (35, 39, 58)
            cor_borda = (255, 255, 130) if hover else AMARELO_TITULO
            pygame.draw.rect(screen, cor_fundo, rect, border_radius=8)
            pygame.draw.rect(screen, cor_borda, rect, width=2, border_radius=8)
            txt = fonte_botao.render(texto_botao, False, cor_borda)
            screen.blit(txt, txt.get_rect(center=(rect.centerx, rect.centery - 2)))

    elif tela_atual == "jogo":
        #fundo escuro nas laterais + torre centralizada
        screen.fill(GALAXIA_COR)

        for estrela in estrelas:
            if random.random() < 0.004:
                estrela[3] = random.randint(100,255)
            b = estrela[3]
            pygame.draw.rect(screen, (b, b, b), (estrela[0], estrela[1], estrela[2], estrela[2]))

        #barra inferior escura
        pygame.draw.rect(screen, (28, 30, 36), (180, 505, 440, 95))

        #caixinha de Moedas
        pygame.draw.rect(screen, (15, 18, 24), (190, 558, 150, 34), border_radius=4)
        pygame.draw.circle(screen, AMARELO_TITULO, (206, 575), 9) #TROCAR POR IMG?? VER!!!
        txt_moedas = fonte_botao.render(f"{moedas:,}", True, BRANCO)
        screen.blit(txt_moedas, (225, 561))

        #caixinha de Imperial Bux
        pygame.draw.rect(screen, (15, 18, 24), (350, 558, 115, 34), border_radius=4)
        #nota verde com detalhe mais claro no meio
        pygame.draw.rect(screen, (55, 175, 65), (360, 566, 22, 16), border_radius=2)
        pygame.draw.rect(screen, (125, 235, 120), (364, 570, 14, 8), border_radius=1)
        txt_bux = fonte_botao.render(str(bux), True, BRANCO)
        screen.blit(txt_bux, (395, 561))


        #botão verde MENU (canto inferior direito)
        botao_menu_verde = pygame.Rect(515, 558, 95, 34)
        pygame.draw.rect(screen, (65, 175, 55), botao_menu_verde, border_radius=6)
        pygame.draw.rect(screen, (130, 235, 110), botao_menu_verde, width=2, border_radius=6)
        txt_menu = fonte_instrucoes.render("MENU", True, BRANCO)
        screen.blit(txt_menu, txt_menu.get_rect(center=botao_menu_verde.center))

        #POÇO DO ELEVADOR (fundo do poço)
        y_topo_poco = 505 - len(andares) * 145
        pygame.draw.rect(screen, (26, 30, 38), (186, y_topo_poco, 58, len(andares) * 145))
        pygame.draw.line(screen, (65, 70, 82), (208, y_topo_poco), (208, 505), 2)
        pygame.draw.line(screen, (65, 70, 82), (222, y_topo_poco), (222, 505), 2)


        #CENÁRIOS DOS ANDARES (desenhados ANTES dos personagens para ficarem no fundo!)
        #DESENHA TODOS OS ANDARES DA LISTA (de baixo para cima)
        altura_andar = 145
        for i, andar in enumerate(andares):
            num_andar = i + 1
            y_topo = 505 - num_andar * altura_andar

            #Cenário e faixa de título do andar
            screen.blit(andar["cenario"], (248, y_topo + 24))
            pygame.draw.rect(screen, (65, 78, 105), (248, y_topo, 366, 24))
            txt_nome = fonte_botao.render(andar["nome"], False, andar["cor_titulo"])
            screen.blit(txt_nome, txt_nome.get_rect(center=(431, y_topo + 10)))

            if andar.get("tipo") == "comercial" and len(andar["trabalhadores"]) == 0:
                txt_closed = fonte_botao.render("closed", False, (255, 175, 50))
                screen.blit(txt_closed, (530, y_topo + 2))
            
            elif andar.get("tipo") == "residencial":
                txt_lot = fonte_instrucoes.render(f"{len(andar['moradores'])}/5", True, (150, 220, 255))
                screen.blit(txt_lot, (565, y_topo + 1))


            #Indicadores visuais dos 3 produtos (igual ao print do jogo original!)
            elif "produtos" in andar:
                falta_estoque = False
                for idx_p, prod in enumerate(andar["produtos"]):
                    #3 quadradinhos no canto direito da barra de título (check verde, amarelo, X vermelho)
                    box_mini = pygame.Rect(546 + idx_p * 21, y_topo + 3, 18, 18)
                    if prod["estoque"] > 0:
                        pygame.draw.rect(screen, (50, 175, 65), box_mini, border_radius=3)
                        #Desenha um 'V' (check) branco
                        pygame.draw.lines(screen, BRANCO, False, [
                            (box_mini.x + 4, box_mini.y + 9),
                            (box_mini.x + 8, box_mini.y + 13),
                            (box_mini.x + 14, box_mini.y + 5)
                        ], 2)
                    elif prod["tempo"] > 0:
                        pygame.draw.rect(screen, (220, 175, 40), box_mini, border_radius=3)
                        txt_prep = fonte_instrucoes.render("..", True, PRETO)
                        screen.blit(txt_prep, txt_prep.get_rect(center=box_mini.center))
                    else:
                        falta_estoque = True
                        pygame.draw.rect(screen, (205, 45, 45), box_mini, border_radius=3)
                        # Desenha um 'X' branco
                        pygame.draw.line(screen, BRANCO, (box_mini.x + 4, box_mini.y + 4), (box_mini.right - 5, box_mini.bottom - 5), 2)
                        pygame.draw.line(screen, BRANCO, (box_mini.right - 5, box_mini.y + 4), (box_mini.x + 4, box_mini.bottom - 5), 2)

                #Botão quadrado amarelo com caixinha no canto direito do andar quando falta estoque!
                if falta_estoque:
                    botao_stock = pygame.Rect(560, y_topo + 30, 46, 46)
                    pygame.draw.rect(screen, (30, 32, 38), botao_stock.inflate(4, 4), border_radius=6)
                    pygame.draw.rect(screen, (150, 120, 20), botao_stock, border_radius=5)
                    pygame.draw.rect(screen, (235, 205, 50), (botao_stock.x, botao_stock.y, 46, 42), border_radius=5)
                    pygame.draw.rect(screen, (255, 240, 130), (botao_stock.x, botao_stock.y, 46, 42), width=2, border_radius=5)
                    #Ícone de caixinha branca no meio do botão amarelo
                    pygame.draw.rect(screen, BRANCO, (botao_stock.x + 13, botao_stock.y + 11, 20, 18), border_radius=2)
                    pygame.draw.line(screen, (150, 120, 20), (botao_stock.x + 13, botao_stock.y + 17), (botao_stock.x + 33, botao_stock.y + 17), 2)


            pygame.draw.rect(screen, (15, 18, 24), (205, y_topo + 65, 20, 22), border_radius=3)
            txt_num = fonte_botao.render(str(num_andar), False, BRANCO)
            screen.blit(txt_num, txt_num.get_rect(center=(215, y_topo + 74)))

        #TOPO DA TORRE + BOTÃO ADD LEVEL (sobe sozinho quando você constrói)
        y_topo_torre = 505 - len(andares) * altura_andar
        pygame.draw.rect(screen, (95, 100, 112), (180, y_topo_torre - 40, 440, 40))
        pygame.draw.line(screen, (145, 150, 165), (180, y_topo_torre - 40), (620, y_topo_torre - 40), 3)

        if len(novos_andares_disponiveis) > 0:
            botao_add = pygame.Rect(315, y_topo_torre - 80, 170, 52)
            cor_borda_add = AMARELO_TITULO if moedas >= custo_andar else (120, 120, 130)
            pygame.draw.rect(screen, (35, 38, 46), botao_add, border_radius=8)
            pygame.draw.rect(screen, cor_borda_add, botao_add, width=2, border_radius=8)
            txt_add = fonte_botao.render("add level", False, BRANCO)
            screen.blit(txt_add, txt_add.get_rect(center=(400, y_topo_torre - 63)))
            txt_custo = fonte_botao.render(str(custo_andar), False, cor_borda_add)
            screen.blit(txt_custo, txt_custo.get_rect(center=(400, y_topo_torre - 43)))


        #MOVIMENTO DO ELEVADOR (agora com [0] no get_pressed)
        clicando = pygame.mouse.get_pressed()[0]
        teclas = pygame.key.get_pressed()

        subindo = (clicando and botao_cima_rect.collidepoint(mouse_pos)) or teclas[pygame.K_UP]
        descendo = (clicando and botao_baixo_rect.collidepoint(mouse_pos)) or teclas[pygame.K_DOWN]

        #Limite superior do elevador acompanha o último andar construído
        y_min_elevador = 505 - len(andares) * 145 + 65
        if subindo:
            elevador_y = max(float(y_min_elevador), elevador_y - elevador_vel)
        if descendo:
            elevador_y = min(425.0, elevador_y + elevador_vel)


        #Desenha a cabine na altura atualizada
        screen.blit(elevador_img, (188, int(elevador_y)))

        #PASSAGEIRO NO ELEVADOR E DESEMBARQUE
        if subindo or descendo:
            ja_moveu_elevador = True

        if tem_passageiro:
            px = 188 + (54 - passageiro_atual.get_width()) // 2
            py = int(elevador_y) + 60 - passageiro_atual.get_height()
            screen.blit(passageiro_atual, (px, py))

            balao_rect = pygame.Rect(197, int(elevador_y) - 24, 36, 20)
            pygame.draw.rect(screen, BRANCO, balao_rect, border_radius=4)
            pygame.draw.rect(screen, PRETO, balao_rect, width=2, border_radius=4)
            txt_dest = fonte_botao.render(str(andar_destino), False, PRETO)
            screen.blit(txt_dest, txt_dest.get_rect(center=(balao_rect.centerx, balao_rect.centery - 2)))

            if not subindo and not descendo and ja_moveu_elevador:
                andar_parado = None
                for i in range(len(andares)):
                    y_piso_elevador = 505 - (i + 1) * 145 + 65
                    if abs(elevador_y - y_piso_elevador) <= 8:
                        andar_parado = i + 1
                        break

                if andar_parado is not None:
                    acertou = (andar_parado == andar_destino)
                    andar_obj = andares[andar_parado - 1]
                    y_chao = 505 - (andar_parado - 1) * 145

                    # Se for andar RESIDENCIAL, ele se muda para lá (máximo 5 moradores)!
                    if andar_obj.get("tipo") == "residencial" and len(andar_obj["moradores"]) < 5:
                        andar_obj["moradores"].append({
                            "nome": random.choice(NOMES_STAR_WARS),
                            "sprite": passageiro_atual,
                            "olha_dir": passageiro_olha_dir,
                            "emprego": None,
                            "dream_job": "mos espa cafe",
                            "skills": {
                                "food": random.randint(1, 9),
                                "service": random.randint(1, 9),
                                "recreation": random.randint(1, 9),
                                "retail": random.randint(1, 9),
                            }
                        })


                    clientes_no_andar.append({
                        "sprite": passageiro_atual,
                        "olha_dir": passageiro_olha_dir,
                        "x": 248.0,
                        "y_chao": y_chao,
                        "alvo_x": random.randint(390, 520) if acertou else 310,
                        "acertou": acertou,
                        "tempo_consumo": 90 if acertou else 30,
                        "estado": "indo"
                    })
                    tem_passageiro = False
                    ja_moveu_elevador = False

        else:
            if elevador_y >= 420 and not subindo:
                passageiro_atual, passageiro_olha_dir = sortear_passageiro_unico()
                andar_destino = sortear_andar_aberto()
                tem_passageiro = True
                ja_moveu_elevador = False


        #ANIMAÇÃO DOS CLIENTES (suave, com pausas e virando para o lado certo)
        for cliente in clientes_no_andar[:]:
            # Garante que as variáveis de direção e pausa existam
            if "virado_esq" not in cliente:
                cliente["virado_esq"] = False
            if "pausa" not in cliente:
                cliente["pausa"] = 0

            if cliente["estado"] == "indo":
                cliente["virado_esq"] = False
                cliente["x"] += 1.0
                if cliente["x"] >= cliente["alvo_x"]:
                    cliente["estado"] = "consumindo"

            elif cliente["estado"] == "consumindo":
                cliente["tempo_consumo"] -= 1
                if cliente["tempo_consumo"] <= 0:
                    if cliente["acertou"]:
                        moedas += 10
                        cliente["estado"] = "passeando"
                        cliente["pausa"] = random.randint(60, 150)  #Fica parado 1 a 2.5 seg
                        cliente["alvo_x"] = random.randint(275, 555)
                        indice_andar = int((505 - cliente["y_chao"]) // 145)
                        if 0 <= indice_andar < len(andares) and "produtos" in andares[indice_andar]:
                            for prod in andares[indice_andar]["produtos"]:
                                if prod["estoque"] > 0:
                                    prod["estoque"] -= 1
                                    moedas += 5
                                    break

                    else:
                        cliente["estado"] = "saindo"

            elif cliente["estado"] == "passeando":
                if cliente["pausa"] > 0:
                    cliente["pausa"] -= 1
                else:
                    distancia = cliente["alvo_x"] - cliente["x"]
                    if abs(distancia) <= 2:
                        # Chegou no ponto: para por 2 a 4 segundos antes de escolher outro canto
                        cliente["pausa"] = random.randint(120, 240)
                        cliente["alvo_x"] = random.randint(275, 555)
                    elif distancia > 0:
                        cliente["virado_esq"] = False
                        cliente["x"] += 0.8
                    else:
                        cliente["virado_esq"] = True
                        cliente["x"] -= 0.8

            elif cliente["estado"] == "saindo":
                cliente["virado_esq"] = True
                cliente["x"] -= 1.0
                if cliente["x"] <= 245:
                    clientes_no_andar.remove(cliente)
                    continue

            andando_esq = cliente["virado_esq"]
            olha_dir = cliente.get("olha_dir", True)
            precisa_espelhar = andando_esq if cliente["olha_dir"] else not andando_esq
            sprite_desenho = pygame.transform.flip(cliente["sprite"], precisa_espelhar, False)
            screen.blit(sprite_desenho, (int(cliente["x"]), cliente["y_chao"] - sprite_desenho.get_height()))


        #BOTÕES DO ELEVADOR
        desenhar_seta_elevador(screen, botao_cima_rect, "cima", subindo)
        desenhar_seta_elevador(screen, botao_baixo_rect, "baixo", descendo)

        #Atualiza contagem regressiva dos itens em preparo
        for andar in andares:
            if "produtos" in andar:
                for prod in andar["produtos"]:
                    if prod["tempo"] > 0:
                        prod["tempo"] -= 1
                        if prod["tempo"] <= 0:
                            prod["estoque"] = prod["max"]

                ui = TEXTOS[LINGUAGEM]
        botao_fechar = pygame.Rect(548, 412, 54, 34)

        # 1. TELA DE ESCOLHA DO LOCAL DE TRABALHO
        if escolhendo_emprego and morador_selecionado is not None:
            painel = pygame.Rect(184, 55, 432, 406)
            pygame.draw.rect(screen, (18, 36, 76), painel, border_radius=10)
            pygame.draw.rect(screen, (75, 145, 225), painel, width=3, border_radius=10)

            txt_t = fonte_painel.render(ui["escolher_local"], True, AMARELO_TITULO)
            screen.blit(txt_t, txt_t.get_rect(center=(400, 88)))

            comerciais = [a for a in andares if a.get("tipo") == "comercial" and len(a["trabalhadores"]) < 3]
            for idx, c in enumerate(comerciais):
                botao_loc = pygame.Rect(210, 125 + idx * 72, 380, 58)
                eh_sonho = (c["nome"] == morador_selecionado["dream_job"])
                cor_b = AMARELO_TITULO if eh_sonho else (95, 175, 245)
                pygame.draw.rect(screen, (28, 56, 110), botao_loc, border_radius=8)
                pygame.draw.rect(screen, cor_b, botao_loc, width=2, border_radius=8)

                txt_c = fonte_botao.render(c["nome"], False, c["cor_titulo"])
                screen.blit(txt_c, (botao_loc.x + 16, botao_loc.y + 8))
                txt_vagas = fonte_painel.render(f"Vagas: {len(c['trabalhadores'])}/3", True, BRANCO)
                screen.blit(txt_vagas, (botao_loc.x + 16, botao_loc.y + 33))

            desenhar_botao_fechar(screen, botao_fechar, mouse_pos)

        # 2. FICHA DO BITIZEN (textos ajustados com fonte_painel para caberem perfeitamente!)
        elif morador_selecionado is not None:
            painel = pygame.Rect(184, 55, 432, 406)
            pygame.draw.rect(screen, (18, 36, 76), painel, border_radius=10)
            pygame.draw.rect(screen, (75, 145, 225), painel, width=3, border_radius=10)

            sp_g = pygame.transform.scale(morador_selecionado["sprite"], (morador_selecionado["sprite"].get_width() * 3, morador_selecionado["sprite"].get_height() * 3))
            screen.blit(sp_g, (215, 70))
            screen.blit(fonte_instrucoes.render(morador_selecionado["nome"], True, BRANCO), (310, 82))

            # Caixa Current Job / Dream Job (agora usando fonte_painel para não vazar da borda!)
            box_jobs = pygame.Rect(202, 152, 396, 62)
            pygame.draw.rect(screen, (25, 48, 95), box_jobs, border_radius=6)
            pygame.draw.rect(screen, (85, 155, 230), box_jobs, width=2, border_radius=6)

            emp_atual_txt = (morador_selecionado["emprego"] or ui["desempregado"]).upper()
            dream_txt = morador_selecionado["dream_job"].upper()
            screen.blit(fonte_painel.render(f"{ui['emp_atual']} {emp_atual_txt}", True, (130, 235, 110)), (214, 162))
            screen.blit(fonte_painel.render(f"{ui['emp_sonho']} {dream_txt}", True, AMARELO_TITULO), (214, 188))

            # Barras de habilidade
            categorias_skill = [
                ("FOOD", "food", (45, 155, 65)),
                ("SERVICE", "service", (45, 125, 195)),
                ("RECREATION", "recreation", (185, 165, 45)),
                ("RETAIL", "retail", (155, 65, 185)),
            ]
            for idx_s, (rotulo, chave, cor_barra) in enumerate(categorias_skill):
                y_b = 226 + idx_s * 38
                valor = morador_selecionado["skills"][chave]
                pygame.draw.rect(screen, (25, 38, 68), (202, y_b, 396, 30), border_radius=4)
                larg_preenchida = int(350 * (valor / 9.0))
                pygame.draw.rect(screen, cor_barra, (202, y_b, larg_preenchida, 30), border_radius=4)
                pygame.draw.rect(screen, (95, 165, 235), (202, y_b, 396, 30), width=1, border_radius=4)

                screen.blit(fonte_painel.render(rotulo, True, BRANCO), (212, y_b + 6))
                screen.blit(fonte_painel.render(str(valor), True, BRANCO), (576, y_b + 6))

            # Botões EMPREGO (JOB) e EXPULSAR (EVICT) com texto bem centralizado
            botao_job = pygame.Rect(275, 395, 115, 51)
            pygame.draw.rect(screen, (35, 130, 215), botao_job, border_radius=8)
            pygame.draw.rect(screen, (140, 215, 255), botao_job, width=2, border_radius=8)
            txt_j = fonte_painel.render(ui["botao_emprego"], True, BRANCO)
            screen.blit(txt_j, txt_j.get_rect(center=botao_job.center))

            botao_evict = pygame.Rect(410, 395, 115, 51)
            pygame.draw.rect(screen, (165, 45, 55), botao_evict, border_radius=8)
            pygame.draw.rect(screen, (245, 120, 130), botao_evict, width=2, border_radius=8)
            txt_e = fonte_painel.render(ui["botao_expulsar"], True, BRANCO)
            screen.blit(txt_e, txt_e.get_rect(center=botao_evict.center))

            desenhar_botao_fechar(screen, botao_fechar, mouse_pos)

        # 3. PAINEL DO ANDAR ABERTO (altura 406 sem espaço sobrando!)
        elif andar_aberto is not None:
            andar_sel = andares[andar_aberto]
            painel = pygame.Rect(184, 55, 432, 406)
            pygame.draw.rect(screen, (18, 36, 76), painel, border_radius=10)
            pygame.draw.rect(screen, (75, 145, 225), painel, width=3, border_radius=10)

            txt_p_titulo = fonte_botao.render(andar_sel["nome"], False, andar_sel["cor_titulo"])
            screen.blit(txt_p_titulo, txt_p_titulo.get_rect(center=(400, 80)))

            # --- SE FOR ANDAR RESIDENCIAL ---
            if andar_sel.get("tipo") == "residencial":
                for idx in range(5):
                    y_m = 102 + idx * 60
                    box_avatar = pygame.Rect(202, y_m, 54, 54)
                    card_info = pygame.Rect(262, y_m, 336, 54)
                    pygame.draw.rect(screen, (25, 52, 95), box_avatar, border_radius=6)
                    pygame.draw.rect(screen, (95, 175, 245), box_avatar, width=2, border_radius=6)
                    pygame.draw.rect(screen, (25, 48, 95), card_info, border_radius=6)
                    pygame.draw.rect(screen, (95, 175, 245), card_info, width=2, border_radius=6)

                    if idx < len(andar_sel["moradores"]):
                        m = andar_sel["moradores"][idx]
                        sp = pygame.transform.scale(m["sprite"], (int(m["sprite"].get_width() * 1.5), int(m["sprite"].get_height() * 1.5)))
                        screen.blit(sp, sp.get_rect(center=box_avatar.center))

                        if m["emprego"] == m["dream_job"]:
                            pygame.draw.circle(screen, AMARELO_TITULO, (box_avatar.left + 4, box_avatar.bottom - 4), 8)

                        screen.blit(fonte_painel.render(m["nome"], True, BRANCO), (card_info.x + 12, card_info.y + 8))
                        emp_str = (m["emprego"] or ui["desempregado"]).upper()
                        cor_emp = (130, 235, 110) if m["emprego"] else (255, 175, 80)
                        screen.blit(fonte_painel.render(f"{ui['emprego']} {emp_str}", True, cor_emp), (card_info.x + 12, card_info.y + 30))

            #SE FOR ANDAR COMERCIAL
            elif andar_sel.get("tipo") == "comercial":
                tempos_texto = ["1m", "4m", "8m"]
                for idx, prod in enumerate(andar_sel["produtos"]):
                    y_row = 104 + idx * 102
                    tem_trabalhador = idx < len(andar_sel["trabalhadores"])

                    box_esq = pygame.Rect(198, y_row, 74, 92)
                    pygame.draw.rect(screen, (25, 52, 95), box_esq, border_radius=6)
                    pygame.draw.rect(screen, (95, 175, 245), box_esq, width=2, border_radius=6)
                    if tem_trabalhador:
                        trab = andar_sel["trabalhadores"][idx]
                        sp = pygame.transform.scale(trab["sprite"], (trab["sprite"].get_width() * 2, trab["sprite"].get_height() * 2))
                        screen.blit(sp, sp.get_rect(center=box_esq.center))
                    else:
                        txt_hire = fonte_painel.render(ui["contratar"].upper(), True, (130, 210, 255))
                        screen.blit(txt_hire, txt_hire.get_rect(center=box_esq.center))

                    card_dir = pygame.Rect(280, y_row, 322, 92)
                    if not tem_trabalhador:
                        cor_card, cor_topo, cor_borda = (55, 62, 78), (75, 84, 105), (120, 130, 155)
                    elif prod["estoque"] > 0:
                        cor_card, cor_topo, cor_borda = (35, 115, 55), (50, 145, 75), (110, 225, 130)
                    elif prod["tempo"] > 0:
                        cor_card, cor_topo, cor_borda = (155, 120, 25), (185, 145, 35), (250, 220, 95)
                    else:
                        cor_card, cor_topo, cor_borda = (145, 22, 28), (180, 35, 42), (235, 95, 105)

                    pygame.draw.rect(screen, cor_card, card_dir, border_radius=6)
                    pygame.draw.rect(screen, cor_topo, (card_dir.x, card_dir.y, card_dir.width, 24), border_radius=6)
                    pygame.draw.rect(screen, cor_borda, card_dir, width=2, border_radius=6)

                    screen.blit(prod["icone"], (card_dir.x + 10, card_dir.y + 30))

                    txt_nome_p = fonte_painel.render(prod["nome"].upper(), True, BRANCO)
                    screen.blit(txt_nome_p, (card_dir.x + 12, card_dir.y + 4))

                    #Moedinhas no canto direito
                    for m in range(idx + 1):
                        desenhar_moeda_mini(screen, card_dir.right - 16 - m * 15, card_dir.y + 12)

                    #Ícone de reloginho desenhado + Tempo
                    cx_rel, cy_rel = card_dir.x + 66, card_dir.y + 40
                    pygame.draw.circle(screen, (255, 235, 140), (cx_rel, cy_rel), 6, 1)
                    pygame.draw.line(screen, (255, 235, 140), (cx_rel, cy_rel), (cx_rel, cy_rel - 4), 1)
                    pygame.draw.line(screen, (255, 235, 140), (cx_rel, cy_rel), (cx_rel + 3, cy_rel), 1)


    if tela_atual in ("como_jogar", "configuracoes"):
        hover_v = botao_voltar.collidepoint(mouse_pos)
        cor_fundo = (55, 62, 85) if hover_v else (25, 28, 42)
        cor_borda = (255, 255, 130) if hover_v else AMARELO_TITULO
        pygame.draw.rect(screen, cor_fundo, botao_voltar, border_radius=8)
        pygame.draw.rect(screen, cor_borda, botao_voltar, width=2, border_radius=8)
        txt_v = fonte_botao.render(TEXTOS[LINGUAGEM]["voltar"], False, cor_borda)
        screen.blit(txt_v, txt_v.get_rect(center=(botao_voltar.centerx, botao_voltar.centery - 2)))

    pygame.display.update()

pygame.quit()