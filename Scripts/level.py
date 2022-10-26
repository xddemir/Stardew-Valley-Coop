import pygame
from sprites import Water, WildFlower, Generic, Tree
from support import import_folder
from overlay import Overlay
from settings import *
from player import Player
from pytmx.util_pygame import load_pygame


class Level:
    def __init__(self):

        self.display_surface = pygame.display.get_surface()

        self.all_sprites = CameraGroup()
        self.collision_sprites = pygame.sprite.Group()

        self.setup()
        self.overlay = Overlay(self.player)

    def setup(self):
        tmx_data = load_pygame('../Assets/data/map.tmx')

        for layer in ['HouseFloor', 'HouseFurnitureBottom']:
            for x, y, surf in tmx_data.get_layer_by_name(layer).tiles():
                Generic((x * 64, y * 64), surf, self.all_sprites, LAYERS['house bottom'])

        for layer in ['HouseWalls', 'HouseFurnitureTop']:
            for x, y, surf in tmx_data.get_layer_by_name(layer).tiles():
                Generic((x * 64, y * 64), surf, self.all_sprites, LAYERS['main'])

        for layer in ['Fence']:
            for x, y, surf in tmx_data.get_layer_by_name(layer).tiles():
                Generic((x * 64, y * 64), surf, [self.all_sprites,
                                                 self.collision_sprites],
                                                LAYERS['main'])

        water_frames = import_folder("../Assets/graphics/water")
        for layer in ['Water']:
            for x, y , surf in tmx_data.get_layer_by_name(layer).tiles():
                Water((x * 64, y * 64), water_frames, self.all_sprites)

        for obj in tmx_data.get_layer_by_name("Decoration"):
            WildFlower((obj.x, obj.y), obj.image, [self.all_sprites,
                                                   self.collision_sprites])

        for obj in tmx_data.get_layer_by_name("Trees"):
            Tree((obj.x, obj.y), obj.image, [self.all_sprites, 
                                             self.collision_sprites])

        Generic(
            pos=(0, 0),
            surf=pygame.image.load(
                '../Assets/graphics/world/ground.png').convert_alpha(),
            groups=self.all_sprites,
            z=LAYERS['ground'])

        # Collision Tiles
        for x, y, surf in tmx_data.get_layer_by_name("Collision").tiles():
            Generic((x * TILE_SIZE, y * TILE_SIZE), pygame.Surface((TILE_SIZE, TILE_SIZE)), self.collision_sprites)

        # Player
        for obj in tmx_data.get_layer_by_name("Player"):
            if obj.name == "Start":
                self.player = Player((obj.x, obj.y), self.all_sprites, self.collision_sprites)
                

    def run(self, dt):
        self.display_surface.fill("black")
        self.all_sprites.custom_draw(self.player)
        self.all_sprites.update(dt)

        self.overlay.display()


class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pg.display.get_surface()
        self.offset = pygame.math.Vector2()

    def custom_draw(self, player: Player):
        self.offset.x = player.rect.centerx - SCREEN_WIDTH / 2    
        self.offset.y = player.rect.centery - SCREEN_HEIGHT / 2 

        for layer in LAYERS.values():
            # important overlay sorting
            for sprite in sorted(self.sprites(), key= lambda sprite: sprite.rect.centery):
                if layer == sprite.z:
                    offset_rect = sprite.rect.copy()
                    offset_rect.center -= self.offset
                    self.display_surface.blit(sprite.image, offset_rect)
        
    # Edit Camera
    def draw_square(self):
        for x in range(SCREEN_WIDTH // 64):
            for y in range(SCREEN_HEIGHT // 64):
                rect = pg.Rect(x * 64, y * 64, 64, 64)
                pg.draw.rect(self.display_surface, (0, 0, 0), rect, 1)