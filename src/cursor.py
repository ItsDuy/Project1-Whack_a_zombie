import pygame as pg
from pathlib import Path

ASSETS = Path(__file__).resolve().parent.parent / "assets" / "images" / "cursor"

class Cursor:
    def __init__(self, screen: pg.Surface):
        # Cursor in Game
        self.image = pg.image.load(str(ASSETS / "hammer0.png")).convert_alpha()
        self.rect = self.image.get_rect()
        
        self.screen = screen
    def mouse_down(self):
        self.image = pg.image.load(str(ASSETS / "hammer1.png")).convert_alpha()

    def mouse_up(self):
        self.image = pg.image.load(str(ASSETS / "hammer0.png")).convert_alpha()

    def draw(self):
        pg.mouse.set_visible(False)
        self.rect.center = pg.mouse.get_pos()
        self.screen.blit(self.image, self.rect)