from math import *
import pygame.key

import main
import settings
from settings import *

class Player:
    def __init__(self):
        # self.x = 350
        # self.y = 350
        self.x = 160
        self.y = 150
        # self.x = 500
        # self.y = 480

        self.angle = 0
        self.delta = 0
        self.speed = 100

        #collision
        self.side = 50
        self.rect = pygame.Rect(*(self.x, self.y), self.side, self.side)

    def detect_collision_wall(self, dx, dy):
        next_rect = self.rect.copy()
        next_rect.move_ip(dx, dy)
        hit_indexes = next_rect.collidelistall(collision_walls)

        if len(hit_indexes):
            delta_x, delta_y = 0, 0
            for hit_index in hit_indexes:
                hit_rect = collision_walls[hit_index]
                if dx > 0:
                    delta_x += next_rect.right - hit_rect.left
                else:
                    delta_x += hit_rect.right - next_rect.left
                if dy > 0:
                    delta_y += next_rect.bottom - hit_rect.top
                else:
                    delta_y += hit_rect.bottom - next_rect.top
            if abs(delta_x - delta_y) < 50:
                dx, dy = 0, 0
            elif delta_x > delta_y:
                dy = 0
            elif delta_y > delta_x:
                dx = 0

        self.x += dx
        self.y += dy

    def move(self, active):
        self.rect.center = self.x, self.y
        key = pygame.key.get_pressed()
        key2 = pygame.key.get_pressed()
        cos_a, sin_a = cos(self.angle), sin(self.angle)

        if key2[pygame.K_LSHIFT]:
            self.speed += 5
            if self.speed >= 200:
                self.speed = 200
        else:
            self.speed = 500

        self.mouse_control(active=active)
        # if key2[pygame.K_ESCAPE]:
        #     quit()

        if key[pygame.K_w]:
            dx = cos_a * self.delta * self.speed
            dy = sin_a * self.delta * self.speed
            self.detect_collision_wall(dx, dy)
        if key[pygame.K_s]:
            dx = cos_a * self.delta * -self.speed
            dy = sin_a * self.delta * -self.speed
            self.detect_collision_wall(dx, dy)
        if key[pygame.K_a]:
            dx = sin_a * self.delta * self.speed
            dy = cos_a * self.delta * -self.speed
            self.detect_collision_wall(dx, dy)
        if key[pygame.K_d]:
            dx = sin_a * self.delta * -self.speed
            dy = cos_a * self.delta * self.speed
            self.detect_collision_wall(dx, dy)

    def mouse_control(self, active):
        if active:
            if pygame.mouse.get_focused():
                diff = pygame.mouse.get_pos()[0] - half_width
                pygame.mouse.set_pos((half_width, half_height))
                self.angle += diff * self.delta * 0.15
