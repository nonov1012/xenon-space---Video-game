from __future__ import annotations
import math
import os
import pygame
from typing import Optional, Tuple, List, Dict
from blazyck import *
from classes.Gif import *
import sys
from PIL import Image, ImageSequence
import numpy as np
from typing import ClassVar

from classes.GlobalVar.GridVar import GridVar
from classes.GlobalVar.ScreenVar import ScreenVar

def load_spritesheet(path: str, frame_width: int, frame_height: int) -> List[pygame.Surface]:
    """
    Charge une spritesheet à partir d'un fichier image.
    
    :param path: Chemin vers le fichier image
    :param frame_width: Largeur de chaque frame en pixels
    :param frame_height: Hauteur de chaque frame en pixels
    :return: Liste de surfaces pygame correspondant à chaque frame
    :rtype: List[pygame.Surface]
    """
    sheet = pygame.image.load(path).convert_alpha()
    sheet_width, sheet_height = sheet.get_size()
    frames = []

    # Parcours toutes les lignes et colonnes
    for y in range(0, sheet_height, frame_height):
        for x in range(0, sheet_width, frame_width):
            # Assure que la frame reste dans la surface
            if x + frame_width <= sheet_width and y + frame_height <= sheet_height:
                frame_surface = sheet.subsurface((x, y, frame_width, frame_height)).copy()
                frames.append(frame_surface)

    return frames

