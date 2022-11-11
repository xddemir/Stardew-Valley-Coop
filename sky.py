# Libraries
import pygame as pg
from support import import_folder
from random import randint, choice

# Components
from sprites import Generic

# Constants
from settings import * 

class Sky:
    """ Sky surface that changes the day color """
    def __init__(self):
        self.display_surface = pg.display.get_surface()
        self.full_surface = pg.Surface((setting.SCREEN_WIDTH, setting.SCREEN_HEIGHT))
        self.start_color = [255, 255, 255]
        self.end_color = (38, 101, 189)

    def display(self, dt):
        for index, value in enumerate(self.end_color):
            if self.start_color[index] > value:
                self.start_color[index] -= 2 * dt

        self.full_surface.fill(self.start_color)
        self.display_surface.blit(self.full_surface, (0, 0), special_flags=pg.BLEND_RGBA_MULT)


class Drop(Generic):
    """ Rain-drop sprites created per frame """

    def __init__(self, pos, moving, surf, groups, z) -> None:
        # general setup
        super().__init__(pos, surf, groups, z)
        self.lifetime = randint(400 ,500)
        self.start_time = pg.time.get_ticks()

        # moving
        self.moving = moving
        if self.moving: 
            self.pos= pg.math.Vector2(self.rect.topleft)
            self.direction = pg.math.Vector2(-2, 4)
            self.speed = randint(200, 250)


    def update(self, dt):
        if self.moving:
            self.pos += self.direction * self.speed * dt
            self.rect.topleft = (round(self.pos.x), round(self.pos.y))
        
        if pg.time.get_ticks() - self.start_time >= self.lifetime:
            self.kill()
    

class Rain:
    """ Rain components that controls rain drops and floor """

    def __init__(self, all_sprites):
        self.all_sprites = all_sprites
        self.rain_drops = import_folder('Assets/graphics/rain/drops/')
        self.rain_floor = import_folder('Assets/graphics/rain/floor/')
        self.floor_w, self.floor_h = pg.image.load('Assets/graphics/world/ground.png').get_size()

    def create_floor(self):
        Drop(
            surf= choice(self.rain_floor),
            pos = (randint(0, self.floor_w), randint(0, self.floor_h)),
            moving= False,
            groups= self.all_sprites,
            z = setting.LAYERS['rain floor'])

    def create_drops(self):
            Drop(
                surf= choice(self.rain_drops),
                pos = (randint(0, self.floor_w), randint(0, self.floor_h)),
                moving= False,
                groups= self.all_sprites,
                z = setting.LAYERS['rain floor'])

    def update(self):
        self.create_drops()
        self.create_floor()