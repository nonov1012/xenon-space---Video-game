import pygame
import numpy as np
from typing import Tuple, List, Optional

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
                 colonne: int = 0,
                 uid: Optional[int] = None):
        # caractéristiques
        self.pv_max = pv_max
        self.pv_actuel = pv_max
        self.attaque = attaque
        self.port_attaque = port_attaque
        self.port_deplacement = port_deplacement
        self.cout = cout
        self.valeur_mort = valeur_mort
        self.taille = tuple(taille)
        self.peut_miner = peut_miner
        self.peut_transporter = peut_transporter
        self.cargaison = np.array([None, None, None], dtype=object)

        # graphisme / niveau
        self.image = image
        self.tier = tier

        # id stable
        self.id = uid

        # position réelle
        self.ligne = ligne
        self.colonne = colonne
        self.direction = "haut"

        # aperçu (preview)
        self.aperçu_direction = self.direction
        self.aperçu_ligne = ligne
        self.aperçu_colonne = colonne

    # ------------ utilitaires ------------
    def donner_dimensions(self, direction: str) -> Tuple[int, int]:
        """Retourne (largeur, hauteur) selon l'orientation."""
        if direction in ("haut", "bas"):
            return self.taille
        elif direction in ("droite", "gauche"):
            return (self.taille[1], self.taille[0])

    def _centre_depuis_coin(self, ligne_coin, colonne_coin, direction):
        largeur, hauteur = self.donner_dimensions(direction)
        return ligne_coin + (hauteur-1)/2, colonne_coin + (largeur-1)/2

    def _coin_depuis_centre(self, centre_l, centre_c, direction):
        largeur, hauteur = self.donner_dimensions(direction)
        return int(round(centre_l-(hauteur-1)/2)), int(round(centre_c-(largeur-1)/2))

    # ------------ dessin ------------
    def dessiner(self, surface, taille_case, preview=False):
        if preview:
            ligne, colonne, direction = self.aperçu_ligne, self.aperçu_colonne, self.aperçu_direction
        else:
            ligne, colonne, direction = self.ligne, self.colonne, self.direction

        largeur, hauteur = self.donner_dimensions(direction)
        x, y = colonne*taille_case, ligne*taille_case
        w, h = largeur*taille_case, hauteur*taille_case

        if direction=="haut":
            img = self.image
        elif direction=="droite":
            img = pygame.transform.rotate(self.image, -90)
        elif direction=="gauche":
            img = pygame.transform.rotate(self.image, 90)
        elif direction=="bas":
            img = pygame.transform.rotate(self.image, 180)

        img = pygame.transform.scale(img, (w,h))
        surface.blit(img, (x,y))

    # ------------ combat ------------
    def attaquer(self, cible: "Ship"):
        cible.subir_degats(self.attaque)

    def subir_degats(self, degats):
        self.pv_actuel -= degats

    def est_mort(self):
        return self.pv_actuel <= 0

    # ------------ plateau numpy ------------
    def occuper_plateau(self, plateau, valeur, direction=None, ligne=None, colonne=None):
        if direction is None: direction=self.direction
        if ligne is None: ligne=self.ligne
        if colonne is None: colonne=self.colonne
        largeur, hauteur = self.donner_dimensions(direction)
        for l in range(ligne, ligne+hauteur):
            for c in range(colonne, colonne+largeur):
                plateau[l,c]=valeur

    def verifier_collision(self, plateau, ligne, colonne, direction):
        largeur, hauteur = self.donner_dimensions(direction)
        for l in range(ligne, ligne+hauteur):
            for c in range(colonne, colonne+largeur):
                if plateau[l,c]!=0: return False
        return True

    # ------------ déplacement / attaque ------------
    def positions_possibles_adjacentes(self, nombre_colonne, nombre_lignes, plateau, direction=None):
        if direction is None:
            direction = self.direction
        largeur, hauteur = self.donner_dimensions(direction)
        positions=[]
        for dl in range(-self.port_deplacement,self.port_deplacement+1):
            for dc in range(-self.port_deplacement,self.port_deplacement+1):
                if dl==0 and dc==0: continue
                if abs(dl)+abs(dc)<=self.port_deplacement:
                    nl, nc = self.aperçu_ligne + dl, self.aperçu_colonne + dc
                    if 0<=nl<=nombre_lignes-hauteur and 0<=nc<=nombre_colonne-largeur:
                        collision = False
                        for l in range(nl, nl+hauteur):
                            for c in range(nc, nc+largeur):
                                if plateau[l,c]!=0 and plateau[l,c]!=self.id:
                                    collision=True
                        if not collision:
                            positions.append((nl,nc))
        return positions

    def positions_possibles_attaque(self, nombre_colonne, nombre_lignes, direction=None):
        if direction is None:
            direction = self.direction
        largeur, hauteur = self.donner_dimensions(direction)
        positions=[]
        for dl in range(-self.port_attaque,self.port_attaque+1):
            for dc in range(-self.port_attaque,self.port_attaque+1):
                if dl==0 and dc==0: continue
                if abs(dl)+abs(dc)<=self.port_attaque:
                    nl, nc = self.aperçu_ligne + dl, self.aperçu_colonne + dc
                    if 0<=nl<=nombre_lignes-hauteur and 0<=nc<=nombre_colonne-largeur:
                        positions.append((nl,nc))
        return positions


    def deplacement(self, case_cible, nombre_colonne, nombre_lignes, plateau, ships):
        if self.id is None: raise ValueError("Ship.id non défini")
        ligne, colonne = case_cible
        cible_direction = self.aperçu_direction

        # ---- attaque si possible ----
        if case_cible in self.positions_possibles_attaque(nombre_colonne,nombre_lignes):
            cible_id = plateau[ligne,colonne]
            if cible_id!=0 and cible_id!=self.id:
                cible_ship = next((s for s in ships if s.id==int(cible_id)), None)
                if cible_ship:
                    self.attaquer(cible_ship)
                    if cible_ship.est_mort():
                        cible_ship.occuper_plateau(plateau,0)
                        ships.remove(cible_ship)
                    return True

        # ---- déplacement ----
        if case_cible not in self.positions_possibles_adjacentes(nombre_colonne,nombre_lignes, plateau):
            return False

        ancienne_ligne, ancienne_colonne, ancienne_direction = self.ligne,self.colonne,self.direction
        self.occuper_plateau(plateau,0,direction=ancienne_direction,ligne=ancienne_ligne,colonne=ancienne_colonne)
        if self.verifier_collision(plateau, ligne, colonne, cible_direction):
            self.ligne,self.colonne,self.direction = ligne,colonne,cible_direction
            self.occuper_plateau(plateau,int(self.id),direction=self.direction,ligne=self.ligne,colonne=self.colonne)
            return True
        else:
            self.occuper_plateau(plateau,int(self.id),direction=ancienne_direction,ligne=ancienne_ligne,colonne=ancienne_colonne)
            return False

    # ------------ rotation aperçu ------------
    def rotation_aperçu(self, nombre_colonne, nombre_lignes):
        ordre = ["haut","droite","bas","gauche"]
        idx = ordre.index(self.aperçu_direction) if self.aperçu_direction in ordre else 0
        nouvelle_direction = ordre[(idx+1)%len(ordre)]
        centre_l, centre_c = self._centre_depuis_coin(self.aperçu_ligne,self.aperçu_colonne,self.aperçu_direction)
        nouvelle_ligne, nouvelle_col = self._coin_depuis_centre(centre_l,centre_c,nouvelle_direction)
        largeur, hauteur = self.donner_dimensions(nouvelle_direction)
        if 0<=nouvelle_ligne<=nombre_lignes-hauteur and 0<=nouvelle_col<=nombre_colonne-largeur:
            self.aperçu_direction = nouvelle_direction
            self.aperçu_ligne, self.aperçu_colonne = nouvelle_ligne, nouvelle_col

    def rotation_aperçu_si_possible(self, case_souris, nombre_colonne, nombre_lignes):
        self.aperçu_ligne,self.aperçu_colonne = case_souris
        self.rotation_aperçu(nombre_colonne,nombre_lignes)


# ------------ Sous-classes ------------

class CombatShip(Ship):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.peut_miner = False
        self.peut_transporter = False

class MinerShip(Ship):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.peut_miner = True
        self.peut_transporter = False

class TransportShip(Ship):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.peut_miner = False
        self.peut_transporter = True
