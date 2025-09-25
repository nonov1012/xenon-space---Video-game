import pygame
import numpy as np
import os
from typing import Tuple, List, Optional
from classes.ShipAnimator import ShipAnimator
from blazyck import *

# =======================
# Classe Ship = Vaisseau
# =======================

class Ship:
    def __init__(self,
                 pv_max: int, attaque: int, port_attaque: int, port_deplacement: int, cout: int, valeur_mort: int,
                 taille: Tuple[int,int], peut_miner: bool, peut_transporter: bool, image: pygame.Surface,
                 tier: int, ligne: int = 0, colonne: int = 0, id: Optional[int] = None,
                 path: str = None):
        
        # ---- Caractéristiques ----
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

        # Inventaire de transport (3 slots)
        self.cargaison = np.array([None, None, None], dtype=object)

        # ---- Graphisme & niveau ----
        self.image = image
        self.tier = tier

        # ---- Identifiant stable ----
        self.id = id

        # ---- Position réelle ----
        self.ligne = ligne
        self.colonne = colonne
        self.direction = "haut"  # direction par défaut

        # ---- Aperçu (preview avant placement / action) ----
        self.aperçu_direction = self.direction
        self.aperçu_ligne = ligne
        self.aperçu_colonne = colonne


        # Initialisation de l’Animator
        pixel_coord = (colonne * TAILLE_CASE, ligne * TAILLE_CASE)
        self.animator = ShipAnimator(path, taille, pixel_coord)

        # Charger les animations
        for anim in ["base", "engine", "shield", "destruction"]:
            self.animator.load_animation(anim, f"{anim}.png")

        self.animator.play("base")


    # ------------ UTILITAIRES ------------
    def donner_dimensions(self, direction: str) -> Tuple[int, int]:
        """Retourne (largeur, hauteur) selon l’orientation du vaisseau."""
        if direction in ("haut", "bas"):
            return self.taille
        elif direction in ("droite", "gauche"):
            # Inverser largeur/hauteur quand le vaisseau est couché
            return (self.taille[1], self.taille[0])

    def _centre_depuis_coin(self, ligne_coin, colonne_coin, direction):
        """Calcule les coordonnées du centre à partir du coin supérieur gauche."""
        largeur, hauteur = self.donner_dimensions(direction)
        return ligne_coin + (hauteur-1)/2, colonne_coin + (largeur-1)/2

    def _coin_depuis_centre(self, centre_l, centre_c, direction):
        """Calcule le coin supérieur gauche à partir du centre du vaisseau."""
        largeur, hauteur = self.donner_dimensions(direction)
        return int(round(centre_l-(hauteur-1)/2)), int(round(centre_c-(largeur-1)/2))

    # ------------ COMBAT ------------
    def attaquer(self, cible: "Ship"):
        """Inflige des dégâts à une cible."""
        cible.subir_degats(self.attaque)
        largeur, hauteur = cible.donner_dimensions(cible.direction)
        target_x = (cible.colonne + largeur / 2) * TAILLE_CASE
        target_y = (cible.ligne + hauteur / 2) * TAILLE_CASE

        # Lancer le projectile
        self.animator.fire("big bullet", (target_x, target_y), True, projectile_speed=4)


    def subir_degats(self, degats):
        """Réduit les PV suite à des dégâts subis."""
        self.pv_actuel = max(0, self.pv_actuel - max(0, degats))
        if self.pv_actuel > 0:
            self.animator.play("shield", reset=True)
        else:
            self.animator.play("destruction", reset=True)


    def est_mort(self):
        """Retourne True si le vaisseau est détruit."""
        return self.pv_actuel <= 0


    # ------------ INTERACTION AVEC LE PLATEAU (numpy) ------------
    def occuper_plateau(self, plateau, valeur, direction=None, ligne=None, colonne=None):
        """Occupe des cases du plateau avec une valeur (ex: id du vaisseau)."""
        if direction is None: direction=self.direction
        if ligne is None: ligne=self.ligne
        if colonne is None: colonne=self.colonne
        largeur, hauteur = self.donner_dimensions(direction)
        for l in range(ligne, ligne+hauteur):
            for c in range(colonne, colonne+largeur):
                plateau[l,c]=valeur

    def verifier_collision(self, plateau, ligne, colonne, direction):
        """Vérifie si le vaisseau peut se placer sans collision."""
        largeur, hauteur = self.donner_dimensions(direction)
        for l in range(ligne, ligne+hauteur):
            for c in range(colonne, colonne+largeur):
                if plateau[l,c]!=0: return False
        return True


    # ------------ DÉPLACEMENT / ATTAQUE ------------
    def positions_possibles_adjacentes(self, nombre_colonne, nombre_lignes, plateau, direction=None):
        """Retourne les cases atteignables par déplacement (en tenant compte des collisions)."""
        if direction is None:
            direction = self.direction
        largeur, hauteur = self.donner_dimensions(direction)
        positions=[]
        for y in range(-self.port_deplacement,self.port_deplacement+1):
            for i in range(-self.port_deplacement,self.port_deplacement+1):
                if y==0 and i==0: 
                    continue
                # distance de Manhattan
                if abs(y)+abs(i)<=self.port_deplacement:
                    nl, nc = self.ligne + y, self.colonne + i
                    if 0 <= nl <= nombre_lignes - hauteur and 0 <= nc <= nombre_colonne - largeur:
                        collision = False
                        for l in range(nl, nl+hauteur):
                            for c in range(nc, nc+largeur):
                                if plateau[l,c]!=0 and plateau[l,c]!=self.id:
                                    collision = True
                        if not collision:
                            positions.append((nl,nc))
        return positions

    def positions_possibles_attaque(self, nombre_colonne, nombre_lignes, direction=None):
        """Retourne les cases attaquables (en tenant compte de la portée)."""
        if direction is None:
            direction = self.direction
        positions=[]
        for y in range(-self.port_attaque, self.port_attaque+1):
            for i in range(-self.port_attaque, self.port_attaque+1):
                if y == 0 and i == 0:
                    continue
                if abs(y) + abs(i) <= self.port_attaque:
                    nl, nc = self.ligne + y, self.colonne + i
                    if 0 <= nl < nombre_lignes and 0 <= nc < nombre_colonne:
                        positions.append((nl, nc))
        return positions

    def deplacement(self, case_cible, nombre_colonne, nombre_lignes, plateau, Ships, taille_case):
        """Déplace le vaisseau ou attaque si une cible est dans la portée."""
        if self.id is None: raise ValueError("Ship.id non défini")
        ligne, colonne = case_cible
        cible_direction = self.aperçu_direction  # orientation visée

        # ---- Attaque si possible ----
        if case_cible in self.positions_possibles_attaque(nombre_colonne, nombre_lignes, direction=cible_direction):
            cible_id = plateau[ligne,colonne]
            if cible_id!=0 and cible_id!=self.id:
                cible_Ship = next((s for s in Ships if s.id==int(cible_id)), None)
                if cible_Ship:
                    self.attaquer(cible_Ship)
                    if cible_Ship.est_mort():
                        cible_Ship.occuper_plateau(plateau,0)
                        Ships.remove(cible_Ship)
                    return True

        # ---- Déplacement ----
        if case_cible not in self.positions_possibles_adjacentes(nombre_colonne, nombre_lignes, plateau, direction=cible_direction):
            return False
        
        # Sauvegarde ancienne position
        ancienne_ligne, ancienne_colonne, ancienne_direction = self.ligne,self.colonne,self.direction
        self.occuper_plateau(plateau,0,direction=ancienne_direction,ligne=ancienne_ligne,colonne=ancienne_colonne)

        # Vérifie si pas de collision à la nouvelle position
        if self.verifier_collision(plateau, ligne, colonne, cible_direction):
            self.ligne,self.colonne,self.direction = ligne,colonne,cible_direction
            self.occuper_plateau(plateau,int(self.id),direction=self.direction,ligne=self.ligne,colonne=self.colonne)
            largeur, hauteur = self.donner_dimensions(self.direction)
            x, y = colonne * taille_case, ligne * taille_case
            w, h = largeur * taille_case, hauteur * taille_case

            # Mise à jour de la position + dimensions
            self.animator.x = x
            self.animator.y = y
            self.animator.pixel_w = w
            self.animator.pixel_h = h

            # Conversion direction → angle (ShipAnimator attend un angle en degrés)
            if cible_direction == "haut":
                self.animator.target_angle = 0
            elif cible_direction == "droite":
                self.animator.target_angle = -90
            elif cible_direction == "gauche":
                self.animator.target_angle = 90
            elif cible_direction == "bas":
                self.animator.target_angle = 180

            self.animator.update_and_draw()


            return True
        else:
            # Réoccupe ancienne position en cas d’échec
            self.occuper_plateau(plateau,int(self.id),direction=ancienne_direction,ligne=ancienne_ligne,colonne=ancienne_colonne)
            return False


    # ------------ ROTATION (aperçu) ------------
    def rotation_aperçu(self, nombre_colonne, nombre_lignes):
        """Tourne l’aperçu du vaisseau (cycle haut → droite → bas → gauche)."""
        ordre = ["haut","droite","bas","gauche"]
        idx = ordre.index(self.aperçu_direction) if self.aperçu_direction in ordre else 0
        nouvelle_direction = ordre[(idx+1)%len(ordre)]

        # Recalcule la position à partir du centre
        centre_l, centre_c = self._centre_depuis_coin(self.aperçu_ligne,self.aperçu_colonne,self.aperçu_direction)
        nouvelle_ligne, nouvelle_col = self._coin_depuis_centre(centre_l,centre_c,nouvelle_direction)
        largeur, hauteur = self.donner_dimensions(nouvelle_direction)

        # Valide la rotation si toujours dans les limites de la grille
        if 0<=nouvelle_ligne<=nombre_lignes-hauteur and 0<=nouvelle_col<=nombre_colonne-largeur:
            self.aperçu_direction = nouvelle_direction
            self.aperçu_ligne, self.aperçu_colonne = nouvelle_ligne, nouvelle_col

    def rotation_aperçu_si_possible(self, case_souris, nombre_colonne, nombre_lignes):
        """Positionne l’aperçu sur une case donnée puis tente une rotation."""
        self.aperçu_ligne,self.aperçu_colonne = case_souris
        self.rotation_aperçu(nombre_colonne,nombre_lignes)


