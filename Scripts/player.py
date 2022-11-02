from operator import truediv
import pygame as pg
from settings import *
from support import import_folder
from timerHandler import Timer


class Player(pg.sprite.Sprite):
    """ Player that interacts with the whole scene via user"""

    def __init__(self, pos, group, collision_group, tree_sprites, interaction) -> None:
        super().__init__(group)

        self.import_assets()
        self.status = 'down_idle'
        self.frame_index = 0

        # general setup
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center=pos)
        self.z = LAYERS['main']
        self.hitbox = self.rect.copy().inflate((-126, -70))

        # movement
        self.direction = pg.math.Vector2()
        self.pos = pg.math.Vector2(self.rect.center)
        self.speed = 200

        # collision
        self.collision_sprites = collision_group

        # timers
        self.timers: dict = {
            'tool use': Timer(350, self.use_tool),
            'tool switch': Timer(200),
            'seed use': Timer(350, self.use_seed),
            'seed switch': Timer(200)
        }

        # tools
        self.tools = ['hoe', 'axe', 'water']
        self.tool_index = 0
        self.selected_tool = self.tools[self.tool_index]

        # seeds
        self.seeds = ['tomato', 'corn']
        self.seed_index = 0
        self.selected_seed = self.seeds[self.seed_index]

        # interaction
        self.tree_sprites = tree_sprites
        self.interaction_sprites = interaction
        self.sleep = False

        # Inventory
        self.player_inventory = {
            "wood": 0,
            "apple": 0,
            "corn": 0,
            "tomato": 0}

    def use_tool(self):

        if self.selected_tool == "hoe":
            pass
        if self.selected_tool == "axe":
            for tree in self.tree_sprites.sprites():
                if tree.rect.collidepoint(self.target_pos):
                    tree.damage()

        if self.selected_tool == "water":
            pass

    def get_target_pos(self):
        self.target_pos = self.rect.center + PLAYER_TOOL_OFFSET[self.status.split("_")[0]]

    def use_seed(self):
        pass

    def import_assets(self):
        """ Import player animations"""

        self.animations = {'up': [], 'down': [], 'left': [], 'right': [],
                           'right_idle': [], 'left_idle': [], 'up_idle': [], 'down_idle': [],
                           'right_hoe': [], 'left_hoe': [], 'down_hoe': [], 'up_hoe': [],
                           'right_axe': [], 'left_axe': [], 'down_axe': [], 'up_axe': [],
                           'right_water': [], 'left_water': [], 'down_water': [], 'up_water': []}

        for anim in self.animations.keys():
            path = '../Assets/graphics/character/' + anim
            self.animations[anim] = import_folder(path)

    def input(self):
        """ Gets proper direction and status via keyboard"""

        keys = pg.key.get_pressed()

        if not self.timers['tool use'].active and not self.sleep:
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

            # tool use
            if keys[pg.K_SPACE]:
                # timer for the tool use
                self.timers['tool use'].activate()
                self.direction = pg.math.Vector2()
                self.frame_index = 0

            # change tool
            if keys[pg.K_q] and not self.timers['tool switch'].active:
                self.timers['tool switch'].activate()

                self.tool_index += 1
                self.tool_index = self.tool_index if self.tool_index < len(
                    self.tools) else 0

                self.selected_tool = self.tools[self.tool_index]

            # use seed
            if keys[pg.K_LCTRL]:
                self.timers['seed use'].activate()
                self.direction = pg.math.Vector2()
                self.frame_index = 0

            # change seed
            if keys[pg.K_e] and not self.timers['seed switch'].active:
                self.timers['seed switch'].activate()

                self.seed_index += 1
                self.seed_index = self.seed_index if self.seed_index < len(
                    self.seeds) else 0

                self.selected_seed = self.seeds[self.seed_index]

            # interactive
            if keys[pg.K_RETURN]:
                collided_interaction_sprite = pg.sprite.spritecollide(self, 
                                                                      self.interaction_sprites, 
                                                                      False)

                if collided_interaction_sprite:
                    if collided_interaction_sprite[0].name == "Trader":
                        pass
                    else:
                        self.status = "left_idle"
                        self.sleep = True

    def update_timers(self):
        """ Update timers """

        for timer in self.timers.values():
            timer.update()

    def get_status(self):
        """ Gets proper sprite name by directions that player moves """

        # idle movement
        if self.direction.magnitude() == 0:
            self.status = self.status.split('_')[0] + '_idle'
        # tool use
        if self.timers['tool use'].active:
            self.status = self.status.split('_')[0] + '_' + self.selected_tool

        if self.timers['tool switch'].active:
            self.status = self.status.split('_')[0] + '_' + self.selected_tool

        if self.timers['seed use'].active:
            self.status = self.status.split("_")[0]

    def collision(self, direction):
        """ Checks collisions vertically and horizontally"""

        for sprite in self.collision_sprites.sprites():
            if hasattr(sprite, 'hitbox'):
                if sprite.hitbox.colliderect(self.hitbox):
                    if direction == 'horizontal':
                        # moving right
                        if self.direction.x > 0:
                            self.hitbox.right = sprite.hitbox.left
                        if self.direction.x < 0:
                            self.hitbox.left = sprite.hitbox.right

                        self.rect.centerx = self.hitbox.centerx
                        self.pos.x = self.hitbox.centerx

                    if direction == 'vertical':
                        # moving top
                        if self.direction.y > 0:
                            self.hitbox.bottom = sprite.hitbox.top
                        if self.direction.y < 0:
                            self.hitbox.top = sprite.hitbox.bottom
                        
                        self.rect.centery = self.hitbox.centery
                        self.pos.y = self.hitbox.centery

    def move(self, dt):
        """ the usual way is to add direction to the self.rect
        but self.rect only gets values and if you want to make
        you should another vector then assign it to handle floating point """

        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()

        # Horizontal movement
        self.pos.x += self.direction.x * self.speed * dt
        self.hitbox.centerx = round(self.pos.x)
        self.rect.centerx = self.hitbox.centerx
        self.collision('horizontal')

        # Vertical movement
        self.pos.y += self.direction.y * self.speed * dt
        self.hitbox.centery = round(self.pos.y)
        self.rect.centery = self.hitbox.centery
        self.collision('vertical')

    def animate(self, dt):
        """ animates player sprites by frame index"""

        self.frame_index += 4 * dt
        if self.frame_index > len(self.animations[self.status]):
            self.frame_index = 0

        self.image = self.animations[self.status][int(self.frame_index)]

    def update(self, dt):
        """ Updates per frame"""

        self.input()
        self.get_status()
        self.update_timers()
        self.get_target_pos()

        self.move(dt)
        self.animate(dt)
