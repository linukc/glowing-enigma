import pygame
import sys
pygame.init()

from config import *
sc = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
from menu import start_screen
from heroes import HeroA, HeroB

if __name__ == "__main__":
    all_sprites = pygame.sprite.Group()
    heroA = HeroA(all_sprites) # as sprite
    heroB = HeroB(all_sprites) # as sprite

    game_config = start_screen(sc, heroA, heroB)

    sc.fill(WHITE)
    print(game_config)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()

    pygame.quit()

