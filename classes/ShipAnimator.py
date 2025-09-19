import os
import pygame
from classes.Animator import Animator
from typing import Optional, Tuple, List, Dict

class ShipAnimator(Animator):
    """
    Gère l'animation de plusieurs vaisseaux sous forme statique et plusieurs animations à partir de spritesheets.
    """
    def __init__(
        self,
        screen : pygame.Surface,
        path : str,
        dimensions : Tuple[int, int],   # (width_tiles, height_tiles)
        coord : Tuple[int, int],        # (x, y) en pixels
        tile_size : int = 100,
        default_fps : int = 10,
        PV_actuelle : int = 100,
        PV_max : int = 100 
    ):
        super().__init__(screen, path, dimensions, coord, tile_size, default_fps)

        # Stat du vaisseau
        self.PV_actuelle = PV_actuelle
        self.PV_max = PV_max

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
    
    def update(self, PV_actuelle : int, PV_max : int):
        self.PV_actuelle = PV_actuelle
        self.PV_max = PV_max