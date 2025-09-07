import pygame as pg
import os
from typing import Tuple, Callable

class ReplayBoard:
    def __init__(self, screen: pg.Surface, font_size: int = 28):
        self.screen = screen
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        
        # Font setup
        font_path = os.path.join('assets', 'Fonts', 'Minecraft.ttf')
        try:
            self.large_font = pg.font.Font(font_path, font_size * 2)  # Larger font for title
            self.font = pg.font.Font(font_path, font_size)
            self.button_font = pg.font.Font(font_path, font_size)
        except FileNotFoundError:
            # Fallback to system font if file not found
            self.large_font = pg.font.SysFont(None, font_size * 2)
            self.font = pg.font.SysFont(None, font_size)
            self.button_font = pg.font.SysFont(None, font_size)
        
        # Colors
        self.text_color = (255, 255, 255)
        self.game_over_color = (255, 0, 0)  # Red color for Game Over text
        self.highlight_color = (255, 255, 0)  # Yellow
        self.button_color = (100, 100, 100)
        self.button_hover_color = (150, 150, 150)
        self.button_text_color = (255, 255, 255)
        
        # Panel setup
        self.panel_width = 500
        self.panel_height = 300
        self.panel_rect = pg.Rect(
            (self.screen_width - self.panel_width) // 2, 
            (self.screen_height - self.panel_height) // 2,
            self.panel_width, 
            self.panel_height
        )
        
        # Buttons
        button_width = 200
        button_height = 50
        button_spacing = 20
        
        # Replay button
        self.replay_button_rect = pg.Rect(
            self.panel_rect.centerx - button_width - button_spacing // 2,
            self.panel_rect.bottom - button_height - 30,
            button_width,
            button_height
        )
        
        # Menu button
        self.menu_button_rect = pg.Rect(
            self.panel_rect.centerx + button_spacing // 2,
            self.panel_rect.bottom - button_height - 30,
            button_width,
            button_height
        )
        
        # Hover state
        self.replay_hover = False
        self.menu_hover = False
        
    def calculate_accuracy(self, hits: int, misses: int) -> float:
        """Calculate player accuracy as a percentage"""
        total = hits + misses
        if total == 0:
            return 0.0
        return (hits / total) * 100
    
    def handle_events(self, event) -> str:
        """Handle mouse events and return action if a button is clicked"""
        if event.type == pg.MOUSEMOTION:
            # Check if mouse is hovering over buttons
            self.replay_hover = self.replay_button_rect.collidepoint(event.pos)
            self.menu_hover = self.menu_button_rect.collidepoint(event.pos)
        
        elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            # Handle button clicks
            if self.replay_hover:
                return "replay"
            elif self.menu_hover:
                return "menu"
        
        elif event.type == pg.KEYDOWN:
            # Handle keyboard shortcuts
            if event.key == pg.K_r:
                return "replay"
            elif event.key == pg.K_m:
                return "menu"
                
        return None
        
    def draw(self, score: int, hits: int, misses: int):
        """Draw the replay board with game stats"""
        # Calculate accuracy
        accuracy = self.calculate_accuracy(hits, misses)
        
        # Semi-transparent overlay
        overlay = pg.Surface((self.screen_width, self.screen_height), pg.SRCALPHA)
        overlay.fill((0, 0, 0, 180))  # Black with 70% opacity
        self.screen.blit(overlay, (0, 0))
        
        # Draw panel background
        pg.draw.rect(self.screen, (50, 50, 50), self.panel_rect, border_radius=10)
        pg.draw.rect(self.screen, (80, 80, 80), self.panel_rect, width=3, border_radius=10)
        
        # Draw title with red color
        title_text = self.large_font.render("Game Over!", True, self.game_over_color)
        title_rect = title_text.get_rect(centerx=self.panel_rect.centerx, top=self.panel_rect.top + 20)
        self.screen.blit(title_text, title_rect)
        
        # Draw score
        score_text = self.font.render(f"Final Score: {score}", True, self.text_color)
        score_rect = score_text.get_rect(centerx=self.panel_rect.centerx, top=title_rect.bottom + 30)
        self.screen.blit(score_text, score_rect)
        
        # Draw accuracy
        accuracy_text = self.font.render(f"Accuracy: {accuracy:.1f}%", True, self.text_color)
        accuracy_rect = accuracy_text.get_rect(centerx=self.panel_rect.centerx, top=score_rect.bottom + 15)
        self.screen.blit(accuracy_text, accuracy_rect)
        
        # Draw hit/miss stats
        stats_text = self.font.render(f"Hits: {hits} | Misses: {misses}", True, self.text_color)
        stats_rect = stats_text.get_rect(centerx=self.panel_rect.centerx, top=accuracy_rect.bottom + 15)
        self.screen.blit(stats_text, stats_rect)
        
        # Draw replay button
        replay_color = self.button_hover_color if self.replay_hover else self.button_color
        pg.draw.rect(self.screen, replay_color, self.replay_button_rect, border_radius=5)
        pg.draw.rect(self.screen, (30, 30, 30), self.replay_button_rect, width=2, border_radius=5)
        
        replay_text = self.button_font.render("Replay (R)", True, self.button_text_color)
        replay_text_rect = replay_text.get_rect(center=self.replay_button_rect.center)
        self.screen.blit(replay_text, replay_text_rect)
        
        # Draw menu button
        menu_color = self.button_hover_color if self.menu_hover else self.button_color
        pg.draw.rect(self.screen, menu_color, self.menu_button_rect, border_radius=5)
        pg.draw.rect(self.screen, (30, 30, 30), self.menu_button_rect, width=2, border_radius=5)
        
        menu_text = self.button_font.render("Menu (M)", True, self.button_text_color)
        menu_text_rect = menu_text.get_rect(center=self.menu_button_rect.center)
        self.screen.blit(menu_text, menu_text_rect)
