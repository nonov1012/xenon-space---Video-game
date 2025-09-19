import pygame
import random
import math
from PIL import Image
from classes.Animator import Animator
from classes.Start_Animation.StarField import StarField
from classes.Start_Animation.PlanetManager import PlanetManager
from classes.MotherShip import MotherShip
from classes.Point import Point
from blazyck import *

def create_space_background(screen: pygame.Surface, planete_path: str, num_stars=100, screen_ratio=1.0):
    """
    Initialise le fond spatial avec étoiles et planètes.
    Retourne : stars, planet_manager, B1 (vaisseau centré)
    """
    screen_width, screen_height = screen.get_size()

    # --- Étoiles ---
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

    # --- Gestionnaire de planètes ---
    planet_manager = PlanetManager(
        screen,
        planete_path,
        speed_range=(1, 2 * screen_ratio),
        planet_size_range=(4, int(5 * screen_ratio)),
        prob_increment=1
    )

    # --- Vaisseau centré ---
    center_x = screen_width // 2
    center_y = screen_height // 2
    vaisseau_w = 4 * TAILLE_CASE * screen_ratio
    vaisseau_h = 5 * TAILLE_CASE * screen_ratio
    x = int(center_x - vaisseau_w / 2)
    y = int(center_y - vaisseau_h / 2)

    B1 = MotherShip(
        screen,
        Point(x, y),
        tier=1,
        show_health=False,
        largeur=4 * screen_ratio,
        hauteur=5 * screen_ratio
    )
    B1.animator.set_angle(90)
    B1.animator.play("base")
    B1.animator.play("engine")

    return stars, planet_manager, B1

pygame.init()
info = pygame.display.Info()
screen_width = info.current_w
screen_height = info.current_h
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

screen_ratio = (screen_width * 100 / 600) / 100

# Création du fond spatial et du vaisseau
stars, planet_manager, B1 = create_space_background(screen, PLANETES_PATH, num_stars=100, screen_ratio=screen_ratio)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))
    stars.update()
    stars.draw(screen)
    planet_manager.update_and_draw()
    B1.animator.update_and_draw()
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
