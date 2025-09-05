# src/zombies.py
from pathlib import Path
from typing import List, Tuple, Optional
import pygame as pg

ASSETS = Path(__file__).resolve().parent.parent / "assets" / "images" / "zombies"

class Zombies:
    def __init__(self, screen: pg.Surface, z_size: int,
                 idle_fps: float = 10.0, death_fps: float = 12.0,
                 linger_after_death: float = 0.4):
        self.screen = screen
        self.size = (z_size, z_size)
        self.idle_fps = idle_fps
        self.death_fps = death_fps
        self.linger_after_death = linger_after_death

        # State
        self.state: str = "idle"   # "idle" | "death"
        self.index: int = 0
        self.accum: float = 0.0
        self.frame_time: float = 1.0 / self.idle_fps
        self.loop: bool = True
        self.finished: bool = False
        self.linger: float = 0.0
        self.hit: bool = False

        # Visuals
        self.image: Optional[pg.Surface] = None
        self.rect: Optional[pg.Rect] = None

        # Frames
        self.idle_frames: List[pg.Surface] = self.load_frames(ASSETS / "idle")
        self.death_frames: List[pg.Surface] = self.load_frames(ASSETS / "death")

        if not self.idle_frames:
            raise RuntimeError(f"No idle frames found in {ASSETS / 'idle'}")
        if not self.death_frames:
            print(f"[Zombies] Warning: no death frames found in {ASSETS / 'death'}")
        
        self.image = self.idle_frames[0]
        self.rect = self.image.get_rect(topleft=(0, 0))

        # Property
        self.idle_cycle = (len(self.idle_frames) / self.idle_fps) if self.idle_fps > 0 else 0.6
        self.stay_timer = 2.0 * self.idle_cycle       
        self.respawn_delay = 0.1           
        self.respawn_timer = 0.0

    def load_frames(self, folder: Path) -> List[pg.Surface]:
        """ Loaders """
        paths = sorted(folder.glob("*.png"), key=numeric_key)
        frames: List[pg.Surface] = []
        for p in paths:
            img = pg.image.load(str(p)).convert_alpha()
            if img.get_size() != self.size:
                img = pg.transform.smoothscale(img, self.size)
            frames.append(img)
        return frames

    def reset(self):
        """ Reset Properies """
        self.idle_cycle = (len(self.idle_frames) / self.idle_fps) if self.idle_fps > 0 else 0.6
        self.stay_timer = 2.0 * self.idle_cycle                  
        self.respawn_timer = 0.0 
        self.hit = False
        
    # --- Controls ---
    def play_idle(self):
        """ Setting for Idle state """
        self.state = "idle"
        self.index = 0
        self.accum = 0.0
        self.frame_time = 1.0 / self.idle_fps
        self.loop = True
        self.finished = False
        self.linger = 0.0
        if self.idle_frames:
            self.image = self.idle_frames[0]

    def play_death(self):
        """ Setting for Death state """
        self.state = "death"
        self.index = 0
        self.accum = 0.0
        self.frame_time = 1.0 / self.death_fps
        self.loop = False
        self.finished = False
        self.linger = 0.0
        if self.death_frames:
            self.image = self.death_frames[0]

    # --- Update & Draw ---
    def step_frame(self):
        """ Moving to next Frame """
        frames = self.idle_frames if self.state == "idle" else self.death_frames
        if not frames:
            return

        self.index += 1
        if self.index >= len(frames):
            if self.loop:
                self.index = 0
            else:
                """ Delaying Time for Death state """
                self.index = len(frames) - 1
                self.finished = True
                self.linger = self.linger_after_death

        self.image = frames[self.index]

    def update(self, dt: float):
        """ Update new Frame """
        if self.finished:
            if self.linger > 0:
                self.linger -= dt
            return

        self.accum += dt
        while self.accum >= self.frame_time:
            self.accum -= self.frame_time
            self.step_frame()

    def draw(self, center_pos: Tuple[int, int]):
        """Render the Zombie on screen"""
        if not self.rect:
            return
        self.rect.center = (int(center_pos[0]), int(center_pos[1]))
        if self.image:
            self.screen.blit(self.image, self.rect)

    def bar_draw(self, center_pos: Tuple[int, int]):
        """ Drawing bar timer over Zombie's head """
        if self.stay_timer <= 0:
            return
    
        fraction = max(0.0, min(1.0, self.stay_timer / (self.idle_cycle * 2)))
        
        BAR_W, BAR_H = 72, 8
        x = int(center_pos[0] - BAR_W / 2) 
        y = int(center_pos[1] - self.size[0] // 2 - 12)

        bg_rect = pg.Rect(x, y, BAR_W, BAR_H)
        pg.draw.rect(self.screen, (35, 35, 35), bg_rect, border_radius = 4)

        r = int(255 * (1.0 - fraction))
        g = int(200 * fraction)
        fill_rect = pg.Rect(x + 1, y + 1, int((BAR_W - 2) * fraction), BAR_H - 2)
        
        # Apply linear interpolation from Green to Red
        pg.draw.rect(self.screen, (r, g, 60), fill_rect, border_radius = 4)         
        pg.draw.rect(self.screen, (220, 220, 220), bg_rect, width = 1, border_radius = 4)  

    @property
    def is_finished(self) -> bool:
        return self.finished

def numeric_key(p: Path):
    import re
    m = re.findall(r'(\d+)', p.stem)
    return [int(x) for x in m] if m else [p.stem]