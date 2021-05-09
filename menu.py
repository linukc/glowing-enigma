import pygame
import sys

from config import *
from utils import load_image

TITLE_FONT = pygame.font.Font(None, 50)
TITLE_COLOR = WHITE
DESCRIPTION_FONT = pygame.font.Font(None, 25)
DESCRIPTION_COLOR = WHITE
FPS = 10

class Button(object):
    def __init__(self, 
                        surface, 
                        pos, 
                        size=(100, 50), 
                                text="button", 
                                borders_color=WHITE, 
                                font_color=WHITE, 
                                bg_color=BLACK):

        self.base_surface = surface #window surface
        self.pos = pos #upper left corner
        self.size = size
        self.text = text
        self.font = pygame.font.Font(None, 25)
        self.borders_color = borders_color
        self.font_color = font_color
        self.bg_color = bg_color
        self._is_pressed = False

        self.surface = pygame.Surface(size) 
        self.rect = self.surface.get_rect()
        self.g_rect = self.rect.move(self.pos) #rect in global window's frame; for collide
        self.draw()

    def draw(self):
        text = self.font.render(self.text, 1, self.font_color)
        text_w = text.get_width()
        text_h = text.get_height()
        text_x = self.rect.width // 2 - text.get_width() // 2
        text_y = self.rect.height // 2 - text.get_height() // 2

        self.surface.fill(self.bg_color)
        self.surface.blit(text, (text_x, text_y))
        pygame.draw.rect(self.surface, self.borders_color, self.rect, width=3)
        self.base_surface.blit(self.surface, self.pos)

    def update(self, *args):
        if (args and args[0].type == pygame.MOUSEBUTTONDOWN and 
                    self.g_rect.collidepoint(args[0].pos)):
            self._is_pressed = True

    def pressed(self):
        return self._is_pressed


def arrange_content(surface, text, width_border, image):
    title_height = 0.05* WIN_HEIGHT
    thumbnail_height = 0.1* WIN_HEIGHT
    description_height = 0.6* WIN_HEIGHT

    #title
    string_rendered = TITLE_FONT.render(text.get('title'), 1, TITLE_COLOR)
    string_rect = string_rendered.get_rect().move((width_border, title_height))
    surface.blit(string_rendered, string_rect)

    #image
    surface.blit(image, image.get_rect().move((width_border, thumbnail_height)))

    #description
    for i, line in enumerate(text.get('description')):
        string_rendered = DESCRIPTION_FONT.render(line, 1, DESCRIPTION_COLOR)
        string_rect = string_rendered.get_rect().move((width_border, description_height+i*20))
        surface.blit(string_rendered, string_rect)
    

def start_screen(surface, heroA, heroB):
    
    game_config = {"left_player_mode": None,
                   "right_player_mode": None}

    left_player_text = {"title": "Игрок 1",
                        "description": ["1 Способность (клавиша R):",
                                        "Стреляет с перезарядкой в 1 секунду; Урон 10",
                                        "2 Способность (клавиша T):",
                                        "Раз в 7 секунд создает несколь дист. бомб; Урон 20",
                                        "Чтобы перемещать героя", "нажимайте клавишы W A S D"]}

    right_player_text = {"title": "Игрок 2",
                        "description": ["1 Способность (клавиша 1NUM):",
                                        "Стреляет с перезарядкой в 1 секунду; Урон 10",
                                        "2 Способность (клавиша 2NUM):",
                                        "описание 2",
                                        "Раз в 7 секунд создает несколь дист. бомб; Урон 20",
                                        "P.S NUM это цифры справа от стрелок"]}

    arrange_content(surface, text=left_player_text, width_border=0.05*WIN_WIDTH, image=heroA.thumbnail)
    arrange_content(surface, text=right_player_text, width_border=0.55*WIN_WIDTH, image=heroB.thumbnail)
    pygame.display.flip()

    button_left_single = Button(surface, (0.1*WIN_WIDTH, 0.9*WIN_HEIGHT), text="Игрок")
    button_left_auto = Button(surface, (0.1*WIN_WIDTH + button_left_single.rect.width + 50, 0.9*WIN_HEIGHT), text="Бот")
    button_right_single = Button(surface, (0.6*WIN_WIDTH, 0.9*WIN_HEIGHT), text="Игрок")
    button_right_auto = Button(surface, (0.6*WIN_WIDTH + button_right_single.rect.width + 50, 0.9*WIN_HEIGHT), text="Бот")

    left_group = (button_left_single, button_left_auto)
    right_group = (button_right_single, button_right_auto)

    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

            button_left_single.update(event)
            button_left_auto.update(event)
            button_right_single.update(event)
            button_right_auto.update(event)

        if not game_config.get("left_player_mode"):
            if button_left_single.pressed():
                game_config["left_player_mode"] = "player"
            elif button_left_auto.pressed():
                game_config["left_player_mode"] = "auto"
            
        if not game_config.get("right_player_mode"):
            if button_right_single.pressed():
                game_config["right_player_mode"] = "player"
            elif button_right_auto.pressed():
                game_config["right_player_mode"] = "auto"

        if game_config.get("left_player_mode") and game_config.get("right_player_mode"):
            running = False

        pygame.display.update([button_left_single.g_rect,
                               button_left_auto.g_rect,
                               button_right_single.g_rect,
                               button_right_auto.g_rect])
        clock.tick(FPS)

    return game_config
