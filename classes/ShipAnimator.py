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
    ) -> None:
        """
        Constructeur de la classe ShipAnimator.
        :param path: Chemin vers le dossier contenant les sprites du vaisseau
        :param dimensions: Dimensions du vaisseau (largeur, hauteur en cases)
        :param coord: Coordonnées du vaisseau (x, y) en pixels
        :param tile_size: Taille d'une tuile en pixels
        :param default_fps: Nombre d'images par seconde pour l'animation par défaut
        :param PV_actuelle: Points de vie actuels
        :param PV_max: Points de vie maximum
        :param angle: Angle de rotation du vaisseau (en degrés)
        :param show_health: Afficher la barre de vie
        :param color: Couleur du contour de la barre de vie
        :param alpha: Niveau de transparence (0 = invisible, 255 = opaque)
        """
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
            """
            Ajuste l'angle de rotation du vaisseau vers la cible direction.
            """
            self.slow_set_angle()

        # Fonction interne pour blitter avec alpha
        def blit_with_alpha(surface, pos):
            """
            Blit une surface avec un niveau de transparence donné.
            """
            if self.alpha < 255:
                surface = surface.copy()
                surface.set_alpha(self.alpha)
            Animator.screen.blit(surface, pos)

        # --- Image statique si aucune animation prioritaire ---
        if hasattr(self, "static_image") and self.static_image and (self.current_anim not in ("sheild", "destruction")):
            """
            Dessine l'image statique du vaisseau si elle existe et si aucune animation prioritaire.
            """
            rotated_img = pygame.transform.rotate(self.static_image, self.angle)
            rect = rotated_img.get_rect(center=(self.x + self.pixel_w // 2, self.y + self.pixel_h // 2))
            blit_with_alpha(rotated_img, rect.topleft)

        # --- Animation prioritaire ---
        if self.current_anim and self.current_anim != "engine":
            """
            Dessine l'animation prioritaire du vaisseau.
            """
            frames = self.animations[self.current_anim]
            now = pygame.time.get_ticks()
            if not hasattr(self, "_last_update"):
                self._last_update = now

            if now - self._last_update >= self.frame_duration_ms:
                self._last_update = now
                self.frame_index += 1

            if self.frame_index >= len(frames):
                """
                Animation terminée, on remet l'index à 0 et on met fin à l'animation.
                """
                self.frame_index = 0
                if self.current_anim == "weapons":
                    self.finished = True
                self.current_anim = None
            else:
                """
                Dessine la frame actuelle de l'animation en appliquant la rotation autour du centre.
                """
                rotated_frame = pygame.transform.rotate(frames[self.frame_index], self.angle)
                rect = rotated_frame.get_rect(center=(self.x + self.pixel_w // 2, self.y + self.pixel_h // 2))
                blit_with_alpha(rotated_frame, rect.topleft)

        # --- Dessiner le moteur (boucle infinie) ---
        if hasattr(self, "idle") and self.idle and "engine" in self.animations:
            """
            Dessine le moteur du vaisseau (boucle infinie).
            """
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
            """
            Dessine la barre de vie du vaisseau.
            """
            self.display_health()

        self.fire()

        return self.finished



    def draw_image(self):
        """
        Dessine l'image statique si elle existe.

        L'image statique est une image qui n'est pas animée.
        Elle est chargée une seule fois et est dessinée à chaque mise à jour si elle existe.
        """
        if self.static_image:
            Animator.screen.blit(self.static_image, (self.x, self.y))

    def display_health(self):
        """
        Dessine la barre de vie du vaisseau.

        La barre de vie est une barre horizontale qui montre la quantité de vie actuelle du vaisseau.
        """
        # dimensions de la barre de vie
        bar_w = int(self.pixel_w)
        bar_h = 5

        # position de la barre de vie
        x = self.x
        y = self.y + self.pixel_h - bar_h

        # dessine le fond de la barre de vie
        pygame.draw.rect(Animator.screen, (255, 0, 0), (x, y, bar_w, bar_h))

        # calcul de la largeur de la partie de la barre qui repésente la quantité de vie actuelle
        cur_w = int(self.PV_actuelle * bar_w / self.PV_max) if self.PV_max > 0 else 0

        # dessine la partie de la barre qui repésente la quantité de vie actuelle
        pygame.draw.rect(Animator.screen, self.color, (x, y, cur_w, bar_h))

    def disepear(self, duration_ms: int = 1000) -> bool:
        """
        Applique un fondu progressif sur l'animation courante ou l'image statique.
        Retourne True quand le vaisseau doit être retiré.
        """
        # Initialisation du temps de départ de la disparition
        if not hasattr(self, "_disappear_start"):
            self._disappear_start = pygame.time.get_ticks()

        # Calcul du temps écoulé depuis le lancement de la disparition
        now = pygame.time.get_ticks()
        elapsed = now - self._disappear_start
        # Calcul de l'alpha en fonction du temps écoulé
        alpha = max(0, 255 - int(255 * (elapsed / duration_ms)))  # part de 255 → 0

        # Sélection de l'image courante
        if self.current_anim:
            # Si une animation est en cours, on prend la frame actuelle
            frames = self.animations[self.current_anim]
            base_surface = frames[self.frame_index]
        elif self.static_image:
            # Si pas d'animation, on prend l'image statique
            base_surface = self.static_image
        else:
            # Si pas d'image, on considère que la disparition est terminée
            return elapsed >= duration_ms

        # Copie de l'image pour appliquer l'alpha
        temp = base_surface.copy()
        temp.set_alpha(alpha)
        # Dessin de l'image avec l'alpha
        Animator.screen.blit(temp, (self.x, self.y))

        # Retourne True si la disparition est terminée
        return elapsed >= duration_ms

    
    def update(self, PV_actuelle : int, PV_max : int):
        """
        Met à jour les points de vie actuels et maximaux du vaisseau.
        
        :param PV_actuelle: Points de vie actuels du vaisseau
        :param PV_max: Points de vie maximum du vaisseau
        """
        self.PV_actuelle = PV_actuelle
        self.PV_max = PV_max

    def play_with_fade(self, name: str, fade_duration: int = 1000, reset: bool = False):
        """
        Joue une animation et applique un fondu progressif.
        
        :param name: Nom de l'animation à jouer.
        :param fade_duration: Durée du fondu en millisecondes (défaut = 1000).
        :param reset: Si True, réinitialise l'animation à sa première frame (défaut = False).
        :return: True si l'animation + le fade sont terminés.
        """
        self.idle = False
        self.play(name, reset=reset)  # définit current_anim
        self.update_and_draw()  # avance et dessine l'animation

        done = self.disepear(duration_ms=fade_duration)  # applique le fade
        return done
    
    def distance(self, target: Tuple[int, int]) -> float:
        """
        Retourne la distance entre le vaisseau et la cible.

        :param target: Coordonnées de la cible (x, y)
        :return: La distance entre le vaisseau et la cible
        :rtype: float
        """
        # Calcul de la distance entre le vaisseau et la cible
        # en utilisant la formule de Pythagore
        return math.sqrt((target[0] - self.x) ** 2 + (target[1] - self.y) ** 2)
    
    def fire(self, projectile_type: str = None, target: Tuple[int, int] = None, is_fired: bool = False, projectile_speed: int = None):
        """
        Fait feu du vaisseau.

        :param projectile_type: Type de projectile (projectile, laser, ...)
        :param target: Coordonnées de la cible (x, y)
        :param is_fired: Si True, le vaisseau est considéré comme ayant déjà tiré
        :param projectile_speed: Vitesse du projectile (en cases par seconde)
        """
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
            proj_x = center_x / TAILLE_CASE -4
            proj_y = center_y / TAILLE_CASE
 
            # --- Animation du projectile (si pas laser) ---
            if projectile_type != "laser":
                bullet = ProjectileAnimator(
                    (frame_w / TAILLE_CASE, frame_h / TAILLE_CASE),
                    (proj_x, proj_y),
                    projectile_type=self.projectile_type,
                    speed=self.projectile_speed*1.7,
                    duration_ms=int((self.distance(self.target) / self.projectile_speed) * (1000 / 50)),
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
        """
        Met à jour toutes les animations de cette classe uniquement.

        Vérifie si chaque animation est encore en vie et si oui, met à jour son état et l'affiche.
        Si l'animation est terminée, on la supprime de la liste des animations.
        """
        for animation in getattr(cls, "liste_animation", []):
            if isinstance(animation, ShipAnimator):
                if animation.alive:
                    # Mettre à jour l'état et l'affichage de l'animation
                    animation.update_and_draw()
                else:
                    # Si l'animation est terminée, on la supprime de la liste
                    
                    if animation.play_with_fade("destruction"):
                        # Suppression de l'animation de la liste
                        animation.remove_from_list()
    

    
