# Libraries
import pygame as pg

# Components
from settings import *

# Constants
from player import Player

class Overlay:
    """ Draws UI Elements to the display surface"""
    
    def __init__(self, player: Player) -> None:
        self.display_surface = pg.display.get_surface()
        self.player = player

        overlay_path = '../Assets/graphics/overlay/'
        self.tool_surface = {tool: pg.image.load(f'{overlay_path}{tool}.png').convert_alpha() 
                             for tool in player.tools}

        self.seed_surface = {seed: pg.image.load(f'{overlay_path}{seed}.png').convert_alpha()
                             for seed in player.seeds}

    def display(self):
        # tool
        tool_surf = self.tool_surface[self.player.selected_tool]
        tool_rect = tool_surf.get_rect(midbottom= (setting.OVERLAY_POSITIONS['tool']))
        self.display_surface.blit(tool_surf, tool_rect)

        # seed
        seed_surf = self.seed_surface[self.player.selected_seed]
        seed_rect = seed_surf.get_rect(midbottom= (setting.OVERLAY_POSITIONS['seed']))
        self.display_surface.blit(seed_surf, seed_rect)
