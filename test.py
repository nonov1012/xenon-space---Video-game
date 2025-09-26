import pygame
from classes.Ship import Transport, Foreuse, Petit, Moyen, Lourd
from classes.MotherShip import MotherShip
from classes.Animator import *
from classes.ShipAnimator import ShipAnimator
from classes.ProjectileAnimator import ProjectileAnimator
from classes.Point import Point, Type
from classes.Map import Map
from blazyck import *
from classes.PlanetAnimator import PlanetAnimator

def set_prevision_for_ship(ship, case, direction):
    largeur, hauteur = ship.donner_dimensions(direction)
    ship.prevision.pixel_w = largeur * TAILLE_CASE
    ship.prevision.pixel_h = hauteur * TAILLE_CASE
    ship.prevision.x = case[1] * TAILLE_CASE + OFFSET_X
    ship.prevision.y = case[0] * TAILLE_CASE

    if direction == "haut":
        ship.prevision.target_angle = 0
    elif direction == "droite":
        ship.prevision.target_angle = -90
    elif direction == "gauche":
        ship.prevision.target_angle = 90
    elif direction == "bas":
        ship.prevision.target_angle = 180

# --- Paramètres ---
pygame.init()
fenetre = pygame.display.set_mode((NB_CASE_X * TAILLE_CASE + OFFSET_X, NB_CASE_Y * TAILLE_CASE))
pygame.display.set_caption("Xenon Space - Déplacement/Attaque")

# Définir l'écran pour Animator
Animator.set_screen(fenetre)

# --- Création de la carte ---
game_map = Map()
# Ajouter quelques planètes et astéroïdes
game_map.generer_planet(3)
game_map.generer_asteroides(10)

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

# Fonction pour trouver une position libre
def trouver_position_libre(grille, taille_vaisseau):
    for y in range(len(grille) - taille_vaisseau[1] + 1):
        for x in range(len(grille[0]) - taille_vaisseau[0] + 1):
            libre = True
            for dy in range(taille_vaisseau[1]):
                for dx in range(taille_vaisseau[0]):
                    if grille[y + dy][x + dx].type not in (Type.VIDE, Type.ATMOSPHERE):
                        libre = False
                        break
                if not libre:
                    break
            if libre:
                return Point(y, x)
    return Point(5, 5)  # position par défaut si rien trouvé

# Lourd 1
sl1point = Point(5, 6)
sl1 = Lourd(pv_max=500, attaque=300, port_attaque=6, port_deplacement=3, cout=800,
            valeur_mort=int(800*0.6), taille=(3,3), peut_miner=False, peut_transporter=False,
            image=img_Lourd, tier=4, cordonner=sl1point, id=next_uid, path=img_lourd_dir)
next_uid += 1
ships.append(sl1)

# Lourd 2 
sl2point = Point(9, 2)
if sl2point.x == sl1point.x and sl2point.y == sl1point.y:
    sl2point = Point(sl1point.x + 5, sl1point.y + 5)
sl2 = Lourd(pv_max=500, attaque=300, port_attaque=6, port_deplacement=3, cout=800,
            valeur_mort=int(800*0.6), taille=(3,3), peut_miner=False, peut_transporter=False,
            image=img_Lourd, tier=4, cordonner=sl2point, id=next_uid, path=img_lourd_dir)
next_uid += 1
ships.append(sl2)

# Moyen
sm1point = Point(10, 13)
sm1 = Moyen(pv_max=900, attaque=250, port_attaque=5, port_deplacement=5, cout=800,
            valeur_mort=int(800*0.6), taille=(2,2), peut_miner=False, peut_transporter=False,
            image=img_moyen, tier=1, cordonner=sm1point, id=next_uid, path=img_moyen_dir)
next_uid += 1
ships.append(sm1)

# Transport
st1point = Point(20, 18)
st1 = Transport(pv_max=1200, attaque=150, port_attaque=4, port_deplacement=8, cout=800,
                valeur_mort=int(800*0.6), taille=(3,4), peut_miner=False, peut_transporter=True,
                image=img_transport, tier=1, cordonner=st1point, id=next_uid, path=img_transport_dir)
next_uid += 1
ships.append(st1)

# Petit
sp1point = Point(4, 40)
sp1 = Petit(pv_max=300, attaque=100, port_attaque=3, port_deplacement=6, cout=800,
            valeur_mort=int(800*0.6), taille=(2,2), peut_miner=False, peut_transporter=False,
            image=img_petit, tier=1, cordonner=sp1point, id=next_uid, path=img_petit_dir)
next_uid += 1
ships.append(sp1)

