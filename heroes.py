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
    def __init__(self, group):
        super().__init__(group)


class HeroA(Base_Hero):
    thumbnail = load_image("heroA_thumbnail.jpg")

    def __init__(self, group):
        super().__init__(group)


class HeroB(Base_Hero):
    thumbnail = load_image("heroB_thumbnail.jpg")

    def __init__(self, group):
        super().__init__(group)