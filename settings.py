from math import *
import pygame.image
import pygame
import levels
import json as js

# 1 - white
# 2 - yellow
# 3 - blue
# 4 - color quest guy
# 5 - need blue(3)
# 6 - need yellow(2)
# 7 - red
# 8 - blue


pygame.init()

try:
    with open("game/settings/settings.json", 'r') as f:
        sett = js.load(f)
except:
    with open("game/settings/settings.json", 'w') as f:
        sett = {
            'FOV' : pi / 2,
            'numRays' : 400,
            'MAPSCALE' : 10,
            'numL' : 1,
            'mouse_sensivity' : 0.15
        }
        js.dump(sett, f)

numOfLvl = sett['numL']
textMap = levels.levelsList[str(numOfLvl)]


mouse_sensivity = sett['mouse_sensivity']

maxSize = pygame.display.Info()

width = 1600
height = 900
half_width = width / 2
half_height = height / 2

pygame.display.set_mode((width, height), pygame.FULLSCREEN)

blockSize = 100
rangeColBlock = blockSize//2
rangeColBlockPlus = blockSize*2

MAPSCALE = sett['MAPSCALE']
MAPPOS = (0, 0)
MAP_SIZE_SURF = (width//MAPSCALE*1.5, height//MAPSCALE*1.55)
MAP_BLOCK_SIZE = blockSize//MAPSCALE

mapWidth = len(textMap[0])
mapHeight = len(textMap)

blockMapTextures = {

}

mini_map = set()

blockMap = set()
yBlockPos = 0
blockOne = list()
blockQuest = {

}
collision_walls = []
collision_walls_draw = []

def initMap(textMap):
    blockMap.clear()
    blockQuest.clear()
    blockMapTextures.clear()
    blockOne.clear()
    mini_map.clear()
    collision_walls.clear()
    yBlockPos = 0
    for row in textMap:
        xBlockPos = 0
        for column in list(row):
            if column != '.':
                blockMap.add((xBlockPos, yBlockPos))
                mini_map.add((xBlockPos // MAPSCALE, yBlockPos // MAPSCALE))
                blockMapTextures[(xBlockPos, yBlockPos)] = column
                collision_walls.append(pygame.Rect(xBlockPos, yBlockPos, blockSize, blockSize))
            if column == '2' or column == '3' or column == '4' or column == '5' or column == 'o':
                blockOne.append((xBlockPos, yBlockPos))
            if column == '!' or column == '@' or column == '$' or column == '%':
                blockQuest[(xBlockPos, yBlockPos)] = column
            xBlockPos += blockSize
        yBlockPos += blockSize
initMap(textMap)

FOV = sett['FOV']
halfFOV = FOV / 2
maxDepth = width // blockSize
numRays = sett['numRays']
deltaRays = FOV / (numRays - 1)
dist = numRays / (2 * tan(halfFOV))
coef = dist * blockSize * 2400//numRays
scale = width // numRays
depthCoef = 2




textureSize = 512
textureScale = textureSize // blockSize

textures = {
            '1': pygame.image.load('textures/colorWhiteWall.png').convert(),
            '2': pygame.image.load('textures/colorYellowWall.png').convert(),
            '3': pygame.image.load('textures/colorBlueWall.png').convert(),
            '4': pygame.image.load('textures/colorRedWall.png').convert(),
            '5': pygame.image.load('textures/colorGreenWall.png').convert(),
            '<': pygame.image.load('textures/robot.png').convert(),
            '!': pygame.image.load('textures/blockWallNeedYellow.png').convert(),
            '@': pygame.image.load('textures/blockWallNeedBlue.png').convert(),
            '$': pygame.image.load('textures/blockWallNeedRed.png').convert(),
            '%': pygame.image.load('textures/blockWallNeedGreen.png').convert(),
            'o': pygame.image.load('textures/blockNumberOne.png').convert(),
            }

ui = {
    'mouse1' : pygame.image.load("textures/mouse1_button.png"),
    'mouse2' : pygame.image.load("textures/mouse2_button.png"),
    'mouse3' : pygame.image.load("textures/mouse3_button.png"),
    '3' : pygame.image.load("textures/blue_ui.png"),
    '2' : pygame.image.load("textures/yellow_ui.png"),
    '4' : pygame.image.load("textures/red_ui.png"),
    '5' : pygame.image.load("textures/green_ui.png"),
    'wrong' : pygame.image.load("textures/wrong_ui.png"),
    'lvl1' : pygame.image.load("textures/lvl1_guide.png"),
    'lvl2' : pygame.image.load("textures/lvl2_guide.png"),
    'lvl3' : pygame.image.load("textures/lvl3_guide.png"),
    'lvl4' : pygame.image.load("textures/lvl4_guide.png"),
    'lvl5' : pygame.image.load("textures/lvl5_guide.png"),
    'lvl6' : pygame.image.load("textures/lvl6_guide.png"),
    'lvl7' : pygame.image.load("textures/lvl7_guide.png"),
    'lvl8' : pygame.image.load("textures/lvl8_guide.png"),
    'lvl9' : pygame.image.load("textures/lvl9_guide.png"),
    'lvl10' : pygame.image.load("textures/lvl10_guide.png"),
    'end1' : pygame.image.load("textures/end1.png"),
    'end2' : pygame.image.load("textures/end2.png"),
    'end3' : pygame.image.load("textures/end3.png"),
    'end4' : pygame.image.load("textures/end4.png"),
    'end5' : pygame.image.load("textures/theEnd.png"),
    'colorsBlack' : pygame.image.load("textures/lvl9_ui.png"),
    'controls' : pygame.image.load("textures/controls.png"),
    'q' : pygame.image.load("textures/q_button.png"),
    'press' : pygame.image.load("textures/press.png")

}




