# Libraries
import pygame as pg
from os import walk


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
            surface_dict[name.split(".")[0]] = pg.image.load(full_path).convert_alpha()
    
    return surface_dict