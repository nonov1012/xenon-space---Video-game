import pygame
from Ship_class import Ship

# --- Paramètres du plateau ---
TAILLE_CASE = 40
NOMBRE_LIGNE = 20
NOMBRE_colonneONNE = 20
LARGEUR = NOMBRE_colonneONNE * TAILLE_CASE
HAUTEUR = NOMBRE_LIGNE * TAILLE_CASE

pygame.init()
fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Plateau avec Ship et déplacement intégré")

# --- Image factice pour les vaisseaux ---
img = pygame.Surface((TAILLE_CASE, TAILLE_CASE))
img.fill((100, 100, 255))

# --- Création de vaisseaux ---
ships = [
    #PV_max: int, attaque: int, porter_attaque: int, porter_distance: int,cout: int,
    # valeur_mort: int, taille: tuple, miner: bool, transport: bool,image: pygame.image,
    # tier: int, ligne=0, colonneonne=0):
    Ship(200, 75, 3, 3, 325, 200, (1, 3), False, False, img, 1, 2, 2),
    Ship(400, 175, 4, 4, 650, 390, (2, 1), False, False, img, 1, 4, 7),
]

selection_ship = None

fonctionne = True
while fonctionne:
    position_souris = pygame.mouse.get_pos()
    case_souris = (position_souris[1] // TAILLE_CASE, position_souris[0] // TAILLE_CASE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            fonctionne = False

        # --- Clic souris ---
        if event.type == pygame.MOUSEBUTTONDOWN:
            if selection_ship:
                # Déplacement via Ship
                selection_ship.deplacement(case_souris, NOMBRE_colonneONNE, NOMBRE_LIGNE)
                selection_ship = None
            else:
                # Sélection d’un vaisseau
                for ship in ships:
                    taille, height = ship.donne_dimension(ship.direction)
                    if (ship.ligne <= case_souris[0] < ship.ligne + height and
                        ship.colonne <= case_souris[1] < ship.colonne + taille):
                        selection_ship = ship
                        selection_ship.aperçu_direction = ship.direction
                        break

        # --- Rotation avec R ---
        if event.type == pygame.KEYDOWN and selection_ship:
            if event.key == pygame.K_r:
                selection_ship.rotation_aperçu_si_possible(case_souris, NOMBRE_colonneONNE, NOMBRE_LIGNE)

    # --- Dessin plateau ---
    fenetre.fill((255, 255, 255))
    for ligne in range(NOMBRE_LIGNE):
        for colonne in range(NOMBRE_colonneONNE):
            colonneor = (200, 200, 200) if (ligne + colonne) % 2 == 0 else (100, 100, 100)
            pygame.draw.rect(fenetre, colonneor,
                             (colonne * TAILLE_CASE, ligne * TAILLE_CASE, TAILLE_CASE, TAILLE_CASE))

    # --- Dessin vaisseaux ---
    for ship in ships:
        ship.dessin(fenetre, TAILLE_CASE)

    # --- Cases possibles ---
    if selection_ship:
        for ligne, colonne in selection_ship.donne_position_possible(NOMBRE_colonneONNE, NOMBRE_LIGNE):
            rect = pygame.Rect(colonne * TAILLE_CASE, ligne * TAILLE_CASE, TAILLE_CASE, TAILLE_CASE)
            pygame.draw.rect(fenetre, (255, 255, 0), rect, 3)

        # --- Prévisualisation ---
        if case_souris in selection_ship.donne_position_possible(NOMBRE_colonneONNE, NOMBRE_LIGNE):
            ligne, colonne = case_souris
            taille, height = selection_ship.donne_dimension(selection_ship.aperçu_direction)
            surf = pygame.Surface((taille * TAILLE_CASE, height * TAILLE_CASE), pygame.SRCALPHA)
            surf.fill((255, 0, 0, 120))
            fenetre.blit(surf, (colonne * TAILLE_CASE, ligne * TAILLE_CASE))

    pygame.display.flip()

pygame.quit()
