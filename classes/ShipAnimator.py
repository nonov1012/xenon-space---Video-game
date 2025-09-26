import math
import os
import pygame
from classes.Animator import Animator
from classes.ProjectileAnimator import ProjectileAnimator
from typing import Optional, Tuple, List, Dict
from blazyck import *

class ShipAnimator(Animator):
    """
    Gère l'animation de plusieurs vaisseaux sous forme statique et plusieurs animations à partir de spritesheets.
    """
    def __init__(
        self,
        path : str,
        dimensions : Tuple[int, int],   # (width_tiles, height_tiles)
        coord : Tuple[int, int],        # (x, y) en pixels
        tile_size : int = TAILLE_CASE,
        default_fps : int = 10,
        PV_actuelle : int = 100,
        PV_max : int = 100,
        angle : int = 0,
        show_health : bool = True,
        color : Tuple[int, int, int] = (0, 255, 0),
        alpha : int = 255
    ):
        super().__init__(path, dimensions, coord, tile_size, default_fps)

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

        # booléen qui permet de savoir si on affiche la barre de vie ou non
        self.show_health = show_health

        # couleur du contour de la barre de vie
        self.color = color
        self.alpha = alpha
        self.alive = True

    def update_and_draw(self) -> bool:
        """
        Met à jour et dessine le vaisseau avec rotation selon self.angle.
        Retourne True uniquement si l'animation courante (non engine) est terminée.
        Paramètre alpha : transparence (0 = invisible, 255 = opaque).
        """
        self.finished = False

        # --- Mouvement ---
        self.move()
        if hasattr(self, "target_angle") and self.angle != self.target_angle:
            self.slow_set_angle()

        # Fonction interne pour blitter avec alpha
        def blit_with_alpha(surface, pos):
            if self.alpha < 255:
                surface = surface.copy()
                surface.set_alpha(self.alpha)
            Animator.screen.blit(surface, pos)

        # --- Image statique si aucune animation prioritaire ---
        if hasattr(self, "static_image") and self.static_image and not self.current_anim:
            rotated_img = pygame.transform.rotate(self.static_image, self.angle)
            rect = rotated_img.get_rect(center=(self.x + self.pixel_w // 2, self.y + self.pixel_h // 2))
            blit_with_alpha(rotated_img, rect.topleft)
            
            if self.current_anim == "base":
                self.current_anim = None

        # --- Animation prioritaire ---
        if self.current_anim and self.current_anim != "engine":
            frames = self.animations[self.current_anim]
            now = pygame.time.get_ticks()
            if not hasattr(self, "_last_update"):
                self._last_update = now

            if now - self._last_update >= self.frame_duration_ms:
                self._last_update = now
                self.frame_index += 1

            if self.frame_index >= len(frames):
                # Animation terminée
                self.frame_index = 0
                if self.current_anim == "weapons":
                    self.finished = True  # seulement ici
                self.current_anim = None
            else:
                rotated_frame = pygame.transform.rotate(frames[self.frame_index], self.angle)
                rect = rotated_frame.get_rect(center=(self.x + self.pixel_w // 2, self.y + self.pixel_h // 2))
                blit_with_alpha(rotated_frame, rect.topleft)

        # --- Dessiner le moteur (boucle infinie) ---
        if hasattr(self, "idle") and self.idle and "engine" in self.animations:
            frames = self.animations["engine"]
            now = pygame.time.get_ticks()
            if not hasattr(self, "_engine_index"):
                self._engine_index = 0
                self._engine_last = now
            if now - self._engine_last >= self.frame_duration_ms:
                self._engine_last = now
                self._engine_index = (self._engine_index + 1) % len(frames)
            rotated_frame = pygame.transform.rotate(frames[self._engine_index], self.angle)
            rect = rotated_frame.get_rect(center=(self.x + self.pixel_w // 2, self.y + self.pixel_h // 2))
            blit_with_alpha(rotated_frame, rect.topleft)

        # Barre de vie
        if hasattr(self, "show_health") and self.show_health:
            self.display_health()

        self.fire()

        return self.finished



    def draw_image(self):
        """Dessine l'image statique si elle existe."""
        if self.static_image:
            Animator.screen.blit(self.static_image, (self.x, self.y))

    def display_health(self):
        bar_w = int(self.pixel_w)
        bar_h = 10
        x = self.x
        y = self.y + self.pixel_h - bar_h
        pygame.draw.rect(Animator.screen, (255, 0, 0), (x, y, bar_w, bar_h))
        cur_w = int(self.PV_actuelle * bar_w / self.PV_max) if self.PV_max > 0 else 0
        pygame.draw.rect(Animator.screen, self.color, (x, y, cur_w, bar_h))

    def disepear(self, duration_ms: int = 1000) -> bool:
        """
        Applique un fondu progressif sur l'animation courante ou l'image statique.
        Retourne True quand le vaisseau doit être retiré.
        """
        if not hasattr(self, "_disappear_start"):
            self._disappear_start = pygame.time.get_ticks()

        now = pygame.time.get_ticks()
        elapsed = now - self._disappear_start
        alpha = max(0, 255 - int(255 * (elapsed / duration_ms)))  # part de 255 → 0

        # --- Choisir l’image courante ---
        if self.current_anim:
            frames = self.animations[self.current_anim]
            base_surface = frames[self.frame_index]
        elif self.static_image:
            base_surface = self.static_image
        else:
            return elapsed >= duration_ms

        # --- Appliquer l'alpha directement ---
        temp = base_surface.copy()
        temp.set_alpha(alpha)
        Animator.screen.blit(temp, (self.x, self.y))

        return elapsed >= duration_ms

    
    def update(self, PV_actuelle : int, PV_max : int):
        self.PV_actuelle = PV_actuelle
        self.PV_max = PV_max

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
    def distance(self, target: Tuple[int, int]):
        return math.sqrt((target[0] - self.x) ** 2 + (target[1] - self.y) ** 2)
    
    def fire(self, projectile_type: str = None, target: Tuple[int, int] = None, is_fired: bool = False, projectile_speed: int = None):
        if is_fired:
            self.play("weapons", reset=False)
            self.projectile_type = projectile_type
            self.target = target
            self.projectile_speed = projectile_speed

        if self.finished:
            # --- Dimensions réelles de la frame du projectile ---
            frame_w, frame_h = ProjectileAnimator.projectiles_data[self.projectile_type]

            # --- Coordonnées du centre du vaisseau ---
            center_x = self.x + self.pixel_w / 2
            center_y = self.y + self.pixel_h / 2

            # --- Calcul de la position devant le vaisseau selon l'angle ---
            # Angle 0 = haut, rotation anti-horaire, projectile au devant du vaisseau
            angle_rad = math.radians(self.angle)
            distance = self.pixel_h / 2  # distance devant le nez
            
            # Calcul correct pour ton système de coordonnées
            spawn_x = center_x - math.sin(angle_rad) * distance
            spawn_y = center_y - math.cos(angle_rad) * distance

            # --- Conversion en coordonnées grille ---
            proj_x = spawn_x
            proj_y = spawn_y

            # --- Animation du projectile (si pas laser) ---
            if projectile_type != "laser":
                bullet = ProjectileAnimator(
                    (frame_w / TAILLE_CASE, frame_h / TAILLE_CASE),
                    (proj_x, proj_y),
                    projectile_type=self.projectile_type,
                    speed=self.projectile_speed,
                    duration_ms=int((self.distance(self.target) / self.projectile_speed) * (1000 / 10)),
                )
                bullet.play(self.projectile_type, True, frame_size=(frame_w, frame_h))
            else:
                bullet = ProjectileAnimator(
                    (frame_w / TAILLE_CASE, frame_h / TAILLE_CASE),
                    (proj_x, proj_y),
                    projectile_type=self.projectile_type,
                    speed=self.projectile_speed,
                    duration_ms = 5 * 1000 
                )

            # --- Activation du projectile ---
            bullet.set_target(self.target)

            self.finished = False

    @classmethod
    def update_all(cls):
        """Met à jour toutes les animations de cette classe uniquement"""
        for animation in getattr(cls, "liste_animation", []):
            if animation.alive:
                animation.update_and_draw()
            else:
                if animation.play_with_fade("destruction"):
                    animation.remove_from_list()
                    
    
