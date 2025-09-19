import pygame

class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        pygame.mixer.set_num_channels(2)
        self.music_channel = pygame.mixer.Channel(0)
        self.sfx_channel = pygame.mixer.Channel(1)
        self.sounds = {}
    
    # --- Gestion musique ---
    def play_music(self, filepath, loops=-1):
        """Joue une musique en boucle (-1 = infini)"""
        music = pygame.mixer.Sound(filepath)
        self.music_channel.play(music, loops=loops)

    def stop_music(self):
        self.music_channel.stop()
        
    # --- Gestion SFX ---
    def load_sfx(self, name, filepath):
        """Charge un effet sonore"""
        self.sounds[name] = pygame.mixer.Sound(filepath)

    def play_sfx(self, name):
        """Joue un effet sonore"""
        if name in self.sounds:
            self.sfx_channel.play(self.sounds[name])

    def stop_sfx(self):
        self.sfx_channel.stop()


if __name__ == "__main__":
    pygame.init()
    sm = SoundManager()
    
    sm.play_music("sounds/musiques/music_ingame.mp3")
    sm.load_sfx("laser_base", "sounds/base/laser_base.mp3")
    sm.play_sfx("laser_base")
    
    pygame.time.wait(30000000)