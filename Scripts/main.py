# Libraries
import threading
import pygame as pg
import sys

# Component
from level import Level

# Constants
from settings import *


class Game:
    """ Starts the game and level """

    def __init__(self) -> None:
        self.Initialize()
        self.screen = pg.display.set_mode((setting.SCREEN_WIDTH, setting.SCREEN_HEIGHT))
        self.clock = pg.time.Clock()
        self.level = Level()

    def Initialize(self):
        """ Initialize pre-functions before object is instantiated """
        print(setting.SCREEN_WIDTH, setting.SCREEN_HEIGHT)
        pg.init()

    def run(self):
        while True:
            for event in pg.event.get():
                keys = pg.key.get_pressed()
                if event.type == pg.QUIT or keys[pg.K_ESCAPE]:
                    pg.quit()
                    sys.exit()

            dt = self.clock.tick() / 1000
            self.level.run(dt)
            pg.display.update()

if __name__ == "__main__":


    game = Game()
    game.run()