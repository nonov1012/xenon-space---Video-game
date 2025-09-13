import pygame
import sys
from vaisseau import Vaisseau
from deplacement import Deplacement

# --- Constantes ---
TAILLE_CASE = 40
NB_CASES = 15
LARGEUR = NB_CASES * TAILLE_CASE
HAUTEUR = NB_CASES * TAILLE_CASE

# --- Couleurs ---
BLANC = (255, 255, 255)
GRIS = (200, 200, 200)
NOIR = (0, 0, 0)
BLEU = (0, 0, 255)
ORANGE = (255, 150, 0)
VERT = (50, 200, 50)
ROUGE = (200, 50, 50)
BLEU_TRANSPARENT = (0, 0, 255, 120)

# --- Initialisation pygame ---
pygame.init()
ecran = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Déplacement Vaisseau")

clock = pygame.time.Clock()

# --- Grille avec obstacles ---
grille = [[0]*NB_CASES for _ in range(NB_CASES)]
for i in range(4, 10):
    grille[7][i] = 1
    grille[i][10] = 1

# --- Création du vaisseau et du gestionnaire de déplacement ---
vaisseau = Vaisseau(2, 2)
deplacement = Deplacement(vaisseau, grille, rayon=3)

# --- Fonctions de dessin ---
def dessiner_grille(surface):
    """Dessine la grille et les obstacles."""
    for i in range(NB_CASES):
        for j in range(NB_CASES):
            rect = pygame.Rect(i*TAILLE_CASE, j*TAILLE_CASE, TAILLE_CASE, TAILLE_CASE)
            if grille[j][i] == 1:
                pygame.draw.rect(surface, NOIR, rect)
            pygame.draw.rect(surface, GRIS, rect, 1)

def dessiner_cases_accessibles(surface):
    """Dessine les cases accessibles autour du vaisseau."""
    for (x, y) in deplacement.cases_accessibles:
        rect = pygame.Rect(x*TAILLE_CASE, y*TAILLE_CASE,
                           vaisseau.largeur*TAILLE_CASE, vaisseau.hauteur*TAILLE_CASE)
        pygame.draw.rect(surface, VERT, rect, 2)

def dessiner_fantome(surface, souris_cx, souris_cy):
    """Dessine un fantôme bleu transparent sur la case accessible la plus proche de la souris."""
    if not vaisseau.selectionne or not deplacement.cases_accessibles:
        return
    distances = [(abs(souris_cx - x) + abs(souris_cy - y), (x, y)) for (x, y) in deplacement.cases_accessibles]
    distances.sort()
    x, y = distances[0][1]
    surf = pygame.Surface((vaisseau.largeur*TAILLE_CASE, vaisseau.hauteur*TAILLE_CASE), pygame.SRCALPHA)
    surf.fill(BLEU_TRANSPARENT)
    surface.blit(surf, (x*TAILLE_CASE, y*TAILLE_CASE))

def dessiner_chemin(surface):
    """Dessine le chemin planifié du vaisseau."""
    for (x, y) in vaisseau.chemin:
        rect = pygame.Rect(x*TAILLE_CASE, y*TAILLE_CASE,
                           vaisseau.largeur*TAILLE_CASE, vaisseau.hauteur*TAILLE_CASE)
        pygame.draw.rect(surface, ROUGE, rect, 2)

# --- Boucle principale ---
while True:
    souris_x, souris_y = pygame.mouse.get_pos()
    case_cx, case_cy = souris_x // TAILLE_CASE, souris_y // TAILLE_CASE

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Sélection du vaisseau si on clique dessus
            if vaisseau.x <= case_cx < vaisseau.x + vaisseau.largeur and \
               vaisseau.y <= case_cy < vaisseau.y + vaisseau.hauteur:
                vaisseau.selectionne = True
            elif vaisseau.selectionne:
                # Déplacement vers la case accessible la plus proche
                if deplacement.cases_accessibles:
                    distances = [(abs(case_cx - x) + abs(case_cy - y), (x, y)) for (x, y) in deplacement.cases_accessibles]
                    distances.sort()
                    cible = distances[0][1]
                    vaisseau.chemin = deplacement.astar((vaisseau.x, vaisseau.y), cible)

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                vaisseau.pivoter(deplacement)
                deplacement.mettre_a_jour_cases_accessibles()

    # --- Mise à jour ---
    deplacement.mettre_a_jour_cases_accessibles()
    deplacement.deplacer_vaisseau()

    # --- Dessin ---
    ecran.fill(BLANC)
    dessiner_grille(ecran)
    dessiner_cases_accessibles(ecran)
    dessiner_fantome(ecran, case_cx, case_cy)
    dessiner_chemin(ecran)
    vaisseau.dessiner(ecran)

    pygame.display.flip()
    clock.tick(15)
