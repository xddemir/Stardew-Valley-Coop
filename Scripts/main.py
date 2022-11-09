# Libraries
import pygame as pg
import sys

# Component
from level import Level

# Constants
from settings import *

class Game:
    """ Starts the game and level """

    def __init__(self) -> None:
        self.Initialization()
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pg.time.Clock()
        self.level = Level()

    def Initialize(self):
        """ Initialize pre-functions before object is instantiated """
        
        pg.init()

    def run(self):
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

            dt = self.clock.tick() / 1000
            self.level.run(dt)
            pg.display.update()

if __name__ == "__main__":
    game = Game()
    game.run()