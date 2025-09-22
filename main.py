import pygame
import numpy as np
from classes.Ship_class import petit, moyen, lourd, Transport, foreuse
from classes.MotherShip_class import MotherShip

# --- Paramètres ---
TAILLE_CASE = 40
NOMBRE_LIGNES = 20
NOMBRE_COLONNES = 20
LARGEUR = NOMBRE_COLONNES * TAILLE_CASE
HAUTEUR = NOMBRE_LIGNES * TAILLE_CASE

pygame.init()
fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Xenon Space - Déplacement/Attaque")

# --- Plateau ---
plateau = np.zeros((NOMBRE_LIGNES, NOMBRE_COLONNES), dtype=int)

# --- Images ---
img_lourd = pygame.image.load("assets/img/ships/lourd/lourd.png").convert_alpha()
img_moyen = pygame.image.load("assets/img/ships/moyen/moyen.png").convert_alpha()
img_petit = pygame.image.load("assets/img/ships/petit/petit.png").convert_alpha()
img_foreuse = pygame.image.load("assets/img/ships/foreuse/foreuse.png").convert_alpha()
img_transport = pygame.image.load("assets/img/ships/transport/transport.png").convert_alpha()

# --- Création vaisseaux ---
next_uid = 1
ships = []

s1 = moyen(200, 75, 3, 3, 325, 200, (3,3), False, False, img_moyen, 1, ligne=2, colonne=2, uid=next_uid)
next_uid += 1
s2 = lourd(400, 175, 6, 4, 650, 390, (3,4), False, False, img_lourd, 1, ligne=4, colonne=7, uid=next_uid)
next_uid += 1
s3 = petit(400, 75, 8, 3, 325, 200, (1,1), False, False, img_petit, 1, ligne=5, colonne=5, uid=next_uid)
next_uid += 1
s6 = petit(400, 75, 8, 3, 325, 200, (1,1), False, False, img_petit, 1, ligne=6, colonne=5, uid=next_uid)
next_uid += 1
s7 = petit(400, 75, 8, 3, 325, 200, (1,1), False, False, img_petit, 1, ligne=7, colonne=5, uid=next_uid)
next_uid += 1
s8 = petit(400, 75, 8, 3, 325, 200, (1,1), False, False, img_petit, 1, ligne=8, colonne=5, uid=next_uid)
next_uid += 1
s4 = Transport(400, 75, 3, 3, 325, 200, (3,4), False, True, img_transport, 1, ligne=6, colonne=2, uid=next_uid)
next_uid += 1
s5 = foreuse(400, 75, 3, 3, 325, 200, (2,2), False, False, img_foreuse, 1, ligne=9, colonne=9, uid=next_uid)
next_uid += 1

#B1 = MotherShip(400, 75, 3, 3, 325, 200, (2,2), False, False, img_foreuse, 1, ligne=12, colonne=12, uid=next_uid)

ships.extend([s1, s2, s3, s4, s5, s6, s7, s8])

# --- Placer vaisseaux ---
for s in ships:
    s.occuper_plateau(plateau, int(s.id))

# --- Variables de sélection ---
selection_ship = None
selection_cargo = None
interface_transport_active = False

clock = pygame.time.Clock()
fonctionne = True

