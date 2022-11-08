# Libraries
import pygame as pg

# Constants
from settings import *


class Transition:
    """ Transation scene when the day gets restarted """
    
    def __init__(self, reset, player) -> None:
        # setup
        self.display_surface = pg.display.get_surface()
        self.reset = reset
        self.player = player

        # overlay image
        self.image = pg.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.color = 255
        self.speed = -2

    def play(self):

        self.color += self.speed

        if self.color <= 0:
            self.speed *= -1
            self.color = 0
            self.reset()
        if self.color > 255:
            self.color = 255
            self.speed *= -1
            self.player.sleep = False

        self.image.fill((self.color, self.color, self.color))
        self.display_surface.blit(self.image, (0, 0), special_flags= pg.BLEND_RGBA_MULT)