from os import stat
import pygame as pg
from settings import *
from support import import_folder


class Player(pg.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)

        self.import_assets()
        self.status = 'down_idle'
        self.frame_index = 0

        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center = pos)

        # movement
        self.direction = pg.math.Vector2()
        self.pos = pg.math.Vector2(self.rect.center)
        self.speled = 200

    
    def import_assets(self):
        self.animations = {'up': [], 'down': [], 'left':[], 'right':[],
                           'right_idle': [], 'left_idle': [],'up_idle': [], 'down_idle': [],
                           'right_hoe': [], 'left_hoe': [], 'down_hoe': [],
                           'right_axe': [], 'left_axe': [], 'down_axe': [],
                           'right_water': [], 'left_water': [], 'down_water': []}

        for anim in self.animations.keys():
            path = '../Assets/graphics/character/' + anim
            self.animations[anim] = import_folder(path)
    
    def input(self):
        keys = pg.key.get_pressed()

        if keys[pg.K_UP]:
            self.direction.y = -1
            self.status = 'up'
        elif keys[pg.K_DOWN]:
            self.direction.y = 1
            self.status = 'down'
        else:
            self.direction.y = 0
          
        if keys[pg.K_LEFT]:
            self.direction.x = -1
            self.status = 'left'
        elif keys[pg.K_RIGHT]:
            self.direction.x = 1
            self.status = 'right'
        else:
            self.direction.x = 0
           
    def get_status(self):
        # idle movement
       if self.direction.magnitude() == 0:
            self.status = self.status.split('_')[0] + '_idle'

    def move(self, dt):
        # the usual way is to add direction to the self.rect
        # but self.rect only gets integer values and if you 
        # want to make the movement independent from frame
        # you should another vector then assign it to handle floating point
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()

        # Horizontal movement
        self.pos.x += self.direction.x * self.speed * dt
        self.rect.centerx = self.pos.x
        
        # Vertical movement
        self.pos.y += self.direction.y * self.speed * dt
        self.rect.centery = self.pos.y

    def animate(self, dt):
        self.frame_index += 4 * dt
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0
        
        self.image = self.animations[self.status][int(self.frame_index)]

    def update(self, dt):
        self.input()
        self.get_status()
        self.move(dt)
        self.animate(dt)
        