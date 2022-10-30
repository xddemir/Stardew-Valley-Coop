import pygame as pg
from settings import *
from random import randint

class Generic(pg.sprite.Sprite):
    def __init__(self, pos, surf, groups, z=LAYERS['main']) -> None:
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)
        self.z = z

        self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.2,
                                               -self.rect.height * 0.75)


class Water(Generic):
    def __init__(self, pos, frames, groups) -> None:
        self.frames = frames
        self.frame_index = 0

        # sprite setup
        super().__init__(pos=pos,
                         surf=self.frames[self.frame_index],
                         groups=groups,
                         z=LAYERS['water'])

    def animate(self, dt):
        self.frame_index += 4 * dt
        if self.frame_index > len(self.frames):
            self.frame_index = 0

        self.image = self.frames[int(self.frame_index)]

    def update(self, dt):
        self.animate(dt)


class WildFlower(Generic):
    def __init__(self, pos, surf, groups) -> None:
        super().__init__(pos, surf, groups)
        self.hitbox = self.rect.copy().inflate(-20, -self.rect.height * 0.9)


class Tree(Generic):
    def __init__(self, pos, surf, groups, name) -> None:
        super().__init__(pos, surf, groups)

        self.apples_surf = pg.image.load("../Assets/graphics/fruit/apple.png").convert_alpha()
        self.apple_pos = APPLE_POS[name]
        self.apple_sprites = pg.sprite.Group()
        self.create_fruit()
            
    def create_fruit(self):
        for pos in self.apple_pos:
            pos = pos[0] + self.rect.left, pos[1] + self.rect.top 
            if randint(0, 10) < 2:
                Generic(pos, self.apples_surf, [self.apple_sprites, self.groups()[0]], LAYERS['fruit'])

