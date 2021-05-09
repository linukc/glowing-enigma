import pygame
import random
pygame.init()

from config import *
from utils import terminate
sc = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
from menu import start_screen
from heroes import HeroA, HeroB
from arena import Border, Particle, create_particles

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

    game_config = start_screen(sc, heroA, heroB)
    heroA.mode = game_config.get("left_player_mode")
    heroB.mode = game_config.get("right_player_mode")

    clock = pygame.time.Clock()
    FPS = 30
    #end game animation
    created_particles = 0
    particle_x_start = None 
    particle_y_start = None

    #start_game animation

    #pygame.time.set_timer(INCREASE_RADIUS, 1000) для анимаций
    #gameloop
    running = True
    while running:
        #stop condition
        if created_particles > 10:
            pygame.time.set_timer(CREATE_PARTICLES, 0)
            if not particles_sprites.sprites():
                terminate()

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                terminate()
            if event.type == CREATE_PARTICLES:
                create_particles((random.choice(particle_x_start), random.choice(particle_y_start)), sc.get_rect())
                created_particles += 1

        keys = pygame.key.get_pressed()
        all_sprites.update(keys, events)

        loser = heroA if heroA.xp <= 0 else (heroB if heroB.xp <= 0 else None) #loser is always one
        if loser and loser.xp <= 0: # game end animation creation; if only once
            #if will only perform once
            loser.xp = 1

            heroA.lock()
            heroB.lock()
            if loser.orientation == "leftward":
                particle_x_start = range(WIN_WIDTH//8 + WIN_WIDTH//2, 3*WIN_WIDTH//8+ WIN_WIDTH//2)
            else:
                particle_x_start = range(WIN_WIDTH//8, 3*WIN_WIDTH//8)
            particle_y_start = range(WIN_HEIGHT//8, 3*WIN_HEIGHT//8)
            pygame.time.set_timer(CREATE_PARTICLES, 500)

        elif not particles_sprites.sprites:
            running = False

        sc.fill(WHITE)
        all_sprites.draw(sc)

        pygame.display.flip()
        clock.tick(FPS)



