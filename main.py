import pygame
from classes.Ship import Transport, Foreuse, Petit, Moyen, Lourd
from classes.MotherShip import MotherShip
from classes.Animator import *
from classes.ShipAnimator import ShipAnimator
from classes.ProjectileAnimator import ProjectileAnimator
from classes.Point import Point

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

# --- Plateau (liste de listes) ---
plateau = [[0 for _ in range(NOMBRE_COLONNES)] for _ in range(NOMBRE_LIGNES)]

# --- Images / dossiers ---
img_Lourd = pygame.image.load("assets/img/ships/lourd/base.png").convert_alpha()
img_moyen = pygame.image.load("assets/img/ships/moyen/base.png").convert_alpha()
img_petit = pygame.image.load("assets/img/ships/petit/base.png").convert_alpha()
img_foreuse = pygame.image.load("assets/img/ships/foreuse/base.png").convert_alpha()
img_transport = pygame.image.load("assets/img/ships/transport/base.png").convert_alpha()

img_lourd_dir = "assets/img/ships/lourd"
img_moyen_dir = "assets/img/ships/moyen"
img_petit_dir = "assets/img/ships/petit"
img_foreuse_dir = "assets/img/ships/foreuse"
img_transport_dir = "assets/img/ships/transport"
img_base_dir = "assets/img/ships/base"

# --- Création vaisseaux ---
next_uid = 1
ships = []

# Lourd 1
sl1point = Point(8, 8)
sl1 = Lourd(pv_max=500, attaque=300, port_attaque=6, port_deplacement=3, cout=800,
            valeur_mort=int(800*0.6), taille=(3,3), peut_miner=False, peut_transporter=False,
            image=img_Lourd, tier=4, cordonner=sl1point, id=next_uid, path=img_lourd_dir)
next_uid += 1
ships.append(sl1)

# Lourd 2
sl2point = Point(12, 12)
sl2 = Lourd(pv_max=500, attaque=300, port_attaque=6, port_deplacement=3, cout=800,
            valeur_mort=int(800*0.6), taille=(3,3), peut_miner=False, peut_transporter=False,
            image=img_Lourd, tier=4, cordonner=sl2point, id=next_uid, path=img_lourd_dir)
next_uid += 1
ships.append(sl2)

# Moyen
sm1point = Point(12, 1)
sm1 = Moyen(pv_max=900, attaque=250, port_attaque=5, port_deplacement=5, cout=800,
            valeur_mort=int(800*0.6), taille=(2,2), peut_miner=False, peut_transporter=False,
            image=img_moyen, tier=1, cordonner=sm1point, id=next_uid, path=img_moyen_dir)
next_uid += 1
ships.append(sm1)

# Transport
st1point = Point(7,7)
st1 = Transport(pv_max=1200, attaque=150, port_attaque=4, port_deplacement=8, cout=800,
                valeur_mort=int(800*0.6), taille=(3,4), peut_miner=False, peut_transporter=True,
                image=img_transport, tier=1, cordonner=st1point, id=next_uid, path=img_transport_dir)
next_uid += 1
ships.append(st1)

# Petit
sp1point = Point(12,10)
sp1 = Petit(pv_max=300, attaque=100, port_attaque=3, port_deplacement=6, cout=800,
            valeur_mort=int(800*0.6), taille=(2,2), peut_miner=False, peut_transporter=False,
            image=img_petit, tier=1, cordonner=sp1point, id=next_uid, path=img_petit_dir)
next_uid += 1
ships.append(sp1)

# Foreuse
sf1point = Point(16,16)
sf1 = Foreuse(pv_max=500, attaque=0, port_attaque=0, port_deplacement=3, cout=800,
              valeur_mort=int(800*0.6), taille=(2,2), peut_miner=True, peut_transporter=False,
              image=img_foreuse, tier=1, cordonner=sf1point, id=next_uid, path=img_foreuse_dir)
next_uid += 1
ships.append(sf1)

smm1point = Point(0,0)
smm1 = MotherShip(pv_max=500,attaque=0,port_attaque=0, port_deplacement=0, cout=800, valeur_mort=int(800*0.6),
                  taille=(4,5), tier=1, cordonner=smm1point, id=next_uid,path=img_base_dir)
