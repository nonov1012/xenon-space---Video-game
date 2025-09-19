import os
# Constantes

# Taille de la map
NB_CASE_X = 50 # Nombre de cases en largeur
NB_CASE_Y = 30 # Nombre de cases en hauteur
TAILLE_CASE = 35 # Taille d'une case en pixels
MAX_PLANETES_ANIMATIONS = 4 # Nombre d'animations de planètes différents

# Chemain des fichiers
BASE_DIR = os.path.dirname(__file__) # Chemain du dossier du projet
IMG_PATH = os.path.join(BASE_DIR, "assets", "img")
PLANETES_PATH = os.path.join(IMG_PATH, "planets")

if __name__ == "__main__":
    print("\n" + IMG_PATH)
