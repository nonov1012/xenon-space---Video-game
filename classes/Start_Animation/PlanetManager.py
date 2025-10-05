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
        """
        Initialisation du gestionnaire de planètes.

        :param speed_range: Tuple[float, float] - Intervalle de vitesse pour les planètes
        :param planet_size_range: Tuple[int, int] - Intervalle de taille pour les planètes
        :param prob_increment: int - Incrément de probabilité par frame
        """
        # Chemin vers le dossier contenant les spritesheets des planètes
        self.path = PLANETES_PATH
        # Intervalle de vitesse pour les planètes
        self.speed_range = speed_range
        # Intervalle de taille pour les planètes
        self.planet_size_range = planet_size_range
        # Liste des planètes actives
        self.planets = []
        # Noms des planètes possibles
        self.planet_names = ["planet1", "planet2", "planet3", "planet4"]

        # Probabilité de spawn actuelle
        self.spawn_prob = 0
        # Incrément de probabilité par frame
        self.prob_increment = prob_increment

    def spawn_planet(self):
        """
        Crée dynamiquement une planète avec des paramètres aléatoires.

        :return: None
        """
        min_size, max_size = self.planet_size_range
        # Taille aléatoire de la planète
        w = random.randint(int(min_size), int(max_size))
        h = w

        # Nom de la planète aléatoire
        name = random.choice(self.planet_names)
        # Coordonnées aléatoires de la planète
        x = random.randint(-w * 3, -w * 2)
        y = random.randint(0, (Animator.screen.get_height() - 50))
        y = y / TAILLE_CASE
        # Vitesse aléatoire de la planète
        speed = random.randint(self.speed_range[0], self.speed_range[1])

        # Crée de la planète
        planet = PlanetAnimator((w, h), (x, y), default_fps=(15*speed/2), speed=speed)
        # Joue l'animation de la planète
        planet.play(name, True)
        # Centre de la planète
        centre = planet.get_center()
        # Fixe la cible de la planète
        planet.set_target((Animator.screen.get_width() + planet.pixel_w * 10, centre[1]), True, "right")

        # Réinitialiser la probabilité après spawn
        self.spawn_prob = 1

    def update_and_draw(self):
        """
        Mettre à jour et dessine les planètes.

        Vérifie si la probabilité de spawn est à 0, si oui, crée une nouvelle planète.
        Incrémente la probabilité de spawn.
        Génère une planète si le tirage est réussi.
        Met à jour les planètes existantes.
        """
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
