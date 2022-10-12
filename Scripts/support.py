import pygame as pg
from os import walk


def import_folder(path) -> list:
    surface_list = []

    for _, __, names in walk(path):
        for name in names:
            full_path = path + "/" + name
            img = pg.image.load(full_path).convert_alpha()
            surface_list.append(img)
    
    return surface_list