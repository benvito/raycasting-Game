import pygame as pg
import time
from math import *
import settings
from settings import *
from PIL import Image
textureV, textureH = 0, 0

def rayCasting(display, player):
    try:
        global textureV, textureH
        inBlockPos = {'left': player.x - player.x // blockSize * blockSize,
                      'right': blockSize - (player.x - player.x // blockSize * blockSize),
                      'top': player.y - player.y // blockSize * blockSize,
                      'bottom': blockSize - (player.y - player.y // blockSize * blockSize)}

        for ray in range(numRays):
            cur_angle = player.angle - halfFOV + deltaRays * ray
            cos_a, sin_a = cos(cur_angle), sin(cur_angle)
            vl, hl = 0, 0

            #Вертикали
            for k in range(mapWidth):
                if cos_a > 0:
                    vl = inBlockPos['right'] / cos_a + blockSize / cos_a * k + 1
                elif cos_a < 0:
                    vl = inBlockPos['left'] / -cos_a + blockSize / -cos_a * k + 1

                xw, yw = vl * cos_a + player.x, vl * sin_a + player.y
                fixed = xw // blockSize * blockSize, yw // blockSize * blockSize
                if fixed in blockMap:
                    textureV = blockMapTextures[fixed]
                    break

            #Горизонтали
            for k in range(mapHeight):
                if sin_a > 0:
                    hl = inBlockPos['bottom'] / sin_a + blockSize / sin_a * k + 1
                elif sin_a < 0:
                    hl = inBlockPos['top'] / -sin_a + blockSize / -sin_a * k + 1

                xh, yh = hl * cos_a + player.x, hl * sin_a + player.y
                fixed = xh // blockSize * blockSize, yh // blockSize * blockSize
                if fixed in blockMap:
                    textureH = blockMapTextures[fixed]
                    break

            ray_size = min(vl, hl) * depthCoef
            toX, toY = ray_size * cos(cur_angle) + player.x, ray_size * sin(cur_angle) + player.y
            #pg.draw.line(display, pg.Color("yellow"), (minimapTempPlayer.x, minimapTempPlayer.y), (toX, toY))

            if hl > vl:
                ray_size = vl
                mr = yw
                textNum = textureV
            else:
                ray_size = hl
                mr = xh
                textNum = textureH

            # ray_size = min(vl, hl) * depthCoef
            mr = int(mr) % blockSize

            #Дефолт отрисовка лучей(тест)
            # toX, toY = ray_size * cos(cur_angle) + minimapTempPlayer.x, ray_size * sin(cur_angle) + minimapTempPlayer.y
            # pg.draw.line(display, pg.Color("yellow"), (minimapTempPlayer.x, minimapTempPlayer.y), (toX, toY))

            ray_size += cos(player.angle - cur_angle)
            height_c = coef / (ray_size + 0.0001)
            c = height_c
            textures[textNum].set_alpha(c)
            wallLine = textures[textNum].subsurface(mr * textureScale, 0, textureScale, textureSize)
            wallLine = pg.transform.scale(wallLine, (scale, int(height_c))).convert_alpha()
            display.blit(wallLine, (ray * scale, half_height - height_c // 2))
            # elif textNum == '2':
            #     c = 255 / (1 + ray_size ** 2 * 0.0000005)
            #     color = (c//1.05, c, c//10)
            #     block = pg.draw.rect(display, color, (ray * scale, half_height - height_c // 2, scale, height_c))
            # else:
            #     c = 255 / (1 + ray_size ** 2 * 0.0000005)
            #     color = (c, c, c)
            #     block = pg.draw.rect(display, color, (ray * scale, half_height - height_c // 2, scale, height_c))

            # flat = textureFlat
            # display.blit(flat, (0, 0, width, half_height))
            # display.blit(flat, (512, 0, width, half_height))
            # display.blit(flat, (512 + 512, 0, width, half_height))
            # display.blit(flat, (512 + 512 + 512, 0, width, half_height))

            # Прямоугольники
            # c = 255 / (1 + ray_size ** 2 * 0.0000005)
            # color = (c, c, c)
            # block = pg.draw.rect(display, color, (ray * scale, half_height - height_c // 2, scale, height_c))
    except:
        pass