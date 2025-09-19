import os
import pygame
from typing import Optional, Tuple, List, Dict
from blazyck import *
from classes.Gif import *
import sys
from PIL import Image, ImageSequence
import numpy as np

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
    Gère l'image statique et plusieurs animations à partir de spritesheets.
    """
    def __init__(
        self,
        screen: pygame.Surface,
        path: str,
        dimensions: Tuple[int, int],   # (width_tiles, height_tiles)
        coord: Tuple[int, int],        # (x, y) en pixels
        tile_size: int = TAILLE_CASE,
        default_fps: int = 10
    ):
        self.screen = screen
        self.path = path
        self.tile_size = tile_size

        # attribut de l'entité
        self.pixel_w = dimensions[0] * tile_size
        self.pixel_h = dimensions[1] * tile_size

        # position
        self.x, self.y = coord

        # animations
        self.animations: Dict[str, List[pygame.Surface]] = {}  # nom -> liste de frames
        self.current_anim: Optional[str] = None
        self.frame_index = 0
        self.last_update = 0
        self.frame_duration_ms = 1000 // max(1, default_fps)

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
        Efface l'image actuelle en remplissant la zone avec 'color'.
        """
        rect = pygame.Rect(self.x, self.y, self.pixel_w, self.pixel_h)
        pygame.draw.rect(self.screen, color, rect)

    def update_and_draw(self):
        """
        Met à jour et dessine l'animation de l'entité.
        """
        # --- Effacer l'image actuelle ---
        

        # --- Changer de frame d'animation ---
        frames = self.animations[self.current_anim]
        now = pygame.time.get_ticks()
        if now - self.last_update >= self.frame_duration_ms:
            self.last_update = now
            if self.frame_index < len(frames):
                self.frame_index += 1

        if self.frame_index == len(frames) - 1:
            self.frame_index = 0

        # --- Dessiner la frame d'animation ---
        self.screen.blit(frames[self.frame_index], (self.x, self.y))

def main():
    pygame.init()
    screen = pygame.display.set_mode((175, 175))
    clock = pygame.time.Clock()
    pygame.display.set_caption("Test affichage Planètes")

    # Créer un objet à tester
    P1 = Animator(screen, PLANETES_PATH, (5, 5), (-1, -1), default_fps=15)
    P1.play("planet1", True)
    P1.update_and_draw()

    # --- Liste pour stocker les frames ---
    frames = []

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 2:
                    animation = P1.current_anim
                    num = int(animation[6])
                    if num >= MAX_PLANETES_ANIMATIONS:
                        print(f"Limite atteinte : {animation}")
                        running = False
                    else:
                        animation = animation[:6] + str(num + 1) + animation[7:]
                        P1.play(animation, True)
                if event.button == 1:
                    animation = P1.current_anim
                    num = int(animation[6])
                    next_num = ((num) % MAX_PLANETES_ANIMATIONS) + 1
                    animation = animation[:6] + str(next_num) + animation[7:]
                    P1.play(animation, True)

        # --- Update & draw ---
        P1.erase()
        P1.update_and_draw()
        pygame.display.flip()
        clock.tick(60)

        # --- Capturer la frame pour GIF ---
        frame_array = pygame.surfarray.array3d(screen)
        frame_array = np.transpose(frame_array, (1, 0, 2))
        frame_image = Image.fromarray(frame_array)
        frames.append(frame_image)

    # --- Sauvegarder le GIF ---
    if frames and False == True:
        frames[0].save("capture.gif", save_all=True, append_images=frames[1:], duration=1000//60, loop=0)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

