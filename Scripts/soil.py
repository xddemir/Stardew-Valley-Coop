import pygame
import random
from support import import_folder_dict
from settings import *
from pytmx.util_pygame import load_pygame


class SoilTile(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups) -> None:
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft= pos)
        self.z = LAYERS['soil']


class WaterTile(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups) -> None:
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)
        self.z = LAYERS["soil water"]


class SoilLayer:
    def __init__(self, all_sprites):

        # sprite groups
        self.all_sprites = all_sprites
        self.soil_sprites = pygame.sprite.Group()
        self.water_sprites = pygame.sprite.Group()

        self.soil_surf_dict = import_folder_dict("../Assets/graphics/soil")

        self.create_soil_grid()
        self.create_hit_rects()

    def water(self, target_pos):
        for soil_sprite in self.soil_sprites.sprites():
            if soil_sprite.rect.collidepoint(target_pos):
                x, y = soil_sprite.rect.x // TILE_SIZE, soil_sprite.rect.y // TILE_SIZE
                if 'W' not in self.grid[y][x]:
                    self.grid[y][x].append('W')
                    WaterTile((soil_sprite.rect.x, soil_sprite.rect.y),
                              pygame.image.load(f'../Assets/graphics/soil_water/{random.randint(0, 2)}.png'),
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
        ground = pygame.image.load('../Assets/graphics/world/ground.png')
        h_tiles, v_tiles = ground.get_width() // TILE_SIZE, ground.get_height() // TILE_SIZE

        self.grid = [[[] for col in range(h_tiles)] for row in range(v_tiles)]
        for x, y, _ in load_pygame('../Assets/data/map.tmx').get_layer_by_name("Farmable").tiles():
            self.grid[y][x].append('F')

    def create_hit_rects(self):
        self.hit_rects = []

        for index_row, row in enumerate(self.grid):
            for index_col, cell in enumerate(row):
                if 'F' in cell:
                    x, y = index_row * TILE_SIZE, index_col * TILE_SIZE
                    rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
                    self.hit_rects.append(rect)
    
    def get_hit(self, point):
        for rect in self.hit_rects:
            if rect.collidepoint(point):
                x, y = rect.x // TILE_SIZE, rect.y // TILE_SIZE
                if 'F' in self.grid[y][x]:
                    self.grid[y][x].append('X')
                    self.create_soil_tiles()
    
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

                    SoilTile((index_col * TILE_SIZE, index_row * TILE_SIZE),
                             self.soil_surf_dict[tile_type],
                             [self.all_sprites, self.soil_sprites])