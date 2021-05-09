import pygame

WIN_WIDTH = 1000 #must div by 8
WIN_HEIGHT = 700
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

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

all_sprites = pygame.sprite.Group()
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()
heroes_sprites = pygame.sprite.Group()
particles_sprites = pygame.sprite.Group()

CREATE_PARTICLES = pygame.USEREVENT + 1 #24 to 32