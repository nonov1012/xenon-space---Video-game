"""
Ship_class.py
------------------
Classe Ship (version francisée, commentée).

But :
    - Représente un Ship sur une grille (placement, rotation, attaque, etc.).
    - Fournit un mécanisme d'aperçu (preview) séparé de la position réelle,
      et une rotation cyclique : haut -> gauche -> bas -> droite -> ...
    - La rotation d'aperçu est réalisée *autour du centre* de l'aperçu pour
      minimiser les débordements lors du changement d'orientation.

Note :
    - bug sur la rotation parfois le cul et la tête s'inverse
    - bug l'aperçu montre toujours l'image vers le haut
"""

import pygame
import numpy as np
from typing import Tuple, List

class Ship:
    def __init__(self,
                 pv_max: int,
                 attaque: int,
                 port_attaque: int,
                 port_deplacement: int,
                 cout: int,
                 valeur_mort: int,
                 taille: Tuple[int, int],
                 peut_miner: bool,
                 peut_transporter: bool,
                 image: pygame.Surface,
                 tier: int,
                 ligne: int = 0,
                 colonne: int = 0):
        
        """
        Initialise le vaisseau et ses états.

        :param pv_max: points de vie max
        :param attaque: puissance d'attaque
        :param port_attaque: portée d'attaque (Manhattan)
        :param port_deplacement: portée de déplacement (Manhattan)
        :param cout: coût
        :param valeur_mort: ce que rapporte la destruction
        :param taille: (largeur, hauteur) en cases à l'orientation par défaut
        :param peut_miner: bool
        :param peut_transporter: bool
        :param image: pygame.Surface représentant le sprite (orienté "bas" par défaut)
        :param tier: niveau / tier
        :param ligne, colonne: position initiale (coin supérieur gauche)
        """
        # caractéristiques
        self.pv_max = pv_max
        self.pv_actuel = pv_max
        self.attaque = attaque
        self.port_attaque = port_attaque
        self.port_deplacement = port_deplacement
        self.cout = cout
        self.valeur_mort = valeur_mort
        self.taille = tuple(taille)  # (largeur, hauteur)
        self.peut_miner = peut_miner
        self.peut_transporter = peut_transporter
        self.cargaison = np.array([None, None, None], dtype=object)

        # graphisme / niveau
        self.image = image
        self.tier = tier

        # position réelle (coin sup-gauche) et direction réelle
        self.ligne = ligne
        self.colonne = colonne
        self.direction = "bas"  # haut -> gauche -> bas -> droite

        # aperçu (preview) — peut différer de la position réelle jusqu'à validation
        self.aperçu_direction = self.direction
        self.aperçu_ligne = ligne
        self.aperçu_colonne = colonne

    # ------------ utilitaires ------------
    def donner_dimensions(self, direction: str) -> Tuple[int,int]:
        """Retourne (largeur, hauteur) selon l'orientation."""
        if direction in ("haut", "bas"):
            return self.taille
        return (self.taille[1], self.taille[0])


    def _centre_depuis_coin(self, ligne_coin: int, colonne_coin: int, direction: str) -> Tuple[float, float]:
        largeur, hauteur = self.donner_dimensions(direction)
        centre_ligne = ligne_coin + (hauteur - 1) / 2.0
        centre_colonne = colonne_coin + (largeur - 1) / 2.0
        return centre_ligne, centre_colonne

    def _coin_depuis_centre(self, centre_ligne: float, centre_colonne: float, direction: str) -> Tuple[int,int]:
        largeur, hauteur = self.donner_dimensions(direction)
        nouvelle_ligne = int(round(centre_ligne - (hauteur - 1) / 2.0))
        nouvelle_colonne = int(round(centre_colonne - (largeur - 1) / 2.0))
        return nouvelle_ligne, nouvelle_colonne

    # ------------ dessin ------------
    def dessiner(self, surface: pygame.Surface, taille_case: int, preview: bool = False):
        """Dessine le vaisseau (ou son aperçu si preview=True)."""
        if preview:
            ligne = self.aperçu_ligne
            colonne = self.aperçu_colonne
            direction = self.aperçu_direction
        else:
            ligne = self.ligne
            colonne = self.colonne
            direction = self.direction

        largeur, hauteur = self.donner_dimensions(direction)
        x = colonne * taille_case
        y = ligne * taille_case
        w = largeur * taille_case
        h = hauteur * taille_case

        if direction == "bas":
            img = self.image
        elif direction == "haut":
            img = pygame.transform.rotate(self.image, 180)
        elif direction == "gauche":
            img = pygame.transform.rotate(self.image, 90)
        else:  # droite
            img = pygame.transform.rotate(self.image, -90)

        img = pygame.transform.scale(img, (w, h))
        surface.blit(img, (x, y))

    # ------------ combat ------------
    def attaquer(self, cible: "Ship"):
        cible.subir_degats(self.attaque)

    def subir_degats(self, degats: int):
        self.pv_actuel -= degats

    # alias ancien nom
    subis_degat = subir_degats

    def est_mort(self) -> bool:
        return self.pv_actuel <= 0

    # ------------ déplacement ------------
    def positions_possibles_adjacentes(self, nombre_colonne: int, nombre_lignes: int) -> List[Tuple[int,int]]:
        """Positions (coin) atteignables par la portée de déplacement (Manhattan)."""
        largeur, hauteur = self.donner_dimensions(self.direction)
        coin_ligne, coin_col = self.ligne, self.colonne

        positions = []
        for dl in range(-self.port_deplacement, self.port_deplacement + 1):
            for dc in range(-self.port_deplacement, self.port_deplacement + 1):
                if dl == 0 and dc == 0:
                    continue
                if abs(dl) + abs(dc) <= self.port_deplacement:
                    nl = coin_ligne + dl
                    nc = coin_col + dc
                    if 0 <= nl <= nombre_lignes - hauteur and 0 <= nc <= nombre_colonne - largeur:
                        positions.append((nl, nc))
        return positions

    # alias compatibilité
    position_possible_adjacent = positions_possibles_adjacentes

    def verification_dedans(self, ligne_coin: int, colonne_coin: int, direction: str,
                           nombre_colonne: int, nombre_lignes: int) -> bool:
        largeur, hauteur = self.donner_dimensions(direction)
        return 0 <= ligne_coin <= nombre_lignes - hauteur and 0 <= colonne_coin <= nombre_colonne - largeur

    def deplacement(self, case_cible, nombre_colonne, nombre_lignes):
        """Déplace le vaisseau vers case_cible si possible"""
        ligne, colonne = case_cible
        largeur, hauteur = self.donner_dimensions(self.aperçu_direction)

        # Ajustement comme dans la preview
        if self.aperçu_direction == "haut":
            ligne -= hauteur - 1
        elif self.aperçu_direction == "gauche":
            colonne -= largeur - 1

        if (case_cible in self.position_possible_adjacent(nombre_colonne, nombre_lignes) and
            self.verification_dedans(ligne, colonne, self.aperçu_direction, nombre_colonne, nombre_lignes)):
            self.ligne = ligne
            self.colonne = colonne
            self.direction = self.aperçu_direction
            return True
        return False


    # ------------ rotation aperçu ------------
    def rotation_aperçu(self, nombre_colonne: int, nombre_lignes: int):
        """
        Effectue la rotation de l'aperçu dans l'ordre bas -> gauche -> haut -> droite,
        en conservant le centre de l'aperçu pour éviter les débordements.
        """
        ordre = ["bas", "gauche", "haut", "droite"]
        try:
            idx = ordre.index(self.aperçu_direction)
        except ValueError:
            idx = 0
            self.aperçu_direction = "bas"
        nouvelle_direction = ordre[(idx + 1) % 4]

        # centre basé sur l'actuel coin d'aperçu
        centre_l, centre_c = self._centre_depuis_coin(self.aperçu_ligne, self.aperçu_colonne, self.aperçu_direction)
        nouvelle_ligne, nouvelle_col = self._coin_depuis_centre(centre_l, centre_c, nouvelle_direction)

        if self.verification_dedans(nouvelle_ligne, nouvelle_col, nouvelle_direction, nombre_colonne, nombre_lignes):
            self.aperçu_direction = nouvelle_direction
            self.aperçu_ligne = nouvelle_ligne
            self.aperçu_colonne = nouvelle_col

    def rotation_aperçu_si_possible(self, case_souris: Tuple[int,int], nombre_colonne: int, nombre_lignes: int):
        """
        Wrapper pour garder l'API d'origine : met la position d'aperçu sur la case souris,
        puis tente la rotation.
        """
        self.aperçu_ligne, self.aperçu_colonne = case_souris
        self.rotation_aperçu(nombre_colonne, nombre_lignes)