# Foreuse
sf1point = Point(25, 29)
sf1 = Foreuse(pv_max=500, attaque=0, port_attaque=0, port_deplacement=3, cout=800,
              valeur_mort=int(800*0.6), taille=(2,2), peut_miner=True, peut_transporter=False,
              image=img_foreuse, tier=1, cordonner=sf1point, id=next_uid, path=img_foreuse_dir)
next_uid += 1
ships.append(sf1)

# MotherShip dans une zone de base
smm1point = Point(0, 0)
smm1 = MotherShip(pv_max=500, attaque=0, port_attaque=0, port_deplacement=0, cout=800, 
                  valeur_mort=int(800*0.6), taille=(4,5), tier=1, cordonner=smm1point, 
                  id=next_uid, path=img_base_dir)
next_uid += 1
ships.append(smm1)

# --- Placer vaisseaux sur la grille ---
for s in ships:
    s.occuper_plateau(game_map.grille, Type.VAISSEAU)

# --- Variables de sélection ---
selection_ship = None
selection_cargo = None
interface_transport_active = False
clock = pygame.time.Clock()
fonctionne = True
afficher_grille = True
afficher_zones = False

# Couleurs pour l'affichage des zones
colors = {
    Type.VIDE: (0, 0, 0, 0),                     # transparent
    Type.PLANETE: (255, 215, 0, 128),            # or
    Type.ATMOSPHERE: (0, 200, 255, 128),         # bleu clair
    Type.ASTEROIDE: (139, 69, 19, 128),          # marron
    Type.BASE: (100, 100, 125, 128),             # gris foncé
    Type.VAISSEAU: (255, 0, 0, 128),             # rouge
}

