import pygame
import sys
pygame.init()

from config import *
sc = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
from menu import start_screen
from heroes import HeroA, HeroB

if __name__ == "__main__":
    # first player == A player == left player
    # second player == B player == right player
    control_config_A = {"up": pygame.K_w,
                        "down": pygame.K_s,
                        "right": pygame.K_d,
                        "left": pygame.K_a,
                        "first_cast": pygame.K_r,
                        "second_cast": pygame.K_t,
                        "third_cast": pygame.K_y}
    control_config_B = {"up": pygame.K_UP,
                        "down": pygame.K_DOWN,
                        "right": pygame.K_RIGHT,
                        "left": pygame.K_LEFT,
                        "first_cast": pygame.K_KP1,
                        "second_cast": pygame.K_KP2,
                        "third_cast": pygame.K_KP3}

    heroes_sprites = pygame.sprite.Group()
    heroA = HeroA(heroes_sprites, control_config_A, orientation="leftward")
    heroB = HeroB(heroes_sprites, control_config_B, orientation="rightward")

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
        
        keys = pygame.key.get_pressed()
        heroes_sprites.update(keys)

        sc.fill(WHITE)
        heroes_sprites.draw(sc)
        pygame.display.flip()

        clock.tick(FPS)

    pygame.quit()

