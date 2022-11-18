from math import *

import pygame.image

import levels

# 1 - white
# 2 - yellow
# 3 - blue
# 4 - color quest guy
# 5 - need 3
# 6 - need 2
import ray_casting

textMap = [
           "111111111111111111111111",
           "1......................1",
           "1....2.................1",
           "1....2............111111",
           "1...........22.....1.1.1",
           "1....1...............1.1",
           "111111.................5",
           "1..........322.........4",
           "1..............1.......6",
           "1......1.....11111.....1",
           "1.....1111...1...1.....1",
           "1......1...............1",
           "1......................1",
           "111111111111111111111111",
           ]

width = 1600
height = 900
half_width = width / 2
half_height = height / 2

numOfLvl = 1

blockSize = 100


mapWidth = len(textMap[0])
mapHeight = len(textMap)

blockMapTextures = {

}

blockMap = set()
yBlockPos = 0
blockOne = list()
blockQuest = {

}
for row in textMap:
    xBlockPos = 0
    for column in list(row):
        if column != '.':
            blockMap.add((xBlockPos, yBlockPos))
            blockMapTextures[(xBlockPos, yBlockPos)] = column
        if column == '2' or column == '3':
            blockOne.append((xBlockPos, yBlockPos))
        if column == '5' or column == '6':
            blockQuest[(xBlockPos, yBlockPos)] = column
        xBlockPos += blockSize
    yBlockPos += blockSize


FOV = pi / 2
halfFOV = FOV / 2
maxDepth = width // blockSize
numRays = 400
deltaRays = FOV / (numRays - 1)
dist = numRays / (2 * tan(halfFOV))
coef = dist * blockSize * 7
scale = width // numRays
depthCoef = 2


textureSize = 512
textureScale = textureSize // blockSize
textures = {'1': pygame.image.load('colorWhiteWall.png'),
            '2': pygame.image.load('colorYellowWall.png'),
            '3': pygame.image.load('colorBlue.png'),
            '4': pygame.image.load('robotlvl1.png'),
            '5': pygame.image.load('colorWhiteWall.png'),
            '6': pygame.image.load('colorWhiteWall.png')}

def initMap(textMap):
    blockMap.clear()
    blockQuest.clear()
    blockMapTextures.clear()
    blockOne.clear()
    yBlockPos = 0
    for row in textMap:
        xBlockPos = 0
        for column in list(row):
            if column != '.':
                blockMap.add((xBlockPos, yBlockPos))
                blockMapTextures[(xBlockPos, yBlockPos)] = column
            if column == '2' or column == '3':
                blockOne.append((xBlockPos, yBlockPos))
            if column == '5' or column == '6':
                blockQuest[(xBlockPos, yBlockPos)] = column
            xBlockPos += blockSize
        yBlockPos += blockSize

