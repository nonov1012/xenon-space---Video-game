import os
import pygame
from typing import Optional, Tuple, List, Dict

def load_spritesheet(path: str, frame_width: int, frame_height: int) -> List[pygame.Surface]:
    sheet = pygame.image.load(path).convert_alpha()
    sheet_width, sheet_height = sheet.get_size()
    frames = []
    for x in range(0, sheet_width, frame_width):
        if x + frame_width <= sheet_width:
            frame_surface = sheet.subsurface((x, 0, frame_width, frame_height)).copy()
            frames.append(frame_surface)
    return frames


class Animator:
    def __init__(
        self,
        screen : pygame.Surface,
        path : str,
        dimensions : Tuple[int, int],   # (width_tiles, height_tiles)
        coord : Tuple[int, int],        # (x, y) en pixels
        tile_size : int = 35,
        default_fps : int = 10,
        PV_actuelle : int = 100,
        PV_max : int = 100 
    ):
        self.screen = screen
        self.path = path
        self.tile_size = tile_size

        # --- dimensions en nombre de cases ---
        self.tile_w, self.tile_h = dimensions   # <<< ici
        self.pixel_w = self.tile_w * tile_size
        self.pixel_h = self.tile_h * tile_size

        self.PV_actuelle = PV_actuelle
        self.PV_max = PV_max
        self.x, self.y = coord


        # image statique (chargée une seule fois)
        self.static_image = None
        base_path = os.path.join(self.path, "base.png")
        if os.path.isfile(base_path):
            img = pygame.image.load(base_path).convert_alpha()
            self.static_image = pygame.transform.scale(img, (self.pixel_w, self.pixel_h))

        # animations
        self.animations: Dict[str, List[pygame.Surface]] = {}  # nom -> liste de frames
        self.current_anim: Optional[str] = None
        self.frame_index = 0
        self.last_update = 0
        self.frame_duration_ms = 1000 // max(1, default_fps)

        # booléen qui permet de savoir si on fait l'animation d'engine ou non
        self.idle : bool = True

    def load_animation(self, name: str, filename: str, frame_size: Optional[Tuple[int, int]] = None):
        """
        Charge une animation et l'enregistre dans le dictionnaire.
        name = identifiant ("death", "weapon", "idle", etc.)
        filename = nom du fichier spritesheet (relatif au self.path)
        frame_size = (w,h) si les frames ne sont pas carrées
        """
        frames_path = os.path.join(self.path, filename)
        if not os.path.isfile(frames_path):
            raise FileNotFoundError(f"No spritesheet at {frames_path}")

        sheet = pygame.image.load(frames_path).convert_alpha()
        sheet_w, sheet_h = sheet.get_size()

        if frame_size:
            fw, fh = frame_size
        else:
            fh = sheet_h
            fw = fh if sheet_w % fh == 0 else sheet_w

        frames = load_spritesheet(frames_path, fw, fh)
        frames = [pygame.transform.scale(f, (self.pixel_w, self.pixel_h)) for f in frames]
        self.animations[name] = frames

    def play(self, name: str, reset: bool = False, frame_size: Optional[Tuple[int, int]] = None):
        """
        Définit l'animation courante.
        Si l'animation n'est pas encore chargée, essaie de la charger depuis un fichier <name>.png.
        """
        if name not in self.animations:
            filename = f"{name}.png"
            self.load_animation(name, filename, frame_size=frame_size)

        if reset or name != self.current_anim:
            self.current_anim = name
            self.frame_index = 0
            self.last_update = pygame.time.get_ticks()


    def update_and_draw(self):
        """
        Met à jour et dessine l'animation courante avec priorité.
        - 'engine' tourne toujours en fond.
        - Les animations prioritaire ('death', 'weapons', ...) passent par-dessus.
        - Si aucune animation prioritaire, on affiche l'image statique.
        """
        # --- Effacer l'image actuelle ---
        self.erase()

        # --- Dessiner l'animation prioritaire par-dessus ---
        if self.current_anim and self.current_anim != "engine":
            # Animation du shield 
            if self.current_anim == "shield":
                self.screen.blit(self.static_image, (self.x, self.y))

            frames = self.animations[self.current_anim]
            now = pygame.time.get_ticks()
            if now - self.last_update >= self.frame_duration_ms:
                self.last_update = now
                if self.frame_index < len(frames):
                    self.frame_index += 1

            if self.frame_index == len(frames) - 1:
                self.current_anim = None
            else:
                self.screen.blit(frames[self.frame_index], (self.x, self.y))
        else:
            # Si aucune animation prioritaire, dessiner l'image statique
            if self.static_image:
                self.screen.blit(self.static_image, (self.x, self.y))

        if self.idle:
            # --- Dessiner le moteur en fond ---
            if "engine" in self.animations:
                frames = self.animations["engine"]
                now = pygame.time.get_ticks()
                # Avancer la frame du moteur si temps écoulé
                if not hasattr(self, "_engine_index"):
                    self._engine_index = 0
                    self._engine_last = now
                if now - self._engine_last >= self.frame_duration_ms:
                    self._engine_last = now
                    self._engine_index = (self._engine_index + 1) % len(frames)
                self.screen.blit(frames[self._engine_index], (self.x, self.y))

        self.display_health()


    def draw_image(self):
        """Dessine l'image statique si elle existe."""
        if self.static_image:
            self.screen.blit(self.static_image, (self.x, self.y))

    def display_health(self):
        bar_w = int(self.pixel_w)
        bar_h = 20
        x = self.x
        y = self.y + self.pixel_h - bar_h
        pygame.draw.rect(self.screen, (255, 0, 0), (x, y, bar_w, bar_h))
        cur_w = int(self.PV_actuelle * bar_w / self.PV_max) if self.PV_max > 0 else 0
        pygame.draw.rect(self.screen, (0, 255, 0), (x, y, cur_w, bar_h))

    def disepear(self, duration_ms: int = 1000) -> bool:
        """
        Applique un fondu progressif sur l'animation courante ou l'image statique.
        Retourne True quand le vaisseau doit être retiré.
        """
        if not hasattr(self, "_disappear_start"):
            self._disappear_start = pygame.time.get_ticks()

        now = pygame.time.get_ticks()
        elapsed = now - self._disappear_start
        alpha = min(255, int(255 * (elapsed / duration_ms)))

        # dessiner l'image ou animation courante
        if self.current_anim:
            frames = self.animations[self.current_anim]
            self.screen.blit(frames[self.frame_index], (self.x, self.y))
        elif self.static_image:
            self.screen.blit(self.static_image, (self.x, self.y))

        overlay = pygame.Surface((self.pixel_w, self.pixel_h))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(alpha)
        self.screen.blit(overlay, (self.x, self.y))
        
        return elapsed >= duration_ms
    
    def erase(self, color=(0,0,0)):
        """
        Efface l'image actuelle en remplissant la zone avec 'color'.
        La taille est recalculée à chaque appel pour suivre la taille du vaisseau sur le plateau.
        """
        w = self.tile_w * self.tile_size
        h = self.tile_h * self.tile_size
        rect = pygame.Rect(self.x, self.y, w, h)
        pygame.draw.rect(self.screen, color, rect)


    def play_with_fade(self, name: str, fade_duration: int = 1000, reset: bool = False):
        """
        Joue une animation et applique un fondu progressif.
        Retourne True si l'animation + le fade sont terminés.
        """
        self.idle = False
        self.play(name, reset=reset)  # définit current_anim
        self.update_and_draw()  # avance et dessine l'animation

        done = self.disepear(duration_ms=fade_duration)  # applique le fade
        return done
    
    def update(self, PV_actuelle : int, PV_max : int):
        self.PV_actuelle = PV_actuelle
        self.PV_max = PV_max
    
    def is_animation_finished(self, name: str) -> bool:
        """Retourne True si l'animation spécifiée est terminée."""
        if self.current_anim != name:
            return True  # si l'animation n'est pas en cours, considérer comme finie
        return self.frame_index >= len(self.animations.get(name, [])) - 1
