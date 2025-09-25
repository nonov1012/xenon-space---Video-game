import pygame
import numpy as np
from classes.Ship import Transport, Foreuse, Petit, Moyen, Lourd
from classes.MotherShip import MotherShip
from classes.Animator import *
from classes.ShipAnimator import ShipAnimator
from classes.ProjectileAnimator import ProjectileAnimator

# --- Paramètres ---
TAILLE_CASE = 32
NOMBRE_LIGNES = 20
NOMBRE_COLONNES = 20
LARGEUR = NOMBRE_COLONNES * TAILLE_CASE
HAUTEUR = NOMBRE_LIGNES * TAILLE_CASE

pygame.init()
fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR))
pygame.display.set_caption("Xenon Space - Déplacement/Attaque")

# Définir l’écran pour Animator
Animator.set_screen(fenetre)


# --- Plateau ---
plateau = np.zeros((NOMBRE_LIGNES, NOMBRE_COLONNES), dtype=int)

# --- Images / dossiers ---
img_Lourd = pygame.image.load("assets/img/ships/lourd/base.png").convert_alpha()
img_moyen = pygame.image.load("assets/img/ships/moyen/base.png").convert_alpha()
img_petit = pygame.image.load("assets/img/ships/petit/base.png").convert_alpha()
img_foreuse = pygame.image.load("assets/img/ships/foreuse/base.png").convert_alpha()
img_transport = pygame.image.load("assets/img/ships/transport/base.png").convert_alpha()

# dossiers pour Animator
img_base = "assets/img/ships/base"
img_lourd_dir = "assets/img/ships/lourd"
img_moyen_dir = "assets/img/ships/moyen"
img_petit_dir = "assets/img/ships/petit"
img_foreuse_dir = "assets/img/ships/foreuse"
img_transport_dir = "assets/img/ships/transport"




# --- Création vaisseaux ---
next_uid = 1
ships = []

sl1 = Lourd(pv_max=500, attaque=300, port_attaque=6, port_deplacement=3, cout=800,
            valeur_mort=800*0.6, taille=(3,3), peut_miner=False, peut_transporter=False,
            image=img_Lourd, tier=4, ligne=8, colonne=8, id=next_uid, BASE_IMG_DIR=img_lourd_dir)
next_uid += 1
ships.append(sl1)

sl2 = Lourd(pv_max=500, attaque=300, port_attaque=6, port_deplacement=3, cout=800,
            valeur_mort=800*0.6, taille=(3,3), peut_miner=False, peut_transporter=False,
            image=img_Lourd, tier=4, ligne=12, colonne=12, id=next_uid, BASE_IMG_DIR=img_lourd_dir)
next_uid += 1
ships.append(sl2)
"""
sm1 = Moyen(pv_max=900, attaque=250, port_attaque=5, port_deplacement=5, cout=800,
            valeur_mort=800*0.6, taille=(2,2), peut_miner=False, peut_transporter=False,
            image=img_moyen, tier=1, ligne=12, colonne=1, id=next_uid, BASE_IMG_DIR=img_moyen_dir)
next_uid += 1
ships.append(sm1)

st1 = Transport(pv_max=1200, attaque=150, port_attaque=4, port_deplacement=8, cout=800,
            valeur_mort=800*0.6, taille=(3,4), peut_miner=False, peut_transporter=True,
            image=img_transport, tier=1, ligne=7, colonne=7, id=next_uid, BASE_IMG_DIR=img_transport_dir)
next_uid += 1
ships.append(st1)

sp1 = Petit(pv_max=300, attaque=100, port_attaque=3, port_deplacement=6, cout=800,
            valeur_mort=800*0.6, taille=(1,1), peut_miner=False, peut_transporter=False,
            image=img_petit, tier=1, ligne=12, colonne=10, id=next_uid, BASE_IMG_DIR=img_petit_dir)
next_uid += 1
ships.append(sp1)

sf1 = Foreuse(pv_max=500, attaque=0, port_attaque=0, port_deplacement=3, cout=800,
            valeur_mort=800*0.6, taille=(2,2), peut_miner=True, peut_transporter=False,
            image=img_foreuse, tier=1, ligne=16, colonne=16, id=next_uid, BASE_IMG_DIR=img_foreuse_dir)
next_uid += 1
ships.append(sf1)

# MotherShip
b2 = MotherShip(fenetre, position=(0, 0), tier=1, largeur=4, hauteur=5, uid=next_uid, BASE_IMG_DIR=img_base)
next_uid += 1
ships.append(b2)
"""

# --- Placer vaisseaux sur le plateau ---
# Placer vaisseaux sur le plateau 
for s in ships:
    # s.id doit être défini . utiliser int(s.id) si nécessaire.
    s.occuper_plateau(plateau, int(s.id))


# --- Variables de sélection ---
selection_ship = None
selection_cargo = None
interface_transport_active = False

clock = pygame.time.Clock()
fonctionne = True

Animator.set_screen(fenetre)

