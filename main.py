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
    ship.prevision.x = case[1] * TAILLE_CASE
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
    
    # del menu.menuPrincipal.planet_manager
    # del menu.menuPrincipal.B1
    
    map_obj = Map()
    print(parametres["Nombre de planetes"]["valeur"])
    map_obj.generer_planet(parametres["Nombre de planetes"]["valeur"])
    map_obj.generer_asteroides(parametres["Nombre d'asteroides"]["valeur"])
    
    # couleurs
    colors = {
        Type.VIDE: (0, 0, 0, 0),                     # noir
        Type.PLANETE: (255, 215, 0, 128),            # or
        Type.ATMOSPHERE: (0, 200, 255, 128),         # bleu clair
        Type.ASTEROIDE: (255, 215, 0, 128),          # or
        Type.BASE: (100, 100, 125, 128),             # gris foncé
    }
    
    # Status discord
    discord = DiscordRP(RPC_ID)
    discord.connect()
    

    player = Player("TestPlayer", solde_initial=3000)
    shop = Shop(player, font, ecran)

    # MotherShip
    B1 = MotherShip(Point(0 , 0), tier=1, show_health=True, largeur=4, hauteur=5)
    B1.animator.play("base")
    B1.animator.update_and_draw()
    B1.animator.play("engine")
    B2 = MotherShip(Point(46 , 25), tier=1, show_health=True, largeur=4, hauteur=5)
    B2.animator.play("base")
    B2.animator.update_and_draw()
    B2.animator.play("engine")
    
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

    # Lourd 1
    sl1point = Point(8, 8)
    sl1 = Lourd(pv_max=500, attaque=300, port_attaque=6, port_deplacement=3, cout=800,
                valeur_mort=int(800*0.6), taille=(3,3), peut_miner=False, peut_transporter=False,
                image=img_Lourd, tier=4, cordonner=sl1point, id=next_uid, path=img_lourd_dir)
    next_uid += 1
    print(sl1.animator.x)
    print(TAILLE_CASE)
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
    

    afficher_grille = False
    running = True
    while running:
        discord.update("En jeu")
        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
                menuPause = menu.PauseMenu(ecran, sm)
                menuPause.run()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_LCTRL:
                afficher_grille = not afficher_grille
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                shop.handle_click(event.pos)

        ecran.fill((0, 0, 0, 0))
        
        stars.update()
        stars.draw(ecran)
        
        # Vérifie si LSHIFT est enfoncé
        keys = pygame.key.get_pressed()
        afficher_zones = keys[pygame.K_LSHIFT]

        map_obj.generer_grille(ecran, afficher_zones ,afficher_grille, colors)

        Animator.update_all()
        PlanetAnimator.update_all()
        ShipAnimator.update_all()

        # Dessin des images (planètes + astéroïdes)
        for (ax, ay), img in map_obj.asteroide_img_map.items():
            ecran.blit(img, (ax * TAILLE_CASE + OFFSET_X, ay * TAILLE_CASE))
        
        
        coins_text = font.render(f"Coins: {player.economie.solde}", True, (255, 255, 0))
        ecran.blit(coins_text, (10, 10))

        # Dessiner la boutique
        shop.draw()
        
        
        souris = pygame.mouse.get_pos()
        ecran.blit(new_cursor, souris)
        
        clock.tick(60)
        pygame.display.flip()

    pygame.quit()
