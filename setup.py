import pygame

#COLORS:
BG_COLOR = (10, 10, 25)  #Dark space blue
DEATH_STAR_GRAY = (160, 160, 160)  #Gray color for the Death Star
TRENCH_GRAY = (110, 110, 110)  #Darker gray for the trench
DISH_GRAY = (130, 130, 130)  #Gray for the superlaser dish (death star's eye)

#WINDOW DIMENSIONS:
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))

#DEATH STAR DIMENSIONS:
center_x, center_y = WIDTH // 2, HEIGHT // 2
radius = 40

setup(
    name="Tiny Death Star",
    version="1.0",
    description="Tiny Death Star in Pygame",
    authors=["Isabel Heckmann", "José Eduardo Terras Mello", "Maria Luíza Tebaldi Franco"],
    packages=["tiny_death_star"],
    install_requires=[
        "pygame>=2.0.0",
    ],
    entry_points={
        "console_scripts": [
            "tiny_death_star=tiny_death_star.main:main",
        ],
    },
    classifiers=[
        "Programming Language <IP_ADDRESS> Python <IP_ADDRESS> 3",
        "License <IP_ADDRESS> OSI Approved <IP_ADDRESS> MIT License",
        "Operating System <IP_ADDRESS> OS Independent",
    ],
    python_requires=">=3.6",
)

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tiny Death Star")  #MUDAR!!!
pygame.init()

game = True

while game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False

    window.fill(BG_COLOR)  #Fill the window with the background color
    pygame.display.flip()  #Update the display

pygame.draw.circle(window, DEATH_STAR_GRAY, (center_x, center_y), radius)  #Draw the Death Star
pygame.draw.line(window, TRENCH_GRAY, (center_x - radius, center_y), (center_x + radius, center_y), 2)  #Draw the trench

dish_x = center_x - 12
dish_y = center_y - 12
dish_radius = 8
pygame.draw.circle(screen, DISH_GRAY, (dish_x, dish_y), dish_radius, 1)  # Outer ring
pygame.draw.circle(screen, DISH_GRAY, (dish_x, dish_y), 3)  #Center focus

#Update display
pygame.display.flip()

pygame.quit()
sys.exit()