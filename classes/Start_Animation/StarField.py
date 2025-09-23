import pygame
import random
import math
from classes.Animator import Animator
from blazyck import *

class StarField:
    """
    Champ d'étoiles scintillantes avec mouvement vertical et horizontal fluide.
    """
    def __init__(self, width, height, num_stars=200, min_radius=1, max_radius=4,
                 colors=None, size_distribution="uniform",
                 move_amplitude=2, move_horizontal=0):
        self.width = width
        self.height = height
        self.move_amplitude = move_amplitude
        self.move_horizontal = move_horizontal
        self.stars = []
        self.colors = colors or [(255, 255, 255), (200, 200, 255), (255, 255, 180)]
        self.min_radius = min_radius
        self.max_radius = max_radius
        self.size_distribution = size_distribution
        self.angle = 0  # angle global pour mouvement vertical et scintillement

        # Génération des étoiles
        for _ in range(num_stars):
            x = random.uniform(0, width)
            y = random.uniform(0, height)

            if size_distribution == "uniform":
                r = random.randint(min_radius, max_radius)
            elif size_distribution == "small-biased":
                r = int(random.random()**2 * (max_radius - min_radius) + min_radius)
            elif size_distribution == "large-biased":
                r = int((1 - random.random()**2) * (max_radius - min_radius) + min_radius)
            else:
                r = random.randint(min_radius, max_radius)

            color = random.choice(self.colors)
            phase = random.uniform(0, 2*math.pi)  # décalage pour scintillement

            self.stars.append({
                "x": x,
                "y": y,
                "r": r,
                "base_color": color,
                "phase": phase  # pour scintillement individuel
            })

    def update(self):
        self.angle += 0.05  # vitesse du mouvement vertical global

        for star in self.stars:
            # Déplacement horizontal fluide avec rebouclage
            star["x"] = (star["x"] + self.move_horizontal) % self.width

    def draw(self, surface):
        for star in self.stars:
            r, g, b = star["base_color"]
            # Scintillement sinusoïdal fluide
            brightness = 200 + 55 * math.sin(self.angle + star["phase"])
            factor = brightness / 255
            color = (int(r * factor), int(g * factor), int(b * factor))

            # Mouvement vertical oscillant
            y = star["y"] + math.sin(self.angle + star["phase"]) * self.move_amplitude

            pygame.draw.circle(surface, color, (int(star["x"]), int(y)), star["r"])
