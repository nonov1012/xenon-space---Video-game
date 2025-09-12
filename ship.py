# programme crée par Dupuis Brian
# Ce programme continent la class ship,

import pygame

# class ship permet la création des vaisseaux et gére toute les choses en rapport avec les mécanique du vaisseau
class Ship:
    def __init__(self, PV_max: int, att :int, distance_att : int, distance_dep : int, cout : int , money_dead : int, taille, minage : bool, transport : bool, img : pygame.image, tiers : int):
        self.PV_max = PV_max    # PV max du vaisseau
        self.PV_actuelle = PV_max   # PV actuelle du Vaisseau
        self.att = att  # dégâts du vaisseau
        self.distance_att = distance_att    # distance d'attaque du vaisseau
        self.distance_dep = distance_dep    # distance de deplacement du vaisseau
        self.cout = cout    # cout du vaisseau
        self.money_dead = money_dead    # l'argent que rapporte ce navire a l'adversaire
        self.taille = taille    # taille du vaisseau sur la carte
        self.minage = minage    # peut t'il miner ? 
        self.transport = transport  # peut-il transporte d'autre vaisseau
        self.stockage = None    # ce qu'il contient
        self.img = img          # continent le lien de l'image du vaisseau
        self.tiers = tiers      # le tier de la base requie pour le crée

    """def ma_methode(self):
        # Exemple de méthode
        print("Méthode appelée")

    def __str__(self):
        return f"MaClasse(param1={self.param1}, param2={self.param2})"""

img = pygame.image.load("img.png")
petit = Ship(200, 75, 3, 3, 325, (325*0.6), 1, False, False, img, 1)    #expemple de creation d'un vaisseau petit
moyen = Ship(400, 175, 4, 4, 650, (650*0.6), 1, False, False, img, 1)   #expemple de creation d'un vaisseau moyen
foreuse = Ship(300, 0, 0, 3, 400, (400*0.6), 1, False, False, img, 2)   #expemple de creation d'une foreuse
transporteur = Ship(600, 60, 6, 6, 500, (500*0.6), 2, False, False, img, 3) #expemple de creation d'un transporteur
grand = Ship(750, 300, 6, 6, 1050, (1050*0.6), 2, False, False, img, 4) #expemple de creation d'un vaisseau grand



