#################################################################
#  __   __ __                      _____                        #
#  \ \ / //_/                     / ____|                       #
#   \ V / ___ _ __   ___  _ __   | (___  _ __   __ _  ___ ___   #
#    > < / _ \ '_ \ / _ \| '_ \   \___ \| '_ \ / _` |/ __/ _ \  #
#   / . \  __/ | | | (_) | | | |  ____) | |_) | (_| | (_|  __/  #
#  /_/ \_\___|_| |_|\___/|_| |_| |_____/| .__/ \__,_|\___\___|  #
#                                       | |                     #
#                                       |_|                     #
#################################################################
# Développé par :                                               #
# - nonov1012                                                   #
# - 
# - 
# - 
# - 
# -
#################################################################
# Copyright (c) 2025                                            #
# Tous droits réservés. Merci de ne pas reproduire              #
# ou modifier le code sans autorisation.                        #
#################################################################

# Import lib
import pygame

# Import classes
import menu.menuPrincipal
from classes.Map import Map
from classes.Start_Animation.StarField import StarField
from classes.Point import Type, Point
from blazyck import *
from classes.Discord import DiscordRP
from classes.Animator import Animator
from classes.PlanetAnimator import PlanetAnimator
from classes.ShipAnimator import ShipAnimator
from classes.Shop import Shop
from classes.Player import Player
from classes.MotherShip import MotherShip
from classes.ProjectileAnimator import ProjectileAnimator
from classes.Economie import Economie
from classes.Ship import Transport, Foreuse, Petit, Moyen, Lourd

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

