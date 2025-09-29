import pygame
import random
from classes.Animator import Animator
from classes.PlanetAnimator import PlanetAnimator
from blazyck import *

class PlanetManager:
    """
    Gère dynamiquement les planètes avec probabilité croissante.
    """
    def __init__(self, speed_range=(1, 3),
                 planet_size_range=(20, 20), prob_increment=1):
        self.path = PLANETES_PATH
        self.speed_range = speed_range
        self.planet_size_range = planet_size_range
        self.planets = []
        self.planet_names = ["planet1", "planet2", "planet3", "planet4"]

        self.spawn_prob = 0
        # Incrément de probabilité par frame
        self.prob_increment = prob_increment

    def spawn_planet(self):
        min_size, max_size = self.planet_size_range
        w = random.randint(int(min_size), int(max_size))
        h = w

        name = random.choice(self.planet_names)
        x = random.randint(-w * 3, -w * 2)
        y = random.randint(0, (Animator.screen.get_height() - 50))
        y = y / TAILLE_CASE
        speed = random.randint(self.speed_range[0], self.speed_range[1])

        planet = PlanetAnimator((w, h), (x, y), default_fps=(15*speed/2), speed=speed)
        planet.play(name, True)
        centre = planet.get_center()
        planet.set_target((Animator.screen.get_width() + planet.pixel_w * 10, centre[1]), True, "right")

        # Réinitialiser la probabilité après spawn
        self.spawn_prob = 1

    def update_and_draw(self):
        if self.spawn_prob == 0:
            self.spawn_planet()

        # --- Incrémenter la probabilité ---
        self.spawn_prob += self.prob_increment

        # --- Générer une planète si tirage réussi ---
        res = random.randrange(0, self.spawn_prob)
        if res > 300:
            self.spawn_planet()

        # --- Mettre à jour les planètes existantes ---
        for planet in PlanetAnimator.liste_animation:
            # Supprimer si hors écran
            if planet.x > Animator.screen.get_width() + planet.pixel_w + 100:
                planet.remove_from_list()
