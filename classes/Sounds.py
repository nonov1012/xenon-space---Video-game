import pygame

class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        pygame.mixer.set_num_channels(2)
        self.music_channel = pygame.mixer.Channel(0)
        self.sfx_channel = pygame.mixer.Channel(1)
        self.sounds = {}
        self.music_volume = 100
        self.sfx_volume = 100
    
    # --- Gestion musique ---
    def play_music(self, filepath, loops=-1):
        """Joue une musique en boucle (-1 = infini)"""
        music = pygame.mixer.Sound(filepath)
        self.music_channel.play(music, loops=loops)

    def stop_music(self):
        self.music_channel.stop()
        
    def set_music_volume(self, volume):
        """
        Définit le volume de la musique.
        volume: int entre 0 et 100
        """
        self.music_volume = volume
        self.music_channel.set_volume(volume / 100)
        
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
        
    def set_sfx_volume(self, volume):
        """
        Définit le volume des effets sonores.
        volume: int entre 0 et 100
        """
        self.sfx_volume = volume
        # applique volume à tous les SFX chargés
        for sound in self.sounds.values():
            sound.set_volume(volume / 100)
        self.sfx_channel.set_volume(volume / 100)


if __name__ == "__main__":
    pygame.init()
    sm = SoundManager()
    sm.play_music("assets/sounds/musics/music_ingame.mp3")
    sm.load_sfx("laser_base", "assets/sounds/base/laser_base.mp3")
    sm.play_sfx("laser_base")
    pygame.time.wait(3000)
    print("volume = 10 %")
    sm.set_music_volume(10)
    
    pygame.time.wait(30000000)