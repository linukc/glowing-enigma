import pygame
from config import *

BORDER_WIDTH = 1

class Border(pygame.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if x1 == x2:
            self.add(vertical_borders)
            self.image = pygame.Surface([BORDER_WIDTH, y2 - y1])
            self.rect = pygame.Rect(x1, y1, BORDER_WIDTH, y2 - y1)
        else:
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, BORDER_WIDTH])
            self.rect = pygame.Rect(x1, y1, x2 - x1, BORDER_WIDTH)