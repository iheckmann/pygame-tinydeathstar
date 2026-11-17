import sys
import pygame

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


pygame.init()
pygame.mixer.init()

pygame.mixer.music.load("Tiny-Death-Star_Main-Star-Wars-Theme.mp3")
pygame.mixer.music.play(-1)  #Reproduzir em loop (pygame.mixer.music.stop() para parar a música)


game = True

font = pygame.font.SysFont(None, 48)
text = font.render('Tiny Death Star', True, (AMARELO_TITULO))

while game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False

    screen.fill(GALAXIA_COR)  #Preencher o fundo com a cor do espaço
    screen.blit(text, (JANELA_LARGURA // 2 - text.get_width() // 2, 50))  #Exibir o texto no centro da tela

    pygame.display.update()  # Mostra o novo frame para o jogador

pygame.quit()