import pygame
import random
from config import *
from utils import load_image


class Bullet(pygame.sprite.Sprite):
    image = load_image("bullet.png")

    def __init__(self, pos, orientation, opponent):
        super().__init__(all_sprites)
        self.add(bullets_sprites)
        self.image = Bullet.image
        self.orientation = orientation
        self.opponent = opponent
        if self.orientation == "rightward": #original image looks left to right
            self.image = pygame.transform.flip(self.image, True, False)
        self.image = pygame.transform.scale(self.image, (30, 10))
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.vx = 20

    def update(self, *args):
        if self.orientation == "leftward":
            self.rect = self.rect.move((self.vx, 0))
        else:
            self.rect = self.rect.move((-self.vx, 0))
        
        if pygame.sprite.spritecollideany(self, self.opponent):
            self.opponent.sprite.xp -= 20
            self.kill()


class Base_Hero(pygame.sprite.Sprite):

    def __init__(self, control_config, orientation, thumbnail):
        super().__init__(all_sprites)
        self.add(heroes_sprites)
        self.control_config = control_config
        self.mode = "player"
        self.locked = False

        self.up = control_config.get("up")
        self.down = control_config.get("down")
        self.right = control_config.get("right")
        self.left = control_config.get("left")

        self.first_cast = control_config.get("first_cast")
        self.first_cast_pressed = pygame.time.get_ticks()

        self.second_cast = control_config.get("second_cast")
        self.third_cast = control_config.get("third_cast")

        self.orientation = orientation
        self.thumbnail = thumbnail
        if orientation == "rightward": #original image looks left to right
            self.thumbnail = pygame.transform.flip(self.thumbnail, True, False)
        self.image = pygame.transform.scale(self.thumbnail, (100, 100))
        self.rect = self.image.get_rect()

        if orientation == "leftward": #player 1
            self.rect.x = 20
            self.rect.y = 30
        else: #player 2
            self.rect.x = 0.875*WIN_WIDTH
            self.rect.y = 0.8*WIN_HEIGHT

        self.x_step = 5
        self.y_step = 5

        #for collidence with borders
        self.x_direction = 1 # 1 if moved along x axes else -1;
        self.y_direction = 1 # 1 if moved along y axes else -1;
        self.max_xp = 100 #1,2,5,10,20,25,50,100
        self.xp = self.max_xp

    def get_opponent(self):
        return [sprite for sprite in heroes_sprites.sprites() if sprite != self][0] #only 2 heroes

    def lock(self):
        self.locked = True

    def unlock(self):
        self.locked = False

    def update(self, *args):

        keys = args[0]
        #XP bar
        pygame.draw.rect(self.image, WHITE, (0, 0, self.rect.width, 10), border_radius=2)
        pygame.draw.rect(self.image, RED, (0, 0, self.xp*(self.rect.width/self.max_xp), 10), border_radius=2)
        pygame.draw.rect(self.image, BLACK, (0, 0, self.rect.width, 10), width=1, border_radius=2)

        #base cast (shot)
        if keys[self.first_cast] and not self.locked:
            time = pygame.time.get_ticks()
            if time - self.first_cast_pressed > 1000:
                if self.orientation == "leftward":
                    Bullet((self.rect.x+self.rect.width, self.rect.y+self.rect.height//2), self.orientation, 
                        pygame.sprite.GroupSingle(self.get_opponent()))
                else:
                    Bullet((self.rect.x, self.rect.y+self.rect.height//2), self.orientation, 
                        pygame.sprite.GroupSingle(self.get_opponent()))
                self.first_cast_pressed = time

        x = 0
        y = 0
        #movements
        if self.mode == "player" and not self.locked:
            x = self.x_step * (keys[self.right] - keys[self.left])
            y = self.y_step* (keys[self.down] - keys[self.up])
        elif not self.locked:#auto
            x = 0
            delta_y = self.rect.y - self.get_opponent().rect.y
            y = -self.y_step if delta_y>self.y_step else (self.y_step if delta_y<-self.y_step else 0) #if elif else

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
        if self.mode == "player":
            self.y_step = 8

    def update(self, *args):
        keys = args[0]
        events = args[1]
        super().update(keys)


class HeroB(Base_Hero):
    thumbnail = load_image("heroA_thumbnail.jpg", -1) #must be 300x300

    def __init__(self, control_config, orientation):
        super().__init__(control_config, orientation, HeroB.thumbnail)
        self.max_xp = 100
        if self.mode == "player":
            self.y_step = 8

    def update(self, *args):
        keys = args[0]
        events = args[1]
        super().update(keys)