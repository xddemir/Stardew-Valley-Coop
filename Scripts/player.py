import pygame as pg
from settings import *


class Player(pg.sprite.sprite):
    def __init__(self, pos, group):
        super().__init__(group)

        self.image = pg.Surface((64, 32))
        self.image.fill("green")
        self.rect = self.image.get_rect(center = pos)

    def input(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_UP]:
            pass
        if keys[pg.K_DOWN]:
            pass
        if keys[pg.K_LEFT]:
            pass
        if keys[pg.K_RIGHT]:
            pass

    def update(self, dt):
        pass
        