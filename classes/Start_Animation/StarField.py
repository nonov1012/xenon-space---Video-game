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
        """
        Initialisation du champ d'étoiles.

        :param width: Largeur du champ en pixels
        :param height: Hauteur du champ en pixels
        :param num_stars: Nombre d'étoiles générées
        :param min_radius: Rayon minimum des étoiles
        :param max_radius: Rayon maximum des étoiles
        :param colors: Couleurs possibles pour les étoiles
        :param size_distribution: Distribution des tailles des étoiles
        :param move_amplitude: Amplitude du mouvement vertical global
        :param move_horizontal: Vitesse du mouvement horizontal global
        """
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

            # Distribution des tailles des étoiles
            if size_distribution == "uniform":
                r = random.randint(min_radius, max_radius)
            elif size_distribution == "small-biased":
                r = int(random.random()**2 * (max_radius - min_radius) + min_radius)
            elif size_distribution == "large-biased":
                r = int((1 - random.random()**2) * (max_radius - min_radius) + min_radius)
            else:
                r = random.randint(min_radius, max_radius)

            # Couleur et décalage pour scintillement individuel
            color = random.choice(self.colors)
            phase = random.uniform(0, 2*math.pi)

            self.stars.append({
                "x": x,
                "y": y,
                "r": r,
                "base_color": color,
                "phase": phase  # pour scintillement individuel
            })

    def update(self):
        """
        Met à jour l'angle global du mouvement vertical et
        les positions des étoiles.
        """
        self.angle += 0.05  # vitesse du mouvement vertical global

        for star in self.stars:
            # Déplacement horizontal fluide avec rebouclage
            # On ajoute la vitesse de mouvement horizontal global
            # à la position actuelle de l'étoile et on prend le modulo
            # de la largeur de l'écran pour reboucler lorsque l'étoile sort de l'écran
            star["x"] = (star["x"] + self.move_horizontal) % self.width

    def draw(self, surface):
        """
        Dessine les étoiles sur la surface passée en paramètre.

        :param surface: La surface sur laquelle dessiner les étoiles
        """
        for star in self.stars:
            r, g, b = star["base_color"]
            # Le scintillement est un effet qui fait varier la luminosité de l'étoile
            # en fonction du temps, créant un effet de clignotement
            brightness = 200 + 55 * math.sin(self.angle + star["phase"])
            factor = brightness / 255
            color = (int(r * factor), int(g * factor), int(b * factor))

            # Le mouvement vertical est un mouvement oscillant qui fait varier la position verticale de l'étoile
            # en fonction du temps, créant un effet de mouvement fluide
            y = star["y"] + math.sin(self.angle + star["phase"]) * self.move_amplitude

            # Dessin de l'étoile sur la surface
            pygame.draw.circle(surface, color, (int(star["x"]), int(y)), star["r"])
