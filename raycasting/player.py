from math import *
import pygame.key

from settings import *

class Player:
    def __init__(self):
        self.x = 140
        self.y = 160
        self.angle = 0
        self.delta = 0
        self.speed = 100

    def move(self):
        key = pygame.key.get_pressed()
        key2 = pygame.key.get_pressed()
        cos_a, sin_a = cos(self.angle), sin(self.angle)

        if key2[pygame.K_LSHIFT]:
            self.speed += 5
            if self.speed >= 200:
                self.speed = 200
        else:
            self.speed = 100

        self.mouse_control()
        # if key2[pygame.K_ESCAPE]:
        #     quit()

        if key[pygame.K_w]:
            self.x += cos_a * self.delta * self.speed
            self.y += sin_a * self.delta * self.speed
        if key[pygame.K_s]:
            self.x -= cos_a * self.delta * self.speed
            self.y -= sin_a * self.delta * self.speed
        if key[pygame.K_a]:
            self.x += sin_a * self.delta * self.speed
            self.y -= cos_a * self.delta * self.speed
        if key[pygame.K_d]:
            self.x -= sin_a * self.delta * self.speed
            self.y += cos_a * self.delta * self.speed

    def mouse_control(self):
        if pygame.mouse.get_focused():
            diff = pygame.mouse.get_pos()[0] - half_width
            pygame.mouse.set_pos((half_width, half_height))
            self.angle += diff * self.delta * 0.2
