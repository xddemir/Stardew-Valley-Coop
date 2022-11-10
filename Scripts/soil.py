# Libraries
import pygame as pg
import random
from pytmx.util_pygame import load_pygame

# Default
from support import import_folder_dict, import_folder

# Constant
from settings import *


class SoilTile(pg.sprite.Sprite):

    def __init__(self, pos, surf, groups) -> None:
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft= pos)
        self.z = setting.LAYERS['soil']


class WaterTile(pg.sprite.Sprite):
    def __init__(self, pos, surf, groups) -> None:
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)
        self.z = setting.LAYERS["soil water"]


class Plant(pg.sprite.Sprite):
    def __init__(self, plant_type, groups, soil, is_watered) -> None:
        super().__init__(groups)
        self.plant_type = plant_type
        self.soil = soil
        self.frames = import_folder(f'../Assets/graphics/fruit/{plant_type}')
        self.age = 0
        self.max_age = len(self.frames) - 1
        self.grow_speed = setting.GROW_SPEEDS[plant_type]
        self.image = self.frames[self.age]

        self.is_watered =  is_watered
        self.is_harvestable = False

        self.y_offset = -16 if plant_type == 'corn' else -8
        self.rect = self.image.get_rect(midbottom = soil.rect.midbottom + pg.math.Vector2(0, self.y_offset))
        self.z = setting.LAYERS['ground plant']

    def grow(self):
        
        if int(self.age) > 0:
            self.hitbox = self.rect.copy().inflate(-26, -self.rect.height * 0.4)

        if self.is_watered(self.rect.center):
            self.z = setting.LAYERS['main'] if int(self.age) > 0 else setting.LAYERS['ground plant']
            self.age = min(self.age + self.grow_speed, self.max_age)
            self.is_harvestable = self.age == self.max_age
            self.image = self.frames[int(self.age)]
            self.rect = self.image.get_rect(midbottom = self.soil.rect.midbottom + pg.math.Vector2(0, self.y_offset))

