# src/animation.py
import pygame as pg
from typing import List, Optional

class AnimationClip:
    def __init__(self, frames: List[pg.Surface], frame_time: float = 0.08, loop: bool = True):
        assert frames, "AnimationClip needs at least one frame"
        self.frames = frames
        self.frame_time = frame_time
        self.loop = loop
        self.length = len(frames)

    def frame(self, i: int) -> pg.Surface:
        return self.frames[i % self.length]

class Animator:
    def __init__(self):
        self.clip: Optional[AnimationClip] = None
        self.idx = 0
        self.t = 0.0
        self.finished = False

    def play(self, clip: AnimationClip, reset: bool=True):
        if self.clip is not clip or reset:
            self.clip = clip
            self.idx = 0
            self.t = 0.0
            self.finished = False

    def update(self, dt: float):
        if not self.clip or self.finished:
            return
        self.t += dt
        while self.t >= self.clip.frame_time and not self.finished:
            self.t -= self.clip.frame_time
            self.idx += 1
            if self.idx >= self.clip.length:
                if self.clip.loop:
                    self.idx = 0
                else:
                    self.idx = self.clip.length - 1
                    self.finished = True

    def image(self) -> Optional[pg.Surface]:
        if not self.clip:
            return None
        return self.clip.frame(self.idx)