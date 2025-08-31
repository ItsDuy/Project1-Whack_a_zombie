import pygame
import random
import sys
import time
import os

pygame.init()

SCREEN_WIDTH=1024
SCREEN_HEIGHT=768
TILE_SIZE=64
HOLE_SIZE=128
FPS=60
HOLE_RADIUS=50
GAME_DURATION=60

WHITE=(255,255,255)
BLACK=(0,0,0)
BLUE=(0,0,255)
GREEN=(0,255,0)
RED=(255,0,0)

screen=pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Zombie Whack-a-Mole")
font = pygame.font.SysFont(None, 36)
running = True

# Hole position x TILE_SIZE
holes_positions=[
    (3, 3),
    (7, 3),
    (11, 3),
    (3, 7),
    (7, 7),
    (11, 7)
]

#
# # Check if image file exists, otherwise use a placeholder
# zombie_image_path = "Zombies000.png"
# if os.path.exists(zombie_image_path):
#     zombie_png = pygame.image.load(zombie_image_path)
#     zombie_png = pygame.transform.smoothscale(zombie_png, (HOLE_RADIUS*2, HOLE_RADIUS*2))
# else:
#     # Create a placeholder if image doesn't exist
#     zombie_png = pygame.Surface((HOLE_RADIUS*2, HOLE_RADIUS*2), pygame.SRCALPHA)
#     pygame.draw.circle(zombie_png, (0, 200, 0), (HOLE_RADIUS, HOLE_RADIUS), HOLE_RADIUS)
#     pygame.draw.circle(zombie_png, (0, 100, 0), (HOLE_RADIUS-10, HOLE_RADIUS-10), 10)
#     pygame.draw.circle(zombie_png, (0, 100, 0), (HOLE_RADIUS+10, HOLE_RADIUS-10), 10)
#
# active_zombie = None
# zombie_timer = 0
# zombie_duration = 2.0  # How long a zombie stays visible
# current_zombie_duration = 0  # Store the duration for the current zombie
# score_hits = 0
# score_misses = 0
# game_start = 0
# game_over = False
#
#
# def draw_holes():
#     for pos in holes_positions:
#         pygame.draw.circle(screen, BLACK, pos, HOLE_RADIUS)
#
# def spawn_zombie():
#     return random.choice(holes_positions)
#
# def draw_zombie(position, time_remaining, total_time):
#     # Draw zombie at the specified position, centered on the hole
#     x, y = position
#     screen.blit(zombie_png, (x - HOLE_RADIUS, y - HOLE_RADIUS))
#
#     # Draw time slider above the zombie
#     slider_width = HOLE_RADIUS * 2
#     slider_height = 10
#     slider_x = x - HOLE_RADIUS
#     slider_y = y - HOLE_RADIUS - 20  # Position above the zombie
#
#     # Background of slider (empty part)
#     pygame.draw.rect(screen, BLACK, (slider_x, slider_y, slider_width, slider_height), 1)
#
#     # Filled part of slider (remaining time)
#     fill_width = int(slider_width * (time_remaining / total_time))
#     if fill_width > 0:  # Avoid drawing empty rectangles
#         # Color changes from green to red as time decreases
#         color_ratio = time_remaining / total_time
#         color = (int(255 * (1 - color_ratio)), int(255 * color_ratio), 0)
#         pygame.draw.rect(screen, color, (slider_x, slider_y, fill_width, slider_height))
#
# def draw_timer(seconds_left):
#     timer_text = font.render(f"Time: {seconds_left}s", True, BLACK)
#     screen.blit(timer_text, (SCREEN_WIDTH - 150, 20))
#
# def draw_score():
#     hits_text = font.render(f"Hits: {score_hits}", True, GREEN)
#     misses_text = font.render(f"Misses: {score_misses}", True, RED)
#     screen.blit(hits_text, (20, 20))
#     screen.blit(misses_text, (20, 60))
#
# def check_zombie_click(mouse_pos):
#     global active_zombie, score_hits, zombie_timer, current_zombie_duration
#
#     if active_zombie:
#         x, y = active_zombie
#         # Calculate if the click is within the zombie area
#         distance = ((mouse_pos[0] - x) ** 2 + (mouse_pos[1] - y) ** 2) ** 0.5
#         if distance <= HOLE_RADIUS:
#             # Hit!
#             score_hits += 1
#             active_zombie = None
#             zombie_timer = 0
#             current_zombie_duration = 0
#             return True
#     return False
#
# def draw_game_over():
#     overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
#     overlay.fill((0, 0, 0, 180))  # Semi-transparent black overlay
#     screen.blit(overlay, (0, 0))
#
#     game_over_text = font.render("GAME OVER", True, WHITE)
#     final_score = font.render(f"Final Score: {score_hits} hits, {score_misses} misses", True, WHITE)
#     restart_text = font.render("Press SPACE to play again", True, WHITE)
#
#     screen.blit(game_over_text, (SCREEN_WIDTH//2 - game_over_text.get_width()//2, SCREEN_HEIGHT//2 - 60))
#     screen.blit(final_score, (SCREEN_WIDTH//2 - final_score.get_width()//2, SCREEN_HEIGHT//2))
#     screen.blit(restart_text, (SCREEN_WIDTH//2 - restart_text.get_width()//2, SCREEN_HEIGHT//2 + 60))
#
# def reset_game():
#     global active_zombie, zombie_timer, current_zombie_duration, score_hits, score_misses, game_start, game_over
#     active_zombie = None
#     zombie_timer = 0
#     current_zombie_duration = 0
#     score_hits = 0
#     score_misses = 0
#     game_start = time.time()
#     game_over = False
#
# def main():
#     global active_zombie, zombie_timer, current_zombie_duration, score_hits, score_misses, game_start, game_over
#
#     clock = pygame.time.Clock()
#     reset_game()
#
#     running = True
#     while running:
#         current_time = time.time()
#         seconds_left = max(0, GAME_DURATION - int(current_time - game_start))
#
#         # Check for game over
#         if seconds_left <= 0 and not game_over:
#             game_over = True
#
#         # Process events
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 running = False
#             elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
#                 if not game_over:
#                     if not check_zombie_click(event.pos) and active_zombie:
#                         # Miss! (only count if there was an active zombie)
#                         score_misses += 1
#             elif event.type == pygame.KEYDOWN:
#                 if event.key == pygame.K_SPACE and game_over:
#                     reset_game()
#
#         # Game logic (only if game is not over)
#         if not game_over:
#             # Zombie spawning logic
#             zombie_timer -= 1/FPS
#
#             # If no active zombie or timer expired, spawn a new one
#             if active_zombie is None or zombie_timer <= 0:
#                 if active_zombie:
#                     # If there was a zombie and timer expired, count as miss
#                     score_misses += 1
#
#                 active_zombie = spawn_zombie()
#                 current_zombie_duration = random.uniform(1.0, zombie_duration)
#                 zombie_timer = current_zombie_duration
#
#         # Drawing
#         screen.fill(WHITE)
#         draw_holes()
#
#         if active_zombie and not game_over:
#             # Pass the remaining time and total duration to the draw function
#             draw_zombie(active_zombie, zombie_timer, current_zombie_duration)
#
#         draw_timer(seconds_left)
#         draw_score()
#
#         if game_over:
#             draw_game_over()
#
#         pygame.display.flip()
#         clock.tick(FPS)
#
#     pygame.quit()
#     sys.exit()

