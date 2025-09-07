# src/whack_a_zombie.py
import pygame as pg
from pathlib import Path
try:
    from .background import Background
    from .SoundManager import SoundManager
    from .ScoreBoard import ScoreBoard
    from .cursor import Cursor
    from .zombies import Zombies
    from .ReplayBoard import ReplayBoard
except ImportError:
    from background import Background
    from SoundManager import SoundManager
    from ScoreBoard import ScoreBoard
    from cursor import Cursor
    from zombies import Zombies
    from ReplayBoard import ReplayBoard
import sys
import random
from typing import List, Tuple
from typing import List, Tuple
import math

# Initialize
pg.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 1024, 768
TILE_SIZE = 64
HOLE_SIZE = 128
SCREEN = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
FPS = 60
pg.display.set_caption("Whack a Zombies")

# GAME CONSANTS
GAME_TIME = 20
SCORE_PER_HIT = 1
ZOMBIE_SIZE = 64

""" Helper Functions """
def gen_pos(cols, rows) -> List[List]:
    """ Generate positions for Holes """
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

def collide(mouse_pos, spawn_pos: Tuple[float, float]) -> bool:
    """ Check if Zombie is clicked or not """
    radius = TILE_SIZE
    x_mouse, y_mouse = mouse_pos
    x_center, y_center = spawn_pos
    distance = math.sqrt(
        math.pow(x_mouse - x_center, 2) + \
        math.pow(y_mouse - y_center, 2)
    )
    if distance <= radius:
        return True
    return False

def center_pos(pos: Tuple[float, float]) -> Tuple[float, float]:
    """ Centering the Position """
    x, y = pos
    return (x + HOLE_SIZE / 2, y + HOLE_SIZE / 2)

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
    holes_center = [center_pos(pos) for pos in holes_positions]     # Standardize the positions of holds

    # Background
    bg = Background(SCREEN, TILE_SIZE, holes_positions)

    # Audio
    music = SoundManager()
    music.play_background_music()

    # Scoreboard
    scoreboard = ScoreBoard(SCREEN, time_limit=GAME_TIME)

    # Cursor
    pg.mouse.set_visible(False)
    cursor = Cursor(SCREEN)

    # Zombies
    zombie = Zombies(SCREEN, ZOMBIE_SIZE, idle_fps=10, death_fps=12)
    current_pos = random.choice(holes_center)
    zombie.play_idle()

    # Initialize ReplayBoard
    replay_board = ReplayBoard(SCREEN)
    
    # Flags
    running = True
    playing = True
    show_replay_board = False

    while running:
        dt = clock.get_time() / 1000

        for e in pg.event.get():
            """ Events for game play """
            if e.type == pg.QUIT:
                running = False
                pg.quit()
                sys.exit(0)

            # Handle replay board events when it's shown
            if not show_replay_board:
                # Normal gameplay events
                if e.type == pg.MOUSEBUTTONDOWN and e.button == 1:
                    cursor.mouse_down()
                    if collide(e.pos, current_pos):
                        if playing and zombie.state != "death" and not zombie.hit:
                            music.play_sound("hit")
                            zombie.play_death()
                            zombie.hit = True
                            scoreboard.increase_score(SCORE_PER_HIT)
                            print("Click: HIT")
                    else:
                        # Fallback sound/UX if they clicked empty space:
                        music.play_sound("miss")
                elif e.type == pg.KEYDOWN and e.key == pg.K_r and not show_replay_board:
                    # Restart during gameplay
                    playing = True
                    scoreboard.reset()
                    current_pos = random.choice(holes_center)
                    zombie.play_idle()
                    zombie.reset()
            else:
                action = replay_board.handle_events(e)
                if action == "replay":
                    # Restart the game
                    playing = True
                    show_replay_board = False
                    scoreboard.reset()
                    current_pos = random.choice(holes_center)
                    zombie.play_idle()
                    zombie.reset()
                elif action == "menu":
                    # Exit to menu (not implemented - just restart for now)
                    """
                    playing = True
                    show_replay_board = False
                    scoreboard.reset()
                    current_pos = random.choice(holes_center)
                    zombie.play_idle()
                    zombie.reset()
                    """
                    pass

        # Update game timer
        if playing:
            playing = scoreboard.update()
            # Show replay board when game ends
            if not playing:
                show_replay_board = True

        # Random Zombie
        zombie.update(dt)   # Update next Frame
        if zombie.state == "idle" and zombie.respawn_timer <= 0:
            zombie.stay_timer -= dt
            if zombie.stay_timer <= 0 and playing:
                scoreboard.increase_misses() 
                print("Click: MISS")
                current_pos = random.choice(holes_center)
                zombie.play_idle()
                zombie.reset()
        if zombie.is_finished and zombie.linger <= 0:
            zombie.respawn_timer += dt
            if zombie.respawn_timer >= zombie.respawn_delay:
                current_pos = random.choice(holes_center)
                zombie.play_idle()
                zombie.reset()

        # Draw function
        bg.draw()
        scoreboard.draw()
        if playing:
            zombie.draw(current_pos)
            if zombie.state == 'idle' and zombie.respawn_timer <= 0:
                zombie.bar_draw(current_pos)
        
        # Draw replay board if game is over
        if show_replay_board:
            replay_board.draw(scoreboard.score, scoreboard.hits, scoreboard.misses)
            
        # Always draw cursor last so it's on top
        cursor.draw(dt)   

        pg.display.flip()
        clock.tick(FPS)  

    # Quit
    pg.quit()
    sys.exit(0)


if __name__ == "__main__":
    main()