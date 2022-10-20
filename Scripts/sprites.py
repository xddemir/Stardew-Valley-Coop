import pygame as pg
from settings import *


class Generic(pg.sprite.Sprite):
    def __init__(self, pos, surf, groups, z = LAYERS['main']) -> None:
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)
        self.z = z


class Water(Generic):
    def __init__(self, pos, frames, groups) -> None:
        self.frames = frames
        self.frame_index = 0
        
        # sprite setup
        super().__init__(pos, 
                         surf=self.frames[self.frame_index],
                         groups=groups,
                         z=LAYERS['water'])

        