import pygame as pg
import time
from math import *

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
display = pg.display.set_mode((width, height), pg.FULLSCREEN)
surf_map = pg.Surface(MAP_SIZE_SURF)
clock = pg.time.Clock()
player = Player()
pg.mouse.set_visible(False)
flat = pg.image.load('nebo2.png')
blocksActive = {
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

countOfDraw = 0
enableMoving = True

menu = Menu()
drawing = Drawing(display, surf_map)

def menuFalse():
    global menuActive
    menuActive = False

menu.add_option('Continue', menuFalse)
menu.add_option('Restart', lvlSwitch)
menu.add_option(f'Pixels per ray: {settings.numRays}', lambda: print(settings.numRays))
menu.add_option('FullScreen', fullscreenSwicth)
menu.add_option('Quit', quit)
keyMultiDown = True
menuActive = False

while True:

    key2 = pg.key.get_pressed()

    tmpPosX = player.x
    tmpPosY = player.y

    # от "Приложение не отвечает"
    for event in pg.event.get():
        if event.type == pg.QUIT:
            quit()

    player.delta = delta_time()
    move_thread = threading.Thread(target=player.move, args=(enableMoving,) ,name='move_thread')
    move_thread.start()

    display.fill((0, 0, 0))

    drawing.bg()

    pg.draw.circle(display, pg.Color("yellow"), (player.x, player.y), 0)

    drawing.world(player)

    #Minimap
    mini_map_thread = threading.Thread(target=drawing.mini_map, args=(player,), name='MiniMap')
    mini_map_thread.start()



    drawing.info(clock, player)

    clickAble = f2.render('Нажмите "SPACE" чтобы действовать', True, (255, 178, 213))


    # menu
    if event.type == pg.KEYDOWN:
        if pg.key.get_pressed()[pg.K_ESCAPE] and menuActive:
            menuActive = False
            t.sleep(0.1)
        elif pg.key.get_pressed()[pg.K_ESCAPE] and not menuActive:
            menuActive = True
            menu.current_option_index = 0

    if pg.key.get_pressed()[pg.K_z]:
        try:
            if doubleBack != True:
                if countOfDraw > 0:
                    countOfDraw -= 1
                blockMapTextures[coloredBlocks[0]] = str(tempbackup[0])
                doubleBack = True
        except:
            pass


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


    doubleDrawOff = True
    # Убирание окраски
    for blockOnes in blockOne:
        if blockOnes[0] - 50 < player.x < blockOnes[0] + 120 and blockOnes[1] - 50 < player.y < blockOnes[1] + 120 and doubleDrawOff:
            display.blit(clickAble, (20, 250))
            blockClickAvaliable = True
            if blockClickAvaliable:
                if event.type == pg.MOUSEBUTTONDOWN and pg.mouse.get_pressed()[0]:
                    for bb in blockMapTextures:
                        if blockOnes == bb:
                            try:
                                blocksActive[blockOnes] = blockMapTextures[blockOnes]
                                blockMapTextures[blockOnes] = '1'
                                print(blocksActive)
                                print(len(blocksActive)-countOfDraw)
                                blockClickAvaliable = False
                                doubleDrawOff = False
                            except:
                                print('error in block color take')
        else:
            blockClickAvaliable = False

    for i in range(0, len(blockOne)):
        if blockOne[i] in blocksActive:
            blockOne.remove(blockOne[i])
            break

    # pos nearly block and drawing
    for blockNow in blockMapTextures:
        questBlock = False
        if blockNow[0] - 70 < player.x < blockNow[0] + 140 and blockNow[1] - 70 < player.y < blockNow[1] + 130 and doubleDrawOff:
            if event.type == pg.MOUSEBUTTONDOWN and pg.mouse.get_pressed()[2] and countOfDraw < len(blocksActive):
                if blockMapTextures[blockNow] == '4':
                    questBlock = True
                if questBlock == False:
                    tempbackup.clear()
                    coloredBlocks.clear()
                    tempbackup.append(blockMapTextures[blockNow])
                    blockMapTextures[blockNow] = blocksActive[list(blocksActive.keys())[countOfDraw]]
                    coloredBlocks.append(blockNow)
                    countOfDraw += 1
                    print(blocksActive)
                    doubleDrawOff = False
                    doubleBack = False


    # quest
    if doubleQuest == False:
        quest1()
    if timer == True:
        timeStop = t.time()


    clock.tick(0)
    pg.display.flip()


