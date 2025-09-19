import os
# Constantes

# Taille de la map
NB_CASE_X = 50 # Nombre de cases en largeur
NB_CASE_Y = 30 # Nombre de cases en hauteur
TAILLE_CASE = 35 # Taille d'une case en pixels

# Path pour les images
import os

# Chemin vers le dossier du fichier courant
base_dir = os.path.dirname(__file__)

# Construire le chemin relatif vers le dossier des images
IMG_PATH = os.path.join(base_dir, "assets", "img")

if __name__ == "__main__":
    print("\n" + IMG_PATH)