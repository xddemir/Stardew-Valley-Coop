# Libraries
import pygame as pg
from random import randint, choice

# Utils
from timerHandler import Timer

# Constants
from settings import *


class Generic(pg.sprite.Sprite):
    """ Sprite concrete class to be extended by sub-classes """
    
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


class Particle(Generic):
    def __init__(self, pos, surf, groups, z, duration = 200):
        super().__init__(pos, surf, groups, z)
        self.start_time = pg.time.get_ticks()
        self.duration = duration

        # white surface
        mask_surf = pg.mask.from_surface(self.image)
        new_surf = mask_surf.to_surface()
        new_surf.set_colorkey((0, 0, 0))
        self.image = new_surf
    
    def update(self, dt):
        current_time = pg.time.get_ticks()
        if current_time - self.start_time > self.duration:
            self.kill()


class Tree(Generic):
    def __init__(self, pos, surf, groups, name, player_add) -> None:
        super().__init__(pos, surf, groups)

        self.player_add = player_add

        # tree attributes
        self.health = randint(3, 6)
        self.alive = True

        self.name = name

        stump_name = 'small' if name == "Small" else "large"
        self.stump_surf = pg.image.load(f"../Assets/graphics/stumps/{stump_name}.png").convert_alpha()
        self.invul_timer = Timer(200)

        self.apples_surf = pg.image.load("../Assets/graphics/fruit/apple.png").convert_alpha()
        self.apple_pos = APPLE_POS[name]
        self.apple_sprites = pg.sprite.Group()
        self.create_fruit()
            
    def create_fruit(self):
        for pos in self.apple_pos:
            pos = pos[0] + self.rect.left, pos[1] + self.rect.top 
            if randint(0, 10) < 2:
                Generic(pos, self.apples_surf, [self.apple_sprites, self.groups()[0]], LAYERS['fruit'])

    def damage(self):
        # Getting damage
        self.health -= 1

        # Remove an apple
        if len(self.apple_sprites.sprites()) > 0:
            random_apple = choice(self.apple_sprites.sprites())
            Particle(random_apple.rect.topleft,
                     random_apple.image,
                     self.groups()[0],
                     LAYERS['fruit'])
            
            # will get back in the later implementations
            self.player_add("apple", 1)

            random_apple.kill()

    def check_death(self):
        if self.health > 0: return None

        Particle(self.rect.topleft,
                 self.image,
                 self.groups()[0],
                 LAYERS['main'])

        self.image = self.stump_surf
        self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
        self.hitbox = self.rect.copy().inflate(-10, -self.rect.height * 0.8)
        self.alive = False

    def update(self, dt):
        if self.alive:
            self.check_death()


class Interaction(Generic):
    def __init__(self, pos, size, groups, name):
        surf = pg.Surface(size)
        super().__init__(pos, surf, groups)
        
        self.name = name

        