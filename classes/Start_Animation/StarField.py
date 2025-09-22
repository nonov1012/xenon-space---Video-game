import pygame
import random
import math
from classes.Animator import Animator
from blazyck import *


class StarField:
    """
    Champ d'étoiles scintillantes avec mouvement vertical synchronisé.
    """
    def __init__(self, width, height, num_stars=200, min_radius=1, max_radius=4,
                 min_distance=10, colors=None, size_distribution="uniform", move_amplitude=2):
        self.width = width
        self.height = height
        self.move_amplitude = move_amplitude
        self.stars = []
        self.colors = colors or [(255, 255, 255), (200, 200, 255), (255, 255, 180)]
        self.min_radius = min_radius
        self.max_radius = max_radius
        self.size_distribution = size_distribution
        self.angle = 0  # angle global pour mouvement vertical synchronisé

        attempts = 0
        while len(self.stars) < num_stars and attempts < num_stars * 20:
            x = random.randint(0, width-1)
            y = random.randint(0, height-1)

            if size_distribution == "uniform":
                r = random.randint(min_radius, max_radius)
            elif size_distribution == "small-biased":
                r = int(random.random()**2 * (max_radius - min_radius) + min_radius)
            elif size_distribution == "large-biased":
                r = int((1 - random.random()**2) * (max_radius - min_radius) + min_radius)
            else:
                r = random.randint(min_radius, max_radius)

            color = random.choice(self.colors)
            brightness = random.randint(150, 255)
            speed = random.uniform(0.5, 2.0)

            # Vérifier distance minimale
            too_close = False
            for star in self.stars:
                dist = math.hypot(star["x"] - x, star["base_y"] - y)
                if dist < min_distance:
                    too_close = True
                    break

            if not too_close:
                self.stars.append({
                    "x": x,
                    "base_y": y,
                    "r": r,
                    "base_color": color,
                    "brightness": brightness,
                    "delta": random.choice([-1, 1]),
                    "speed": speed
                })
            attempts += 1

    def update(self):
        # Mettre à jour le scintillement
        for star in self.stars:
            change = star["delta"] * random.uniform(1, 5) * star["speed"]
            star["brightness"] += change
            if star["brightness"] > 255:
                star["brightness"] = 255
                star["delta"] = -1
            elif star["brightness"] < 150:
                star["brightness"] = 150
                star["delta"] = 1

        # Avancer l'angle global pour mouvement vertical synchronisé
        self.angle += 0.05  # vitesse du mouvement

    def draw(self, surface):
        for star in self.stars:
            r, g, b = star["base_color"]
            factor = star["brightness"] / 255
            color = (int(r * factor), int(g * factor), int(b * factor))
            # Ajouter sinus pour mouvement vertical synchronisé
            y = star["base_y"] + math.sin(self.angle) * self.move_amplitude
            pygame.draw.circle(surface, color, (int(star["x"]), int(y)), star["r"])