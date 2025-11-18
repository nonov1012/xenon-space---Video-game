import math
from typing import Optional, Tuple
import pygame
from blazyck import *
from classes.Animator import Animator

class ProjectileAnimator(Animator):
    projectiles_data = {
        "bullet": (4, 16),
        "big bullet": (8, 16),
        "torpedo": (11, 32),
        "wave": (64, 64),
        "laser": (18, 38)  # le sprite n'est pas utilisé :)
    }

    def __init__(
        self,
        dimensions: Tuple[int, int],
        coord: Tuple[int, int],
        default_fps: int = 10,
        speed: int = 3,
        movable: bool = True,
        projectile_type: str = "projectile",
        dissipate_speed: Optional[float] = None,
        duration_ms: Optional[int] = 30
    ):
        """
        Initialisation de l'Animator de projetile.
        
        :param dimensions: Dimensions du sprite en cases
        :param coord: Coordonnées initiales (x, y) en pixels
        :param default_fps: Nombre de frames par seconde (défaut = 10)
        :param speed: Vitesse de mouvement (défaut = 1)
        :param movable: Si True, le projectile peut être déplacé
        :param projectile_type: Type de projectile (projectile, laser, ...)
        :param dissipate_speed: Vitesse de dissipation du laser (défaut = None)
        :param duration_ms: Durée de vie en millisecondes (défaut = 5000)
        """
        super().__init__(PROJECTILES_PATH, dimensions, coord, TAILLE_CASE, default_fps, speed)
        self.movable = movable
        self.projectile_type = projectile_type
        self.duration_ms = duration_ms   # durée de vie en millisecondes
        self.start_time = pygame.time.get_ticks() if duration_ms else None

        if projectile_type == "laser":
            self.x = self.x + self.pixel_w / 2

            # Calcul de la distance si une cible est déjà fixée
            if hasattr(self, "target") and self.target:
                dx = self.target[0] - self.x
                dy = self.target[1] - self.y
                length = math.hypot(dx, dy)
            else:
                length = 100  # valeur par défaut si pas encore de cible

            # Vitesse de dissipation proportionnelle à la longueur
            if dissipate_speed is None:
                self.dissipate_speed = max(1, int(length * 0.05))  
            else:
                self.dissipate_speed = dissipate_speed


    def update_and_draw(self):
        """
        Met à jour et dessine le projectile ou le laser.
        
        Vérifie si la durée de vie est atteinte et dans ce cas,
        supprime le projectile de la liste.
        
        Choisit si on dessine un projectile classique ou un laser segmenté.
        """
        # --- Vérification durée de vie ---
        if self.duration_ms is not None and self.start_time is not None:
            now = pygame.time.get_ticks()
            if now - self.start_time >= self.duration_ms:
                self.active = False
                self.remove_from_list()  # Supprime le projectile de la liste
                return  # On arrête là, il n'est plus dessiné

        # --- Dessin classique ou laser ---
        if self.projectile_type == "laser":
            self._draw_laser()
        else:
            super().update_and_draw()

    def erase(self, color=(0, 0, 0)):
        """
        Efface l'image actuelle en remplissant la zone avec 'color'.

        Si l'objet est un laser, on efface la ligne rouge qui le représente.
        Sinon, on utilise la méthode erase de la classe parente.
        """
        if self.projectile_type == "laser":
            # Si le laser n'a pas encore été généré, il n'y a rien à effacer
            if not hasattr(self, "_laser_width"):
                return

            # Surface temporaire pour stocker l'image à effacer
            temp_surface = pygame.Surface(Animator.screen.get_size(), pygame.SRCALPHA)

            # Efface le cœur rouge
            pygame.draw.line(
                temp_surface,
                color,
                # Point de départ (x, y)
                (self.x, self.y),
                # Point d'arrivée (x, y)
                (self.target[0], self.target[1]),
                # Largeur de la ligne (en pixels)
                getattr(self, "_laser_width", 0)
            )

            # Application de la surface temporaire sur l'écran
            Animator.screen.blit(temp_surface, (0, 0))
        else:
            # Appel de la méthode erase de la classe parente
            return super().erase(color)

    def _compute_distance(self) -> float:
        """
        Retourne la distance entre l'origine (self.x, self.y) et la cible définie par set_target().

        :return: La distance entre l'origine et la cible.
        :rtype: float
        """
        cx = self.x
        cy = self.y
        dx = self.target[0] - cx
        dy = self.target[1] - cy
        # Calcul de la distance en utilisant la formule de Pythagore
        return math.hypot(dx, dy)

    # --- Laser avec dissipation ---
    def _draw_laser(self):
        """
        Dessine un laser avec dissipation, multicouches et intensité variable.

        :return: None
        :rtype: None
        """
        if not self.active or self.target is None:
            return

        # Paramètres
        width_max = self.pixel_w
        dissipate_speed = self.dissipate_speed
        laser_length = self._compute_distance()

        # Attributs persistants
        if not hasattr(self, "_laser_width"):
            self._laser_width = 0
        if not hasattr(self, "_laser_active"):
            self._laser_active = True
        if not hasattr(self, "_laser_phase"):
            self._laser_phase = 0

        # Gestion de l'extension/dissipation
        if self._laser_active:
            self._laser_width = min(self._laser_width + dissipate_speed, width_max)
        else:
            self._laser_width = max(self._laser_width - dissipate_speed, 0)

        # Animation phase (sert pour le sinus)
        self._laser_phase += 1

        # Fonction utilitaire
        
        def draw_line_with_caps(base_alpha, start, end, width, pulse=False, color=(255, 0, 0)):
            """
            Trace une ligne + deux cercles avec alpha qui pulse.

            :param base_alpha: La valeur de base pour alpha
            :param start: Le point de départ
            :param end: Le point d'arrivée
            :param width: La largeur de la ligne
            :param pulse: Si True, l'alpha pulse
            :param color: La couleur de la ligne
            :return: None
            :rtype: None
            """
            if pulse:
                variation = 80
                alpha = max(0, min(255,
                    int(base_alpha + variation * math.sin(self._laser_phase * 0.2))
                ))
            else:
                alpha = base_alpha

            col = (color[0], color[1], color[2], alpha)

            # Ligne
            pygame.draw.line(temp_surface, col, start, end, width)
            # Extrémités
            radius = max(1, width // 2)
            pygame.draw.circle(temp_surface, col, start, radius)
            pygame.draw.circle(temp_surface, col, end, radius)

        # Dessin du laser
        if self._laser_width > 0:
            temp_surface = pygame.Surface(Animator.screen.get_size(), pygame.SRCALPHA)

            start = (int(self.x), int(self.y))
            end = (int(self.target[0]), int(self.target[1]))

            # Trois lignes rouges (toutes pulsent)
            draw_line_with_caps(50,  start, end, int(self._laser_width), pulse=True)
            draw_line_with_caps(120, start, end, int((self._laser_width / 10) * 8), pulse=True)
            draw_line_with_caps(255, start, end, int((self._laser_width / 10) * 6), pulse=True)

            # Aura blanche (toujours opaque, pas de pulsation)
            draw_line_with_caps(255, start, end, int((self._laser_width / 10) * 4), pulse=False, color=(255, 255, 255))

            Animator.screen.blit(temp_surface, (0, 0))
