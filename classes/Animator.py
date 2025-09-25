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

def load_spritesheet(path: str, frame_width: int, frame_height: int) -> list[pygame.Surface]:
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
    screen = None

    @staticmethod
    def set_screen(screen: pygame.surface):
        Animator.screen = screen

    """
    Gère l'image statique et plusieurs animations à partir de spritesheets.
    """
    def __init__(
        self,
        path: str,
        dimensions: Tuple[int, int],   # (width_tiles, height_tiles)
        coord: Tuple[int, int],        # (x, y) en pixels
        tile_size: int = TAILLE_CASE,
        default_fps: int = 10,
        speed : int = 1
        ):
        self.path = path
        self.tile_size = tile_size

        # attribut de l'entité
        self.pixel_w = dimensions[0] * tile_size
        self.pixel_h = dimensions[1] * tile_size

        # position
        self.x = coord[0] * tile_size
        self.y = coord[1] * tile_size

        # --- dimensions en nombre de cases ---
        self.tile_w, self.tile_h = dimensions   # <<< ici
        self.pixel_w = self.tile_w * tile_size
        self.pixel_h = self.tile_h * tile_size

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
        name = identifiant ("death", "weapon", "idle", etc.)
        filename = nom du fichier spritesheet (relatif au self.path)
        frame_size = (w,h) si les frames ne sont pas carrées
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
        Si l'animation n'est pas encore chargée, essaie de la charger depuis un fichier <name>.png ou <name>.gif.
        """
        if name not in self.animations:
            filename = f"{name}.png"
            if not os.path.isfile(os.path.join(self.path, filename)):
                filename = f"{name}.gif"
            self.load_animation(name, filename, frame_size=frame_size)

        if reset or name != self.current_anim:
            self.current_anim = name
            self.frame_index = 0
            self.last_update = pygame.time.get_ticks()

    def erase(self, color=(0, 0, 0)):
        """
        Efface l'image actuelle en remplissant la zone avec 'color',
        en tenant compte de la rotation pour éviter les traces.
        """
        if self.current_anim is None or self.current_anim not in self.animations:
            return

        # prendre la frame actuelle
        frame = self.animations[self.current_anim][self.frame_index]
        # appliquer la rotation
        rotated_frame = pygame.transform.rotate(frame, self.angle)
        rect = rotated_frame.get_rect(center=(self.x + self.pixel_w/2, self.y + self.pixel_h/2))
        pygame.draw.rect(Animator.screen, color, rect)


    def update_and_draw(self):
        """
        Met à jour et dessine l'animation de l'entité avec rotation selon self.angle.
        """
        # --- Mouvement ---
        self.move()
        if self.angle != self.target_angle:
            self.slow_set_angle()

        # --- Changer de frame d'animation ---
        frames = self.animations[self.current_anim]
        now = pygame.time.get_ticks()
        if now - self.last_update >= self.frame_duration_ms:
            self.last_update = now
            self.frame_index = (self.frame_index + 1) % len(frames)

        # --- Dessiner la frame d'animation ---
        frame = frames[self.frame_index]

        # appliquer la rotation autour du centre
        rotated_frame = pygame.transform.rotate(frame, -self.angle)  # négatif si 0° = vers la droite
        rect = rotated_frame.get_rect(center=(self.x + self.pixel_w/2, self.y + self.pixel_h/2))
        Animator.screen.blit(rotated_frame, rect.topleft)

    def get_center(self):
        return (self.x + self.pixel_w // 2, self.y + self.pixel_h // 2)


    
    def set_target(self, target: Tuple[int, int], angle_targeted: bool = True, image_facing: str = "up"):
        self.target = target
        self.active = True

        # centre actuel du projectile / entité
        cx = self.x + self.pixel_w // 2
        cy = self.y + self.pixel_h // 2

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

        # angle final normalisé en [0,360)
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

        # avancer dans la direction calculée
        self.x += self.vx * self.speed
        self.y += self.vy * self.speed

        # coordonnées du centre du projectile
        cx = self.x + self.pixel_w / 2
        cy = self.y + self.pixel_h / 2

        # vecteur restant jusqu'à la cible
        dx_remain = self.target[0] - cx
        dy_remain = self.target[1] - cy

        # produit scalaire : si <= 0, le centre a atteint ou dépassé la cible
        if (dx_remain * self.vx + dy_remain * self.vy) <= 0:
            self.x = self.target[0] - self.pixel_w / 2
            self.y = self.target[1] - self.pixel_h / 2
            self.active = False

    def set_angle(self, angle: float):
        """
        Définit l'angle du vaisseau en degrés.
        0° = orientation initiale de l'image.
        """
        self.angle = angle % 360
        self.target_angle = self.angle

    def slow_set_angle(self):
        """
        Fait tourner l'objet progressivement vers target_angle.
        
        :param target_angle: angle cible en degrés (0° = orientation initiale)
        :param max_delta: rotation maximale par appel (en degrés)
        """
        # Normaliser l'angle cible
        current = self.angle % 360

        # Calculer la plus courte différence (en tenant compte du wrap-around)
        diff = (self.target_angle - current + 540) % 360 - 180  # entre -180 et +180

        # Limiter la rotation
        if abs(diff) <= self.max_delta:
            self.angle = self.target_angle
        else:
            self.angle += self.max_delta * (1 if diff > 0 else -1)

        # Normaliser après rotation
        self.angle %= 360

    def set_target_angle(self, angle: float):
        self.target_angle = angle % 360

    @classmethod
    def update_all(cls):
        """Met à jour toutes les animations de cette classe uniquement"""
        for animation in getattr(cls, "liste_animation", []):
            animation.update_and_draw()

    @classmethod
    def erase_all(cls):
        """Efface toutes les animations de cette classe uniquement"""
        for animation in getattr(cls, "liste_animation", []):
            animation.erase()

    def remove_from_list(self):
        """Retire l'objet de la liste de sa classe"""
        cls = self.__class__
        if hasattr(cls, "liste_animation") and self in cls.liste_animation:
            cls.liste_animation.remove(self)
