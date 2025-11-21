import os
import pygame

# ========== VARIABLES GLOBALES ==========
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
BASE_W = 1920
BASE_H = 1080

SCALE_X = 1
SCALE_Y = 1
SCALE = 1

# Shop
BAR_HEIGHT = 85
ICON_SIZE = 50
ICON_MARGIN = 20
CASE_PADDING = 8
FONT_SIZE = 30

# Map
NB_CASE_X = 50
NB_CASE_Y = 30
BASE_TAILLE_CASE = 0
TAILLE_CASE = 0
GRID_WIDTH = 0
OFFSET_X = 0

# Planètes
MAX_PLANETES_ANIMATIONS = 50
PLANETES_FRAME_SIZE = (75, 75)

# Chemins
BASE_DIR = os.path.dirname(__file__)
IMG_PATH = os.path.join(BASE_DIR, "assets", "img")
PLANETES_PATH = os.path.join(IMG_PATH, "planets")
PROJECTILES_PATH = os.path.join(IMG_PATH, "projectiles")
ASTEROIDES_PATH = os.path.join(IMG_PATH, "asteroides")
ICONES_PATH = os.path.join(BASE_DIR, "assets", "icons")

# Stats
CSTE = 10
PLANETES_REWARD = 150
ASTEROIDES_REWARD = 100
POURCENT_DEATH_REWARD = 0.6

RPC_ID = "1419749281190903848"

# ========== FONCTIONS DE MISE À JOUR ==========

def update_all(screen: pygame.Surface):
    """Met à jour toutes les dimensions dépendantes de l'écran."""
    update_screen(screen)
    update_shop()
    update_map_size()


def update_screen(screen: pygame.Surface) -> None:
    """Met à jour les infos de résolution + SCALE."""
    global SCREEN_WIDTH, SCREEN_HEIGHT
    global SCALE_X, SCALE_Y, SCALE

    SCREEN_WIDTH = screen.get_width()
    SCREEN_HEIGHT = screen.get_height()

    SCALE_X = SCREEN_WIDTH / BASE_W
    SCALE_Y = SCREEN_HEIGHT / BASE_H
    SCALE = min(SCALE_X, SCALE_Y)


def update_shop() -> None:
    """Met à jour les dimensions de la barre du shop."""
    global BAR_HEIGHT, ICON_SIZE, ICON_MARGIN, CASE_PADDING

    BAR_HEIGHT = int(85 * SCALE)
    ICON_SIZE = int(50 * SCALE)
    ICON_MARGIN = int(20 * SCALE)
    CASE_PADDING = int(8 * SCALE)


def update_map_size() -> None:
    """Met à jour la taille de la map et le centrage horizontal."""
    global BASE_TAILLE_CASE, TAILLE_CASE, GRID_WIDTH, OFFSET_X

    BASE_TAILLE_CASE = (BASE_H - BAR_HEIGHT) // NB_CASE_Y
    TAILLE_CASE = int(BASE_TAILLE_CASE * SCALE)

    GRID_WIDTH = NB_CASE_X * TAILLE_CASE
    OFFSET_X = max((SCREEN_WIDTH - GRID_WIDTH) // 2, 100)

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((400, 800), pygame.RESIZABLE)
    update_all(screen)
    print("WIDTH =", SCREEN_WIDTH, "HEIGHT =", SCREEN_HEIGHT, "SCALE =", SCALE)
