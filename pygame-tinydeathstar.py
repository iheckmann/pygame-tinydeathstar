import sys
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

botoes_menu = [
    ("i n i c i a r", pygame.Rect(280, 410, 240, 36)),
    ("c o m o   j o g a r", pygame.Rect(280, 454, 240, 36)),
    ("c o n f i g u r a ç õ e s", pygame.Rect(280, 498, 240, 36)),
    ("s a i r", pygame.Rect(280, 542, 240, 36))
]

def carregar_personagem(caminho, escala=2):
    img = pygame.image.load(caminho).convert_alpha()
    
    # Recorta as sobras transparentes em volta para o pé encostar certinho no chão
    rect_recorte = img.get_bounding_rect()
    img = img.subsurface(rect_recorte).copy()

    w, h = img.get_size()
    return pygame.transform.scale(img, (w * escala, h * escala))


#PERSONAGENS
vader = carregar_personagem("tiny-death-star/characters/the-force/Darth_Vader.png", escala=2)
stormtrooper = carregar_personagem("tiny-death-star/characters/troops/Stormtrooper.png", escala=2)
c3po = carregar_personagem("tiny-death-star/characters/droids/C-3PO.png", escala = 2)

## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -







#LOOP PRINCIPAL DO JOGO:
game = True
while game:
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if tela_atual == "menu":
                for texto, rect in botoes_menu:
                    if rect.collidepoint(mouse_pos):
                        if texto == "i n i c i a r":
                            tela_atual = "jogo"
                        elif texto == "c o m o   j o g a r":
                            tela_atual = "como_jogar"
                        elif texto == "c o n f i g u r a ç õ e s":
                            tela_atual = "configuracoes"
                        elif texto == "s a i r":
                            game = False
            else:
                if botao_voltar.collidepoint(mouse_pos):
                    tela_atual = "menu"

    screen.fill(GALAXIA_COR)  #Preencher o fundo com a cor do espaço


    if tela_atual == "menu":
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
        screen.blit(vader, (650, 390))


        #botões do menu principal
        for texto, rect in botoes_menu:
            pygame.draw.rect(screen, (25, 28, 42), rect, border_radius=8)
            pygame.draw.rect(screen, AMARELO_TITULO, rect, width=2, border_radius=8)
            txt = fonte_botao.render(texto, False, AMARELO_TITULO)
            txt_rect = txt.get_rect(center=(rect.centerx, rect.centery - 2))
            screen.blit(txt, txt_rect)

        for texto, rect in botoes_menu:
            if rect.collidepoint(mouse_pos):
                hover = rect.collidepoint(mouse_pos)
                cor_fundo = (55, 62, 85) if hover else (25, 28, 42)
                cor_borda = (255, 255, 130) if hover else AMARELO_TITULO

                pygame.draw.rect(screen, cor_fundo, rect, border_radius=8)
                pygame.draw.rect(screen, cor_borda, rect, width=2, border_radius=8)
                txt = fonte_botao.render(texto, False, cor_borda)
                screen.blit(txt, txt.get_rect(center=(rect.centerx, rect.centery - 2)))

    elif tela_atual in ("como_jogar", "configuracoes"):
        pygame.draw.rect(screen, (25, 28, 42), botao_voltar, border_radius=8)
        pygame.draw.rect(screen, AMARELO_TITULO, botao_voltar, width=2, border_radius=8)
        txt = fonte_botao.render("voltar", False, AMARELO_TITULO)
        screen.blit(txt, txt.get_rect(center=(botao_voltar.centerx, botao_voltar.centery - 2)))

    pygame.display.update()

pygame.quit()