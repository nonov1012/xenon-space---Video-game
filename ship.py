# Programme créé par Dupuis Brian
# Ce programme contient la classe Ship

import pygame
import numpy as np

# La classe Ship permet la création des vaisseaux et gère toutes les mécaniques associées
class Ship:
    def __init__(self, PV_max: int, att: int, distance_att: int, distance_dep: int,
                 cout: int, money_dead: int, taille, minage: bool, transport: bool, 
                 img: pygame.image, tiers: int):
        

        self.PV_max = PV_max              # Points de vie maximum du vaisseau
        self.PV_actuelle = PV_max         # Points de vie actuels du vaisseau
        self.att = att                    # Dégâts du vaisseau
        self.distance_att = distance_att  # Portée d'attaque du vaisseau
        self.distance_dep = distance_dep  # Distance de déplacement du vaisseau
        self.cout = cout                  # Coût de construction du vaisseau
        self.money_dead = money_dead      # L'argent rapporté à l'adversaire en cas de destruction
        self.taille = taille              # Taille du vaisseau sur la carte
        self.minage = minage              # Peut-il miner ?
        self.transport = transport        # Peut-il transporter d'autres vaisseaux ?
        stockage = np.array([None, None, None], dtype=Ship)
        self.stockage = stockage              # Contenu du vaisseau (si applicable)
        self.img = img                    # Image du vaisseau
        self.tiers = tiers                # Niveau requis pour le construire

    def move(self):  # Méthode qui gère le déplacement
        pass

    def attack(self):  # Méthode qui gère l'attaque
        pass

    def draw(self):  # ?
        pass

    def take_damage(self):  # Méthode qui gère la prise de dégâts
        pass

    def dead(self):  # Méthode qui gère la destruction du vaisseau
        pass


# Exemple de création de vaisseaux
#img = pygame.image.load("test.png")

#petit = Ship(200, 75, 3, 3, 325, (325 * 0.6), 1, False, False, img, 1)       # Vaisseau petit
#moyen = Ship(400, 175, 4, 4, 650, (650 * 0.6), 1, False, False, img, 1)      # Vaisseau moyen
#foreuse = Ship(300, 0, 0, 3, 400, (400 * 0.6), 1, True, False, img, 2)       # Foreuse
#transporteur = Ship(600, 60, 6, 6, 500, (500 * 0.6), 2, False, True, img, 3) # Transporteur
#grand = Ship(750, 300, 6, 6, 1050, (1050 * 0.6), 2, False, False, img, 4)    # Grand vaisseau