# --- Boucle principale ---
while fonctionne:
    clock.tick(60)
    position_souris = pygame.mouse.get_pos()
    case_souris = (position_souris[1] // TAILLE_CASE, position_souris[0] // TAILLE_CASE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            fonctionne = False

        # --- Clic gauche = déplacement / attaque ---
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if selection_ship is not None and not interface_transport_active:
                selection_ship.deplacement(case_souris, NOMBRE_COLONNES, NOMBRE_LIGNES, plateau, ships)
                selection_ship = None
                selection_cargo = None
            else:
                # Sélectionner un vaisseau
                for ship in ships[:]:
                    largeur, hauteur = ship.donner_dimensions(ship.direction)
                    if (ship.ligne <= case_souris[0] < ship.ligne + hauteur and
                        ship.colonne <= case_souris[1] < ship.colonne + largeur):
                        selection_ship = ship
                        selection_ship.aperçu_direction = ship.direction
                        selection_ship.aperçu_ligne = ship.ligne
                        selection_ship.aperçu_colonne = ship.colonne
                        break

        # --- Clic droit = transport / embarquement / débarquement ---
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3 and selection_ship:
            if isinstance(selection_ship, Transport):
                clicked_on_mini = False
                for i, ship in enumerate(selection_ship.cargaison):
                    rect = pygame.Rect(selection_ship.colonne * TAILLE_CASE + i*22,
                                       selection_ship.ligne * TAILLE_CASE - 22, 20, 20)
                    if rect.collidepoint(position_souris):
                        selection_cargo = ship
                        interface_transport_active = True
                        clicked_on_mini = True
                        break
                if not clicked_on_mini and interface_transport_active and selection_cargo:
                    positions_valides = selection_ship.positions_debarquement(selection_cargo, plateau, NOMBRE_LIGNES, NOMBRE_COLONNES)
                    if case_souris in positions_valides:
                        index = selection_ship.cargaison.index(selection_cargo)
                        selection_ship.retirer_cargo(index, case_souris[0], case_souris[1], plateau)
                        ships.append(selection_cargo)
                        selection_cargo = None
                        interface_transport_active = False
            else:
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
        if event.type == pygame.KEYDOWN and selection_ship:
            if event.key == pygame.K_r:
                selection_ship.rotation_aperçu_si_possible(case_souris, NOMBRE_COLONNES, NOMBRE_LIGNES)

    # --- Dessin plateau ---
    fenetre.fill((255,255,255))
    for ligne in range(NOMBRE_LIGNES):
        for colonne in range(NOMBRE_COLONNES):
            couleur = (200,200,200) if (ligne+colonne)%2==0 else (160,160,160)
            pygame.draw.rect(fenetre, couleur, (colonne*TAILLE_CASE, ligne*TAILLE_CASE, TAILLE_CASE, TAILLE_CASE))

    # --- Mettre à jour et dessiner les vaisseaux ---
    for ship in ships[:]: 
        ship.dessiner(fenetre, TAILLE_CASE)

        # Vérifier si le vaisseau est mort et que l'animation est terminée
        if hasattr(ship, "est_mort") and ship.est_mort():
            ship.occuper_plateau(plateau, 0)
            ships.remove(ship)
            print(f"{ship.__class__.__name__} détruit")



    # --- Affichage cargaison transport ---
    if selection_ship and isinstance(selection_ship, Transport):
        selection_ship.afficher_cargaison(fenetre, TAILLE_CASE)

    # --- Preview déplacement / débarquement ---
    if selection_ship:
        if interface_transport_active and selection_cargo:
            positions_possibles = selection_ship.positions_debarquement(selection_cargo, plateau, NOMBRE_LIGNES, NOMBRE_COLONNES)
            for ligne, colonne in positions_possibles:
                pygame.draw.rect(fenetre, (255,255,0), (colonne*TAILLE_CASE, ligne*TAILLE_CASE, TAILLE_CASE, TAILLE_CASE), 3)
            if case_souris in positions_possibles:
                largeur, hauteur = selection_cargo.donner_dimensions(selection_cargo.direction)
                surf = pygame.transform.scale(selection_cargo.image, (largeur*TAILLE_CASE, hauteur*TAILLE_CASE))
                surf.set_alpha(150)
                fenetre.blit(surf, (case_souris[1]*TAILLE_CASE, case_souris[0]*TAILLE_CASE))
        else:
            positions_possibles = selection_ship.positions_possibles_adjacentes(NOMBRE_COLONNES, NOMBRE_LIGNES, plateau, direction=selection_ship.aperçu_direction)
            for ligne, colonne in positions_possibles:
                pygame.draw.rect(fenetre, (255,255,0), (colonne*TAILLE_CASE, ligne*TAILLE_CASE, TAILLE_CASE, TAILLE_CASE), 3)
            if case_souris in positions_possibles:
                largeur, hauteur = selection_ship.donner_dimensions(selection_ship.aperçu_direction)
                surf = pygame.transform.scale(selection_ship.image, (largeur*TAILLE_CASE, hauteur*TAILLE_CASE))
                surf.set_alpha(150)
                fenetre.blit(surf, (case_souris[1]*TAILLE_CASE, case_souris[0]*TAILLE_CASE))

    # --- Preview attaque ---
    if selection_ship and not interface_transport_active:
        positions_attaque = selection_ship.positions_possibles_attaque(NOMBRE_COLONNES, NOMBRE_LIGNES, direction=selection_ship.aperçu_direction)
        for ligne, colonne in positions_attaque:
            pygame.draw.rect(fenetre, (255,100,100), (colonne*TAILLE_CASE, ligne*TAILLE_CASE, TAILLE_CASE, TAILLE_CASE), 2)
    fenetre.fill((0,0,0))
    ShipAnimator.update_all()
    ProjectileAnimator.update_all()
    pygame.display.flip()
    

pygame.quit()
