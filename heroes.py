import pygame
import os 
import random
from config import *


def load_image(name, color_key=None):
    fullname = os.path.join('images', name)
    image = pygame.image.load(fullname).convert()

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


class Base_Hero(pygame.sprite.Sprite):

    def __init__(self, control_config, orientation, thumbnail):
        super().__init__(all_sprites)
        self.add(heroes_sprites)
        self.control_config = control_config
        self.mode = "auto"

        self.up = control_config.get("up")
        self.down = control_config.get("down")
        self.right = control_config.get("right")
        self.left = control_config.get("left")

        self.orientation = orientation
        self.thumbnail = thumbnail
        if orientation == "rightward": #original image looks left to right
            self.thumbnail = pygame.transform.flip(self.thumbnail, True, False)
        self.image = pygame.transform.scale(self.thumbnail, (100, 100))
        self.rect = self.image.get_rect()

        if orientation == "leftward": #player 1
            self.rect.x = 0.1*WIN_WIDTH
            self.rect.y = 0.4*WIN_HEIGHT
        else: #player 2
            self.rect.x = 0.8*WIN_WIDTH
            self.rect.y = 0.4*WIN_HEIGHT

        self.vx = 5
        self.vy = 5
        self.max_xp = 1500

    def update(self, keys):
        #xp bar
        pygame.draw.rect(self.image, RED, (0, 0, self.rect.width, 10), border_radius=3)
        pygame.draw.rect(self.image, BLACK, (0, 0, self.rect.width, 10), width=1, border_radius=3)
        #movements
        if self.mode == "player":
            x = self.vx * (keys[self.right] - keys[self.left])
            y = self.vy * (keys[self.down] - keys[self.up])
            self.rect = self.rect.move((x, y))


class HeroA(Base_Hero):
    thumbnail = load_image("heroA_thumbnail.jpg", -1) #must be 300x300

    def __init__(self, control_config, orientation):
        super().__init__(control_config, orientation, HeroA.thumbnail)
        self.max_xp = 1000

    def update(self, *args):
        keys = args[0]
        super().update(keys)


class HeroB(Base_Hero):
    thumbnail = load_image("heroA_thumbnail.jpg", -1) #must be 300x300

    def __init__(self, control_config, orientation):
        super().__init__(control_config, orientation, HeroB.thumbnail)
        self.max_xp = 850

    def update(self, *args):
        keys = args[0]
        super().update(keys)