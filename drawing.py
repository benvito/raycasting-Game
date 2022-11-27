import pygame as pg
from settings import *
from math import *
from ray_casting import rayCasting

class Drawing:
    def __init__(self, surf, surf_map):
        self.surf = surf
        self.surf_map = surf_map
        self.font = pg.font.SysFont('Arial', 25, bold=True)

    def bg(self):
        # Небо
        pg.draw.rect(self.surf, (9, 5, 5), (0, 0, width, half_height))
        # Пол
        pg.draw.rect(self.surf, (9, 5, 5), (0, half_height, width, half_height))

    def world(self, player):
        ray_casting.rayCasting(self.surf, player)

    def info(self, clock, player):
        display_fps = str(int((clock.get_fps())))
        render = self.font.render(("FPS: " + str(int(clock.get_fps()))), True, (114,160,193))
        positions = self.font.render(("   X:   " + str(int(player.x)) + "   Y:   " + str(int(player.y))), True,
                              (114, 160, 193))
        speedHud = self.font.render(('Speed:  ' + str(player.speed)), True, (114, 160, 193))

        self.surf.blit(positions, (1400, 30))
        self.surf.blit(speedHud, (1465, 50))
        self.surf.blit(render,(1500,10))

    def mini_map(self, player):
        map_x, map_y = player.x // MAPSCALE, player.y // MAPSCALE
        self.surf_map.fill(pg.Color(0,0,0))
        # plPos = pg.draw.circle(self.surf_map, pg.Color(12,169,11), (map_x, map_y), 2)
        pg.draw.circle(self.surf_map, pg.Color('green'), (map_x, map_y), 5)
        pg.draw.line(self.surf_map, pg.Color("green"), (map_x, map_y), (map_x + 12 * cos(player.angle),
                                                                        map_y + 12 * sin(player.angle)), 2)

        for x,y in mini_map:
            minimapTempMap = pg.draw.rect(self.surf_map, pg.Color('gray'), (x, y, MAP_BLOCK_SIZE, MAP_BLOCK_SIZE), 0)
            # if minimapTempMap.colliderect(plPos):
            #     player.x = tmpPosX
            #     player.y = tmpPosY

        self.surf.blit(self.surf_map, MAPPOS)
