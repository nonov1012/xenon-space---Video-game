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
