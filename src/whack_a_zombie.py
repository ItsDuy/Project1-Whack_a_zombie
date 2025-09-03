# whack_a_zombie.py
import pygame as pg
from pathlib import Path
try:
    from .background import Background
    from .SoundManager import SoundManager
    from .ScoreBoard import ScoreBoard
except ImportError:
    from background import Background
    from SoundManager import SoundManager
    from ScoreBoard import ScoreBoard
import sys
import random
from typing import List
import math

# Initialize
pg.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 1024, 768
TILE_SIZE = 64
HOLE_SIZE = 128
SCREEN = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
SPAWN_POS = None
pg.display.set_caption("Whack a Zombies")

#GAME CONSANTS
GAME_TIME=60
SCORE_PER_HIT=1

def gen_pos(cols, rows) -> List[List]:
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

def collide(mouse_pos, spawn_pos: List) -> bool:
    radius = TILE_SIZE
    x_mouse, y_mouse = mouse_pos
    for x_spawn, y_spawn in spawn_pos:
            x_center = x_spawn + HOLE_SIZE / 2
            y_center = y_spawn + HOLE_SIZE / 2

            distance = math.sqrt(
                math.pow(x_mouse - x_center, 2) + \
                math.pow(y_mouse - y_center, 2)
            )
            if distance <= radius:
                return True
    return False

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

    # Scoreboard
    scoreboard = ScoreBoard(SCREEN, time_limit=GAME_TIME)

    # Flags
    running = True

    while running:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                running = False
                pg.quit()
                sys.exit(0)
            if e.type == pg.MOUSEBUTTONDOWN and e.button == 1:
                if collide(e.pos, holes_positions):
                    music.play_sound("hit")
                    scoreboard.increase_score(SCORE_PER_HIT)
                    print("Click: HIT")
                else:
                    music.play_sound("miss")
                    scoreboard.increase_misses()
                    print("Click: MISS")

        # Update
        running = scoreboard.update()

        bg.draw()
        scoreboard.draw()
        pg.display.flip()
        clock.tick(60)

    if not running: 
        pg.quit()
        sys.exit(0)


if __name__ == "__main__":
    main()
