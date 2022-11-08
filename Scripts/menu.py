# Libraries
import pygame as pg

# Handler
from timerHandler import Timer

# Constants
from settings import *


class Menu:
    """ Interactive Inventory that display player's items and merchant's """

    def __init__(self, player, toggle_menu):
        # general menu
        self.player = player
        self.toggle_menu = toggle_menu
        self.display_surface = pg.display.get_surface()
        self.font = pg.font.Font('../Assets/font/LycheeSoda.ttf', 30)

        self.width = 400
        self.space = 10
        self.padding = 8

        self.options = list(self.player.player_inventory.keys()) + list(self.player.seed_inventory.keys())
        self.sell_border = len(self.player.player_inventory) - 1
        self.setup()

        # movement
        self.index = 0
        self.timer = Timer(200)

    def display_money(self):
        """ Displays amount of money for each item """

        text_surf = self.font.render(str(self.player.money), False, 'Black')
        text_rect = text_surf.get_rect(midbottom = (SCREEN_WIDTH / 2, SCREEN_HEIGHT - 20))
        pg.draw.rect(self.display_surface, 'White', text_rect.inflate(10, 10), 0, 6)
        self.display_surface.blit(text_surf, text_rect)
    
    def setup(self):
        """ Initial setup Item name, Item Amount and buy-sell section """

        self.text_surfs = []
        self.total_height = 0

        for item in self.options:
            text_surf = self.font.render (item, False, 'Black')
            self.text_surfs.append(text_surf)
            self.total_height += text_surf.get_height() + (self.padding * 2)
        
        self.total_height += (len(self.text_surfs) - 1) * self.space
        self.menu_top = SCREEN_HEIGHT / 2 - self.total_height / 2
        self.main_rect = pg.Rect(SCREEN_WIDTH / 2 - self.width / 2, self.menu_top, self.width, self.total_height)

        self.buy_text = self.font.render("Buy", False, "Black")
        self.sell_text = self.font.render("Sell", False, "Black")

    def input(self):
        keys = pg.key.get_pressed()
        self.timer.update()

        if keys[pg.K_ESCAPE]:
            self.toggle_menu()

        if not self.timer.active:
            if keys[pg.K_UP]:
                self.index = max(self.index - 1, 0)
                self.timer.activate()
            
            if keys[pg.K_DOWN]:
                self.index = min(self.index + 1, len(self.options) - 1)
                self.timer.activate()

            if keys[pg.K_SPACE]:
                self.timer.activate()
                # get item
                current_item = self.options[self.index]
                # sell item
                if self.index <= self.sell_border:
                    if self.player.player_inventory[current_item] > 0:
                        self.player.player_inventory[current_item] -= 1
                        self.player.money += SELL_PRICES[current_item]
                else:
                    if self.player.money >= PURCHASE_PRICES[current_item]:
                        self.player.player_inventory[current_item] += 1
                        self.player.money -= PURCHASE_PRICES[current_item]


    def show_entry(self, text_surf, amount, top, selected):
        """ Displays item background, text, amount with buy-sell texts on the menu surface """

        # background
        bg_rect = pg.Rect(self.main_rect.left, top, self.width, text_surf.get_height() + self.padding * 2)
        pg.draw.rect(self.display_surface, 'White', bg_rect, 0, 4)

        # text
        text_rect = text_surf.get_rect(midleft = (self.main_rect.left + 20, bg_rect.centery))
        self.display_surface.blit(text_surf, text_rect)

        # amount
        amount_surf = self.font.render(str(amount), False, 'Black')
        amount_rect = amount_surf.get_rect(midright = (self.main_rect.right - 20, bg_rect.centery))
        self.display_surface.blit(amount_surf, amount_rect)

        if selected:
            pg.draw.rect(self.display_surface, 'black', bg_rect, 4, 4)
            # sell text
            if self.index <= self.sell_border:
                pos_rect = self.sell_text.get_rect(midleft = (self.main_rect.left + 150, bg_rect.centery))
                self.display_surface.blit(self.sell_text, pos_rect)
            else:
                # buy text
                pos_rect = self.buy_text.get_rect(midleft = (self.main_rect.left + 150, bg_rect.centery))
                self.display_surface.blit(self.buy_text, pos_rect)

    def update(self):
        """ Updates item surface per frame """

        self.input()
        self.display_money()
        for text_index, text_surf in enumerate(self.text_surfs):
            top = self.main_rect.top + text_index * (text_surf.get_height() + (self.padding * 2) + self.space)
            amount_list = list(self.player.player_inventory.values()) + list(self.player.seed_inventory.values())
            self.show_entry(text_surf, amount_list[text_index], top, self.index == text_index)

        