class Background:
    # Creates a tile map according to screen size
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

    # renders them tiles on screen
    def bg_render(self, rows, cols, tile_map):
        # key-value dictionary to select tiles from
        background_tiles = {
            i: pygame.image.load(f"../assets/images/background/tile{i}.png").convert()
            for i in range(1, 10)
        }

        for row in range(rows):
            for col in range(cols):
                tile_number = tile_map[row][col]
                tile_image = background_tiles[tile_number]
                x = col * TILE_SIZE
                y = row * TILE_SIZE
                screen.blit(tile_image, (x, y))

    def add_grass(self, rows, cols):
        global holes_positions
        for row in range(1, rows):
            for col in range(1, cols):

                grass = random.randrange(1, 101, 1)
                if grass < 86:
                    continue
                elif grass < 93:
                    grass_image = pygame.image.load("../assets/images/background/grass1.png").convert()
                    screen.blit(grass_image, (col * TILE_SIZE, row * TILE_SIZE))
                else:
                    grass_image = pygame.image.load("../assets/images/background/grass2.png").convert()
                    screen.blit(grass_image, (col * TILE_SIZE, row * TILE_SIZE))


    # punch the 6 holes onto the screen with coords from holes_position
    def punch_holes(self):
        global holes_positions
        hole_image = pygame.image.load("../assets/images/background/hole.png").convert()
        for x, y in holes_positions:
            screen.blit(hole_image, (x * TILE_SIZE, y * TILE_SIZE))


    def bg(self):
        rows, cols = round(SCREEN_HEIGHT / TILE_SIZE), round(SCREEN_WIDTH / TILE_SIZE)
        tile_map = self.bg_tile_map(rows, cols)

        self.bg_render(rows, cols, tile_map)
        self.add_grass(rows, cols)
        self.punch_holes()



def main():
    global running
    background = Background()
    background.bg()

    pygame.display.flip()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

if __name__ == "__main__":
    main()