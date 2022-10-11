import pygame as pg
from settings import *


class Player(pg.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)

        self.image = pg.Surface((32, 64))
        self.image.fill("green")
        self.rect = self.image.get_rect(center = pos)

        # movement
        self.direction = pg.math.Vector2()
        self.pos = pg.math.Vector2(self.rect.center)
        self.speed = 200
        

    def input(self):
        keys = pg.key.get_pressed()

        if keys[pg.K_UP]:
            self.direction.y = -1
        elif keys[pg.K_DOWN]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[pg.K_LEFT]:
            self.direction.x = -1
        elif keys[pg.K_RIGHT]:
            self.direction.x = 1
        else:
            self.direction.x = 0

    def move(self, dt):
        # the usual way is to add direction to the self.rect
        # but self.rect only gets integer values and if you 
        # want to make the movement independent from frame
        # you should another vector then assign it to handle floating point
        self.pos += self.direction * self.speed * dt
        self.rect.center = self.pos
        

    def update(self, dt):
        self.input()
        self.move(dt)
        