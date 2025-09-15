# main_game.py
import pygame
from Ship_class import Ship

# --- Paramètres du plateau ---
TAILLE_CASE = 40
NOMBRE_LIGNES = 20
NOMBRE_COLONNES = 20
LARGEUR = NOMBRE_COLONNES * TAILLE_CASE
HAUTEUR = NOMBRE_LIGNES * TAILLE_CASE

pygame.init()
fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Plateau avec Ship et déplacement intégré")

# --- Image factice pour les vaisseaux ---
img = pygame.image.load("Foozle/_Previews/Kla'ed/bases/Kla'ed - Battlecruiser - Base.PNG").convert_alpha()
img = pygame.transform.scale(img, (2 * TAILLE_CASE, 3 * TAILLE_CASE))

# --- Création de vaisseaux ---
ships = [
    Ship(200, 75, 3, 3, 325, 200, (1, 3), False, False, img, 1, 2, 2),
    Ship(400, 175, 4, 4, 650, 390, (2, 3), False, False, img, 1, 4, 7),
]

selection_ship = None
fonctionne = True
clock = pygame.time.Clock()

while fonctionne:
    clock.tick(60)
    position_souris = pygame.mouse.get_pos()
    case_souris = (position_souris[1] // TAILLE_CASE, position_souris[0] // TAILLE_CASE)  # (ligne, colonne)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            fonctionne = False

        # --- Clic souris ---
        if event.type == pygame.MOUSEBUTTONDOWN:
            if selection_ship:
                # Tente le déplacement (méthode compatible)
                selection_ship.deplacement(case_souris, NOMBRE_COLONNES, NOMBRE_LIGNES)
                selection_ship = None
            else:
                # Sélection d’un vaisseau si la case clique se trouve sur lui
                for ship in ships:
                    largeur, hauteur = ship.donner_dimensions(ship.direction)
                    if (ship.ligne <= case_souris[0] < ship.ligne + hauteur and
                        ship.colonne <= case_souris[1] < ship.colonne + largeur):
                        selection_ship = ship
                        # initialiser l'aperçu sur la position actuelle du ship
                        selection_ship.aperçu_direction = ship.direction
                        selection_ship.aperçu_ligne = ship.ligne
                        selection_ship.aperçu_colonne = ship.colonne
                        break

        # --- Rotation avec R (si un ship est sélectionné) ---
        if event.type == pygame.KEYDOWN and selection_ship:
            if event.key == pygame.K_r:
                selection_ship.rotation_aperçu_si_possible(case_souris, NOMBRE_COLONNES, NOMBRE_LIGNES)

    # --- Dessin plateau ---
    fenetre.fill((255, 255, 255))
    for ligne in range(NOMBRE_LIGNES):
        for colonne in range(NOMBRE_COLONNES):
            couleur = (200, 200, 200) if (ligne + colonne) % 2 == 0 else (160, 160, 160)
            pygame.draw.rect(fenetre, couleur,
                             (colonne * TAILLE_CASE, ligne * TAILLE_CASE, TAILLE_CASE, TAILLE_CASE))

    # --- Dessin vaisseaux (réels) ---
    for ship in ships:
        ship.dessiner(fenetre, TAILLE_CASE)

    # --- Si un ship est sélectionné, dessiner cases possibles et prévisualisation ---
    if selection_ship:
        for ligne, colonne in selection_ship.positions_possibles_adjacentes(NOMBRE_COLONNES, NOMBRE_LIGNES):
            rect = pygame.Rect(colonne * TAILLE_CASE, ligne * TAILLE_CASE, TAILLE_CASE, TAILLE_CASE)
            pygame.draw.rect(fenetre, (255, 255, 0), rect, 3)

        # --- Prévisualisation ---
        if case_souris in selection_ship.positions_possibles_adjacentes(NOMBRE_COLONNES, NOMBRE_LIGNES):
            ligne, colonne = case_souris
            largeur, hauteur = selection_ship.donner_dimensions(selection_ship.aperçu_direction)

            # Ajustement selon la direction
            if selection_ship.aperçu_direction == "haut":
                ligne -= hauteur - 1
            elif selection_ship.aperçu_direction == "gauche":
                colonne -= largeur - 1

            # Charger et scaler l'image avec transparence
            surf = pygame.transform.scale(selection_ship.image, (largeur * TAILLE_CASE, hauteur * TAILLE_CASE))
            surf.set_alpha(150)
            # Blitter sur la fenêtre
            fenetre.blit(surf, (colonne * TAILLE_CASE, ligne * TAILLE_CASE))



    pygame.display.flip()

pygame.quit()
