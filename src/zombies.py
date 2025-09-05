# src/zombies.py
from pathlib import Path
from typing import List, Tuple, Optional
import math
import pygame as pg

from .animation import AnimationClip, Animator

ASSETS = Path(__file__).resolve().parent.parent / "assets" / "images" / "zombies"

SPAWNING   = "spawning"
IDLE       = "idle"
HIT        = "hit"
DESPAWNING = "despawning"
DEAD       = "dead"

def _load_frames(size: int) -> List[pg.Surface]:
    names = [f"Zombies00{i}.png" for i in range(6)]
    frames: List[pg.Surface] = []
    for n in names:
        img = pg.image.load(str(ASSETS / n)).convert_alpha()
        if size:
            img = pg.transform.smoothscale(img, (size, size))
        frames.append(img)
    return frames

class Zombies:
    """
    One zombie with spawn/despawn animations and a simple state machine.
    Public API:
      spawn_at((x, y)), hit(), despawn(), update(dt), draw(), is_alive()
    """
    def __init__(self, screen: pg.Surface, z_size: int):
        self.screen = screen
        self.size = z_size
        self.pos = pg.Vector2(0, 0)    # center position (set by spawn_at)
        self.state = DEAD
        self.state_time = 0.0
        self.clickable = False
        self._alive = False
        self.max_idle = 1.6   

        # timing/feel
        self.fade_duration = 0.35
        self.pop_strength  = 0.15    # 15% overshoot on spawn
        
        # motion amounts (in pixels)
        self.rise_height = int(self.size * 0.35)  # how far it rises out of the hole
        self.settle_overshoot = 6                 # small "fall" after the rise

        frames = _load_frames(self.size)
        self.clip_idle = AnimationClip(frames, frame_time=0.20, loop=True)

        spawn_frames = frames[:3] if len(frames) >= 3 else frames
        self.clip_spawn = AnimationClip(spawn_frames, frame_time=0.16, loop=False)
        self.clip_despawn = AnimationClip(list(reversed(spawn_frames)), frame_time=0.18, loop=False)

        self.clip_hit = AnimationClip(frames, frame_time=0.12, loop=False)

        self.anim = Animator()
        self._rect = pg.Rect(0, 0, self.size, self.size)

    # ---- lifecycle ----
    def spawn_at(self, center_xy: Tuple[int, int]):
        self.pos.update(center_xy)
        self.state = SPAWNING
        self.state_time = 0.0
        self.clickable = False
        self._alive = True
        self.anim.play(self.clip_spawn, reset=True)
        self._sync_rect()

    def hit(self):
        if self.state == IDLE and self._alive:
            self.state = HIT
            self.state_time = 0.0
            self.clickable = False
            self.anim.play(self.clip_hit, reset=True)

    def despawn(self):
        if self.state == IDLE and self._alive:
            self.state = DESPAWNING
            self.state_time = 0.0
            self.clickable = False
            self.anim.play(self.clip_despawn, reset=True)

    def is_alive(self) -> bool:
        return self._alive

    # ---- update/draw ----
    def update(self, dt: float):
        if not self._alive:
            return
        self.state_time += dt
        self.anim.update(dt)

        if self.state == SPAWNING:
            if self.anim_finished():
                self.state = IDLE
                self.state_time = 0.0
                self.clickable = True
                self.anim.play(self.clip_idle, reset=True)
                
        elif self.state == IDLE:
            # auto-despawn if it lingers too long
            if self.state_time >= self.max_idle:
                self.despawn()

        elif self.state == HIT:
            if self.anim_finished():
                self.state = DEAD
                self._alive = False
                self.clickable = False

        elif self.state == DESPAWNING:
            if self.anim_finished():
                self.state = DEAD
                self._alive = False
                self.clickable = False

        self._sync_rect()

    def draw(self):
        if not self._alive:
            return
        img = self.anim.image()
        if img is None:
            return

        alpha, scale_factor, y_off = self._spawn_despawn_motion()
        to_draw = img

        # apply alpha
        if alpha < 255:
            to_draw = img.copy()
            to_draw.fill((255, 255, 255, alpha), special_flags=pg.BLEND_RGBA_MULT)

        # apply scale
        if abs(scale_factor - 1.0) > 1e-3:
            w, h = to_draw.get_width(), to_draw.get_height()
            to_draw = pg.transform.smoothscale(
                to_draw, (max(1, int(w * scale_factor)), max(1, int(h * scale_factor)))
            )

        rect = to_draw.get_rect(center=(int(self.pos.x), int(self.pos.y + y_off)))
        self.screen.blit(to_draw, rect.topleft)

    # ---- helpers ----
    def _sync_rect(self):
        self._rect.size = (self.size, self.size)
        self._rect.center = (int(self.pos.x), int(self.pos.y))

    def get_rect(self) -> pg.Rect:
        return self._rect

    def anim_finished(self) -> bool:
        return self.anim.finished

    def _spawn_despawn_motion(self) -> Tuple[int, float, float]:
        """(alpha, scale, y_offset) with rise/fall on spawn and sink on despawn."""
        def smooth(t: float) -> float:
            return t*t*(3 - 2*t)  # smoothstep

        if self.state == SPAWNING:
            t = min(1.0, self.state_time / max(1e-6, self.fade_duration))
            s = smooth(t)
            alpha = int(255 * s)
            rise = (1.0 - s) * self.rise_height
            settle = -self.settle_overshoot * (4.0 * s * (1.0 - s))
            y_off = rise + settle
            scale = 1.0 + self.pop_strength * 0.25 * (4.0 * s * (1.0 - s))
            return alpha, scale, y_off

        if self.state == DESPAWNING:
            t = min(1.0, self.state_time / max(1e-6, self.fade_duration))
            s = smooth(t)

            # Fade OUT as it sinks
            alpha = int(255 * (1.0 - s))

            # Sink down into the hole by rise_height
            y_off = s * self.rise_height - 3.0 * (1.0 - s) * s 

            # Slight shrink for a “disappear” feel
            scale = 1.0 - 0.10 * s
            return alpha, scale, y_off

        # IDLE/HIT (no vertical motion)
        return 255, 1.0, 0.0



# --------------------------------------------------------------------
# Manager: spawns, updates, draws, and handles hits
# --------------------------------------------------------------------
class ZombieManager:
    """
    Holds multiple Zombies, spawns them at positions, updates & draws them.
    Public API:
      - spawn(center_xy, size)
      - update(dt), draw()
      - handle_click(mouse_pos)
      - count(), alive()
    """
    def __init__(self, screen: pg.Surface):
        self.screen = screen
        self.entities: List[Zombies] = []

    def spawn(self, center_xy: Tuple[int, int], size: int = 128) -> Zombies:
        z = Zombies(self.screen, size)
        z.spawn_at(center_xy)
        self.entities.append(z)
        return z

    def update(self, dt: float):
        for z in self.entities:
            z.update(dt)
        self.entities = [z for z in self.entities if z.is_alive()]

    def draw(self):
        for z in self.entities:
            z.draw()

    def handle_click(self, mouse_pos: Tuple[int, int]):
        for z in self.entities:
            if z.is_alive() and z.get_rect().collidepoint(mouse_pos) and z.state == IDLE and z.clickable:
                z.hit()
                return True
        return False

    # Convenience helpers (useful in tests/UI)
    def alive(self) -> List[Zombies]:
        return [z for z in self.entities if z.is_alive()]

    def count(self) -> int:
        return len(self.entities)