def start_game(ecran, parametres, random_active):
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 30)
    
    new_cursor = pygame.image.load('assets/img/menu/cursor.png')
    new_cursor = pygame.transform.scale(new_cursor, (40, 40))
    pygame.mouse.set_visible(False)
    
    # Générer la map
    screen_width, screen_height = ecran.get_size()
    num_stars=100
    screen_ratio=1.0
    stars = StarField(
        screen_width,
        screen_height,
        num_stars=int(num_stars * screen_ratio),
        min_radius=1,
        max_radius=3,
        move_amplitude=0
    )
    
    map_obj = Map()
    map_obj.generer_planet(parametres["Nombre de planetes"]["valeur"])
    map_obj.generer_asteroides(parametres["Nombre d'asteroides"]["valeur"])
    
    # couleurs pour l'affichage des zones
    colors = {
        Type.VIDE: (0, 0, 0, 0),
        Type.PLANETE: (255, 215, 0, 128),
        Type.ATMOSPHERE: (0, 200, 255, 128),
        Type.ASTEROIDE: (255, 215, 0, 128),
        Type.BASE: (100, 100, 125, 128),
        Type.VAISSEAU: (255, 0, 0, 128),
    }
    
    # Status discord
    discord = DiscordRP(RPC_ID)
    discord.connect()
    
    player = Player("TestPlayer", solde_initial=3000)
    shop = Shop(player, font, ecran)

    # ===== Ship =====
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

    # MotherShip du joueur (zone de base)
    smm1 = MotherShip(pv_max=5000, attaque=11, port_attaque=10, port_deplacement=0, cout=0,
                      valeur_mort=0, taille=(4,5), tier=1, cordonner=Point(0,0), 
                      id=next_uid, path=img_base_dir)
    next_uid += 1
    ships.append(smm1)

    # Vaisseaux de départ du joueur (dans la zone de base)
    # Petit vaisseau de reconnaissance
    sp1 = Petit(pv_max=300, attaque=1000, port_attaque=3, port_deplacement=6, cout=200,
                valeur_mort=int(200*0.6), taille=(2,2), peut_miner=False, peut_transporter=False,
                image=img_petit, tier=1, cordonner=Point(5,1), id=next_uid, path=img_petit_dir)
    next_uid += 1
    ships.append(sp1)

    # Foreuse de départ
    sf1 = Foreuse(pv_max=500, attaque=0, port_attaque=0, port_deplacement=3, cout=500,
                  valeur_mort=int(500*0.6), taille=(2,2), peut_miner=True, peut_transporter=False,
                  image=img_foreuse, tier=1, cordonner=Point(1,5), id=next_uid, path=img_foreuse_dir)
    next_uid += 1
    ships.append(sf1)

    # --- Placer vaisseaux sur la grille ---
    for s in ships:
        s.occuper_plateau(map_obj.grille, Type.VAISSEAU)

    # --- Variables de sélection et contrôle ---
    selection_ship = None
    selection_cargo = None
    interface_transport_active = False
    afficher_grille = False
    running = True

    while running:
        discord.update("En jeu")
        position_souris = pygame.mouse.get_pos()
        case_souris = ((position_souris[1]) // TAILLE_CASE, 
                       (position_souris[0] - OFFSET_X) // TAILLE_CASE)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            # --- Touches clavier ---
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    # menuPause = menu.PauseMenu(ecran, sm)
                    # menuPause.run()
                elif event.key == pygame.K_LCTRL:
                    afficher_grille = not afficher_grille
                elif event.key == pygame.K_LSHIFT:
                    afficher_zones = True
                # Rotation avec R
                elif event.key == pygame.K_r and selection_ship:
                    selection_ship.rotation_aperçu_si_possible(case_souris, map_obj.grille)
                    
            # --- Clic gauche = sélection/déplacement/attaque ---
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Gérer le shop d'abord
                shop.handle_click(event.pos)
                
                # Gestion des vaisseaux
                if selection_ship and not interface_transport_active:
                    # Vérifier si on clique sur la case d'origine (désélection)
                    if (case_souris[0] == selection_ship.cordonner.x and 
                        case_souris[1] == selection_ship.cordonner.y):
                        selection_ship = None
                        selection_cargo = None
                    else:
                        # Tenter un déplacement/attaque
                        success = selection_ship.deplacement(case_souris, map_obj.grille, ships)
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
            
            # --- Clic droit = transport/embarquement/débarquement ---
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
                        positions_valides = selection_ship.positions_debarquement(selection_cargo, map_obj.grille)
                        if case_souris in positions_valides:
                            index = selection_ship.cargaison.index(selection_cargo)
                            success = selection_ship.retirer_cargo(index, case_souris[0], case_souris[1], 
                                                                 map_obj.grille, ships)
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
                                    selection_ship.liberer_position(map_obj.grille)
                                    ships.remove(selection_ship)
                                    selection_ship = None
                                    selection_cargo = None
                                    interface_transport_active = False
                            break

        # --- Dessin ---
        ecran.fill((0, 0, 0, 0))
        
        stars.update()
        stars.draw(ecran)
        
        # Vérifier si LSHIFT est enfoncé
        keys = pygame.key.get_pressed()
        afficher_zones = keys[pygame.K_LSHIFT]

        # Dessiner la grille
        map_obj.generer_grille(ecran, afficher_zones, afficher_grille, colors)

        # Dessiner les astéroïdes
        for (ax, ay), img in map_obj.asteroide_img_map.items():
            ecran.blit(img, (ax * TAILLE_CASE + OFFSET_X, ay * TAILLE_CASE))

        # Mettre à jour et dessiner les vaisseaux
        for ship in ships[:]:
            if ship.est_mort():
                ship.liberer_position(map_obj.grille)
                ships.remove(ship)
                player.economie.ajouter(ship.valeur_mort)  # Récompense pour destruction
                continue
            
            ship.animator.update_and_draw()

        # Affichage cargaison transport
        if selection_ship and isinstance(selection_ship, Transport):
            selection_ship.afficher_cargaison(ecran)

        # Preview déplacement / débarquement
        if selection_ship:
            if interface_transport_active and selection_cargo:
                # Cases possibles pour débarquer
                positions_possibles = selection_ship.positions_debarquement(selection_cargo, map_obj.grille)
                for ligne, colonne in positions_possibles:
                    pygame.draw.rect(ecran, (255, 255, 0),
                                    (colonne * TAILLE_CASE + OFFSET_X, ligne * TAILLE_CASE, 
                                     TAILLE_CASE, TAILLE_CASE), 3)

                # Afficher preview du cargo si souris sur case valide
                if case_souris in positions_possibles:
                    selection_cargo.prevision.alpha = 120
                    set_prevision_for_ship(selection_cargo, case_souris, selection_cargo.direction)
                    selection_cargo.prevision.update_and_draw()
            else:
                # Cases possibles pour déplacement
                positions_possibles = selection_ship.positions_possibles_adjacentes(
                    map_obj.grille, direction=selection_ship.aperçu_direction
                )
                for ligne, colonne in positions_possibles:
                    pygame.draw.rect(ecran, (0, 255, 0),
                                    (colonne * TAILLE_CASE + OFFSET_X, ligne * TAILLE_CASE, 
                                     TAILLE_CASE, TAILLE_CASE), 3)

                # Preview si souris sur case valide
                if case_souris in positions_possibles:
                    selection_ship.prevision.alpha = 120
                    set_prevision_for_ship(selection_ship, case_souris, selection_ship.aperçu_direction)
                    selection_ship.prevision.update_and_draw()

        # Preview attaque
        if selection_ship and not interface_transport_active:
            positions_attaque = selection_ship.positions_possibles_attaque(
                map_obj.grille, direction=selection_ship.aperçu_direction
            )
            for ligne, colonne in positions_attaque:
                pygame.draw.rect(ecran, (255, 50, 50), 
                                (colonne * TAILLE_CASE + OFFSET_X, ligne * TAILLE_CASE, 
                                 TAILLE_CASE, TAILLE_CASE), 2)
                
                # Si astéroïde minable, afficher en orange
                if (0 <= ligne < len(map_obj.grille) and 0 <= colonne < len(map_obj.grille[0]) and
                    map_obj.grille[ligne][colonne].type == Type.ASTEROIDE and selection_ship.peut_miner):
                    pygame.draw.rect(ecran, (255, 165, 0), 
                                    (colonne * TAILLE_CASE + OFFSET_X, ligne * TAILLE_CASE, 
                                     TAILLE_CASE, TAILLE_CASE), 2)

        # Mise à jour des animations
        Animator.update_all()
        PlanetAnimator.update_all()
        ShipAnimator.update_all()
        ProjectileAnimator.update_all()

        # Affichage des informations
        if selection_ship:
            info_text = f"{selection_ship.__class__.__name__} - PV: {selection_ship.pv_actuel}/{selection_ship.pv_max}"
            text_surface = font.render(info_text, True, (255, 255, 255))
            ecran.blit(text_surface, (10, 40))
        
        # Afficher les coins
        coins_text = font.render(f"Coins: {player.economie.solde}", True, (255, 255, 0))
        ecran.blit(coins_text, (10, 10))

        # Dessiner la boutique
        shop.draw()
        
        # Curseur
        ecran.blit(new_cursor, position_souris)
        
        clock.tick(60)
        pygame.display.flip()

    pygame.quit()