from typing import Optional, Tuple
from classes.Animator import Animator
from blazyck import *

class PlanetAnimator(Animator):
    def __init__(self, dimensions, coord, default_fps=10, speed=1):
        super().__init__(PLANETES_PATH, dimensions, coord, TAILLE_CASE, default_fps, speed)

    def update_and_draw(self):
        self.draw_atmosphere()
        super().update_and_draw()

    def play(self, name: str, reset: bool = False):
        super().play(name, reset, PLANETES_FRAME_SIZE)

    def draw_atmosphere(self, color_atmosphere=(0, 200, 255, 0)):
        # Taille de la planète en pixels
        taille_px = self.pixel_w
        if taille_px <= 0:
            return  # sécurité

        # --- Décalage d'une case autour ---
        at_x = self.x - (TAILLE_CASE * 1.5)
        at_y = self.y - (TAILLE_CASE * 1.5)
        taille_atmos = taille_px + 3 * TAILLE_CASE  # +1 case de chaque côté

        # Nombre de couches (plus = plus lisse)
        couches = taille_atmos // 2  
        increment = max(1, 255 // couches)

        # Surface temporaire avec alpha
        atmos_surface = pygame.Surface((taille_atmos, taille_atmos), pygame.SRCALPHA)

        # Centre de la planète dans la surface
        center = taille_atmos // 2

        at_couleur = (*color_atmosphere[:3], 0)  # (R, G, B, alpha)

        # On dessine des cercles concentriques
        for i in range(couches, 0, -1):
            radius = i
            pygame.draw.circle(atmos_surface, at_couleur, (center, center), radius)
            at_couleur = (
                at_couleur[0],
                at_couleur[1],
                at_couleur[2],
                min(255, at_couleur[3] + increment)
            )

        # On blitte la surface transparente sur l'écran
        self.screen.blit(atmos_surface, (at_x, at_y))

    @staticmethod
    def update_all():
        for animation in PlanetAnimator.liste_animation:
            animation.update_and_draw()