class Animator:
    """
    Gère l'image statique et plusieurs animations à partir de spritesheets.
    """
    def __init__(
        self,
        path: str,
        dimensions: Tuple[int, int],   # (width_tiles, height_tiles)
        coord: Tuple[int, int],        # (x, y) en pixels,
        default_fps: int = 10,
        speed : int = 1
        ):
        """
        Initialisation de l'Animator.
        
        :param path: Chemin vers le dossier contenant les spritesheets
        :param dimensions: (width_tiles, height_tiles) en nombre de cases
        :param coord: (x, y) en pixels
        :param tile_size: Taille des cases en pixels (défaut = TAILLE_CASE)
        :param default_fps: Nombre de frames par seconde (défaut = 10)
        :param speed: Vitesse de mouvement (défaut = 1)
        """
        self.path = path
        self.tile_size = GridVar.cell_size

        # attribut de l'entité
        self.pixel_w = dimensions[0] * self.tile_size
        self.pixel_h = dimensions[1] * self.tile_size

        # position
        self.x = coord[0] * self.tile_size
        self.x += GridVar.offset_x // 2
        self.y = coord[1] * self.tile_size

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
        self.target = (self.x, self.y)
        self.angle = 0

        # mouvement
        self.vx = 0
        self.vy = 0
        self.speed = speed
        self.active = False
        self.max_delta = 1
        self.target_angle = 0

        # --- Clé : chaque sous-classe a sa propre liste ---
        cls = self.__class__
        if not hasattr(cls, "liste_animation"):
            cls.liste_animation = []  # une liste par classe
        cls.liste_animation.append(self)

    def load_animation(self, name: str, filename: str, frame_size: Optional[Tuple[int, int]] = None):
        """
        Charge une animation et l'enregistre dans le dictionnaire.
        
        name: identifiant ("death", "weapon", "idle", etc.)
        filename: nom du fichier spritesheet (relatif au self.path)
        frame_size: (w,h) si les frames ne sont pas carrées
        """
        frames_path = os.path.join(self.path, filename)
        if not os.path.isfile(frames_path):
            raise FileNotFoundError(f"No spritesheet at {frames_path}")

        # Conversion automatique si c'est un GIF
        if filename.lower().endswith(".gif"):
            png_path = frames_path.replace(".gif", ".png")
            if not os.path.isfile(png_path):  # éviter de reconvertir à chaque fois
                gif_to_spritesheet(frames_path, png_path)
            frames_path = png_path

        # Charger la spritesheet
        sheet = pygame.image.load(frames_path).convert_alpha()
        sheet_w, sheet_h = sheet.get_size()

        # Calculer la taille d'une frame
        if frame_size:
            fw, fh = frame_size
        else:
            # si la taille des frames est carrée, on peut utiliser la hauteur
            fh = sheet_h
            fw = fh if sheet_w % fh == 0 else sheet_w

        # Charger les frames et les redimensionner
        frames = load_spritesheet(frames_path, fw, fh)
        frames = [pygame.transform.scale(f, (self.pixel_w, self.pixel_h)) for f in frames]

        # Enregistrer l'animation dans le dictionnaire
        self.animations[name] = frames

    def play(self, name: str, reset: bool = False, frame_size: Optional[Tuple[int, int]] = None):
        """
        Joue une animation par son nom.

        Si l'animation n'est pas déjà chargée, tente de la charger à partir d'un fichier <name>.png ou <name>.gif.
        Si reset est True, réinitialise l'animation à sa première frame.
        Si le nom de l'animation est différent de l'animation actuelle, réinitialise l'animation à sa première frame.

        :param name: Le nom de l'animation à jouer.
        :param reset: Si True, réinitialise l'animation à sa première frame.
        :param frame_size: La taille des frames de l'animation. Si non fourni, les frames sont considérées comme carrées.
        """
        if name not in self.animations:
            filename = f"{name}.png"
            if not os.path.isfile(os.path.join(self.path, filename)):
                filename = f"{name}.gif"
            self.load_animation(name, filename, frame_size=frame_size)

        # Si l'animation n'existe pas ou si l'animation est différente de l'animation actuelle,
        # réinitialise l'animation à sa première frame.
        if reset or name != self.current_anim:
            self.current_anim = name
            self.frame_index = 0
            self.last_update = pygame.time.get_ticks()

    def erase(self, color=(0, 0, 0)):
        """
        Efface l'image actuelle en remplissant la zone avec 'color',
        en tenant compte de la rotation pour éviter les traces.

        :param color: La couleur utilisée pour effacer l'image.
        """
        if self.current_anim is None or self.current_anim not in self.animations:
            # si l'animation n'existe pas, on peut retourner directement
            return

        # prendre la frame actuelle
        frame = self.animations[self.current_anim][self.frame_index]
        # appliquer la rotation
        rotated_frame = pygame.transform.rotate(frame, self.angle)
        rect = rotated_frame.get_rect(center=(self.x + self.pixel_w/2, self.y + self.pixel_h/2))
        # effacer la zone avec la couleur demandée
        pygame.draw.rect(ScreenVar.screen, color, rect)


    def update_and_draw(self):
        """
        Met à jour et dessine l'animation de l'entité avec rotation selon self.angle.

        Met à jour la position de l'entité en fonction de sa vitesse et de la direction cible.
        Changer de frame d'animation en fonction de la durée de vie de l'entité.
        Dessine la frame actuelle de l'animation en appliquant la rotation autour du centre.
        """
        # --- Mouvement ---
        self.move()
        if self.angle != self.target_angle:
            # si l'angle actuel est différent de l'angle cible, on ajuste doucement
            self.slow_set_angle()

        # --- Changer de frame d'animation ---
        frames = self.animations[self.current_anim]
        now = pygame.time.get_ticks()
        if now - self.last_update >= self.frame_duration_ms:
            # si le temps écoulé depuis la derni  re mise à jour est supérieur à la durée de vie d'une frame
            self.last_update = now
            self.frame_index = (self.frame_index + 1) % len(frames)

        # --- Dessiner la frame d'animation ---
        frame = frames[self.frame_index]

        # appliquer la rotation autour du centre
        rotated_frame = pygame.transform.rotate(frame, -self.angle)  # négatif si 0° = vers la droite
        rect = rotated_frame.get_rect(center=(self.x + self.pixel_w/2, self.y + self.pixel_h/2))
        ScreenVar.screen.blit(rotated_frame, rect.topleft)

    def get_center(self) -> Tuple[int, int]:
        """
        Renvoie le centre de l'animateur sous forme d'un tuple de deux entiers (x, y).

        Le centre est calcul  comme le milieu du rectangle
        d  fini par la largeur et la hauteur en pixels de l'animateur.

        Renvoie :
            Tuple[int, int]: Le centre de l'animateur sous forme d'un tuple de deux entiers (x, y)
        """
        # calcul du centre de l'animateur
        # comme le milieu du rectangle d  fini par la largeur et la hauteur en pixels de l'animateur
        return (self.x + self.pixel_w // 2, self.y + self.pixel_h // 2)


    
    def set_target(self, target: Tuple[int, int], angle_targeted: bool = True, image_facing: str = "up"):
        """
        Fixe la cible du projectile et calcule la direction vers la cible.

        :param target: Les coordonnées de la cible (x, y)
        :param angle_targeted: Si True, met à jour l'angle cible (par défaut, False)
        :param image_facing: L'orientation par défaut de l'image (haut, gauche, droite, bas)
        """
        self.target = target
        self.active = True

        # centre actuel du projectile / entité
        cx = self.x
        cy = self.y

        # vecteur direction vers la cible (coordonnées écran)
        dx = self.target[0] - cx
        dy = self.target[1] - cy
        dist = math.hypot(dx, dy)

        if dist == 0:
            self.vx, self.vy = 0.0, 0.0
            return
        else:
            self.vx = dx / dist
            self.vy = dy / dist

        # === IMPORTANT ===
        # math.atan2 attend un système où y positif = vers le haut.
        # Sur l'écran y positif = vers le bas, donc on inverse dy: -dy.
        # angle_to_target (en degrés) : 0 = droite, + = sens trigo (CCW).
        angle_to_target = math.degrees(math.atan2(-dy, dx))

        # offset selon l'orientation "par défaut" de l'image :
        # - "right" : l'image regarde vers la droite (est standard pour atan2)
        # - "up"    : l'image regarde vers le haut (typiquement icône "haut")
        # - "left"  : image regarde vers la gauche
        # - "down"  : image regarde vers le bas
        offsets = {
            "right": 0.0,
            "up": -90.0,
            "left": 180.0,
            "down": 90.0
        }
        offset = offsets.get(image_facing, 0.0)

        # angle final normalisé en [0,360]
        angle = (angle_to_target + offset) % 360.0
        if angle_targeted:
            self.target_angle = angle
        else:
            self.angle = angle
            self.target_angle = angle

    def move(self):
        """
        Déplace le projectile en direction de la cible (vérifie avec le centre).
        """
        if not self.active:
            return

        # Avancer dans la direction calculée
        self.x += self.vx * self.speed
        self.y += self.vy * self.speed

        # Coordonnées du centre du projectile
        cx = self.x
        cy = self.y

        # Vecteur restant jusqu'à la cible
        dx_remain = self.target[0] - cx
        dy_remain = self.target[1] - cy

        # Produit scalaire : si <= 0, le centre a atteint ou dépassé la cible
        # si le produit scalaire est négatif ou nul, cela signifie que le centre
        # du projectile a atteint ou dépassé la cible
        if (dx_remain * self.vx + dy_remain * self.vy) <= 0:
            self.x = self.target[0]
            self.y = self.target[1]
            self.active = False

    def set_angle(self, angle: float):
        """
        Définit l'angle du vaisseau en degrés.
        0° = orientation initiale de l'image.
        
        :param angle: Angle cible en degrés (0° = orientation initiale)
        """
        self.angle = angle % 360
        self.target_angle = self.angle

    def slow_set_angle(self):
        """
        Fait tourner l'objet progressivement vers target_angle.

        :param target_angle: angle cible en degrés (0° = orientation initiale)
        :param max_delta: rotation maximale par appel (en degrés)
        """
        # Normaliser l'angle actuel
        current = self.angle % 360

        # Calculer la plus courte différence (en tenant compte du wrap-around)
        # On ajoute 540 pour passer de -180 à +180 et on prend le modulo 360 pour garder l'angle entre 0 et 360
        # Enfin, on soustrait 180 pour obtenir un angle entre -180 et +180
        diff = (self.target_angle - current + 540) % 360 - 180  # entre -180 et +180

        # Limiter la rotation
        # Si la différence d'angle est inférieure ou égale à la rotation maximale, on met l'angle actuel à jour immédiatement
        # Sinon, on ajoute la rotation maximale à l'angle actuel
        if abs(diff) <= self.max_delta:
            self.angle = self.target_angle
        else:
            self.angle += self.max_delta * (1 if diff > 0 else -1)

        # Normaliser l'angle actuel après rotation
        self.angle %= 360

    def set_target_angle(self, angle: float):
        """
        Définit l'angle cible du vaisseau en degrés.

        :param angle: Angle cible en degrés (0° = orientation initiale)
        """
        # Normaliser l'angle pour le garder entre 0 et 360
        self.target_angle = angle % 360

    @classmethod
    def update_all(cls):
        """
        Met à jour toutes les animations de cette classe uniquement.
        """
        # Pour chaque animation de la liste d'animations
        for animation in getattr(cls, "liste_animation", []):
            # Mettre à jour l'animation et l'afficher
            animation.update_and_draw()

    @classmethod
    def erase_all(cls):
        """
        Efface toutes les animations de cette classe uniquement.
        
        Cette méthode parcourt la liste d'animations de la classe et appelle la méthode erase() sur chaque élément.
        """
        for animation in getattr(cls, "liste_animation", []):
            # Appel de la méthode erase() pour effacer l'animation
            animation.erase()

    def remove_from_list(self):
        """
        Retire l'objet de la liste de sa classe.
        
        Cette méthode est appelée lorsque l'objet n'est plus utile et qu'il faut le retirer de la liste d'objets de sa classe.
        """
        cls = self.__class__
        if hasattr(cls, "liste_animation") and self in cls.liste_animation:
            # Retirer l'objet de la liste d'objets de sa classe
            cls.liste_animation.remove(self)
    
    @classmethod
    def clear_list(cls):
        """
        Vide complètement la liste d'animations de cette classe.

        Cette méthode est appelée pour supprimer la liste d'animations de cette classe.
        """
        if hasattr(cls, "liste_animation"):
            # Supprimer la liste d'animations
            cls.liste_animation.clear()
