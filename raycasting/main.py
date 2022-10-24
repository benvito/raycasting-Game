import pygame as pg
import time
from math import *

import main
from settings import *
from player import Player
from func import *
from ray_casting import *
import time as t
pg.init()
f1 = pg.font.Font(None, 80)
f2 = pg.font.Font(None, 30)

display = pg.display.set_mode((width, height))
clock = pg.time.Clock()
player = Player()
pg.mouse.set_visible(False)
flat = pg.image.load('nebo2.png')
blocksActive = {
}
blockClickAvaliable = False

#Экран загрузки + Управлениеs
# text1 = f1.render('WASD - Ходьба', True, (180, 0, 0))
# text2 = f1.render('Стрелки влево, вправо - Камера', True, (180, 0, 0))
# display.blit(text1, (half_width // 2.5, half_height-100))
# display.blit(text2, (half_width // 2.5, half_height+100))
# pg.display.update()
#
# time.sleep(3)

countOfDraw = 0

menu = Menu()

def menuFalse():
    global menuActive
    menuActive = False


menu.add_option('Continue', menuFalse)
menu.add_option(f'Pixels per ray: {numRays}', lambda: print(numRays))
menu.add_option('Quit', quit)

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
    player.move()

    display.fill((0, 0, 0))

    #Небо
    pg.draw.rect(display, (9,5,5), (0,0, width, half_height))

    #display.blit(flat, (0, 0, width, half_height))


    #Пол
    pg.draw.rect(display, (9,5,5), (0, half_height, width, half_height))


    minimapTempPlayer = pg.draw.circle(display, pg.Color("yellow"), (player.x, player.y), 0)


    rayCasting(display, player, minimapTempPlayer)

    plPos = pg.draw.circle(display, pg.Color(12,169,11), (minimapTempPlayer.x // 8, minimapTempPlayer.y // 8), 2)
    pg.draw.circle(display, pg.Color(12,169,11), (minimapTempPlayer.x // 8, minimapTempPlayer.y // 8), 5)

    for x,y in blockMap:
        minimapTempMap = pg.draw.rect(display, pg.Color('gray'), (x // 8, y // 8, blockSize // 8, blockSize // 8), 0)
        if minimapTempMap.colliderect(plPos):
            player.x = tmpPosX
            player.y = tmpPosY



    pg.display.set_caption('2.5D GAME')

    fps = f2.render(("FPS: " + str(int(clock.get_fps()))), True, (114,160,193))
    positions = f2.render(("   X:   " + str(int(player.x)) + "   Y:   " + str(int(player.y))), True, (114, 160, 193))
    speedHud = f2.render(('Speed:  ' + str(player.speed)), True, (114, 160, 193))
    clickAble = f2.render('Нажмите "SPACE" чтобы действовать', True, (255,178,213))
    display.blit(fps, (1500,10))
    display.blit(positions, (1400,30))
    display.blit(speedHud, (1465,50))


    # menu
    if event.type == pg.KEYDOWN:
        if pg.key.get_pressed()[pg.K_ESCAPE] and menuActive:
            menuActive = False
        elif pg.key.get_pressed()[pg.K_ESCAPE] and not menuActive:
            menuActive = True
            menu.current_option_index = 0

    if menuActive:
        pg.draw.rect(display, (9, 5, 5), (0, 0, width, height))
        menu.draw(display, half_width//2, 100, 75)
        if event.type == pg.KEYDOWN:
            if pg.key.get_pressed()[pg.K_DOWN]:
                menu.switch(1)
            if pg.key.get_pressed()[pg.K_UP]:
                menu.switch(-1)
            if pg.key.get_pressed()[pg.K_RETURN]:
                menu.select()
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
                            blocksActive[blockOnes] = blockMapTextures[blockOnes]
                            blockMapTextures[blockOnes] = '1'
                            print(blocksActive)
                            blockClickAvaliable = False
                            doubleDrawOff = False
        else:
            blockClickAvaliable = False

    for i in range(0, len(blockOne)):
        if blockOne[i] in blocksActive:
            blockOne.remove(blockOne[i])
            break

    # pos nearly block and drawing
    for blockNow in blockMapTextures:
        if blockNow[0] - 70 < player.x < blockNow[0] + 140 and blockNow[1] - 70 < player.y < blockNow[1] + 130 and doubleDrawOff:
            if event.type == pg.MOUSEBUTTONDOWN and pg.mouse.get_pressed()[2] and countOfDraw < len(blocksActive):
                blockMapTextures[blockNow] = blocksActive[list(blocksActive.keys())[countOfDraw]]
                countOfDraw += 1
                print(blocksActive)
                doubleDrawOff = False



    clock.tick(0)
    pg.display.flip()


