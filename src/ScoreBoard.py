import pygame as pg
from typing import Tuple

class ScoreBoard:
    def __init__(self, screen: pg.Surface, font_size: int = 32, 
                 time_limit: int = 15, font_name: str = None):
        self.screen = screen
        self.score = 0
        self.misses = 0
        self.time_limit = time_limit
        self.time_remaining = self.time_limit
        self.start_time = pg.time.get_ticks()
        
        
        # Font setup
        self.font_name = font_name
        self.font = pg.font.SysFont(self.font_name, font_size)
        
        # Colors
        self.text_color = (255, 255, 255)
        self.warning_color = (255, 0, 0)
        
        # Positions for text elements
        self.screen_width = screen.get_width()
        self.score_pos = (20, 20 + font_size + 5)
        self.misses_pos = (20, 20 + font_size * 2 + 10)
        self.timer_pos = (20, 20)
    
    def update(self):
        """Update the timer based on elapsed time"""
        # Calculate time remaining based on elapsed time since start
        elapsed = (pg.time.get_ticks() - self.start_time) // 1000
        self.time_remaining = self.time_limit - elapsed
        
        # Return False when time is up to end the game
        return self.time_remaining > 0
    
    def increase_score(self, points: int = 1):
        """Increase player's score"""
        self.score += points
    
    def increase_misses(self):
        """Increment miss counter"""
        self.misses += 1
    
    def draw(self):
        """Render the scoreboard on screen"""
        # Draw score
        score_text = self.font.render(f"Score: {self.score}", True, self.text_color)
        self.screen.blit(score_text, self.score_pos)
        
        # Draw misses
        misses_text = self.font.render(f"Misses: {self.misses}", True, self.text_color)
        self.screen.blit(misses_text, self.misses_pos)
        
        # Draw timer (red when low on time)
        color = self.warning_color if self.time_remaining < 10 else self.text_color
        timer_text = self.font.render(f"Time: {self.time_remaining}", True, color)
        self.screen.blit(timer_text, self.timer_pos)
    
    def reset(self):
        """Reset scoreboard"""
        self.score = 0
        self.misses = 0
        self.time_remaining = self.time_limit
        self.start_time = pg.time.get_ticks()
        