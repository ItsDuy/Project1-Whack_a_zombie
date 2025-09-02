import os
import pygame

class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.sounds = {}
        self.music_volume = 0.5
        self.sfx_volume = 0.7
        self._load_sounds()
    
    def _load_sounds(self):
        hit_sfx_path="../assets/Sounds/Sfx/hit.wav"
        if os.path.exists(hit_sfx_path):
            self.sounds["hit"] = pygame.mixer.Sound(hit_sfx_path)
        else:
            print(f"Warning: Sound file '{hit_sfx_path}' not found")
        
        for sound in self.sounds.values():
            sound.set_volume(self.sfx_volume)
    
    def play_background_music(self, filename="../assets/Sounds/Music/BackGroundMusic.wav", loop=True):
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