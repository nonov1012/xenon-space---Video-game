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


def start_game(ecran, parametres, random_active):
    print("test")
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
        min_distance=15,
        size_distribution="small-biased",
        move_amplitude=3
    )    
    
    map_obj = Map()
    print(parametres["Nombre de planetes"]["valeur"])
    map_obj.generer_planet(parametres["Nombre de planetes"]["valeur"])
    map_obj.generer_asteroides(parametres["Nombre d'asteroides"]["valeur"])
    
    # couleurs
    COLORS = {
        Type.VIDE: (0, 0, 0, 10),               # noir
        Type.PLANETE: (0, 150, 255),            # bleu clair
        Type.ATMOSPHERE: (0, 255, 150, 125),    # vert clair
        Type.ASTEROIDE: (200, 200, 200),        # gris
        Type.BASE: (100, 100, 100),             # gris foncé
    }

    # Calcul du décalage vertical
    grid_width = NB_CASE_X * TAILLE_CASE
    offset_x = (screen_width - grid_width) // 2

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        ecran.fill((0, 0, 0))
        stars.update()
        stars.draw(ecran)

        # Dessin de la grille centrée verticalement
        for y in range(map_obj.nb_cases_y):
            for x in range(map_obj.nb_cases_x):
                point = map_obj.grille[y][x]
                rect = pygame.Rect(
                    x * TAILLE_CASE + offset_x,
                    y * TAILLE_CASE,
                    TAILLE_CASE,
                    TAILLE_CASE
                )
                if point.type != Type.VIDE:
                    pygame.draw.rect(ecran, COLORS[point.type], rect)  # fond
                pygame.draw.rect(ecran, (40, 40, 40), rect, 1)  # contour

        # Dessin des images (planètes + astéroïdes)
        for (px, py), img in map_obj.planete_img_map.items():
            ecran.blit(img, (px * TAILLE_CASE + offset_x, py * TAILLE_CASE))

        for (ax, ay), img in map_obj.asteroide_img_map.items():
            ecran.blit(img, (ax * TAILLE_CASE + offset_x, ay * TAILLE_CASE))

        pygame.display.flip()

    pygame.quit()