class SoilLayer:
    def __init__(self, all_sprites, collision_sprites) -> None:
        # sprite groups
        self.all_sprites = all_sprites
        self.collision_sprites = collision_sprites
        self.soil_sprites = pg.sprite.Group()
        self.water_sprites = pg.sprite.Group()
        self.plant_sprites = pg.sprite.Group()

        self.soil_surf_dict = import_folder_dict("../Assets/graphics/soil")

        self.raining = True
        self.create_soil_grid()
        self.create_hit_rects()

    def plant_seed(self, target_pos, selected_seed):
        for soil_sprite in self.soil_sprites.sprites():
            if soil_sprite.rect.collidepoint(target_pos):
                x, y = soil_sprite.rect.x // setting.TILE_SIZE, soil_sprite.rect.y // setting.TILE_SIZE
                if 'W' not in self.grid[y][x] or 'P' not in self.grid[y][x]:
                    self.grid[y][x].append('P')
                    Plant(selected_seed, [self.all_sprites, self.plant_sprites, self.collision_sprites], soil_sprite, self.is_watered)


    def water(self, target_pos):
        for soil_sprite in self.soil_sprites.sprites():
            if soil_sprite.rect.collidepoint(target_pos):
                x, y = soil_sprite.rect.x // setting.TILE_SIZE, soil_sprite.rect.y // setting.TILE_SIZE
                if 'W' not in self.grid[y][x]:
                    self.grid[y][x].append('W')
                    WaterTile((soil_sprite.rect.x, soil_sprite.rect.y),
                              pg.image.load(f'../Assets/graphics/soil_water/{random.randint(0, 2)}.png'),
                              [self.all_sprites, self.water_sprites])

    def water_all(self):
        for index_row, row in enumerate(self.grid):
            for index_col, cell in enumerate(row):
                if 'W' not in cell and 'X' in cell:
                    cell.append('W')
                    x, y = index_col * setting.TILE_SIZE, index_row * setting.TILE_SIZE
                    WaterTile((x, y),
                              pg.image.load(f'../Assets/graphics/soil_water/{random.randint(0, 2)}.png'),
                              [self.all_sprites, self.water_sprites])

    def remove_water(self):
        # destroy all water sprites
        for sprite in self.water_sprites.sprites():
            sprite.kill()

        for row in self.grid:
            for cell in row:
                if 'W' in cell:
                    cell.remove('W')

    def create_soil_grid(self):
        ground = pg.image.load('../Assets/graphics/world/ground.png')
        h_tiles, v_tiles = ground.get_width() // setting.TILE_SIZE, ground.get_height() // setting.TILE_SIZE

        self.grid = [[[] for col in range(h_tiles)] for row in range(v_tiles)]
        for x, y, _ in load_pygame('../Assets/data/map.tmx').get_layer_by_name("Farmable").tiles():
            self.grid[y][x].append('F')

    def create_hit_rects(self):
        self.hit_rects = []

        for index_row, row in enumerate(self.grid):
            for index_col, cell in enumerate(row):
                if 'F' in cell:
                    x, y = index_row * setting.TILE_SIZE, index_col * setting.TILE_SIZE
                    rect = pg.Rect(x, y, setting.TILE_SIZE, setting.TILE_SIZE)
                    self.hit_rects.append(rect)
    
    def get_hit(self, point):
        for rect in self.hit_rects:
            if rect.collidepoint(point):
                x, y = rect.x // setting.TILE_SIZE, rect.y // setting.TILE_SIZE
                if 'F' in self.grid[y][x]:
                    self.grid[y][x].append('X')
                    self.create_soil_tiles()
                    if self.raining:
                        self.water_all()

    def is_watered(self, pos):
        x, y = pos[0] // setting.TILE_SIZE, pos[1] // setting.TILE_SIZE
        cell = self.grid[y][x]
        return 'W' in cell

    def update_plants(self):
        for plant in self.plant_sprites.sprites():
            plant.grow()
    
    def create_soil_tiles(self):
        self.soil_sprites.empty()
        for index_row, row in enumerate(self.grid):
            for index_col, cell in enumerate(row):
                if "X" in cell:
                    # top
                    t = 'X' in self.grid[index_row - 1][index_col]
                    # bottom
                    b = 'X' in self.grid[index_row + 1][index_col]
                    # left
                    l = 'X' in self.grid[index_row][index_col - 1]
                    # right
                    r = 'X' in self.grid[index_row][index_col + 1]

                    tile_type = 'o'

                    # check all tiles
                    if all((t, b, l, r)): tile_type = 'x'
                    # only left horizontal tiles 
                    if l and not any((t, b, r)): tile_type = 'r'
                    # only right horizontal 
                    if r and not any((t, l, r)): tile_type = 'l'
                    # only left right horizontal
                    if r and l and not any((t, b)): tile_type = 'lr'

                    # only top vertical tiles
                    if t and not any((l, r, b)): tile_type = 'b'
                    # only bottom vertical tiles
                    if b and not any((l, r , t)): tile_type = 't'
                    # only top bottom vertical tiles
                    if t and b and not any((l, r)): tile_type = 'tb'

                    # corners
                    if l and b and not any((t, r)): tile_type = 'tr'
                    if r and b and not any((t, l)): tile_type = 'tl'
                    if l and t and not any((b, r)): tile_type = 'br'
                    if r and t and not any((b, l)): tile_type = 'bl'

                    # t shapes
                    if all((t, b, r)) and not l: tile_type = 'tbr'
                    if all((t, b, l)) and not r: tile_type = 'tbl'
                    if all((l, r, t)) and not b: tile_type = 'lrb'
                    if all((l, r, b)) and not t: tile_type = 'lrt'

                    SoilTile((index_col * setting.TILE_SIZE, index_row * setting.TILE_SIZE),
                             self.soil_surf_dict[tile_type],
                             [self.all_sprites, self.soil_sprites])