# ------------ Sous-Sous-classes ------------



class Petit(Ship):
    def __init__(self,
                 pv_max: int, attaque: int, port_attaque: int, port_deplacement: int, cout: int, valeur_mort: int,
                 taille: Tuple[int,int], peut_miner: bool, peut_transporter: bool, image: pygame.Surface,
                 tier: int, ligne: int = 0, colonne: int = 0, id: Optional[int] = None,
                 path: str = None):
        
        super().__init__(pv_max, attaque, port_attaque, port_deplacement, cout, valeur_mort,
                 taille, peut_miner, peut_transporter, image,
                 tier, ligne, colonne, id, path)

class Moyen(Ship):
    def __init__(self,
                 pv_max: int, attaque: int, port_attaque: int, port_deplacement: int, cout: int, valeur_mort: int,
                 taille: Tuple[int,int], peut_miner: bool, peut_transporter: bool, image: pygame.Surface,
                 tier: int, ligne: int = 0, colonne: int = 0, id: Optional[int] = None,
                 path: str = None):
        
        super().__init__(pv_max, attaque, port_attaque, port_deplacement, cout, valeur_mort,
                 taille, peut_miner, peut_transporter, image,
                 tier, ligne, colonne, id, path)


class Lourd(Ship):
    def __init__(self,
                 pv_max: int, attaque: int, port_attaque: int, port_deplacement: int, cout: int, valeur_mort: int,
                 taille: Tuple[int,int], peut_miner: bool, peut_transporter: bool, image: pygame.Surface,
                 tier: int, ligne: int = 0, colonne: int = 0, id: Optional[int] = None,
                 path: str = None):
        
        super().__init__(pv_max, attaque, port_attaque, port_deplacement, cout, valeur_mort,
                 taille, peut_miner, peut_transporter, image,
                 tier, ligne, colonne, id, path)




