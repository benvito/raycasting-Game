import pygame as pg
import time
from math import *

import main
from ray_casting import *
from settings import *
pg.font.init()
f1 = pg.font.Font(None, 80)

cur_time = time.time_ns()
def delta_time():
    global cur_time
    delta = (time.time_ns() - cur_time) / 1000000000
    cur_time = time.time_ns()
    return delta

class Menu:
    def __init__(self):
        self.option_surface = []
        self.callbacks = []
        self.current_option_index = 0

    def add_option(self, option, callback):
        self.option_surface.append(f1.render(option, True, (255, 255, 255)))
        self.callbacks.append(callback)

    def switch(self, direction):
        self.current_option_index = max(0, min(self.current_option_index + direction, len(self.option_surface) - 1))

    def select(self):
        self.callbacks[self.current_option_index]()

    def draw(self, surf, x, y, option_y):
        for i, option in enumerate(self.option_surface):
            option_rect = option.get_rect()
            option_rect.topleft = (x, y + i * option_y)
            if i == self.current_option_index:
                pg.draw.rect(surf, (0, 100, 0), option_rect)
            surf.blit(option, option_rect)

