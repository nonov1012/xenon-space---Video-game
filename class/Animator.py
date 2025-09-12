import os
import pygame
from typing import Optional, Tuple, List

def load_spritesheet(path: str, frame_width: int, frame_height: int) -> List[pygame.Surface]:
    sheet = pygame.image.load(path).convert_alpha()
    sheet_width, sheet_height = sheet.get_size()
    frames = []
    for x in range(0, sheet_width, frame_width):
        if x + frame_width <= sheet_width:
            frame_surface = sheet.subsurface((x, 0, frame_width, frame_height)).copy()
            frames.append(frame_surface)
    return frames

class Animator:
    """
    Gère l'image statique et une animation de destruction depuis une spritesheet.
    Ne modifie pas l'entité : prend screen, path, dimensions (tiles), coord (pixels).
    """
    def __init__(
        self,
        screen: pygame.Surface,
        path: str,
        dimensions: Tuple[int, int],   # (width_tiles, height_tiles)
        coord: Tuple[int, int],        # (x, y) en pixels
        tile_size: int = 100,
        death_frame_size: Optional[Tuple[int,int]] = None,
        death_fps: int = 10
    ):
        self.screen = screen
        self.path = path
        self.tile_size = tile_size

        # taille en pixels de l'entité
        self.pixel_w = dimensions[0] * tile_size
        self.pixel_h = dimensions[1] * tile_size

        # position
        self.x, self.y = coord

        # static image (chargée une seule fois)
        self.static_image = None
        base_path = os.path.join(self.path, "base.png")
        if os.path.isfile(base_path):
            img = pygame.image.load(base_path).convert_alpha()
            self.static_image = pygame.transform.scale(img, (self.pixel_w, self.pixel_h))

        # animation (lazy load)
        self.death_frames: Optional[List[pygame.Surface]] = None
        self.death_index = 0
        self.death_last_update = 0
        self.death_frame_duration_ms = 1000 // max(1, death_fps)
        self.death_frame_size = death_frame_size  # (w,h) en px si fourni
        self.death_loop = False  # pour la mort, on veut normalement ne PAS boucler

    def draw_image(self):
        """Dessine l'image statique si elle existe."""
        if self.static_image:
            self.screen.blit(self.static_image, (self.x, self.y))

    def _ensure_death_frames_loaded(self):
        """Charge et découpe la spritesheet de mort si ce n'est pas déjà fait."""
        if self.death_frames is not None:
            return

        frames_path = os.path.join(self.path, "destruction.png")
        if not os.path.isfile(frames_path):
            raise FileNotFoundError(f"No destruction spritesheet at {frames_path}")

        # si frame size fourni, on l'utilise ; sinon on prend la hauteur de la sheet comme frame_height
        sheet = pygame.image.load(frames_path).convert_alpha()
        sheet_w, sheet_h = sheet.get_size()

        if self.death_frame_size:
            fw, fh = self.death_frame_size
        else:
            # supposition: frames en ligne, frame_height = sheet_height, frame_width = a diviser
            fh = sheet_h
            # essayer deviner le nombre de frames en divisant par la hauteur si square, sinon fallback
            # ici on suppose frames contiguës horizontales et hauteur = frame_height
            # on va prendre fw = fh (si image carrée par frame) sinon on divise par entier si possible
            if sheet_w % fh == 0:
                fw = fh
            else:
                # fallback : on prend frame_width = sheet_w (une seule frame)
                fw = sheet_w

        self.death_frames = load_spritesheet(frames_path, fw, fh)

        # redimensionner les frames aux dimensions en pixels de l'entité
        self.death_frames = [
            pygame.transform.scale(f, (self.pixel_w, self.pixel_h)) for f in self.death_frames
        ]
        self.death_index = 0
        self.death_last_update = pygame.time.get_ticks()

    def draw_death(self, loop: bool = False):
        """
        Joue l'animation de destruction. Par défaut n'itère pas (arrête sur la dernière frame).
        Call this every frame while you want the death animation to progress.
        """
        self._ensure_death_frames_loaded()

        now = pygame.time.get_ticks()
        if now - self.death_last_update >= self.death_frame_duration_ms:
            self.death_last_update = now
            # avancer si pas à la dernière frame ou si loop True
            if self.death_index < len(self.death_frames) - 1:
                self.death_index += 1
            elif loop:
                self.death_index = 0

        # blit frame courante
        self.screen.blit(self.death_frames[self.death_index], (self.x, self.y))

    def display_health(self, PV_actuelle: int, PV_max: int):
        bar_w = int(self.pixel_w)
        bar_h = 20
        x = self.x
        y = self.y + self.pixel_h - bar_h
        # fond rouge (max)
        pygame.draw.rect(self.screen, (255, 0, 0), (x, y, bar_w, bar_h))
        # vert = portion actuelle
        if PV_max > 0:
            cur_w = int(PV_actuelle * bar_w / PV_max)
        else:
            cur_w = 0
        pygame.draw.rect(self.screen, (0, 255, 0), (x, y, cur_w, bar_h))
