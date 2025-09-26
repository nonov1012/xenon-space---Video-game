import os
import pygame

pygame.init()

info = pygame.display.Info()
screen_width = info.current_w
screen_height = info.current_h

pygame.quit()
# Constantes

# Taille de la map
NB_CASE_X = 50 # Nombre de cases en largeur
NB_CASE_Y = 30 # Nombre de cases en hauteur
TAILLE_CASE = screen_height // (NB_CASE_Y + 2) # Taille d'une case en pixels

# Adapté l'écran
GRID_WIDTH = NB_CASE_X * TAILLE_CASE
OFFSET_X = (screen_width - GRID_WIDTH) // 2

# Planètes
MAX_PLANETES_ANIMATIONS = 6 # Nombre d'animations de planètes différents
PLANETES_FRAME_SIZE = (75, 75) # Taille d'une frame de planètes

# Chemain des fichiers
BASE_DIR = os.path.dirname(__file__) # Chemain du dossier du projet
IMG_PATH = os.path.join(BASE_DIR, "assets", "img")
PLANETES_PATH = os.path.join(IMG_PATH, "planets")
PROJECTILES_PATH = os.path.join(IMG_PATH, "projectiles")
ASTEROIDES_PATH = os.path.join(IMG_PATH, "asteroides")

RPC_ID = "1419749281190903848"

if __name__ == "__main__":
    print("\n" + IMG_PATH)
