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

        self.x_step = 5
        self.y_step = 5
        #for collidence with borders
        self.x_direction = 1 # 1 if moved along x axes else -1;
        self.y_direction = 1 # 1 if moved along y axes else -1;
        self.max_xp = 100 #1,2,5,10,20,25,50,100
        self.xp = self.max_xp

    def get_opponent(self):
        return [sprite for sprite in heroes_sprites.sprites() if sprite != self][0] #only 2 heroes

    def update(self, keys):
        #XP bar
        pygame.draw.rect(self.image, WHITE, (0, 0, self.rect.width, 10), border_radius=2)
        pygame.draw.rect(self.image, RED, (0, 0, self.xp*(self.rect.width/self.max_xp), 10), border_radius=2)
        pygame.draw.rect(self.image, BLACK, (0, 0, self.rect.width, 10), width=1, border_radius=2)

        #movements
        if self.mode == "player":
            x = self.x_step * (keys[self.right] - keys[self.left])
            y = self.y_step* (keys[self.down] - keys[self.up])
        else: #auto
            x = 0
            delta_y = self.rect.y - self.get_opponent().rect.y
            y = -self.y_step if delta_y>0 else (self.y_step if delta_y<0 else 0) #if elif else

        self.rect = self.rect.move((x, y))

        #collidence with borders
        border_offset = 5
        if pygame.sprite.spritecollideany(self, horizontal_borders):
            if self.y_direction == 1:
                self.rect.y = WIN_HEIGHT - self.rect.height - border_offset - 1
            elif self.y_direction == -1:
                self.rect.y = border_offset + 1
        if pygame.sprite.spritecollideany(self, vertical_borders):
            if self.x_direction == 1:
                if self.orientation == "leftward":
                    self.rect.x = WIN_WIDTH//2 - self.rect.width - 1
                else:
                    self.rect.x = WIN_WIDTH - self.rect.width - border_offset - 1
            elif self.x_direction == -1:
                if self.orientation == "leftward":
                    self.rect.x = border_offset + 1
                else:
                    self.rect.x = WIN_WIDTH//2 + 1
        
        if x > 0: 
            self.x_direction = 1 
        elif x < 0:
            self.x_direction = -1
        if y > 0: 
            self.y_direction = 1 
        elif y < 0:
            self.y_direction = -1


class HeroA(Base_Hero):
    thumbnail = load_image("heroA_thumbnail.jpg", -1) #must be 300x300

    def __init__(self, control_config, orientation):
        super().__init__(control_config, orientation, HeroA.thumbnail)
        self.max_xp = 100
        self.y_step = 8

    def update(self, *args):
        keys = args[0]
        super().update(keys)
        print(self.x_direction, self.y_direction)


class HeroB(Base_Hero):
    thumbnail = load_image("heroA_thumbnail.jpg", -1) #must be 300x300

    def __init__(self, control_config, orientation):
        super().__init__(control_config, orientation, HeroB.thumbnail)
        self.max_xp = 100

    def update(self, *args):
        keys = args[0]
        super().update(keys)

    #создает стенку которая отражает пули (добавляем в group для коллизии движения и отдельную  группу для коллизии пули)