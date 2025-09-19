import pygame
import numpy as np
from classes.Ship_class import CombatShip, MinerShip, TransportShip

# --- Paramètres du plateau ---
TAILLE_CASE = 40
NOMBRE_LIGNES = 20
NOMBRE_COLONNES = 20
LARGEUR = NOMBRE_COLONNES * TAILLE_CASE
HAUTEUR = NOMBRE_LIGNES * TAILLE_CASE

pygame.init()
fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Xenon Space - Déplacement/Attaque")

# --- Plateau numpy ---
plateau = np.zeros((NOMBRE_LIGNES, NOMBRE_COLONNES), dtype=int)

# --- Image factice pour les vaisseaux ---
img = pygame.image.load("assets/img/ships/Kla'ed - Battlecruiser - Base.PNG").convert_alpha()

# --- Création de vaisseaux avec uid unique ---
next_uid = 1
ships = []

s1 = CombatShip(200, 75, 3, 3, 325, 200, (1, 3), False, False, img, 1, ligne=2, colonne=2, uid=next_uid)
next_uid += 1
s2 = CombatShip(400, 175, 6, 4, 650, 390, (2, 3), False, False, img, 1, ligne=4, colonne=7, uid=next_uid)
next_uid += 1

ships.append(s1)
ships.append(s2)

# --- Ajouter sur le plateau ---
for s in ships:
    s.occuper_plateau(plateau, int(s.id))

selection_ship = None
fonctionne = True
clock = pygame.time.Clock()

while fonctionne:
    clock.tick(60)
    position_souris = pygame.mouse.get_pos()
    case_souris = (position_souris[1] // TAILLE_CASE, position_souris[0] // TAILLE_CASE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            fonctionne = False

        # --- Clic souris ---
        if event.type == pygame.MOUSEBUTTONDOWN:
            if selection_ship is not None:
                moved_or_attacked = selection_ship.deplacement(
                    case_souris, NOMBRE_COLONNES, NOMBRE_LIGNES, plateau, ships
                )
                selection_ship = None
            else:
                # Sélection d'un ship
                for ship in ships:
                    largeur, hauteur = ship.donner_dimensions(ship.direction)
                    if (ship.ligne <= case_souris[0] < ship.ligne + hauteur and
                        ship.colonne <= case_souris[1] < ship.colonne + largeur):
                        selection_ship = ship
                        selection_ship.aperçu_direction = ship.direction
                        selection_ship.aperçu_ligne = ship.ligne
                        selection_ship.aperçu_colonne = ship.colonne
                        break

        # --- Rotation avec R ---
        if event.type == pygame.KEYDOWN and selection_ship is not None:
            if event.key == pygame.K_r:
                selection_ship.rotation_aperçu_si_possible(case_souris, NOMBRE_COLONNES, NOMBRE_LIGNES)

    # --- Dessin plateau ---
    fenetre.fill((255, 255, 255))
    for ligne in range(NOMBRE_LIGNES):
        for colonne in range(NOMBRE_COLONNES):
            couleur = (200, 200, 200) if (ligne + colonne) % 2 == 0 else (160, 160, 160)
            pygame.draw.rect(fenetre, couleur,
                             (colonne * TAILLE_CASE, ligne * TAILLE_CASE, TAILLE_CASE, TAILLE_CASE))

    # --- Dessin vaisseaux ---
    for ship in ships:
        ship.dessiner(fenetre, TAILLE_CASE)

    # --- Cases possibles déplacement/attaque + preview ---
    if selection_ship is not None:
        # Déplacement (jaune)
        positions_possibles = selection_ship.positions_possibles_adjacentes(
            NOMBRE_COLONNES, NOMBRE_LIGNES, plateau, direction=selection_ship.aperçu_direction
        )
        for ligne, colonne in positions_possibles:
            rect = pygame.Rect(colonne * TAILLE_CASE, ligne * TAILLE_CASE, TAILLE_CASE, TAILLE_CASE)
            pygame.draw.rect(fenetre, (255, 255, 0), rect, 3)

        # Portée d'attaque (rouge clair)


        positions_attaque = selection_ship.positions_possibles_attaque(
            NOMBRE_COLONNES, NOMBRE_LIGNES, direction=selection_ship.aperçu_direction
        )
        for ligne, colonne in positions_attaque:
            rect = pygame.Rect(colonne * TAILLE_CASE, ligne * TAILLE_CASE, TAILLE_CASE, TAILLE_CASE)
            pygame.draw.rect(fenetre, (255, 100, 100), rect, 2)

        # Aperçu vaisseau sur la case sous la souris
        if case_souris in positions_possibles:
            ligne, colonne = case_souris
            largeur, hauteur = selection_ship.donner_dimensions(selection_ship.aperçu_direction)

            img_preview = selection_ship.image
            if selection_ship.aperçu_direction == "haut":
                img_preview = pygame.transform.rotate(selection_ship.image, 0)
            elif selection_ship.aperçu_direction == "droite":
                img_preview = pygame.transform.rotate(selection_ship.image, -90)
            elif selection_ship.aperçu_direction == "bas":
                img_preview = pygame.transform.rotate(selection_ship.image, 180)
            elif selection_ship.aperçu_direction == "gauche":
                img_preview = pygame.transform.rotate(selection_ship.image, 90)

            surf = pygame.transform.scale(img_preview, (largeur * TAILLE_CASE, hauteur * TAILLE_CASE))
            surf.set_alpha(150)
            fenetre.blit(surf, (colonne * TAILLE_CASE, ligne * TAILLE_CASE))

            # Bordure selon action possible
            occupant = plateau[case_souris[0], case_souris[1]]
            if occupant != 0 and occupant != selection_ship.id and case_souris in positions_attaque:
                border_color = (255, 0, 0)  # attaque possible
            else:
                border_color = (255, 255, 0)  # déplacement

            rect = pygame.Rect(colonne * TAILLE_CASE, ligne * TAILLE_CASE,
                               largeur * TAILLE_CASE, hauteur * TAILLE_CASE)
            pygame.draw.rect(fenetre, border_color, rect, 3)

    pygame.display.flip()

pygame.quit()
