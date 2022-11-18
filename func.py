import pygame as pg
import time
from math import *
from threading import Timer
import time as t

import levels
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

def lvlSwitch():
    import levels
    settings.textMap = levels.levelsList[str(settings.numOfLvl)]
    settings.initMap(settings.textMap)
    main.tempbackup.clear()
    main.coloredBlocks.clear()
    main.blocksActive.clear()
    main.countOfDraw = 0
    main.blockClickAvaliable = 0
    main.player.x = 160
    main.player.y = 140
    main.menuFalse()

def quest1():
    tmp = []
    for blockNeed in blockQuest:
        if blockQuest[blockNeed] == '5':
            if blockMapTextures[blockNeed] == '3':
                tmp.append(1)
        if blockQuest[blockNeed] == '6':
            if blockMapTextures[blockNeed] == '2':
                tmp.append(2)
    if 1 in tmp and 2 in tmp:
        lvlSwitchText = f1.render('Great job! Switching level...', None, (151, 153, 255))
        main.display.blit(lvlSwitchText, (half_width / 2, half_height))
        main.timer = False
        if t.time() - main.timeStop > 2:
            main.doubleQuest = True
            settings.numOfLvl += 1
            lvlSwitch()
        return True
    else:
        main.doubleQuest = False
        return False


