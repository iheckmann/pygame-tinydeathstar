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


fonte_botao = pygame.font.Font("tiny-death-star/fontes/star_jedi/starjedi/Starjedi.ttf", 14)
fonte_titulo_painel = pygame.font.Font("tiny-death-star/fontes/star_jedi/starjedi/Starjedi.ttf", 26)

#som
som_ativo = True 
fonte_instrucoes = pygame.font.SysFont("avenir", 20, bold=True)

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
        ]
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
        ]
    }
    
}

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
for _ in range(75):
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

## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -







#LOOP PRINCIPAL DO JOGO:
game = True
while game:
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

            elif tela_atual in ("como_jogar", "jogo"):
                if botao_voltar.collidepoint(mouse_pos):
                    tela_atual = "menu"

            else:
                if botao_voltar.collidepoint(mouse_pos):
                    tela_atual = "menu"

    screen.fill(GALAXIA_COR)  #Preencher o fundo com a cor do espaço

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

    if tela_atual != "menu":
        hover_v = botao_voltar.collidepoint(mouse_pos)
        cor_fundo = (55, 62, 85) if hover_v else (25, 28, 42)
        cor_borda = (255, 255, 130) if hover_v else AMARELO_TITULO
        pygame.draw.rect(screen, cor_fundo, botao_voltar, border_radius=8)
        pygame.draw.rect(screen, cor_borda, botao_voltar, width=2, border_radius=8)
        txt_v = fonte_botao.render(TEXTOS[LINGUAGEM]["voltar"], False, cor_borda)
        screen.blit(txt_v, txt_v.get_rect(center=(botao_voltar.centerx, botao_voltar.centery - 2)))

    pygame.display.update()

pygame.quit()