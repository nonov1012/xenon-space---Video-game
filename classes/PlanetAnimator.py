from typing import Optional, Tuple
from classes.Animator import Animator
from blazyck import *

class PlanetAnimator(Animator):
    def __init__(self, dimensions, coord, default_fps=10, speed=1):
        super().__init__(PLANETES_PATH, dimensions, coord, TAILLE_CASE, default_fps, speed)
        self._atmosphere_surface: Optional[pygame.Surface] = None
        self._atmosphere_offset: Tuple[int, int] = (0, 0)

    def update_and_draw(self):
        self.draw_atmosphere()
        super().update_and_draw()

    def play(self, name: str, reset: bool = False):
        super().play(name, reset, PLANETES_FRAME_SIZE)

    def draw_atmosphere(self, color_atmosphere=(0, 200, 255),
                        thickness_ratio: float = 0.12,
                        layers: int = 80,
                        edge_alpha: int = 180):
        # Si déjà calculé, on ne le refait pas
        if self._atmosphere_surface is None:
            self._atmosphere_surface, self._atmosphere_offset = self._generate_atmosphere(
                color_atmosphere, thickness_ratio, layers, edge_alpha
            )

        at_x = self.x + self._atmosphere_offset[0] - 1
        at_y = self.y + self._atmosphere_offset[1] - 1

        # Utiliser Animator.screen (même référence que PlanetAnimator.screen)
        Animator.screen.blit(self._atmosphere_surface, (at_x, at_y))

    def _generate_atmosphere(self,
                             color_atmosphere=(0, 200, 255),
                             thickness_ratio: float = 0.12,
                             layers: int = 80,
                             edge_alpha: int = 180) -> Tuple[pygame.Surface, Tuple[int,int]]:
        """
        Retourne (surface_atmosphere, offset) :
        - offset est ajouté à (self.x, self.y) pour obtenir la position de blit
        - thickness_ratio : part de la taille de la planète utilisée pour l'épaisseur
        - layers : nombre approximatif de "anneaux" (plus = plus lisse)
        - edge_alpha : alpha max à l'extérieur (0..255)
        """
        taille_px = self.pixel_w
        if taille_px <= 0:
            return pygame.Surface((1, 1), pygame.SRCALPHA), (0, 0)

        # épaisseur : au moins 2*tile, ou proportionnelle à la planète
        extra = max(2 * TAILLE_CASE, int(taille_px * thickness_ratio))
        taille_atmos = taille_px + 2 * extra

        atmos_surface = pygame.Surface((taille_atmos, taille_atmos), pygame.SRCALPHA)
        center = taille_atmos // 2

        cr, cg, cb = color_atmosphere

        # rayons en float pour précision
        planet_radius = taille_px / 2.0
        rayon_max = taille_atmos / 2.0
        thickness = rayon_max - planet_radius
        if thickness <= 0:
            return pygame.Surface((1, 1), pygame.SRCALPHA), (0, 0)

        # limiter layers à l'épaisseur disponible
        layers = max(1, min(int(layers), int(thickness)))
        step = max(1, int(thickness / layers))

        # dessine de l'extérieur vers l'intérieur, alpha décroissant
        for r in range(int(rayon_max), int(planet_radius), -step):
            t = (r - planet_radius) / thickness  # 1.0 => bord, 0.0 => proche planète
            alpha = int(edge_alpha * (1.0 - t))  # inverse : 0 au bord, max près planète
            if alpha <= 0:
                continue
            pygame.draw.circle(atmos_surface, (cr, cg, cb, alpha), (center, center), r)

        # offset : la surface commence "extra" px à gauche/haut du coin de la planète
        offset = (-extra, -extra)
        return atmos_surface, offset

    # si tu veux forcer la régénération (changement de couleur / ratio / etc.)
    def invalidate_atmosphere(self):
        self._atmosphere_surface = None


