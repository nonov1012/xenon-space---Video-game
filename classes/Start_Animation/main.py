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

def create_space_background(num_stars=100, screen_ratio=1.0):
    """
    Initialise le fond spatial avec des étoiles et des planètes.
    Retourne : les étoiles, le gestionnaire de planètes, B1 (vaisseau centré)
    """
    screen_width, screen_height = Animator.screen.get_size()

    # --- Gestion des étoiles ---
    stars = StarField(
        screen_width,            # largeur de l'écran
        screen_height,           # hauteur de l'écran
        num_stars=num_stars,     # nombre d'étoiles
        min_radius=1,            # rayon minimum des étoiles
        max_radius=3,            # rayon maximum des étoiles
        size_distribution="small-biased",  # distribution aléatoire des tailles
        move_amplitude=0,          # amplitude de mouvement des étoiles
        move_horizontal=1           # mouvement horizontal des étoiles
    )

    # --- Gestionnaire de planètes ---
    planet_manager = PlanetManager(
        speed_range=(1, int(2 * screen_ratio)),  # vitesse aléatoire des planètes
        planet_size_range=(1, int(5 * screen_ratio)),  # taille aléatoire des planètes
        prob_increment=1           # probabilité d'ajout d'une planète
    )

    # --- Vaisseau centré ---
    center_x = (screen_width / TAILLE_CASE) / 2
    center_y = (screen_height / TAILLE_CASE) / 2
    vaisseau_w = 4 * screen_ratio  # largeur du vaisseau
    vaisseau_h = 5 * screen_ratio  # hauteur du vaisseau
    x = int(center_x - vaisseau_w / 1.30)  # position x du vaisseau
    y = int(center_y - vaisseau_h / 2.30)  # position y du vaisseau

    B1 = MotherShip(
        pv_max=5000,          # Points de vie max
        attaque=0,            # Pas d'attaque pour le vaisseau du menu
        port_attaque=0,       # Portée d'attaque
        port_deplacement=0,   # Portée de déplacement (immobile)
        cout=0,               # Coût
        taille=(vaisseau_w, vaisseau_h),  # Taille en tuples
        tier=1,               # Niveau
        cordonner=Point(y, x),  # Position
        id=999,               # ID unique pour le menu
        path="assets/img/ships/base",  # Chemin des assets
        show_health=False
    )


    B1.animator.set_angle(90)  # angle de rotation du vaisseau
    B1.animator.play("base")  # animation du vaisseau
    B1.animator.play("engine")  # animation du vaisseau

    return stars, planet_manager, B1

if __name__ == "__main__":
    pygame.init()
    info = pygame.display.Info()
    screen_width = info.current_w
    screen_height = info.current_h
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()

    Animator.set_screen(screen)

    screen_ratio = (screen_width * 100 / 600) / 100

    # Création du fond spatial et du vaisseau
    stars, planet_manager, B1 = create_space_background(num_stars=100, screen_ratio=screen_ratio)

    # --- Initialisation succès ---
    achievements = AchievementManager()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            if event.type == pygame.QUIT:
                running = False

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

    print("Succès obtenus :", achievements.list_unlocked())
