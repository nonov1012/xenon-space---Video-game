import math
from typing import Tuple
import pygame
from blazyck import *
from classes.Animator import Animator

class ProjectileAnimator(Animator):
    def __init__(
        self,
        dimensions: Tuple[int, int],
        coord: Tuple[int, int],
        tile_size: int = TAILLE_CASE,
        default_fps: int = 10,
        speed: int = 1,
        movable: bool = True,
        projectile_type: str = "projectile",
        dissipate_speed: int = 5
    ):
        super().__init__(PROJECTILES_PATH, dimensions, coord, tile_size, default_fps, speed)
        self.movable = movable
        self.projectile_type = projectile_type
        if projectile_type == "laser":
            self.x = self.x + self.pixel_w / 2
            self.dissipate_speed = dissipate_speed

    def update_and_draw(self):
        """Choisit si on dessine un projectile classique ou un laser segmenté."""
        if self.projectile_type == "laser":
            self._draw_laser()
        else:
            super().update_and_draw()

    def erase(self, color=(0, 0, 0)):
        if self.projectile_type == "laser":
            if not hasattr(self, "_laser_width"):
                return  # rien à effacer

            # On dessine par-dessus le laser actuel
            temp_surface = pygame.Surface(Animator.screen.get_size(), pygame.SRCALPHA)

            # Efface le cœur rouge
            pygame.draw.line(
                temp_surface,
                color,
                (self.x, self.y),
                (self.target[0], self.target[1]),
                getattr(self, "_laser_width", 0)
            )

            Animator.screen.blit(temp_surface, (0, 0))
        else:
            return super().erase(color)


    def _compute_distance(self) -> float:
        """Retourne la distance entre l'origine et la cible définie par set_target()."""
        # Départ = centre haut de l'entité
        cx = self.x
        cy = self.y
        dx = self.target[0] - cx
        dy = self.target[1] - cy
        return math.hypot(dx, dy)

    # --- Laser avec dissipation et aura ---
    def _draw_laser(self):
        """Dessine un laser avec dissipation et aura autour."""
        if not self.active or self.target is None:
            return

        # Paramètres
        width_max = self.pixel_w
        dissipate_speed = 5
        laser_length = self._compute_distance()  # distance vers la cible

        # Attributs persistants
        if not hasattr(self, "_laser_width"):
            self._laser_width = 0
        if not hasattr(self, "_aura_width"):
            self._aura_width = 0
        if not hasattr(self, "_laser_active"):
            self._laser_active = True  # peut être modifié depuis l'extérieur

        # Gestion de l’extension/dissipation
        if self._laser_active:
            self._laser_width = min(self._laser_width + dissipate_speed, width_max)
            self._aura_width = min(self._aura_width + (dissipate_speed / 2), width_max / 2)
        else:
            self._laser_width = max(self._laser_width - dissipate_speed, 0)
            self._aura_width = max(self._aura_width - dissipate_speed, 0)

        # Dessin du laser
        if self._laser_width > 0 or self._aura_width > 0:
            temp_surface = pygame.Surface(Animator.screen.get_size(), pygame.SRCALPHA)

            # Cœur rouge
            pygame.draw.line(
                temp_surface,
                (255, 0, 0),
                (self.x, self.y),
                (self.target[0], self.target[1]),
                self._laser_width
            )

            # Aura blanche
            pygame.draw.line(
                temp_surface,
                (255, 255, 255),
                (self.x, self.y),
                (self.target[0], self.target[1]),
                int(self._aura_width)
            )

            Animator.screen.blit(temp_surface, (0, 0))