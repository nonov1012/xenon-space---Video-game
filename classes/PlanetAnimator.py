from typing import Optional, Tuple
from classes.Animator import Animator
from blazyck import *

class PlanetAnimator(Animator):
    def __init__(self, dimensions, coord, default_fps=10, speed=1):
        """
        Initialisation de l'Animator PlanetAnimator.

        :param dimensions: (width_tiles, height_tiles) en nombre de cases
        :param coord: (x, y) en pixels
        :param default_fps: Nombre de frames par seconde (défaut = 10)
        :param speed: Vitesse de mouvement (défaut = 1)
        """
        super().__init__(PLANETES_PATH, dimensions, coord, TAILLE_CASE, default_fps, speed)
        self._atmosphere_surface: Optional[pygame.Surface] = None # Attribut pour stocker la surface de l'atmosphère
        self._atmosphere_offset: Tuple[int, int] = (0, 0) # Attribut pour stocker le décalage de l'atmosphère


    def update_and_draw(self):
        """
        Met à jour et dessine l'animation de la planète.

        Elle dessine d'abord l'atmosphère de la planète
        puis met à jour et dessine l'animation de la planète elle-même.
        """
        self.draw_atmosphere()
        super().update_and_draw()

    def play(self, name: str, reset: bool = False):
        """
        Joue une animation de la planète.

        :param name: Le nom de l'animation à jouer.
        :param reset: Si True, réinitialise l'animation à sa première frame.
        """
        # Appel de la méthode play de la classe parent
        # On passe le nom de l'animation, si reset est True, on réinitialise l'animation à sa première frame
        # Et on passe la taille de frame des planètes
        super().play(name, reset, PLANETES_FRAME_SIZE)

    def draw_atmosphere(self, color_atmosphere=(0, 200, 255),
                        thickness_ratio: float = 0.12,
                        layers: int = 20,
                        edge_alpha: int = 180):
        """
        Dessine l'atmosphère de la planète.

        Si l'atmosphère n'a pas encore été générée, on la génère
        en utilisant la méthode _generate_atmosphere.
        Sinon, on utilise la surface et l'offset générés précédemment.

        :param color_atmosphere: La couleur de l'atmosphère (par défaut : bleu ciel)
        :param thickness_ratio: La proportion de la taille de la planète pour calculer l'épaisseur de l'atmosphère
        :param layers: Le nombre de couches pour la générer l'atmosphère
        :param edge_alpha: La transparence maximale des bords de l'atmosphère
        """
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
        - layers : nombre approximatif de "couches" (plus = plus lisse)
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
        """
        Invalide l'atmosphère (supprime la surface et l'offset).

        Appelé lorsque la planète change de taille, de couleur, de ratio, etc.
        Permet de régénérer l'atmosphère avec les nouvelles valeurs.
        """
        self._atmosphere_surface = None


