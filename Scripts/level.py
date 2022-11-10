# Libraries
import pygame as pg
from pytmx.util_pygame import load_pygame
from random import randint

# Components
from sprites import Water, WildFlower, Generic, Tree, Interaction, Particle
from overlay import Overlay
from soil import SoilLayer
from transition import Transition
from player import Player
from sky import Rain, Sky
from menu import Menu

# Utils
from support import import_folder

# Constants
from settings import *


class Level:
    """ Handles the whole scene for level """

    def __init__(self):

        self.display_surface = pg.display.get_surface()

        self.all_sprites = CameraGroup()
        self.collision_sprites = pg.sprite.Group()
        self.tree_sprites = pg.sprite.Group()
        self.interaction_sprites = pg.sprite.Group()
        self.soil_layer = SoilLayer(self.all_sprites, self.collision_sprites)

        self.soil_layer = SoilLayer(self.all_sprites, self.collision_sprites)
        self.setup()
        self.overlay = Overlay(self.player)
        self.transition = Transition(self.reset, self.player)

        # sky
        self.rain = Rain(self.all_sprites)
        self.raining = True if randint(0, 100) > 25 else False
        self.soil_layer.raining = self.raining
        self.sky = Sky()

        # shop
        self.menu = Menu(self.player, self.toggle_shop)
        self.shop_active = False

    def player_add(self, item, amount=1):
        """ Adds specific amount of item to player's inventory """

        self.player.player_inventory[item] += amount

    def reset(self):
        """ Reset the day and all growing elements """

        self.soil_layer.update_plants()

        # soil
        self.soil_layer.remove_water()

        self.sky.start_color = [255, 255, 255]

        # is rainy
        self.raining = True if randint(0, 100) > 25 else False
        self.soil_layer.raining = self.raining
        if self.raining:
            self.soil_layer.water_all()

        # apples on the trees
        for tree in self.tree_sprites.sprites():
            for apple in tree.apple_sprites.sprites():
                apple.kill()
            tree.create_fruit()

    def plant_collision(self):
        """ Checks plant is fully growed and collides with player then kill itself """

        if self.soil_layer.plant_sprites:
            for plant in self.soil_layer.plant_sprites.sprites():
                if plant.is_harvestable and plant.rect.colliderect(self.player.hitbox):
                    self.player_add(plant.plant_type)
                    plant.kill()
                    Particle(plant.rect.topleft, plant.image, self.all_sprites, z= setting.LAYERS['main'])
                    self.soil_layer.grid[plant.rect.centery // setting.TILE_SIZE][plant.rect.centerx // setting.TILE_SIZE].remove('P')

    def toggle_shop(self):
        """ Activates and deactivates shop menu"""

        self.shop_active = not self.shop_active

    def setup(self):
        """ Setups all levels and sprites """

        tmx_data = load_pygame('../Assets/data/map.tmx')

        for layer in ['HouseFloor', 'HouseFurnitureBottom']:
            for x, y, surf in tmx_data.get_layer_by_name(layer).tiles():
                Generic((x * 64, y * 64), surf,
                        self.all_sprites, setting.LAYERS['house bottom'])

        for layer in ['HouseWalls', 'HouseFurnitureTop']:
            for x, y, surf in tmx_data.get_layer_by_name(layer).tiles():
                Generic((x * 64, y * 64), surf,
                        self.all_sprites, setting.LAYERS['main'])

        for layer in ['Fence']:
            for x, y, surf in tmx_data.get_layer_by_name(layer).tiles():
                Generic((x * 64, y * 64), surf, [self.all_sprites,
                                                 self.collision_sprites],
                        setting.LAYERS['main'])

        water_frames = import_folder("../Assets/graphics/water")
        for layer in ['Water']:
            for x, y, surf in tmx_data.get_layer_by_name(layer).tiles():
                Water((x * 64, y * 64), water_frames, self.all_sprites)

        for obj in tmx_data.get_layer_by_name("Decoration"):
            WildFlower((obj.x, obj.y), obj.image, [self.all_sprites,
                                                   self.collision_sprites])

        for obj in tmx_data.get_layer_by_name("Trees"):
            Tree(pos=(obj.x, obj.y), surf=obj.image,
                 groups=[self.all_sprites,
                 self.collision_sprites,
                 self.tree_sprites],
                 name=obj.name,
                 player_add=self.player_add)

        Generic(
            pos=(0, 0),
            surf=pg.image.load(
                '../Assets/graphics/world/ground.png').convert_alpha(),
            groups=self.all_sprites,
            z=setting.LAYERS['ground'])

        # Collision Tiles
        for x, y, surf in tmx_data.get_layer_by_name("Collision").tiles():
            Generic((x * setting.TILE_SIZE, y * setting.TILE_SIZE),
                    pg.Surface((setting.TILE_SIZE, setting.TILE_SIZE)),
                    self.collision_sprites)

        # Player
        for obj in tmx_data.get_layer_by_name("Player"):
            if obj.name == "Start":
                self.player = Player(
                    (obj.x, obj.y),
                    self.all_sprites,
                    self.collision_sprites,
                    self.tree_sprites,
                    self.interaction_sprites,
                    self.soil_layer,
                    self.toggle_shop)

            if obj.name == "Bed":
                Interaction((obj.x, obj.y),
                            (obj.width, obj.height),
                            self.interaction_sprites,
                            obj.name)
            
            if obj.name == "Trader":
                Interaction((obj.x, obj.y),
                            (obj.width, obj.height),
                            self.interaction_sprites,
                            obj.name)

    def run(self, dt):
        """ Updates the level per frame """

        self.display_surface.fill("black")
        self.all_sprites.custom_draw(self.player)

        if self.shop_active:
            self.menu.update()
        else:
            self.all_sprites.update(dt)
            self.plant_collision()

        self.overlay.display()
        if self.raining and not self.shop_active:
            self.rain.update()
        self.sky.display(dt)

        if self.player.sleep:
            self.transition.play()


class CameraGroup(pg.sprite.Group):
    """ Follows player and displays all sprites """

    def __init__(self):
        super().__init__()
        self.display_surface = pg.display.get_surface()
        self.offset = pg.math.Vector2()

    def custom_draw(self, player: Player):
        """ Handles the overlay collision and draws all scene according to the player's movement """

        self.offset.x = player.rect.centerx - setting.SCREEN_WIDTH / 2
        self.offset.y = player.rect.centery - setting.SCREEN_HEIGHT / 2

        for layer in setting.LAYERS.values():
            # important overlay sorting
            for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
                if layer == sprite.z:
                    offset_rect = sprite.rect.copy()
                    offset_rect.center -= self.offset
                    self.display_surface.blit(sprite.image, offset_rect)

    # Edit Camera
    def __draw_square(self):
        for x in range(setting.SCREEN_WIDTH // 64):
            for y in range(setting.SCREEN_HEIGHT // 64):
                rect = pg.Rect(x * 64, y * 64, 64, 64)
                pg.draw.rect(self.display_surface, (0, 0, 0), rect, 1)

    def __show_player_sprites(self, player, offset_rect):
        pg.draw.rect(self.display_surface, 'red', offset_rect, 5)
        hitbox_rect = player.hitbox.copy()
        hitbox_rect.center = offset_rect.center
        pg.draw.rect(self.display_surface, 'green', hitbox_rect, 5)
        target_pos = offset_rect.center + \
            setting.PLAYER_TOOL_OFFSET[player.status.split('_')[0]]
        pg.draw.circle(self.display_surface, 'blue', target_pos, 5)
