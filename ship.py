# Programme créé par Dupuis Brian
# Ce programme contient la classe Ship


# La classe Ship permet la création des vaisseaux et gère toutes les mécaniques associées
import pygame
import numpy as np

class Ship:
    def __init__(self, PV_max: int, att: int, distance_att: int, distance_dep: int,
                 cout: int, money_dead: int, taille, minage: bool, transport: bool,
                 img: pygame.image, tiers: int, ligne=0, col=0):

        self.PV_max = PV_max
        self.PV_actuelle = PV_max
        self.att = att
        self.distance_att = distance_att
        self.distance_dep = distance_dep
        self.cout = cout
        self.money_dead = money_dead
        self.taille = taille  # (largeur, hauteur) en cases (par défaut vers le bas)
        self.minage = minage
        self.transport = transport
        self.stockage = np.array([None, None, None], dtype=object)
        self.img = img
        self.tiers = tiers

        # Position de la tête du vaisseau
        self.ligne = ligne
        self.col = col

        # Orientation
        self.direction = "bas"
        self.preview_direction = self.direction

    def move(self, type_case):  # Méthode qui gère le déplacement
        pass

    def attack(self, ship_defendu):  # Méthode qui gère l'attaque
        ship_defendu.take_damage(self.att)

    def draw(self, map):  # ?
        pass


    def take_damage(self, ship_attaquant):  # Méthode qui gère la prise de dégâts
        self.PV_actuelle = self.PV_actuelle - ship_attaquant

    def dead(self):  # Méthode qui gère la destruction du vaisseau
        pass

    def get_dimensions(self, direction):
        """Retourne (largeur, hauteur) en cases selon la direction"""
        if direction in ("haut", "bas"):
            return self.taille
        else:  # gauche/droite
            return (self.taille[1], self.taille[0])

    def draw(self, surface, taille_case):
        """Dessine le vaisseau orienté"""
        largeur, hauteur = self.get_dimensions(self.direction)
        x = self.col * taille_case
        y = self.ligne * taille_case
        w = largeur * taille_case
        h = hauteur * taille_case

        # Choix de la rotation d’image
        if self.direction == "bas":
            img_rot = self.img
        elif self.direction == "haut":
            img_rot = pygame.transform.rotate(self.img, 180)
        elif self.direction == "gauche":
            img_rot = pygame.transform.rotate(self.img, 90)
        elif self.direction == "droite":
            img_rot = pygame.transform.rotate(self.img, -90)

        img_rot = pygame.transform.scale(img_rot, (w, h))
        surface.blit(img_rot, (x, y))

    def positions_possibles(self, nb_colonnes, nb_lignes):
        """Cases adjacentes autour de la tête du vaisseau"""
        largeur, hauteur = self.get_dimensions(self.direction)

        # Tête toujours en haut du vaisseau
        if self.direction == "haut":
            l_tete, c_tete = self.ligne, self.col
        elif self.direction == "bas":
            l_tete, c_tete = self.ligne, self.col
        elif self.direction == "gauche":
            l_tete, c_tete = self.ligne, self.col
        elif self.direction == "droite":
            l_tete, c_tete = self.ligne, self.col + largeur - 1

        positions = []
        for d_l, d_c in [(0, 1), (0, -1), (1, 0), (-1, 0)]:  # droite, gauche, bas, haut
            nl, nc = l_tete + d_l, c_tete + d_c
            if 0 <= nl < nb_lignes and 0 <= nc < nb_colonnes:
                positions.append((nl, nc))

        return positions
    
    def est_dans_plateau(self, ligne, col, direction, nb_colonnes, nb_lignes):
        """Retourne True si tout le vaisseau reste dans le plateau"""
        largeur, hauteur = self.get_dimensions(direction)
        return 0 <= ligne <= nb_lignes - hauteur and 0 <= col <= nb_colonnes - largeur


    def rotate_preview(self, nb_colonnes, nb_lignes, mouse_case):
        """Tourne la preview en respectant les limites du plateau"""
        directions = ["haut", "droite", "bas", "gauche"]
        idx = directions.index(self.preview_direction)
        new_dir = directions[(idx + 1) % 4]

        l, c = mouse_case

        # Vérifie si tout le vaisseau reste dans le plateau
        if self.est_dans_plateau(l, c, new_dir, nb_colonnes, nb_lignes):
            self.preview_direction = new_dir



# Exemple de création de vaisseaux
img = pygame.image.load("test.png")

petit = Ship(200, 75, 3, 3, 325, (325 * 0.6), 1, False, False, img, 1)       # Vaisseau petit
moyen = Ship(400, 175, 4, 4, 650, (650 * 0.6), 2, False, False, img, 1)      # Vaisseau moyen
foreuse = Ship(300, 0, 0, 3, 400, (400 * 0.6), 1, True, False, img, 2)       # Foreuse
#transporteur = Ship(600, 60, 6, 6, 500, (500 * 0.6), 2, False, True, img, 3) # Transporteur
#grand = Ship(750, 300, 6, 6, 1050, (1050 * 0.6), 2, False, False, img, 4)    # Grand vaisseau

