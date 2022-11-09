# Libraries
import pygame as pg
from os import walk, path
from configparser import ConfigParser


# Constants
from settings import *


def import_folder(path) -> list:
    """ Helper function to retrieve images in list format """

    surface_list = []
    for _, __, names in walk(path):
        for name in names:
            full_path = path + "/" + name
            img = pg.image.load(full_path).convert_alpha()
            surface_list.append(img)

    return surface_list


def import_folder_dict(path) -> dict:
    """ Helper function to retrieve images in hash-set """

    surface_dict: dict = {}
    for _, __, names in walk(path):
        for name in names:
            full_path = path + "/" + name
            surface_dict[name.split(".")[0]] = pg.image.load(
                full_path).convert_alpha()

    return surface_dict


def create_config_file():

    config = ConfigParser()

    config["DEFAULT"] = {
        "SCREEN_WIDTH": SCREEN_WIDTH,
        "SCREEN_HEIGHT": SCREEN_HEIGHT,
        "TILE_SIZE": TILE_SIZE
    }

    config["tool"] = {
        "x": OVERLAY_POSITIONS["tool"][0],
        "y": OVERLAY_POSITIONS["tool"][1]
    }

    config['seed'] = {
        "x": OVERLAY_POSITIONS["seed"][0],
        "y": OVERLAY_POSITIONS["seed"][1]
    }

    config["LAYERS"] = {
        'water': LAYERS["water"],
        'ground': LAYERS["ground"],
        'soil': LAYERS["soil"],
        'soil water': LAYERS['soil water'],
        'rain floor': LAYERS["rain floor"],
        'house bottom': LAYERS["house bottom"],
        'ground plant': LAYERS["ground plant"],
        'main': LAYERS["main"],
        'house top': LAYERS["house top"],
        'fruit': LAYERS["fruit"],
        'rain drops': LAYERS["rain drops"]
    }

    config["GROW_SPEEDS"] = {
        'corn': GROW_SPEEDS["corn"],
        'tomato': GROW_SPEEDS["tomato"]
    }

    config["SELL_PRICES"] = {
        'wood': SELL_PRICES["wood"],
        'apple': SELL_PRICES["apple"],
        'corn': SELL_PRICES["corn"],
        'tomato': SELL_PRICES["tomato"]
    }

    config["PURCHASE_PRICES"] = {
        'corn': PURCHASE_PRICES["corn"],
        'tomato': PURCHASE_PRICES["tomato"]
    }

    with open(f"../config.ini", "w") as f:
        config.write(f)

def read_config_file():
    config = ConfigParser()
    config.read(f'../config.ini')
    for key, val in settings.items():
        if isinstance(val, str):
            settings[key] = config[key]
        elif isinstance(val, dict):
            for sub_key in val.keys():
                val[sub_key] = int(config[key][sub_key]) if isinstance(config[key][sub_key], int) else float(config[key][sub_key]) 
                