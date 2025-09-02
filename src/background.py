from pathlib import Path
import random
import pygame as pg
from typing import List

# Images for the Background
ASSETS = Path(__file__).resolve().parent.parent / "assets" / "images" / "background"
class Background:
    def __init__(self, screen: pg.Surface, tile_size: int, hole_positions: List, seed: int = 1337):
        self.screen = screen
        self.tile_size = tile_size
        self.holes_positions = hole_positions   # (1,2) (2,3), (3, 4)
        self.rng = random.Random(seed)

        # preload
        self.tiles = {i: pg.image.load(str(ASSETS / f"tile{i}.png")).convert() for i in range(1,10)}
        self.grass1 = pg.image.load(str(ASSETS / "grass1.png")).convert()
        self.grass2 = pg.image.load(str(ASSETS / "grass2.png")).convert()
        self.hole   = pg.image.load(str(ASSETS / "hole.png")).convert()

        # Draw Random Grass 
        w, h = screen.get_size()
        self.cols = round(w / tile_size)
        self.rows = round(h / tile_size)
        self.grass_map = [[0]*self.cols for _ in range(self.rows)]
        for r in range(1, self.rows):
            for c in range(1, self.cols):
                g = self.rng.randrange(1, 101)
                if g < 86:
                    continue
                self.grass_map[r][c] = 1 if g < 93 else 2  # 1: grass1, 2: grass2

    def bg_tile_map(self, rows, cols):
        tile_map = [[5 for _ in range(cols)] for _ in range(rows)]
        for i in range(rows):
            tile_map[i][0] = 4
            tile_map[i][cols - 1] = 6
        for i in range(cols):
            tile_map[0][i] = 2
            tile_map[rows - 1][i] = 8
        tile_map[0][0] = 1
        tile_map[0][cols - 1] = 3
        tile_map[rows - 1][0] = 7
        tile_map[rows - 1][cols - 1] = 9
        return tile_map

    def draw(self):
        w, h = self.screen.get_size()
        cols = round(w / self.tile_size)
        rows = round(h / self.tile_size)

        tile_map = self.bg_tile_map(rows, cols)

        # render tiles
        for r in range(rows):
            for c in range(cols):
                num = tile_map[r][c]
                self.screen.blit(self.tiles[num], (c*self.tile_size, r*self.tile_size))

        # add grass
        for r in range(1, self.rows):
            for c in range(1, self.cols):
                if self.grass_map[r][c] == 1:
                    self.screen.blit(self.grass1, (c * self.tile_size, r * self.tile_size))
                elif self.grass_map[r][c] == 2:
                    self.screen.blit(self.grass2, (c * self.tile_size, r * self.tile_size))
        
        # punch holes
        for x, y in self.holes_positions:  
            self.screen.blit(self.hole, (int(x), int(y)))
                                                                                                                                  