next_uid += 1
ships.append(smm1)

# --- Placer vaisseaux sur le plateau ---
for s in ships:
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
            if selection_ship and not interface_transport_active:
                selection_ship.deplacement(case_souris, NOMBRE_COLONNES, NOMBRE_LIGNES, plateau, ships, TAILLE_CASE)
                selection_ship = None
                selection_cargo = None
            else:
                # Sélectionner un vaisseau
                for ship in ships[:]:
                    largeur, hauteur = ship.donner_dimensions(ship.direction)
                    if (ship.cordonner.x <= case_souris[0] < ship.cordonner.x + hauteur and
                        ship.cordonner.y <= case_souris[1] < ship.cordonner.y + largeur):
                        selection_ship = ship
                        selection_ship.aperçu_direction = ship.direction
                        selection_ship.aperçu_cordonner.x = ship.cordonner.x
                        selection_ship.aperçu_cordonner.y = ship.cordonner.y
                        break

        # --- Clic droit = transport / embarquement / débarquement ---
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3 and selection_ship:
            if isinstance(selection_ship, Transport):
                clicked_on_mini = False
                for i, ship in enumerate(selection_ship.cargaison):
                    if ship is None:
                        continue
                    rect = pygame.Rect(selection_ship.cordonner.y * TAILLE_CASE + i*22,
                                       selection_ship.cordonner.x * TAILLE_CASE - 22, 20, 20)
                    if rect.collidepoint(position_souris):
                        selection_cargo = ship
                        interface_transport_active = True
                        clicked_on_mini = True
                        break
                if not clicked_on_mini and interface_transport_active and selection_cargo:
                    positions_valides = selection_ship.positions_debarquement(
                        selection_cargo, plateau, NOMBRE_LIGNES, NOMBRE_COLONNES)
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
                    if (target.cordonner.x <= case_souris[0] < target.cordonner.x + hauteur and
                        target.cordonner.y <= case_souris[1] < target.cordonner.y + largeur):
                        if isinstance(target, Transport):
                            success = target.ajouter_cargo(selection_ship)
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
    # --- Mettre à jour et dessiner les vaisseaux ---
    for ship in ships[:]:
        if ship.est_mort():
            # Libère les cases du plateau
            ship.occuper_plateau(plateau, 0)

            # Supprime l’animation du vaisseau
            ship.animator.remove_from_list()  # retirer de Animator global

            # Retirer le vaisseau de la liste
            ships.remove(ship)
            print(f"{ship.__class__.__name__} détruit")
            continue  # passe au suivant

        # Dessin normal du vaisseau vivant
        ship.animator.update_and_draw()


    # --- Affichage cargaison transport ---
    if selection_ship and isinstance(selection_ship, Transport):
        selection_ship.afficher_cargaison(fenetre, TAILLE_CASE)

    # --- Preview déplacement / débarquement ---
    if selection_ship:
        if interface_transport_active and selection_cargo:
            positions_possibles = selection_ship.positions_debarquement(
                selection_cargo, plateau, NOMBRE_LIGNES, NOMBRE_COLONNES)
            for ligne, colonne in positions_possibles:
                pygame.draw.rect(fenetre, (255,255,0), (colonne*TAILLE_CASE, ligne*TAILLE_CASE, TAILLE_CASE, TAILLE_CASE), 3)
            if case_souris in positions_possibles:
                largeur, hauteur = selection_cargo.donner_dimensions(selection_cargo.direction)
                surf = pygame.transform.scale(selection_cargo.image, (largeur*TAILLE_CASE, hauteur*TAILLE_CASE))
                surf.set_alpha(150)
                fenetre.blit(surf, (case_souris[1]*TAILLE_CASE, case_souris[0]*TAILLE_CASE))
        else:
            positions_possibles = selection_ship.positions_possibles_adjacentes(
                NOMBRE_COLONNES, NOMBRE_LIGNES, plateau, direction=selection_ship.aperçu_direction)
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

    ShipAnimator.update_all()
    ProjectileAnimator.update_all()
    pygame.display.flip()

pygame.quit()
