# il faut rendre les variables et méthode plus lisible, commenter, metttre en français, description du document
# bug on ne peut pas encore faire tournée dans toute les direction


# ship.py
import pygame
import numpy as np

class Ship:
    def __init__(self, PV_max: int, attaque: int, porter_attaque: int, porter_distance: int,
                 cout: int, valeur_mort: int, taille: tuple, miner: bool, transport: bool,
                 image: pygame.image, tier: int, ligne=0, colonne=0):
        """
        Initialise un vaisseau avec ses caractéristiques.
        :param PV_max: PV maximum du vaisseau
        :param attaque: puissance d'attaque
        :param porter_attaque: distance d'attaque
        :param porter_distance: distance maximale de déplacement
        :param cout: coût du vaisseau
        :param valeur_mort: argent réchautéré à la destruction
        :param taille: taille en cases (largeur, hauteur)
        :param miner: True si le vaisseau peut miner
        :param transport: True si le vaisseau peut transporter
        :param image: image pygame du vaisseau
        :param tier: niveau/tiers du vaisseau
        :param ligne: position de départ en ligne
        :param colonne: position de départ en colonne
        """
        self.PV_max = PV_max
        self.PV_actuelle = PV_max
        self.attaque = attaque
        self.porter_attaque = porter_attaque
        self.porter_distance = porter_distance
        self.cout = cout
        self.valeur_mort = valeur_mort
        self.taille = taille  # (largeur, hauteur) en cases
        self.miner = miner
        self.transport = transport
        self.cargo = np.array([None, None, None], dtype=Ship)
        self.image = image
        self.tier = tier

        self.ligne = ligne
        self.colonne = colonne
        self.direction = "bas"
        self.aperçu_direction = self.direction

    # -------------------- Méthodes principales -------------------- #

    def donne_dimension(self, direction):
        """Retourne (largeur, hauteur) selon la direction"""
        if direction in ("haut", "bas"):
            return self.taille
        else:  # "gauche" ou "droite"
            return (self.taille[1], self.taille[0])

    def dessin(self, surface, taille_case):
        """Dessine le vaisseau sur la surface pygame"""
        largeur, hauteur = self.donne_dimension(self.direction)
        x = self.colonne * taille_case
        y = self.ligne * taille_case
        w = largeur * taille_case
        h = hauteur * taille_case

        if self.direction == "bas":
            img_pygame = self.image
        elif self.direction == "haut":
            img_pygame = pygame.transform.rotate(self.image, 180)
        elif self.direction == "gauche":
            img_pygame = pygame.transform.rotate(self.image, 90)
        elif self.direction == "droite":
            img_pygame = pygame.transform.rotate(self.image, -90)

        img_pygame = pygame.transform.scale(img_pygame, (w, h))
        surface.blit(img_pygame, (x, y))

    def attack(self, ship2):
        """Réduit les PV du vaisseau"""
        ship2.subis_degat(self.attaque)

    def subis_degat(self, degat):
        """Réduit les PV du vaisseau"""
        self.PV_actuelle -= degat

    def dead(self):
        """Vaisseau détruit (pas fini)"""
        return self.PV_actuelle <= 0

    # -------------------- Déplacement -------------------- #

    def position_possible_adjacent(self, nombre_colonne, nombre_lignes):
        """Cases adjacentes autour de la tête du vaisseau"""
        largeur, hauteur = self.donne_dimension(self.direction)
        tete_ligne, tete_colonne = self.ligne, self.colonne
        if self.direction == "droite":
            tete_colonne += largeur - 1
        positions = []
        for d_ligne, d_colonne in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nouvelle_ligne, nouvelle_colonne = tete_ligne + d_ligne, tete_colonne + d_colonne
            if 0 <= nouvelle_ligne < nombre_lignes and 0 <= nouvelle_colonne < nombre_colonne:
                positions.append((nouvelle_ligne, nouvelle_colonne))
        return positions

    def verification_dedans(self, ligne, colonne, direction, nombre_colonne, nombre_lignes):
        """Retourne True si le vaisseau reste dans le plateau
        (petit bug à corriger il se peut que sur la preview 
        il sort du tableau mais il ne valide pas le deplacement)"""

        largeur, hauteur = self.donne_dimension(direction)
        return 0 <= ligne <= nombre_lignes - hauteur and 0 <= colonne <= nombre_colonne - largeur

    def donne_position_possible(self, nombre_colonne, nombre_lignes):
        """Retourne les positions possibles pour le déplacement"""
        return self.position_possible_adjacent(nombre_colonne, nombre_lignes)

    def deplacement(self, case_cible, nombre_colonne, nombre_lignes):
        """Déplace le vaisseau vers case_cible si possible
        (ne prend pas encore en compte la distance de déplacement max)"""
        ligne, colonne = case_cible
        if (ligne, colonne) in self.donne_position_possible(nombre_colonne, nombre_lignes) and \
           self.verification_dedans(ligne, colonne, self.aperçu_direction, nombre_colonne, nombre_lignes):
            self.ligne = ligne
            self.colonne = colonne
            self.direction = self.aperçu_direction
            return True
        return False

    # -------------------- Rotation -------------------- #

    def rotation_aperçu(self, nombre_colonne, nombre_lignes, case_souris):
        """Tourne la prévisualisation si possible
        (petit bug on ne peut tourner que vers le haut ou vers la droite)"""
        directions = ["haut", "droite", "bas", "gauche"]
        idx = directions.index(self.aperçu_direction)
        nouvelle_direction = directions[(idx + 1) % 4]
        ligne, colonne = case_souris

        if self.verification_dedans(ligne, colonne, nouvelle_direction, nombre_colonne, nombre_lignes):
            self.aperçu_direction = nouvelle_direction

    def rotation_aperçu_si_possible(self, case_souris, nombre_colonne, nombre_lignes):
        self.rotation_aperçu(nombre_colonne, nombre_lignes, case_souris)