class Foreuse(Ship):
    def __init__(self,
                 pv_max: int, attaque: int, port_attaque: int, port_deplacement: int, cout: int, valeur_mort: int,
                 taille: Tuple[int,int], peut_miner: bool, peut_transporter: bool, image: pygame.Surface,
                 tier: int, ligne: int = 0, colonne: int = 0, id: Optional[int] = None,
                 path: str = None):
        
        super().__init__(pv_max, attaque, port_attaque, port_deplacement, cout, valeur_mort,
                 taille, peut_miner, peut_transporter, image,
                 tier, ligne, colonne, id, path)




class Transport(Ship):
    def __init__(self,
                 pv_max: int, attaque: int, port_attaque: int, port_deplacement: int, cout: int, valeur_mort: int,
                 taille: Tuple[int,int], peut_miner: bool, peut_transporter: bool, image: pygame.Surface,
                 tier: int, ligne: int = 0, colonne: int = 0, id: Optional[int] = None,
                 path: str = None):
        
        super().__init__(pv_max, attaque, port_attaque, port_deplacement, cout, valeur_mort,
                 taille, peut_miner, peut_transporter, image,
                 tier, ligne, colonne, id, path)
        self.cargaison = []  # liste des vaisseaux stockés

    def ajouter_cargo(self, Ship: Ship, plateau) -> bool:
        """Ajoute un vaisseau dans le transport si possible."""
        # Autoriser seulement petit ou moyen
        if not isinstance(Ship, (Petit, Moyen)):
            return False

        if len(self.cargaison) >= 3:
            return False

        taille_cargo = [self._taille_vaisseau(s) for s in self.cargaison] + [self._taille_vaisseau(Ship)]
        if sum(taille_cargo) > 3:
            return False

        # Retirer du plateau
        Ship.occuper_plateau(plateau, 0)

        # Ajouter dans la cargaison
        self.cargaison.append(Ship)
        return True



    def retirer_cargo(self, index: int, ligne: int, colonne: int, plateau) -> bool:
        """Débarque un vaisseau du transport sur le plateau."""
        if 0 <= index < len(self.cargaison):
            Ship = self.cargaison.pop(index)
            Ship.ligne, Ship.colonne = ligne, colonne
            Ship.direction = "haut"
            Ship.occuper_plateau(plateau, Ship.id)
            return True
        return False

    def _taille_vaisseau(self, Ship: Ship) -> int:
        if isinstance(Ship, Petit):
            return 1
        elif isinstance(Ship, Moyen):
            return 2
        else:
            return 3

    def afficher_cargaison(self, fenetre, taille_case):
        """Affiche les vaisseaux stockés avec images miniatures au-dessus du transport"""
        for i, Ship in enumerate(self.cargaison):
            mini_img = pygame.transform.scale(Ship.image, (20,20))
            x = self.colonne * taille_case + i*22
            y = self.ligne * taille_case - 22
            fenetre.blit(mini_img, (x, y))


    def positions_debarquement(self, Ship_stocke, plateau, nombre_lignes, nombre_colonnes):
        """Retourne les positions valides pour débarquer un vaisseau depuis ce transport."""
        positions_valides = []
        port = Ship_stocke.port_deplacement  # utiliser la portée du vaisseau stocké

        for dy in range(-port, port+1):
            for dx in range(-port, port+1):
                if abs(dy) + abs(dx) > port:
                    continue
                nl = self.ligne + dy
                nc = self.colonne + dx
                largeur, hauteur = Ship_stocke.donner_dimensions(Ship_stocke.direction)

                # Vérifier que tout le rectangle du vaisseau est dans la grille
                if not (0 <= nl <= nombre_lignes - hauteur and 0 <= nc <= nombre_colonnes - largeur):
                    continue

                # Vérifier que toutes les cases sont libres
                collision = False
                for l in range(nl, nl+hauteur):
                    for c in range(nc, nc+largeur):
                        if plateau[l, c] != 0:
                            collision = True
                            break
                    if collision:
                        break

                if not collision:
                    positions_valides.append((nl, nc))

        return positions_valides


