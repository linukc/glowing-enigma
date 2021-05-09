import pygame
from config import *
from utils import load_image
import random

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


class Particle(pygame.sprite.Sprite):
    fire = [load_image("star.png", -1)]
    for scale in (10, 15, 20):
        fire.append(pygame.transform.scale(fire[0], (scale, scale)))

    def __init__(self, pos, dx, dy, screen_rect):
        super().__init__(all_sprites)
        self.add(particles_sprites)
        self.image = random.choice(self.fire)
        self.rect = self.image.get_rect()
        self.screen_rect = screen_rect

        self.velocity = [dx, dy]
        self.rect.x, self.rect.y = pos

        self.gravity = 0.7

    def update(self, *args):
        self.velocity[1] += self.gravity

        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

        if not self.rect.colliderect(self.screen_rect):
            self.kill()


class CountDown(pygame.sprite.Sprite):
    def __init__(self, x, y): # x and y - axis of symmetry
        super().__init__(all_sprites)
        self.add(countdown_sprite)
        self.x = x
        self.y = y
        self.frames = []
        self.current_frame = 0
        self.cut_sheet(load_image("countdown.jpg"), 5, 1)
        self.frames.append(load_image("start.jpg", -1))

        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.x = self.x - self.rect.width // 2
        self.rect.y = self.y - self.rect.height // 2

        self.start_time = pygame.time.get_ticks()

    def cut_sheet(self, sheet, columns, rows):
        rect = pygame.Rect(0, 0, sheet.get_width() // columns, 
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (rect.w * i, rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, rect.size)))

    def update(self, *args):
        if pygame.time.get_ticks() - self.start_time >= 1000:
            self.current_frame += 1
            self.image = self.frames[min(self.current_frame, 5)]
            self.start_time = pygame.time.get_ticks()

        if self.current_frame == 6:
            self.kill()


def create_particles(position, screen_rect):
    particle_count = 20
    numbers = range(-5, 6)
    for _ in range(particle_count):
        Particle(position, random.choice(numbers), random.choice(numbers), screen_rect)