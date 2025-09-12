import pygame
from ship import Ship

TAILLE_CASE = 80
NB_LIGNES = 6
NB_COLONNES = 10

# --- Paramètres du plateau ---
LARGEUR = NB_COLONNES * TAILLE_CASE
HAUTEUR = NB_LIGNES * TAILLE_CASE

# --- Initialisation ---
pygame.init()
fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Plateau avec Ship et rotation en prévisualisation")

# --- Image factice pour les vaisseaux ---
img = pygame.Surface((TAILLE_CASE, TAILLE_CASE))
img.fill((100, 100, 255))

# --- Liste de vaisseaux ---
ships = [
    Ship(200, 75, 3, 3, 325, 200, (1, 3), False, False, img, 1, 2, 2),
    Ship(400, 175, 4, 4, 650, 390, (2, 1), False, False, img, 1, 4, 7),
]

ship_selectionne = None
positions_possibles = []

# --- Boucle principale ---
running = True
while running:
    mouse_pos = pygame.mouse.get_pos()
    mouse_case = (mouse_pos[1] // TAILLE_CASE, mouse_pos[0] // TAILLE_CASE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Clic souris
        if event.type == pygame.MOUSEBUTTONDOWN:
            l, c = mouse_case

            if ship_selectionne:
                # Vérifie si la case est possible ET que tout le vaisseau reste dans le damier
                if (l, c) in positions_possibles and ship_selectionne.est_dans_plateau(
                    l, c, ship_selectionne.preview_direction, NB_COLONNES, NB_LIGNES
                ):
                    ship_selectionne.ligne = l
                    ship_selectionne.col = c
                    ship_selectionne.direction = ship_selectionne.preview_direction
                ship_selectionne = None
                positions_possibles = []

            else:
                # Sélection d’un vaisseau
                for ship in ships:
                    largeur, hauteur = ship.get_dimensions(ship.direction)
                    if (ship.ligne <= l < ship.ligne + hauteur and
                        ship.col <= c < ship.col + largeur):
                        ship_selectionne = ship
                        positions_possibles = ship.positions_possibles(NB_COLONNES, NB_LIGNES)
                        ship_selectionne.preview_direction = ship.direction
                        break

        # Rotation avec R (prévisualisation seulement)
        if event.type == pygame.KEYDOWN and ship_selectionne:
            if event.key == pygame.K_r:
                ship_selectionne.rotate_preview(NB_COLONNES, NB_LIGNES, mouse_case)

    # --- Dessin plateau ---
    fenetre.fill((255, 255, 255))
    for ligne in range(NB_LIGNES):
        for col in range(NB_COLONNES):
            couleur = (200, 200, 200) if (ligne + col) % 2 == 0 else (100, 100, 100)
            pygame.draw.rect(fenetre, couleur,
                             (col * TAILLE_CASE, ligne * TAILLE_CASE, TAILLE_CASE, TAILLE_CASE))

    # --- Dessin des vaisseaux réels ---
    for ship in ships:
        ship.draw(fenetre, TAILLE_CASE)

    # --- Dessin cases possibles au-dessus des vaisseaux ---
    for l, c in positions_possibles:
        rect = pygame.Rect(c * TAILLE_CASE, l * TAILLE_CASE, TAILLE_CASE, TAILLE_CASE)
        pygame.draw.rect(fenetre, (255, 255, 0), rect, 3)

    # --- Prévisualisation ---
    if ship_selectionne and mouse_case in positions_possibles:
        l, c = mouse_case
        largeur, hauteur = ship_selectionne.get_dimensions(ship_selectionne.preview_direction)
        w = largeur * TAILLE_CASE
        h = hauteur * TAILLE_CASE
        x = c * TAILLE_CASE
        y = l * TAILLE_CASE
        surf = pygame.Surface((w, h), pygame.SRCALPHA)
        surf.fill((255, 0, 0, 120))  # rouge transparent
        fenetre.blit(surf, (x, y))

    pygame.display.flip()

pygame.quit()
