from pathlib import Path
import os
import pygame

ASSETS = Path(__file__).resolve().parent.parent / "assets" / "Sounds" 
class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.sounds = {
            "hit": None,
            "miss": None
        }
        self.music_volume = 0.5
        self.sfx_hit_volume = 0.3
        self.sfx_miss_volume = 0.3
        self._load_sounds()
    
    def _load_sounds(self):
        # Hit sound effect
        hit_sfx_path = str(ASSETS / "Sfx" / "Hit.wav")

        # Miss sound effect
        miss_sfx_path = str(ASSETS / "Sfx" / "Miss.wav")

        if os.path.exists(hit_sfx_path):
            self.sounds["hit"] = pygame.mixer.Sound(hit_sfx_path)
        else:
            print(f"Warning: Sound file '{hit_sfx_path}' not found")

        if os.path.exists(miss_sfx_path):
            self.sounds["miss"] = pygame.mixer.Sound(miss_sfx_path)
        else:
            print(f"Warning: Sound file '{miss_sfx_path}' not found")
            
        """
        for sound in self.sounds.values():
            sound.set_volume(self.sfx_volume)
        """
        
        self.sounds["hit"].set_volume(self.sfx_hit_volume)
        self.sounds["miss"].set_volume(self.sfx_miss_volume)

    def play_background_music(self, filename = str(ASSETS / "Music" / "BackGroundMusic.wav"), loop=True):
        if os.path.exists(filename):
            try:
                pygame.mixer.music.load(filename)
                pygame.mixer.music.set_volume(self.music_volume)
                pygame.mixer.music.play(-1 if loop else 0)
                return True
            except pygame.error as e:
                print(f"Error playing music: {e}")
                return False
        else:
            print(f"Warning: Music file '{filename}' not found")
            return False
    
    def play_sound(self, sound_name):
        if sound_name in self.sounds:
            self.sounds[sound_name].play()
            return True
        else:
            print(f"Warning: Sound '{sound_name}' not found")
            return False    