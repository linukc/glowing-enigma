import pygame
import random
pygame.init()

from config import *
from utils import terminate
sc = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
from menu import start_screen
from heroes import HeroA, HeroB
from arena import Border, Particle, create_particles, CountDown

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
    heroA.set_mode(game_config.get("left_player_mode"))
    heroB.set_mode(game_config.get("right_player_mode"))

    clock = pygame.time.Clock()
    FPS = 40

    #start game animation config
    heroA.lock()
    heroB.lock()
    start_phase = True

    #end game animation config
    created_particles = 0
    end_animation_not_started = True
    particle_x_start = None 
    particle_y_start = None

    #start game animation
    if heroA.mode == "player":
        CountDown(WIN_WIDTH//4, WIN_HEIGHT//2)
    if heroB.mode == "player":
        CountDown(3*WIN_WIDTH//4, WIN_HEIGHT//2)

    #gameloop
    running = True
    while running:
        #start control
        if not countdown_sprite.sprites() and start_phase:
            heroA.unlock()
            heroB.unlock()
            start_phase = False

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
        if loser and end_animation_not_started: # game end animation creation; if only once
            
            end_animation_not_started = False
            heroA.lock()
            heroB.lock()
            for bullet in bullets_sprites.sprites():
                bullet.kill()
            for bomb in bombs_sprites.sprites():
                bomb.kill()

            if loser.orientation == "leftward":
                particle_x_start = range(WIN_WIDTH//8 + WIN_WIDTH//2, 3*WIN_WIDTH//8+ WIN_WIDTH//2)
            else:
                particle_x_start = range(WIN_WIDTH//8, 3*WIN_WIDTH//8)
            particle_y_start = range(WIN_HEIGHT//8, 3*WIN_HEIGHT//8)
            pygame.time.set_timer(CREATE_PARTICLES, 500)


        sc.fill(WHITE)
        all_sprites.draw(sc)

        pygame.display.flip()
        clock.tick(FPS)



