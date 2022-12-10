import pygame as pg
import time
from math import *

import asyncio
import random as rn
import main
import ray_casting
import settings
from settings import *
from player import Player
from func import *
import ray_casting
import levels
import time as t
from drawing import Drawing
import threading

pg.init()
f1 = pg.font.Font(None, 80)
f2 = pg.font.Font(None, 30)

tempbackup = []
coloredBlocks = []
display = pg.display.set_mode((width, height), pg.RESIZABLE)
surf_map = pg.Surface(MAP_SIZE_SURF)
clock = pg.time.Clock()
player = Player()
pg.mouse.set_visible(False)
blocksActive = {
}
blocks_draw_avaliable = {
}
blockClickAvaliable = False
doubleQuest = False
timer = True
fullscreenActive = True

pg.display.set_caption('2.5D GAME')

#Экран загрузки + Управлениеs
# text1 = f1.render('WASD - Ходьба', True, (180, 0, 0))
# text2 = f1.render('Стрелки влево, вправо - Камера', True, (180, 0, 0))
# display.blit(text1, (half_width // 2.5, half_height-100))
# display.blit(text2, (half_width // 2.5, half_height+100))
# pg.display.update()
#
# time.sleep(3)

uiSurf = pg.Surface((128,128))
countOfDraw = 0
enableMoving = True

menu = Menu()
drawing = Drawing(display, surf_map)

minimapActive = True
def close():
    quit()
def menuFalse():
    global menuActive
    menuActive = False
def minimapSwitch():
    global minimapActive
    if minimapActive == False:
        minimapActive = True
    else:
        minimapActive = False

menu.add_option('Continue', menuFalse)
menu.add_option('Restart', lvlSwitch)
menu.add_option(f'Pixels per ray: {settings.numRays}', lambda: print(settings.numRays))
menu.add_option('FullScreen', fullscreenSwicth)
menu.add_option('Minimap', minimapSwitch)
menu.add_option('Quit', close)
keyMultiDown = True
menuActive = False

doubleBack = True
tempbackup_color = []
block_in_bag = []
timeTimer = t.perf_counter()
runningGame = True
timerFrame = 0
timerSeconds = 0

