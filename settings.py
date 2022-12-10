from math import *
import pygame.image
import pygame
import levels
import ray_casting

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

}

# 1 - white
# 2 - yellow
# 3 - blue
# 4 - color quest guy
# 5 - need blue(3)
# 6 - need yellow(2)
# 7 - red
# 8 - blue

pygame.init()

textMap = levels.levelsList['4']
numOfLvl = 4

maxSize = pygame.display.Info()

width = 1600
height = 900
half_width = width / 2
half_height = height / 2



blockSize = 100
rangeColBlock = blockSize//2
rangeColBlockPlus = blockSize*2

MAPSCALE = 8
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

FOV = pi / 2
halfFOV = FOV / 2
maxDepth = width // blockSize
numRays = 400
deltaRays = FOV / (numRays - 1)
dist = numRays / (2 * tan(halfFOV))
coef = dist * blockSize * 6
scale = width // numRays
depthCoef = 2

textureSize = 512
textureScale = textureSize // blockSize
textures = {
            '1': pygame.image.load('textures/colorWhiteWall.png'),
            '2': pygame.image.load('textures/colorYellowWall.png'),
            '3': pygame.image.load('textures/colorBlueWall.png'),
            '4': pygame.image.load('textures/colorRedWall.png'),
            '5': pygame.image.load('textures/colorGreenWall.png'),
            '<': pygame.image.load('textures/robot.png'),
            '!': pygame.image.load('textures/blockWallNeedYellow.png'),
            '@': pygame.image.load('textures/blockWallNeedBlue.png'),
            '$': pygame.image.load('textures/blockWallNeedRed.png'),
            '%': pygame.image.load('textures/blockWallNeedGreen.png'),
            'o': pygame.image.load('textures/blockNumberOne.png'),
            }


