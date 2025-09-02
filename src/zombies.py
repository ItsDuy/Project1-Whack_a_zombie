from pathlib import Path
import random
import pygame as pg

# Images for Zombies
ASSETS = Path(__file__).resolve().parent.parent / "assets" / "images" / "zombies"

class Zombies():
    def __init__(self, screen: pg.Surface, z_size: int):
        self.screen = screen
        self.size = z_size
        