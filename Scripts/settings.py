import pygame as pg
from support import convert_config_file
from dataclasses import dataclass

settings = {
    "SCREEN_WIDTH": 0,
    "SCREEN_HEIGHT": 0,
    "TILE_SIZE": 0,
    "tool": {},
    "seed": {},
    "LAYERS": {},
    "GROW_SPEEDS": {},
    "SELL_PRICES": {},
    "PURCHASE_PRICES": {},
    "OVERLAY_POSITIONS": {}
}

@dataclass
class Settings:
    convert_config_file(settings)

    # screen
    SCREEN_WIDTH = settings["SCREEN_WIDTH"]
    SCREEN_HEIGHT = settings["SCREEN_HEIGHT"]

    TILE_SIZE = settings["TILE_SIZE"]

    # overlay positions
    OVERLAY_POSITIONS = settings["OVERLAY_POSITIONS"]

    APPLE_POS = {"Small": [(18, 17), (30, 17), (12, 50),
                        (30, 45), (20, 30), (30, 10)],
                "Large": [(30, 24), (60, 65), (50, 50),
                        (16, 40), (45, 50), (42, 70)]}

    # layers
    LAYERS = settings["LAYERS"]

    # tool offsets
    PLAYER_TOOL_OFFSET = {
        'left': pg.Vector2(-50, 40),
        'right': pg.Vector2(50, 40),
        'up': pg.Vector2(0, -10),
        'down': pg.Vector2(0, 50)
    }

    # grow speeds
    GROW_SPEEDS = settings["GROW_SPEEDS"]

    # sell prices
    SELL_PRICES = settings["SELL_PRICES"]

    # purchase prices
    PURCHASE_PRICES = settings["PURCHASE_PRICES"]


setting = Settings()