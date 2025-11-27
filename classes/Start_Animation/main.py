import pygame
import random
import math
from PIL import Image
from classes.Animator import Animator
from classes.Start_Animation.StarField import StarField
from classes.Start_Animation.PlanetManager import PlanetManager
from classes.ShipAnimator import ShipAnimator
from classes.PlanetAnimator import PlanetAnimator
from classes.MotherShip import MotherShip
from classes.Point import Point
from blazyck import *
from classes.Achievements import AchievementManager 
from classes.GlobalVar.ScreenVar import ScreenVar
from classes.GlobalVar.GridVar import GridVar

def create_space_background():
    """
    Initialise le fond spatial avec des étoiles et des planètes.
    Retourne : les étoiles, le gestionnaire de planètes, B1 (vaisseau centré)
    """
    screen_width, screen_height = ScreenVar.screen.get_size()
    scale = ScreenVar.scale
    

    # --- Gestion des étoiles ---
    stars = StarField(
        screen_width,
        screen_height,
        num_stars=int(200 * ScreenVar.scale),
        min_radius=1,
        max_radius=3,
        size_distribution="small-biased",
        move_amplitude=0,
        move_horizontal=1
    )

    # --- Gestionnaire de planètes ---
    planet_manager = PlanetManager(
        speed_range=(1, int(2 * scale)),
        planet_size_range=(1, int(5 * scale)),
        prob_increment=1
    )

    # --- Vaisseau centré avec taille personnalisée ---
    center_x = (ScreenVar.screen.get_width() // GridVar.cell_size) / 2
    center_y = (ScreenVar.screen.get_height() // GridVar.cell_size) / 2

    vaisseau_w = int(4 * 4 * scale)  # largeur en cases
    vaisseau_h = int(5 * 4 * scale)  # hauteur en cases

    # le vaisseau est tourne vers la gauche
    x = center_x - (vaisseau_h) / 2
    y = center_y - (vaisseau_w) / 2

    B1 = MotherShip(
        tier=1,
        cordonner=Point(y, x),
        id=999,
        path="assets/img/ships/base",
        show_health=False,
        joueur=0,
        taille=(vaisseau_w, vaisseau_h)  # Taille personnalisée pour le menu
    )

    B1.animator.set_angle(90)
    B1.animator.play("base")
    B1.animator.play("engine")

    return stars, planet_manager, B1

if __name__ == "__main__":
    pygame.init()
    info = pygame.display.Info()
    screen_width = info.current_w
    screen_height = info.current_h
    ScreenVar(pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE))
    GridVar()
    screen = ScreenVar.screen
    clock = pygame.time.Clock()

    # Création du fond spatial et du vaisseau
    stars, planet_manager, B1 = create_space_background(num_stars=100)

    # --- Initialisation succès ---
    achievements = AchievementManager()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.VIDEORESIZE:
                ScreenVar.update_scale()
                GridVar.update_grid()

        stars.update()
        screen.fill((0, 0, 0))
        stars.draw(screen)
        planet_manager.update_and_draw()
        Animator.update_all()
        PlanetAnimator.update_all()
        ShipAnimator.update_all()
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
