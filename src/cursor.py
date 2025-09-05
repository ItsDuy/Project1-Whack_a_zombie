import pygame as pg
from pathlib import Path

ASSETS = Path(__file__).resolve().parent.parent / "assets" / "images" / "cursor"

class Cursor:
    def __init__(self, screen: pg.Surface):
        self.img_up = pg.image.load(str(ASSETS / "hammer0.png")).convert_alpha()
        self.img_down = pg.image.load(str(ASSETS / "hammer1.png")).convert_alpha()
        self.image = self.img_up
        self.rect = self.image.get_rect()
        self.screen = screen
        self.hold_timer = 0.0

    def mouse_down(self):
        self.image = self.img_down  
        self.hold_timer = 0.12

    def mouse_up(self):
        self.image = self.img_up    

    def update(self, dt):
        if self.hold_timer > 0:
            self.hold_timer -= dt
            if self.hold_timer <= 0:
                self.mouse_up()

    def draw(self, dt): 
        self.update(dt)
        self.rect.center = pg.mouse.get_pos()
        self.screen.blit(self.image, self.rect)