while runningGame:
    fps = clock.get_fps()+1
    if settings.textMap == levels.levelsList['5']:
        if timerFrame / fps > 3:
            randomColorBlockMap(settings.textMap)
            timerFrame = 0
    if settings.textMap == levels.levelsList['6']:
        if timerFrame / fps > 2:
            randomColorBlockMap(settings.textMap)
            timerFrame = 0
    key2 = pg.key.get_pressed()

    # от "Приложение не отвечает"
    for event in pg.event.get():
        if event.type == pg.QUIT:
            quit()

    player.delta = delta_time()
    player.move(enableMoving)

    display.fill((0, 0, 0))

    drawing.bg()

    pg.draw.circle(display, pg.Color("yellow"), (player.x, player.y), 0)

    drawing.world(player)

    #Minimap
    if minimapActive == True:
        drawing.mini_map(player)
    else:
        pass

    drawing.info(clock, player)

    

    # menu
    if event.type == pg.KEYDOWN:
        if pg.key.get_pressed()[pg.K_ESCAPE] and menuActive:
            menuActive = False
            t.sleep(0.1)
        elif pg.key.get_pressed()[pg.K_ESCAPE] and not menuActive:
            menuActive = True
            menu.current_option_index = 0

    if pg.key.get_pressed()[pg.K_z]:
        if doubleBack != True:
            try:
                if not len(block_in_bag) >= 3:
                    if countOfDraw > 0:
                        countOfDraw -= 1
                    prev_col = blockMapTextures[coloredBlocks[0]]
                    blockMapTextures[coloredBlocks[0]] = str(tempbackup[0])
                    block_in_bag.append(str(tempbackup_color[0]))
                    blocks_draw_avaliable[list(blocksActive.keys())[-1]] = str(tempbackup_color[0])
                    print('blocks_draw_avaliable : ',blocks_draw_avaliable)
                    print('block_in_bag : ',block_in_bag)
                    doubleBack = True
                else:
                    display.blit(ui['wrong'],(1500-55, 725))
            except:
                print("_________________________")
                print("Error in color back")
                print("_________________________")


    doubleDrawOff = True
    # Убирание окраски
    for blockOnes in blockOne:
        if blockOnes[0]-blockSize//2 < player.x < blockOnes[0] + blockSize * 1.5 and blockOnes[1] < player.y < blockOnes[1] + blockSize or \
        blockOnes[1] - blockSize // 2 < player.y < blockOnes[1] + blockSize * 1.5 and blockOnes[0] < player.x <blockOnes[0] + blockSize:
            if doubleDrawOff:
                display.blit(pg.transform.scale(ui['mouse1'],(ui['mouse1'].get_width()//2, ui['mouse1'].get_height()//2)), (70, 750))
                blockClickAvaliable = True
                if blockClickAvaliable and not len(block_in_bag) >= 3:
                    if event.type == pg.MOUSEBUTTONDOWN and pg.mouse.get_pressed()[0]:
                        for bb in blockMapTextures:
                            if blockOnes == bb:
                                try:
                                    block_in_bag.append(blockMapTextures[blockOnes])
                                    blocksActive[blockOnes] = blockMapTextures[blockOnes]
                                    blocks_draw_avaliable[blockOnes] = blockMapTextures[blockOnes]
                                    blockMapTextures[blockOnes] = '1'
                                    print('blocksActive : ',blocksActive)
                                    print('active : ', len(blocksActive)-countOfDraw)
                                    blockClickAvaliable = False
                                    doubleDrawOff = False
                                except:
                                    print("_________________________")
                                    print('Error in block color take')
                                    print("_________________________")
        else:
            blockClickAvaliable = False

    for i in range(0, len(blockOne)):
        if blockOne[i] in blocksActive:
            blockOne.remove(blockOne[i])
            break

    # display active blocks
    k = 0
    for color in block_in_bag:
        display.blit(pg.transform.scale(ui[str(color)],(ui[str(color)].get_width()//2, ui[str(color)].get_height()//2)), (1500 - k*20, 750))
        k+=1

    # pos nearly block and drawing
    for blockNow in blockMapTextures:
        questBlock = False
        if (blockNow[0] - blockSize // 2 < player.x < blockNow[0] + blockSize * 1.5 and blockNow[1] < player.y < blockNow[1] + blockSize) or \
        (blockNow[1] - blockSize // 2 < player.y < blockNow[1] + blockSize * 1.5 and blockNow[0] < player.x < blockNow[0] + blockSize):
            if countOfDraw < len(blocksActive) and doubleDrawOff:
                display.blit(
                    pg.transform.scale(ui['mouse2'], (ui['mouse2'].get_width() // 2, ui['mouse2'].get_height() // 2)),
                    (130, 750))
                if event.type == pg.MOUSEBUTTONDOWN and pg.mouse.get_pressed()[2]:
                    if blockMapTextures[blockNow] == '<':
                        questBlock = True
                    if questBlock == False:
                        tempbackup_color.clear()
                        tempbackup.clear()
                        coloredBlocks.clear()
                        block_in_bag.pop(-1) 
                        tempbackup.append(blockMapTextures[blockNow])
                        tempbackup_color.append(blocks_draw_avaliable[list(blocks_draw_avaliable.keys())[-1]])
                        print('tempbackup_color : ', tempbackup_color)
                        # blockMapTextures[blockNow] = blocksActive[list(blocksActive.keys())[countOfDraw]]
                        blockMapTextures[blockNow] = blocks_draw_avaliable[list(blocks_draw_avaliable.keys())[-1]]
                        coloredBlocks.append(blockNow)
                        blocks_draw_avaliable.pop(list(blocks_draw_avaliable.keys())[-1])
                        countOfDraw += 1         
                        doubleDrawOff = False
                        doubleBack = False


    if menuActive:
        enableMoving = False
        pg.mouse.set_visible(True)
        pg.draw.rect(display, (9, 5, 5), (0, 0, width, height))
        menu.draw(display, half_width//2, 100, 75)
        keyMenu = pg.key.get_pressed()
        if keyMultiDown:
            if keyMenu[pg.K_DOWN]:
                menu.switch(1)
                keyMultiDown = False
                timing = t.time()
            if keyMenu[pg.K_UP]:
                menu.switch(-1)
                keyMultiDown = False
                timing = t.time()
            if keyMenu[pg.K_RETURN]:
                menu.select()
                keyMultiDown = False
                timing = t.time()
        else:
            if t.time() - timing > 0.18:
                keyMultiDown = True

    else:
        pg.mouse.set_visible(False)
        enableMoving = True

    # quest
    quest(numOfLvl)
    if timer == True:
        timeStop = t.time()

    timerFrame+=1
    clock.tick(60)
    pg.display.flip()


