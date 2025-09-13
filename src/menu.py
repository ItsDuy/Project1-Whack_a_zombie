import os
from pathlib import Path
import pygame as pg

ASSETS = Path(__file__).resolve().parent.parent / "assets" / "images" / "menu"
FONT = Path(__file__).resolve().parent.parent / "assets" / "fonts"

class Menu:
    def __init__(self, screen: pg.Surface, font_size: int = 36):
        self.level = 0   # 0, 1, 2 for 6, 9, 12 holes respectively
        self.screen = screen
        self.width = self.screen.get_width()
        self.height = self.screen.get_height()

        font_path = FONT / "Pixellari.ttf"

        try:
            self.large_font = pg.font.Font(font_path, font_size * 3)  # Larger font for title
            self.font = pg.font.Font(font_path, font_size)
        except FileNotFoundError:
            # Fallback to system font if file not found
            self.large_font = pg.font.SysFont(None, font_size * 2)
            self.font = pg.font.SysFont(None, font_size)

        # Colors
        self.title_color = (255, 255, 255)
        self.lv_color = (127, 127, 127)

        self.start_btn = pg.image.load(ASSETS / "Play_Not-Pressed.png").convert()
        self.quit_btn = pg.image.load(ASSETS / "Quit_Not-Pressed.png").convert()
        self.arrow_l = pg.image.load(ASSETS / "arrow_left.png").convert()
        self.arrow_r = pg.image.load(ASSETS / "arrow_right.png").convert()

        btn_size = (76 * 3, 21 * 3)
        arrow_size = (7 * 5, 11 * 5)

        # Buttons
        self.start_btn = pg.transform.scale(self.start_btn, btn_size)
        self.start_btn_rect = self.start_btn.get_rect()
        self.quit_btn = pg.transform.scale(self.quit_btn, btn_size)
        self.quit_btn_rect = self.quit_btn.get_rect()

        # L and R arrows
        self.arrow_l = pg.transform.scale(self.arrow_l, arrow_size)
        self.l_rect = self.arrow_l.get_rect()

        self.arrow_r = pg.transform.scale(self.arrow_r, arrow_size)
        self.r_rect = self.arrow_r.get_rect()

        # Hover states
        self.start_hover = False
        self.quit_hover = False
        self.l_hover = False
        self.r_hover = False

    def handle_events(self, event) -> str:
        if event.type == pg.MOUSEMOTION:
            # Check if mouse is hovering over buttons
            self.start_hover = self.start_btn_rect.collidepoint(event.pos)
            self.l_hover = self.l_rect.collidepoint(event.pos)
            self.r_hover = self.r_rect.collidepoint(event.pos)
            self.quit_hover = self.quit_btn_rect.collidepoint(event.pos)
        elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if self.start_hover:
                print("Play")
                return "play"
            elif self.l_hover:
                print("Left")
                return "left"
            elif self.r_hover:
                print("Right")
                return "right"
            elif self.quit_hover:
                print("Quit")
                return "quit"
        return None

    def draw(self, curr_diff = 0):
        # Semi-transparent overlay
        overlay = pg.Surface((self.width, self.height), pg.SRCALPHA)
        overlay.fill((0, 0, 0, 127))  # Black with 70% opacity
        self.screen.blit(overlay, (0, 0))

        # Draw game title
        title_text = self.large_font.render("WHACK-A-ZOMBIE", False, self.title_color)
        title_rect = title_text.get_rect()
        title_rect.center = (self.width / 2, self.height / 4)
        self.screen.blit(title_text, title_rect)

        # Draw start button
        self.start_btn_rect.center = (self.width / 2, self.height / 2)
        self.screen.blit(self.start_btn, self.start_btn_rect)

        # Draw L and R arrows
        self.l_rect.center = (self.width / 3, self.height / 3 * 2)
        self.r_rect.center = (self.width / 3 * 2, self.height / 3 * 2)
        self.screen.blit(self.arrow_r, self.r_rect)
        self.screen.blit(self.arrow_l, self.l_rect)

        # Draw difficulty
        diff_text = self.font.render("Easy", False, self.lv_color)
        match curr_diff:
            case 0:
                diff_text = self.font.render("Easy", False, self.lv_color)
            case 1:
                diff_text = self.font.render("Medium", False, self.lv_color)
            case 2:
                diff_text = self.font.render("PPL", False, self.lv_color)
        diff_rect = diff_text.get_rect()
        diff_rect.center = (self.width / 2, self.height / 3 * 2)
        self.screen.blit(diff_text, diff_rect)

        # Draw quit button
        self.quit_btn_rect.center = (self.width / 2, self.height / 4 * 3.3)
        self.screen.blit(self.quit_btn, self.quit_btn_rect)