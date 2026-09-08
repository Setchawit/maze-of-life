import pygame
from os.path import join
from os import walk
import os, sys

WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720 # 1920, 1080
TILE_SIZE = 64
FPS = 0

def resource_path(path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, path)