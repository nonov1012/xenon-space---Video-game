import pygame
import random
from classes.Animator import Animator
from blazyck import *

class PlanetManager:
    """
    Gère dynamiquement les planètes avec probabilité croissante.
    """
    def __init__(self, screen, path, speed_range=(1, 3),
                 planet_size_range=(20, 20), prob_increment=1):
        self.screen = screen
        self.path = path
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
        x = random.randint(-w * TAILLE_CASE * 2, -w * TAILLE_CASE * 1)
        y = random.randint(50, Animator.screen.get_height() - 50)
        speed = random.uniform(*self.speed_range)

        planet = Animator(self.path, (w, h), (x, y), default_fps=5)
        planet.play(name, True)
        self.planets.append({"animator": planet, "speed": speed})

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
        for planet_dict in self.planets[:]:
            planet = planet_dict["animator"]
            speed = planet_dict["speed"]

            # Déplacer
            planet.x += speed

            # Supprimer si hors écran
            if planet.x > self.screen.get_width():
                self.planets.remove(planet_dict)
            else:
                planet.update_and_draw()
