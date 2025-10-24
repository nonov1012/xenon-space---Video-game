import os
import pygame

# Constantes

pygame.init()

info = pygame.display.Info()
SCREEN_WIDTH = info.current_w
SCREEN_HEIGHT = info.current_h

pygame.quit()

# Shop
BAR_HEIGHT = 85
ICON_SIZE = 50
ICON_MARGIN = 20
CASE_PADDING = 8

# Taille de la map
NB_CASE_X = 50 # Nombre de cases en largeur
NB_CASE_Y = 30 # Nombre de cases en hauteur
TAILLE_CASE = (SCREEN_HEIGHT - BAR_HEIGHT) // NB_CASE_Y # Taille d'une case en pixels


# Adapté l'écran
GRID_WIDTH = NB_CASE_X * TAILLE_CASE
OFFSET_X = max((SCREEN_WIDTH - GRID_WIDTH) // 2, 100)

# Planètes
MAX_PLANETES_ANIMATIONS = 50 # Nombre d'animations de planètes différents
PLANETES_FRAME_SIZE = (75, 75) # Taille d'une frame de planètes

# Chemain des fichiers
BASE_DIR = os.path.dirname(__file__) # Chemain du dossier du projet
IMG_PATH = os.path.join(BASE_DIR, "assets", "img")
PLANETES_PATH = os.path.join(IMG_PATH, "planets")
PROJECTILES_PATH = os.path.join(IMG_PATH, "projectiles")
ASTEROIDES_PATH = os.path.join(IMG_PATH, "asteroides")

# Stats des vaisseaux
CSTE : int = 10
# Gains

PLANETES_REWARD = 150
ASTEROIDES_REWARD = 100
POURCENT_DEATH_REWARD = 0.6

RPC_ID = "1419749281190903848"

if __name__ == "__main__":
    print("\n" + IMG_PATH)