# --- Boucle principale ---
while fonctionne:
    clock.tick(60)
    position_souris = pygame.mouse.get_pos()
    case_souris = (position_souris[1] // TAILLE_CASE, position_souris[0] // TAILLE_CASE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            fonctionne = False

        # --- Clic gauche = sélection / déplacement / attaque ---
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if selection_ship is not None and not interface_transport_active:
                selection_ship.deplacement(case_souris, NOMBRE_COLONNES, NOMBRE_LIGNES, plateau, ships)
                selection_ship = None
                selection_cargo = None
            else:
                # Sélectionner un vaisseau
                for ship in ships:
                    largeur, hauteur = ship.donner_dimensions(ship.direction)
                    if (ship.ligne <= case_souris[0] < ship.ligne + hauteur and
                        ship.colonne <= case_souris[1] < ship.colonne + largeur):
                        selection_ship = ship
                        selection_ship.aperçu_direction = ship.direction
                        selection_ship.aperçu_ligne = ship.ligne
                        selection_ship.aperçu_colonne = ship.colonne
                        break

        # --- Clic droit = embarquement / interface transport / débarquement ---
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            if selection_ship is not None:
                # Transport sélectionné
                if isinstance(selection_ship, Transport):
                    clicked_on_mini = False
                    # Vérifier clic sur vaisseaux stockés
                    for i, ship in enumerate(selection_ship.cargaison):
                        x_rect = selection_ship.colonne * TAILLE_CASE + i*22
                        y_rect = selection_ship.ligne * TAILLE_CASE - 22
                        rect = pygame.Rect(x_rect, y_rect, 20, 20)
                        if rect.collidepoint(position_souris):
                            selection_cargo = ship
                            interface_transport_active = True
                            clicked_on_mini = True
                            break
                    # Débarquement
                    if not clicked_on_mini and interface_transport_active and selection_cargo is not None:
                        positions_valides = selection_ship.positions_debarquement(selection_cargo, plateau, NOMBRE_LIGNES, NOMBRE_COLONNES)
                        if case_souris in positions_valides:
                            index = selection_ship.cargaison.index(selection_cargo)
                            selection_ship.retirer_cargo(index, case_souris[0], case_souris[1], plateau)
                            ships.append(selection_cargo)
                            selection_cargo = None
                            interface_transport_active = False
                else:
                    # Embarquer un autre vaisseau dans le transport
                    for target in ships:
                        if target == selection_ship: continue
                        largeur, hauteur = target.donner_dimensions(target.direction)
                        if (target.ligne <= case_souris[0] < target.ligne + hauteur and
                            target.colonne <= case_souris[1] < target.colonne + largeur):
                            if isinstance(target, Transport):
                                success = target.ajouter_cargo(selection_ship, plateau)
                                if success:
                                    ships.remove(selection_ship)
                                    selection_ship = None
                                    selection_cargo = None
                                    interface_transport_active = False
                            break

        # --- Rotation avec R ---
        if event.type == pygame.KEYDOWN and selection_ship is not None:
            if event.key == pygame.K_r:
                selection_ship.rotation_aperçu_si_possible(case_souris, NOMBRE_COLONNES, NOMBRE_LIGNES)

    # --- Dessin plateau ---
    fenetre.fill((255,255,255))
    for ligne in range(NOMBRE_LIGNES):
        for colonne in range(NOMBRE_COLONNES):
            couleur = (200,200,200) if (ligne+colonne)%2==0 else (160,160,160)
            pygame.draw.rect(fenetre, couleur, (colonne*TAILLE_CASE, ligne*TAILLE_CASE, TAILLE_CASE, TAILLE_CASE))

    # --- Dessin vaisseaux ---
    for ship in ships:
        ship.dessiner(fenetre, TAILLE_CASE)

    # --- Affichage cargaison transport ---
    if selection_ship is not None and isinstance(selection_ship, Transport):
        selection_ship.afficher_cargaison(fenetre, TAILLE_CASE)

    # --- Cases déplacement / preview ---
    if selection_ship is not None:
        if interface_transport_active and selection_cargo is not None:
            # Cases possibles pour débarquer
            positions_possibles = selection_ship.positions_debarquement(selection_cargo, plateau, NOMBRE_LIGNES, NOMBRE_COLONNES)
            for ligne, colonne in positions_possibles:
                rect = pygame.Rect(colonne*TAILLE_CASE, ligne*TAILLE_CASE, TAILLE_CASE, TAILLE_CASE)
                pygame.draw.rect(fenetre, (255,255,0), rect, 3)
            if case_souris in positions_possibles:
                largeur, hauteur = selection_cargo.donner_dimensions(selection_cargo.direction)
                surf = pygame.transform.scale(selection_cargo.image, (largeur*TAILLE_CASE, hauteur*TAILLE_CASE))
                surf.set_alpha(150)
                fenetre.blit(surf, (case_souris[1]*TAILLE_CASE, case_souris[0]*TAILLE_CASE))
        else:
            # Cases possibles pour déplacement
            positions_possibles = selection_ship.positions_possibles_adjacentes(NOMBRE_COLONNES, NOMBRE_LIGNES, plateau, direction=selection_ship.aperçu_direction)
            for ligne, colonne in positions_possibles:
                rect = pygame.Rect(colonne*TAILLE_CASE, ligne*TAILLE_CASE, TAILLE_CASE, TAILLE_CASE)
                pygame.draw.rect(fenetre, (255,255,0), rect, 3)
            if case_souris in positions_possibles:
                largeur, hauteur = selection_ship.donner_dimensions(selection_ship.aperçu_direction)
                surf = pygame.transform.scale(selection_ship.image, (largeur*TAILLE_CASE, hauteur*TAILLE_CASE))
                surf.set_alpha(150)
                fenetre.blit(surf, (case_souris[1]*TAILLE_CASE, case_souris[0]*TAILLE_CASE))

    # --- Cases attaque ---
    if selection_ship is not None and not interface_transport_active:
        positions_attaque = selection_ship.positions_possibles_attaque(NOMBRE_COLONNES, NOMBRE_LIGNES, direction=selection_ship.aperçu_direction)
        for ligne, colonne in positions_attaque:
            rect = pygame.Rect(colonne*TAILLE_CASE, ligne*TAILLE_CASE, TAILLE_CASE, TAILLE_CASE)
            pygame.draw.rect(fenetre, (255,100,100), rect, 2)

    pygame.display.flip()

pygame.quit()
