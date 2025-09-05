# src/whack_a_zombie.py
import pygame as pg
from pathlib import Path
try:
    from .background import Background
    from .SoundManager import SoundManager
    from .ScoreBoard import ScoreBoard
    from .cursor import Cursor
    from .zombies import ZombieManager, IDLE  # <-- NEW
except ImportError:
    from background import Background
    from SoundManager import SoundManager
    from ScoreBoard import ScoreBoard
    from cursor import Cursor
    from zombies import ZombieManager, IDLE  # <-- NEW
import sys
import random
from typing import List, Tuple
import math
from .zombies import ZombieManager, IDLE

# Initialize
pg.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 1024, 768
TILE_SIZE = 64
HOLE_SIZE = 128
SCREEN = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
SPAWN_POS = None
pg.display.set_caption("Whack a Zombies")

# GAME CONSTANTS
GAME_TIME = 20
SCORE_PER_HIT = 1

# --- SPAWN/DESPAWN TUNING ---
ZOMBIE_SIZE = 96                      # size to scale zombie frames (fits nicely into 128px hole)
SPAWN_INTERVAL_RANGE = (0.6, 1.1)     # seconds between spawns
MAX_CONCURRENT_ZOMBIES = 5            # cap active zombies
ZOMBIE_MAX_IDLE = 1.75                # seconds before auto-despawn if not hit

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

def collide(mouse_pos, spawn_pos: List[Tuple[int, int]]) -> bool:
    """Kept for tests: circle hit-check vs HOLE centers."""
    radius = TILE_SIZE
    x_mouse, y_mouse = mouse_pos
    for x_spawn, y_spawn in spawn_pos:
        x_center = x_spawn + HOLE_SIZE / 2
        y_center = y_spawn + HOLE_SIZE / 2
        distance = math.hypot(x_mouse - x_center, y_mouse - y_center)
        if distance <= radius:
            return True
    return False

def top_left_to_center(pos: Tuple[int, int]) -> Tuple[int, int]:
    """Hole top-left -> center coordinate."""
    x, y = pos
    return (int(x + HOLE_SIZE / 2), int(y + HOLE_SIZE / 2))

def main():
    # Initialize
    clock = pg.time.Clock()

    # Hole layout (3 levels: 6 -> 9 -> 12)
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
    hole_centers = [top_left_to_center(p) for p in holes_positions]  # centers used for spawning & hit-test

    # Background
    bg = Background(SCREEN, TILE_SIZE, holes_positions)

    # Audio
    music = SoundManager()
    music.play_background_music()

    # Scoreboard
    scoreboard = ScoreBoard(SCREEN, time_limit=GAME_TIME)

    # Cursor
    cursor = Cursor(SCREEN)
    pg.mouse.set_visible(False)

    # Zombies
    manager = ZombieManager(SCREEN)
    def to_center(xy): return (xy[0] + HOLE_SIZE//2, xy[1] + HOLE_SIZE//2)
    manager.spawn(to_center(holes_positions[0]), size=96)

    # A quick occupancy map so we don’t double-spawn in one hole
    occupied = {i: False for i in range(len(hole_centers))}

    def spawn_one():
        free_indices = [i for i, occ in occupied.items() if not occ]
        if not free_indices:
            return
        idx = random.choice(free_indices)
        center = hole_centers[idx]
        z = manager.spawn(center, size=ZOMBIE_SIZE)
        occupied[idx] = True
        return idx, z  # you can track if needed

    # Spawn cadence
    spawn_timer = random.uniform(*SPAWN_INTERVAL_RANGE)

    # Flags
    running = True
    playing = True

    while running:
        dt = clock.tick(60) / 1000.0  # seconds/frame

        for e in pg.event.get():
            if e.type == pg.QUIT:
                running = False
                pg.quit()
                sys.exit(0)

            elif e.type == pg.MOUSEBUTTONDOWN and e.button == 1:
                cursor.mouse_down()
                # Primary hit detection goes through the animated zombies:
                hit = manager.handle_click(e.pos)
                if hit and playing:
                    music.play_sound("hit")
                    scoreboard.increase_score(SCORE_PER_HIT)
                    # free up the hole under that zombie (approx by nearest center)
                    # (Optional: only needed if you want immediate re-use)
                else:
                    # Fallback sound/UX if they clicked empty space:
                    music.play_sound("miss")
                    if playing:
                        scoreboard.increase_misses()

            elif e.type == pg.MOUSEBUTTONUP and e.button == 1:
                cursor.mouse_up()

            elif e.type == pg.KEYDOWN and e.key == pg.K_r:
                # Restart
                playing = True
                scoreboard.reset()
                # Clear zombies
                manager.entities.clear()
                for k in occupied.keys():
                    occupied[k] = False
                spawn_timer = random.uniform(*SPAWN_INTERVAL_RANGE)

        # Update game timer
        if playing:
            playing = scoreboard.update()

        # --- SPAWN / DESPAWN CONTROLLER ---
        if playing:
            # schedule new spawns
            spawn_timer -= dt
            if spawn_timer <= 0.0 and len(manager.alive()) < MAX_CONCURRENT_ZOMBIES:
                spawn_one()
                spawn_timer = random.uniform(*SPAWN_INTERVAL_RANGE)

            # auto-despawn zombies that sat in IDLE too long
            for z in manager.alive():
                # If a zombie is lingering in IDLE beyond threshold, despawn
                try:
                    if getattr(z, "state", None) == IDLE and getattr(z, "state_time", 0.0) >= ZOMBIE_MAX_IDLE:
                        z.despawn()
                except Exception:
                    pass

        # Update zombies
        manager.update(dt)
        manager.draw()

        # Recompute occupancy (holes re-open after despawn/hit)
        # Simple nearest-center check (fast enough for small counts)
        for i in occupied.keys():
            occupied[i] = False
        for z in manager.alive():
            # Find nearest hole index to this zombie's position
            zx, zy = int(z.pos.x), int(z.pos.y)
            nearest_idx = min(range(len(hole_centers)),
                              key=lambda k: (hole_centers[k][0]-zx)**2 + (hole_centers[k][1]-zy)**2)
            occupied[nearest_idx] = True
            if z.state == IDLE and z.state_time >= z.max_idle:
                z.despawn()

        # Draw
        bg.draw()
        scoreboard.draw()
        manager.draw()
        cursor.draw()

        pg.display.flip()

    # Quit
    pg.quit()
    sys.exit(0)


if __name__ == "__main__":
    main()