# whack_a_zombie.py
import pygame as pg
from pathlib import Path
try:
    from .background import Background
    from .soundmanager import SoundManager
except ImportError:
    from background import Background
    from soundmanager import SoundManager

import sys
import random

pg.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 1024, 768
TILE_SIZE = 64
HOLE_SIZE = 128
SCREEN = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
SPAWN_POS = None
pg.display.set_caption("Whack a Zombies")

def gen_pos(cols, rows):
    w, h = SCREEN.get_size()       
    padding_col = (w - HOLE_SIZE * cols) / (cols + 1)
    padding_row = (h - HOLE_SIZE * rows) / (rows + 1)

    grid = [[None]*cols for _ in range(rows)]
    for r in range(rows):
        y = r * HOLE_SIZE + (r + 1) * padding_row
        for c in range(cols):
            x = c * HOLE_SIZE + (c + 1) * padding_col
            grid[r][c] = (int(x), int(y))

    return grid
    
def main():
    # Initialize
    clock = pg.time.Clock()
    """
    3 levels of hole: 6 -> 9 -> 12
    """
    num_spawns = random.choice([6, 9, 12])
    match num_spawns:
        case (6 | 9) as n:
            cols = 3
            rows = n // 3
            holes_grid = gen_pos(cols, rows)  
        case 12 as n:
            cols = 4
            rows = n // 4
            holes_grid = gen_pos(cols, rows)  
        case _:
            raise ValueError(f"Unexpected: {num_spawns}")

    holes_positions = [pos for row in holes_grid for pos in row]
    bg = Background(SCREEN, TILE_SIZE, holes_positions)
    music = SoundManager()

    # Play background music
    music.play_background_music()
    
    running = True
    while running:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                running = False

        # vẽ mỗi frame
        
        bg.draw()
        pg.display.flip()
        clock.tick(60)

    if not running: 
        pg.quit()
        sys.exit(0)


if __name__ == "__main__":
    main()
