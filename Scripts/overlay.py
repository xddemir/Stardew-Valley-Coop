from json import tool
import pygame as pg
from settings import *
from player import Player

class Overlay:
    def __init__(self, player: Player) -> None:
        self.display_surface = pg.display.get_surface()
        self.player = player

        overlay_path = '../Assets/graphics/overlay/'
        self.tool_surface = {tool: pg.image.load(f'{overlay_path}{tool}.png').convert_alpha() 
                             for tool in player.tools}

        self.seed_surface = {seed: pg.image.load(f'{overlay_path}{seed}.png').convert_alpha()
                             for seed in player.seeds}