# --- Boucle principale ---
while fonctionne:
    clock.tick(60)
    position_souris = pygame.mouse.get_pos()
    case_souris = ((position_souris[1]) // TAILLE_CASE, (position_souris[0] - OFFSET_X) // TAILLE_CASE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            fonctionne = False

        # --- Touches pour affichage ---
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LCTRL:
                afficher_grille = not afficher_grille
            elif event.key == pygame.K_LSHIFT:
                afficher_zones = not afficher_zones

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if selection_ship and not interface_transport_active:
                # Vérifier si on clique sur la case d'origine du vaisseau sélectionné (coin haut-gauche)
                if (case_souris[0] == selection_ship.cordonner.x and 
                    case_souris[1] == selection_ship.cordonner.y):
                    # Désélectionner le vaisseau
                    selection_ship = None
                    selection_cargo = None
                else:
                    # Tenter un déplacement/attaque
                    success = selection_ship.deplacement(case_souris, game_map.grille, ships)
                    if success:
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
                        selection_ship.aperçu_cordonner._x = ship.cordonner.x
                        selection_ship.aperçu_cordonner._y = ship.cordonner.y
                        break

        # --- Clic droit = transport / embarquement / débarquement ---
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3 and selection_ship:
            if isinstance(selection_ship, Transport):
                clicked_on_mini = False
                for i, ship in enumerate(selection_ship.cargaison):
                    if ship is None:
                        continue
                    rect = pygame.Rect(selection_ship.cordonner.y * TAILLE_CASE + OFFSET_X + i*22,
                                       selection_ship.cordonner.x * TAILLE_CASE - 22, 20, 20)
                    if rect.collidepoint(position_souris):
                        selection_cargo = ship
                        interface_transport_active = True
                        clicked_on_mini = True
                        break
                
                if not clicked_on_mini and interface_transport_active and selection_cargo:
                    positions_valides = selection_ship.positions_debarquement(selection_cargo, game_map.grille)
                    if case_souris in positions_valides:
                        index = selection_ship.cargaison.index(selection_cargo)
                        success = selection_ship.retirer_cargo(index, case_souris[0], case_souris[1], 
                                                             game_map.grille, ships)
                        if success:
                            selection_cargo = None
                            interface_transport_active = False
            else:
                # Embarquer dans un transport
                for target in ships:
                    if target == selection_ship: 
                        continue
                    largeur, hauteur = target.donner_dimensions(target.direction)
                    if (target.cordonner.x <= case_souris[0] < target.cordonner.x + hauteur and
                        target.cordonner.y <= case_souris[1] < target.cordonner.y + largeur):
                        if isinstance(target, Transport):
                            success = target.ajouter_cargo(selection_ship)
                            if success:
                                selection_ship.liberer_position(game_map.grille)
                                ships.remove(selection_ship)
                                selection_ship = None
                                selection_cargo = None
                                interface_transport_active = False
                        break

        # --- Rotation avec R ---
        if event.type == pygame.KEYDOWN and selection_ship:
            if event.key == pygame.K_r:
                selection_ship.rotation_aperçu_si_possible(case_souris, game_map.grille)

    # --- Dessin du fond ---
    fenetre.fill((10, 10, 20))  # Fond spatial sombre

    # --- Dessin de la carte ---
    game_map.generer_grille(fenetre, afficher_zones, afficher_grille, colors)

    # --- Dessiner les astéroïdes ---
    for (ax, ay), img in game_map.asteroide_img_map.items():
        fenetre.blit(img, (ax * TAILLE_CASE + OFFSET_X, ay * TAILLE_CASE))

    # --- Mettre à jour et dessiner les vaisseaux ---
    for ship in ships[:]:
        if ship.est_mort():
            # Libère les cases de la grille en restaurant le terrain approprié (cases atmosphère)
            ship.liberer_position(game_map.grille)
            # Retirer le vaisseau de la liste
            ships.remove(ship)
            print(f"{ship.__class__.__name__} détruit")
            continue

        # Dessin normal du vaisseau vivant
        ship.animator.update_and_draw()

    # --- Affichage cargaison transport ---
    if selection_ship and isinstance(selection_ship, Transport):
        selection_ship.afficher_cargaison(fenetre)

    # --- Preview déplacement / débarquement ---
    if selection_ship:
        if interface_transport_active and selection_cargo:
            # Cases possibles pour débarquer
            positions_possibles = selection_ship.positions_debarquement(selection_cargo, game_map.grille)
            for ligne, colonne in positions_possibles:
                # Jaune pour le débarquement
                pygame.draw.rect(fenetre, (255, 255, 0),
                                (colonne * TAILLE_CASE + OFFSET_X, ligne * TAILLE_CASE, 
                                 TAILLE_CASE, TAILLE_CASE), 3)

            # Afficher préview du cargo seulement si la souris est sur une case valide
            if case_souris in positions_possibles:
                selection_cargo.prevision.alpha = 120
                set_prevision_for_ship(selection_cargo, case_souris, selection_cargo.direction)
                selection_cargo.prevision.update_and_draw()

        else:
            # Cases possibles pour déplacement
            positions_possibles = selection_ship.positions_possibles_adjacentes(
                game_map.grille, direction=selection_ship.aperçu_direction
            )
            for ligne, colonne in positions_possibles:
                # Vert clair pour les déplacements possibles
                pygame.draw.rect(fenetre, (0, 255, 0),
                                (colonne * TAILLE_CASE + OFFSET_X, ligne * TAILLE_CASE, 
                                 TAILLE_CASE, TAILLE_CASE), 3)

            # Afficher préview seulement si souris est sur une case valide
            if case_souris in positions_possibles:
                selection_ship.prevision.alpha = 120
                set_prevision_for_ship(selection_ship, case_souris, selection_ship.aperçu_direction)
                selection_ship.prevision.update_and_draw()

    # --- Preview attaque ---
    if selection_ship and not interface_transport_active:
        positions_attaque = selection_ship.positions_possibles_attaque(
            game_map.grille, direction=selection_ship.aperçu_direction
        )
        for ligne, colonne in positions_attaque:
            # Rouge vif pour les attaques
            pygame.draw.rect(fenetre, (255, 50, 50), 
                            (colonne * TAILLE_CASE + OFFSET_X, ligne * TAILLE_CASE, 
                             TAILLE_CASE, TAILLE_CASE), 2)
            
            # Si c'est un astéroïde et qu'on peut miner, afficher en orange
            if (0 <= ligne < len(game_map.grille) and 0 <= colonne < len(game_map.grille[0]) and
                game_map.grille[ligne][colonne].type == Type.ASTEROIDE and selection_ship.peut_miner):
                pygame.draw.rect(fenetre, (255, 165, 0), 
                                (colonne * TAILLE_CASE + OFFSET_X, ligne * TAILLE_CASE, 
                                 TAILLE_CASE, TAILLE_CASE), 2)

    # --- Mise à jour des animations ---
    Animator.update_all()
    PlanetAnimator.update_all()
    ShipAnimator.update_all()
    ProjectileAnimator.update_all()

    # --- Affichage des informations ---
    if selection_ship:
        font = pygame.font.Font(None, 24)
        info_text = f"{selection_ship.__class__.__name__} - PV: {selection_ship.pv_actuel}/{selection_ship.pv_max}"
        text_surface = font.render(info_text, True, (255, 255, 255))
        fenetre.blit(text_surface, (10, 10))

    pygame.display.flip()

pygame.quit()