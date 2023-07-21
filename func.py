import pygame as pg
import time
from math import *
from threading import Timer

import settings
import pygame.event
import time as t

import json as js

import random as rn

import levels
import main
from ray_casting import *
from settings import *
pg.font.init()
f1 = pg.font.Font(None, 80)

lvlSwitches = False

cur_time = time.time_ns()

level5_quest = set()

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

def toBlack():
    settings.textures['2'] = pygame.image.load('textures/colorYellowWallBlack.png').convert()
    settings.textures['3'] =  pygame.image.load('textures/colorBlueWallBlack.png').convert()
    settings.textures['4'] =  pygame.image.load('textures/colorRedWallBlack.png').convert()
    settings.textures['5'] =  pygame.image.load('textures/colorGreenWallBlack.png').convert()
    settings.textures['<'] =  pygame.image.load('textures/robotBlack.png').convert()
    ui['3'] = pygame.image.load("textures/blue_uiBlack.png")
    ui['2'] = pygame.image.load("textures/yellow_uiBlack.png")
    ui['4'] = pygame.image.load("textures/red_uiBlack.png")
    ui['5'] = pygame.image.load("textures/green_uiBlack.png")

def toColor():
    settings.textures['2'] = pygame.image.load('textures/colorYellowWall.png').convert()
    settings.textures['3'] =  pygame.image.load('textures/colorBlueWall.png').convert()
    settings.textures['4'] =  pygame.image.load('textures/colorRedWall.png').convert()
    settings.textures['5'] =  pygame.image.load('textures/colorGreenWall.png').convert()
    settings.textures['<'] =  pygame.image.load('textures/robot.png').convert()
    ui['3'] = pygame.image.load("textures/blue_ui.png")
    ui['2'] = pygame.image.load("textures/yellow_ui.png")
    ui['4'] = pygame.image.load("textures/red_ui.png")
    ui['5'] = pygame.image.load("textures/green_ui.png")

def lvlSwitch():
    settings.textMap = levels.levelsList[str(settings.numOfLvl)]
    with open("game/settings/settings.json", 'w') as f:
        settings.sett['numL'] = settings.numOfLvl
        js.dump(settings.sett, f)
    print(settings.numOfLvl)
    main.tempbackup.clear()
    main.coloredBlocks.clear()
    main.blocksActive.clear()
    main.tempbackup_color.clear()
    main.block_in_bag.clear()
    main.blocks_draw_avaliable.clear()
    main.countOfDraw = 0
    main.blockClickAvaliable = 0
    if settings.numOfLvl == 1:
        main.player.x = 500
        main.player.y = 480
    elif settings.numOfLvl == 2:
        main.player.x = 250
        main.player.y = 300
        toColor()
    elif settings.numOfLvl == 3:
        main.player.x = 2250
        main.player.y = 150
        toColor()
    elif settings.numOfLvl == 9:
        main.player.x = 160
        main.player.y = 150
        toBlack()
    elif settings.numOfLvl == 10:
        main.player.x = 500
        main.player.y = 480
        toColor()
    else:   
        main.player.x = 160
        main.player.y = 150
        toColor()
    main.menuFalse()
    settings.initMap(settings.textMap)
def restart():
    main.display.blit(ui[f'lvl{settings.numOfLvl}'], (0,0))
    if pg.key.get_pressed()[pg.K_SPACE]: 
        main.restartBool = False
        lvlSwitch()
        

def switcher():  
    global lvlSwitches 
    main.display.blit(ui[f'lvl{settings.numOfLvl+1}'], (0,0))
    main.timer = False
    if pg.key.get_pressed()[pg.K_SPACE]:
        level5_quest.clear()
        main.doubleQuest = True 
        settings.numOfLvl += 1 
        lvlSwitch()
        main.timer = True
        level5_quest.clear()
        lvlSwitches = False
    

def quest(lvl):
    global lvlSwitches
    tmp = []
    for blockNeed in blockQuest:
        if blockQuest[blockNeed] == '@':
            if blockMapTextures[blockNeed] == '3':
                tmp.append(1)
                if settings.numOfLvl == 5:
                    level5_quest.add(1)
        if blockQuest[blockNeed] == '!':
            if blockMapTextures[blockNeed] == '2':
                tmp.append(2)
                if settings.numOfLvl == 5:
                    level5_quest.add(2)
                    
        if blockQuest[blockNeed] == '$':
            if blockMapTextures[blockNeed] == '4':
                tmp.append(3)
                if settings.numOfLvl == 5:
                    level5_quest.add(3)
        if blockQuest[blockNeed] == '%':
            if blockMapTextures[blockNeed] == '5':
                tmp.append(4)
                if settings.numOfLvl == 5:
                    level5_quest.add(4)
    if settings.numOfLvl <= 2:
        if len(tmp) >= 2:
            switcher()
            return True
        else:
            main.doubleQuest = False
            return False
    elif settings.numOfLvl == 4 or settings.numOfLvl == 3:
        if len(tmp) >= 3:
            switcher()
            return True
        else:
            main.doubleQuest = False
            return False
    elif settings.numOfLvl == 5:
        lvl5 = f1.render(f'Painted: {len(level5_quest)}/4', None, (151, 153, 255))
        main.display.blit(lvl5, (half_width/2-50, 20))
        if len(level5_quest) >= 4:
            switcher()
            return True
        else:
            main.doubleQuest = False
            return False
    elif settings.numOfLvl == 6 or settings.numOfLvl == 7:
        if len(tmp) >= 2:
            lvlSwitches = True
            switcher()  
            return True
        else:
            main.doubleQuest = False
            return False
    elif settings.numOfLvl == 8:
        if len(tmp) >= 3:
            lvlSwitches = True
            switcher()
            return True
        else:
            main.doubleQuest = False
            return False
    elif settings.numOfLvl == 9:
        if len(tmp) >= 4:
            switcher()
            return True
        else:
            main.doubleQuest = False
            return False
    elif settings.numOfLvl == 10:
        if len(tmp) >= 2:
            main.lastLvlCompl = True
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
                if (x*blockSize, y*blockSize) not in list(settings.blockQuest.keys()):
                    xy_original.append([x,y])
    xy_tmp = xy_original
    for y, row in enumerate(newTextMap):       
        for x, column in enumerate(row):
            if column != '.' and column != '<' and column != '$' and column != '%' and column != '@' and column != '!':
                if (x*blockSize, y*blockSize) not in list(settings.blockQuest.keys()):  
                    ch = rn.choice(textsForShuffle)
                    newTextMap[y][x] = ch
                    textsForShuffle.remove(ch)
                
    for row in newTextMap:
        generatedMap.append(''.join(row))

    initMap(generatedMap)
    


