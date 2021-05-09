import pygame
import sys
pygame.init()

from config import *
sc = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
from menu import start_screen
from heroes import HeroA, HeroB
from arena import Border

if __name__ == "__main__":
    # first player == A player == left player
    # second player == B player == right player

    heroA = HeroA(control_config_A, orientation="leftward")
    heroB = HeroB(control_config_B, orientation="rightward")

    Border(5, 5, WIN_WIDTH - 5, 5)
    Border(5, WIN_HEIGHT - 5, WIN_WIDTH - 5, WIN_HEIGHT - 5)
    Border(5, 5, 5, WIN_HEIGHT - 5)
    Border(WIN_WIDTH - 5, 5, WIN_WIDTH - 5, WIN_HEIGHT - 5)
    Border(WIN_WIDTH // 2, 5, WIN_WIDTH // 2, WIN_HEIGHT - 5)

    #surf_left = pygame.Surface(WIN_WIDTH//2, WIN_HEIGHT)
    #surf_right = pygame.Surface(WIN_WIDTH//2, WIN_HEIGHT)

    game_config = start_screen(sc, heroA, heroB)
    heroA.mode = game_config.get("left_player_mode")
    heroB.mode = game_config.get("right_player_mode")

    clock = pygame.time.Clock()
    FPS = 30

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        sc.fill(WHITE)
        all_sprites.draw(sc)

        keys = pygame.key.get_pressed()
        heroes_sprites.update(keys)

        pygame.display.flip()

        clock.tick(FPS)

    pygame.quit()

