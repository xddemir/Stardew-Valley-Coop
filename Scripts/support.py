# Libraries
import pygame as pg
from os import walk
from configparser import ConfigParser

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


def convert_config_file(setting: dict):
    config = ConfigParser()
    config.read(f'../config.ini')
    for key, val in setting.items():
        if isinstance(val, int):
            setting[key] = int(config["SCREEN_SETTINGS"][key])
        elif isinstance(val, dict) and key in config.sections():
            options = config.options(section=key)
            for option in options:
                option_val = config.get(section=key, option=option)
                setting[key][option] = int(option_val) if isinstance(option_val, int) else float(option_val)
    
    setting["OVERLAY_POSITIONS"]["tool"] = [int(x) for x in config["tool"].values()]
    setting["OVERLAY_POSITIONS"]["seed"] = [int(x) for x in config["seed"].values()]