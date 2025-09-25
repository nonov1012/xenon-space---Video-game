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

def start_game(ecran, parametres, random_active):
    clock = pygame.time.Clock()
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
    COLORS = {
        Type.VIDE: (0, 0, 0, 0),                     # noir
        Type.PLANETE: (255, 215, 0, 128),            # or
        Type.ATMOSPHERE: (0, 200, 255, 128),         # bleu clair
        Type.ASTEROIDE: (255, 215, 0, 128),          # or
        Type.BASE: (100, 100, 125, 128),             # gris foncé
    }
    
    # Status discord
    discord = DiscordRP(RPC_ID)
    discord.connect()
    

    # Calcul du décalage vertical
    grid_width = NB_CASE_X * TAILLE_CASE
    offset_x = (screen_width - grid_width) // 2

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

        ecran.fill((0, 0, 0, 0))
        
        stars.update()
        stars.draw(ecran)
        
        # Vérifie si LSHIFT est enfoncé
        keys = pygame.key.get_pressed()
        afficher_zones = keys[pygame.K_LSHIFT]

        map_obj.generer_grille(ecran, offset_x, afficher_zones ,afficher_grille)

        Animator.update_all()
        PlanetAnimator.update_all()
        ShipAnimator.update_all()

        # Dessin des images (planètes + astéroïdes)
        for (ax, ay), img in map_obj.asteroide_img_map.items():
            ecran.blit(img, (ax * TAILLE_CASE + offset_x, ay * TAILLE_CASE))
        
        
        
        
        clock.tick(60)
        pygame.display.flip()

    pygame.quit()
