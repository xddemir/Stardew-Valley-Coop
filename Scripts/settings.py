import pygame as pg

# screen
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

TILE_SIZE = 64

# overlay positions
OVERLAY_POSITIONS = {
    'tool': (40, SCREEN_HEIGHT - 15),
    'seed': (70, SCREEN_HEIGHT - 5)
}

APPLE_POS = {"Small": [(18, 17), (30, 17), (12, 50), 
                       (30, 45), (20, 30), (30, 10)],
             "Large": [(30, 24), (60, 65), (50, 50),
                       (16, 40), (45, 50), (42, 70)]}
                       

# layers
LAYERS = {
    'water': 0,
    'ground': 1,
    'soil': 2,
    'soil water': 3,
    'rain floor': 4,
    'house bottom': 5,
    'ground plant': 6,
    'main': 7,
    'house top': 8,
    'fruit': 9,
    'rain drops': 10
}

# tool offsets
PLAYER_TOOL_OFFSET = {
    'left': pg.Vector2(-50, 40),
    'right': pg.Vector2(50, 40),
    'up': pg.Vector2(0, -10),
    'down': pg.Vector2(0, 50)
}

# grow speeds
GROW_SPEEDS = {
    'corn': 1,
    'tomato': 0.7
}

# sell prices
SELL_PRICES = {
    'wood': 4,
    'apple': 2,
    'corn': 10,
    'tomato': 20
}

# purchase prices
PURCHASE_PRICES = {
    'corn': 4,
    'tomato': 5
}