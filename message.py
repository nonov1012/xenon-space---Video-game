import pygame
from ship import Ship

# --- Paramètres du plateau ---
TAILLE_CASE = 80
NB_LIGNES = 6
NB_COLONNES = 10
LARGEUR = NB_COLONNES * TAILLE_CASE
HAUTEUR = NB_LIGNES * TAILLE_CASE

pygame.init()
fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Plateau avec Ship et déplacement intégré")

# --- Image factice pour les vaisseaux ---
img = pygame.Surface((TAILLE_CASE, TAILLE_CASE))
img.fill((100, 100, 255))

# --- Création de vaisseaux ---
ships = [
    Ship(200, 75, 3, 3, 325, 200, (1, 3), False, False, img, 1, 2, 2),
    Ship(400, 175, 4, 4, 650, 390, (2, 1), False, False, img, 1, 4, 7),
]

selected_ship = None

running = True
while running:
    mouse_pos = pygame.mouse.get_pos()
    mouse_tile = (mouse_pos[1] // TAILLE_CASE, mouse_pos[0] // TAILLE_CASE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # --- Clic souris ---
        if event.type == pygame.MOUSEBUTTONDOWN:
            if selected_ship:
                # Déplacement via Ship
                selected_ship.move_to(mouse_tile, NB_COLONNES, NB_LIGNES)
                selected_ship = None
            else:
                # Sélection d’un vaisseau
                for ship in ships:
                    width, height = ship.get_dimensions(ship.direction)
                    if (ship.row <= mouse_tile[0] < ship.row + height and
                        ship.col <= mouse_tile[1] < ship.col + width):
                        selected_ship = ship
                        selected_ship.preview_direction = ship.direction
                        break

        # --- Rotation avec R ---
        if event.type == pygame.KEYDOWN and selected_ship:
            if event.key == pygame.K_r:
                selected_ship.rotate_preview_if_possible(mouse_tile, NB_COLONNES, NB_LIGNES)

    # --- Dessin plateau ---
    fenetre.fill((255, 255, 255))
    for row in range(NB_LIGNES):
        for col in range(NB_COLONNES):
            color = (200, 200, 200) if (row + col) % 2 == 0 else (100, 100, 100)
            pygame.draw.rect(fenetre, color,
                             (col * TAILLE_CASE, row * TAILLE_CASE, TAILLE_CASE, TAILLE_CASE))

    # --- Dessin vaisseaux ---
    for ship in ships:
        ship.draw(fenetre, TAILLE_CASE)

    # --- Cases possibles ---
    if selected_ship:
        for row, col in selected_ship.get_possible_positions(NB_COLONNES, NB_LIGNES):
            rect = pygame.Rect(col * TAILLE_CASE, row * TAILLE_CASE, TAILLE_CASE, TAILLE_CASE)
            pygame.draw.rect(fenetre, (255, 255, 0), rect, 3)

        # --- Prévisualisation ---
        if mouse_tile in selected_ship.get_possible_positions(NB_COLONNES, NB_LIGNES):
            row, col = mouse_tile
            width, height = selected_ship.get_dimensions(selected_ship.preview_direction)
            surf = pygame.Surface((width * TAILLE_CASE, height * TAILLE_CASE), pygame.SRCALPHA)
            surf.fill((255, 0, 0, 120))
            fenetre.blit(surf, (col * TAILLE_CASE, row * TAILLE_CASE))

    pygame.display.flip()

pygame.quit()
