import pygame as pg
import time
from math import *
from threading import Timer

import pygame.event
import time as t

import asyncio

import random as rn

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
            b = surf.blit(option, option_rect)
            pos = pygame.mouse.get_pos()
            if b.collidepoint(pos):
                self.current_option_index = i
                for event in pg.event.get():
                    if pg.mouse.get_pressed()[0]:
                        self.select()


def lvlSwitch():
    import levels
    settings.textMap = levels.levelsList[str(settings.numOfLvl)]
    settings.initMap(settings.textMap)
    main.tempbackup.clear()
    main.coloredBlocks.clear()
    main.blocksActive.clear()
    main.tempbackup_color.clear()
    main.block_in_bag.clear()
    main.blocks_draw_avaliable.clear()
    main.countOfDraw = 0
    main.blockClickAvaliable = 0
    main.player.x = 160
    main.player.y = 140
    main.menuFalse()

def quest(lvl):
    tmp = []
    if lvl == 1:
        for blockNeed in blockQuest:
            if blockQuest[blockNeed] == '@':
                if blockMapTextures[blockNeed] == '3':
                    tmp.append(1)
            if blockQuest[blockNeed] == '!':
                if blockMapTextures[blockNeed] == '2':
                    tmp.append(2)
    elif lvl == 2:
        for blockNeed in blockQuest:
                if blockQuest[blockNeed] == '$':
                    if blockMapTextures[blockNeed] == '4':
                        tmp.append(1)
                if blockQuest[blockNeed] == '%':
                    if blockMapTextures[blockNeed] == '5':
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

def fullscreenSwicth():
    if not main.fullscreenActive:
        main.display = pg.display.set_mode((width, height), pg.FULLSCREEN)
        main.fullscreenActive = True
        return
    if main.fullscreenActive:
        main.display = pg.display.set_mode((width, height), pg.RESIZABLE)
        main.fullscreenActive = False
        return

def keyMultiDownTimer():
    timing = t.time()
    if t.time() - timing > 2:
        main.keyMultiDown = True

def epilepcy(textMap):
    text = textMap
    words = []
    for row in text:
        words.append(row)
        for i, char in enumerate(map(list, words)):
            rn.shuffle(char)
            char[0],char[-1] = '1', '1'   
            words[i] = ''.join(char)
    initMap(words)

def randomColorBlockMap(textMap):
    timer = t.perf_counter()
    text = textMap
    newTextMap = []
    generatedMap = []
    for row in text:
        roww = []
        for column in row:
            roww.append(column)
        newTextMap.append(roww)
    textsForShuffle = []
    for row in text:
        for column in row:
            if column != '.' and column != '<' and column != '$' and column != '%' and column != '@' and column != '!':
                textsForShuffle.append(column)
    xy_original = []
    for y, row in enumerate(text):
        for x, column in enumerate(row):
            if column != '.' and column != '<' and column != '$' and column != '%' and column != '@' and column != '!':
                xy_original.append([x,y])
    xy_tmp = xy_original
    for y, row in enumerate(newTextMap):       
        for x, column in enumerate(row):
            if column != '.' and column != '<' and column != '$' and column != '%' and column != '@' and column != '!':
                ch = rn.choice(textsForShuffle)
                newTextMap[y][x] = ch
                textsForShuffle.remove(ch)

    for row in newTextMap:
        generatedMap.append(''.join(row))

    initMap(generatedMap)
    


