import pygame
from typing import Tuple, List, Optional
from classes.ShipAnimator import ShipAnimator
from blazyck import *
from classes.Point import Point
import threading

# =======================
# Classe Ship = Vaisseau
# =======================

class Ship:
    def __init__(self,
                 pv_max: int, attaque: int, port_attaque: int, port_deplacement: int, cout: int, valeur_mort: int,
                 taille: Tuple[int,int], peut_miner: bool, peut_transporter: bool, image: pygame.Surface,
                 tier: int, cordonner: Optional[Point] = None, id: Optional[int] = None,
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
        self.cargaison = [None, None, None]

        # ---- Graphisme & niveau ----
        self.image = image
        self.tier = tier

        # ---- Identifiant stable ----
        self.id = id

        # ---- Position réelle ----
        if cordonner is None:
            cordonner = Point(0,0)
        self.cordonner: Point = cordonner

        self.direction = "haut"  # direction par défaut

        # ---- Aperçu (preview avant placement / action) ----
        self.aperçu_direction = self.direction
        self.aperçu_cordonner = Point(cordonner.x, cordonner.y)

        # Initialisation de l’Animator
        pixel_coord = (cordonner.y, cordonner.x)
        print(pixel_coord)
        self.animator = ShipAnimator(path, taille, pixel_coord, PV_max=pv_max, PV_actuelle=pv_max)
        self.prevision = ShipAnimator(path, taille, pixel_coord, show_health=False, alpha=100)

        # Charger les animations
        for anim in ["base", "engine", "shield", "destruction"]:
            self.animator.load_animation(anim, f"{anim}.png")
            self.prevision.load_animation(anim, f"{anim}.png")

        self.animator.play("base")
        self.prevision.play("base")

    # ------------ UTILITAIRES ------------
    def donner_dimensions(self, direction: str) -> Tuple[int, int]:
        """Retourne (largeur, hauteur) selon l’orientation du vaisseau."""
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

    # ------------ COMBAT ------------
    def attaquer(self, cible: "Ship"):
        cible.subir_degats(self.attaque)
        largeur, hauteur = cible.donner_dimensions(cible.direction)

        # Centre de la cible en pixels
        target_x = (cible.cordonner.y + largeur / 2) * TAILLE_CASE
        target_y = (cible.cordonner.x + hauteur / 2) * TAILLE_CASE

        self.animator.fire(
            projectile_type="torpedo",
            target=(target_x +50, target_y +50),  # centre de la cible en pixels
            is_fired=True,
            projectile_speed=3
        )


    def subir_degats(self, degats):
        self.pv_actuel = max(0, self.pv_actuel - max(0, degats))
        self.animator.PV_actuelle = self.pv_actuel
        if self.pv_actuel > 0:
            self.animator.play("shield", reset=True)
        else:
            self.prevision.remove_from_list()
            self.animator.idle = False
            self.animator.play("destruction", reset=True)
            self.animator.alive = False

    def est_mort(self):
        return self.pv_actuel <= 0

    # ------------ INTERACTION AVEC LE PLATEAU (listes) ------------
    def occuper_plateau(self, plateau, valeur, direction=None, ligne: int = None, colonne: int = None):
        if direction is None:
            direction = self.direction
        if ligne is None:
            ligne = self.cordonner.x
        if colonne is None:
            colonne = self.cordonner.y
        largeur, hauteur = self.donner_dimensions(direction)
        for l in range(ligne, ligne+hauteur):
            for c in range(colonne, colonne+largeur):
                plateau[l][c] = valeur


    def verifier_collision(self, plateau: List[List[int]], ligne: int = 0, colonne: int = 0, direction="haut"):
        largeur, hauteur = self.donner_dimensions(direction)
        for l in range(ligne, ligne + hauteur):
            for c in range(colonne, colonne + largeur):
                if plateau[l][c] != 0:
                    return False
        return True

    # ------------ DÉPLACEMENT / ATTAQUE ------------
    def positions_possibles_adjacentes(self, nombre_colonne, nombre_lignes, plateau, direction=None):
        if direction is None:
            direction = self.direction
        largeur, hauteur = self.donner_dimensions(direction)
        positions = []
        for y in range(-self.port_deplacement, self.port_deplacement + 1):
            for i in range(-self.port_deplacement, self.port_deplacement + 1):
                if y == 0 and i == 0: 
                    continue
                if abs(y) + abs(i) <= self.port_deplacement:
                    nl, nc = self.cordonner.x + y, self.cordonner.y + i
                    if 0 <= nl <= nombre_lignes - hauteur and 0 <= nc <= nombre_colonne - largeur:
                        collision = False
                        for l in range(nl, nl + hauteur):
                            for c in range(nc, nc + largeur):
                                if plateau[l][c] != 0 and plateau[l][c] != self.id:
                                    collision = True
                        if not collision:
                            positions.append((nl, nc))
        return positions

    def positions_possibles_attaque(self, nombre_colonne, nombre_lignes, direction=None):
        if direction is None:
            direction = self.direction
        positions = []
        for y in range(-self.port_attaque, self.port_attaque + 1):
            for i in range(-self.port_attaque, self.port_attaque + 1):
                if y == 0 and i == 0:
                    continue
                if abs(y) + abs(i) <= self.port_attaque:
                    nl, nc = self.cordonner.x + y, self.cordonner.y + i
                    if 0 <= nl < nombre_lignes and 0 <= nc < nombre_colonne:
                        positions.append((nl, nc))
        return positions

    def deplacement(self, case_cible, nombre_colonne, nombre_lignes, plateau, Ships, taille_case):
        if self.id is None: raise ValueError("Ship.id non défini")
        ligne, colonne = case_cible
        cible_direction = self.aperçu_direction

        # ---- Attaque ----
        if case_cible in self.positions_possibles_attaque(nombre_colonne, nombre_lignes, direction=cible_direction):
            cible_id = plateau[ligne][colonne]
            if cible_id != 0 and cible_id != self.id:
                cible_Ship = next((s for s in Ships if s.id == int(cible_id)), None)
                if cible_Ship:
                    self.attaquer(cible_Ship)
                    if cible_Ship.est_mort():
                        cible_Ship.occuper_plateau(plateau, 0)
                        Ships.remove(cible_Ship)
                    return True

        # ---- Déplacement ----
        if case_cible not in self.positions_possibles_adjacentes(nombre_colonne, nombre_lignes, plateau, direction=cible_direction):
            return False
        
        ancienne_ligne, ancienne_colonne, ancienne_direction = self.cordonner.x, self.cordonner.y, self.direction
        self.occuper_plateau(plateau, 0, direction=ancienne_direction, ligne=ancienne_ligne, colonne=ancienne_colonne)

        if self.verifier_collision(plateau, ligne, colonne, cible_direction):
            self.cordonner.deplacer(ligne, colonne)
            self.direction = cible_direction
            self.occuper_plateau(plateau, int(self.id), direction=self.direction, ligne=self.cordonner.x, colonne=self.cordonner.y)

            largeur, hauteur = self.donner_dimensions(self.direction)
            x, y = colonne * taille_case, ligne * taille_case
            w, h = largeur * taille_case, hauteur * taille_case

            self.animator.x = x
            self.animator.y = y
            self.animator.pixel_w = w
            self.animator.pixel_h = h

            self.prevision.angle = self.animator.angle
            self.prevision.alpha = 0
            if cible_direction == "haut": 
                self.animator.target_angle = 0
                self.prevision.target_angle = 0
            elif cible_direction == "droite": 
                self.animator.target_angle = -90
                self.prevision.target_angle = -90
            elif cible_direction == "gauche": 
                self.animator.target_angle = 90
                self.prevision.target_angle = 90
            elif cible_direction == "bas": 
                self.animator.target_angle = 180
                self.prevision.target_angle = 180

            self.animator.update_and_draw()
            return True
        else:
            self.occuper_plateau(plateau, int(self.id), direction=ancienne_direction, ligne=ancienne_ligne, colonne=ancienne_colonne)
            return False

    # ------------ ROTATION (aperçu) ------------
    def rotation_aperçu(self, nombre_colonne, nombre_lignes):
        ordre = ["haut","droite","bas","gauche"]
        idx = ordre.index(self.aperçu_direction) if self.aperçu_direction in ordre else 0
        nouvelle_direction = ordre[(idx+1)%len(ordre)]

        centre_l, centre_c = self._centre_depuis_coin(self.aperçu_cordonner.x, self.aperçu_cordonner.y, self.aperçu_direction)
        nouvelle_ligne, nouvelle_col = self._coin_depuis_centre(centre_l, centre_c, nouvelle_direction)
        largeur, hauteur = self.donner_dimensions(nouvelle_direction)
        x, y = self.aperçu_cordonner.y * TAILLE_CASE, self.aperçu_cordonner.x * TAILLE_CASE
        w, h = largeur * TAILLE_CASE, hauteur * TAILLE_CASE

        self.prevision.x = x
        self.prevision.y = y
        self.prevision.pixel_w = w
        self.prevision.pixel_h = h

        if 0 <= nouvelle_ligne <= nombre_lignes - hauteur and 0 <= nouvelle_col <= nombre_colonne - largeur:
            if nouvelle_direction == "haut": 
                self.prevision.angle = 0
                self.prevision.target_angle = 0
            elif nouvelle_direction == "droite": 
                self.prevision.angle = -90
                self.prevision.target_angle = -90
            elif nouvelle_direction == "gauche": 
                self.prevision.angle = 90
                self.prevision.target_angle = 90
            elif nouvelle_direction == "bas": 
                self.prevision.angle = 180
                self.prevision.target_angle = 180
            self.aperçu_direction = nouvelle_direction
            self.aperçu_cordonner.deplacer(nouvelle_ligne, nouvelle_col)

    def rotation_aperçu_si_possible(self, case_souris, nombre_colonne, nombre_lignes):
        self.aperçu_cordonner.deplacer(*case_souris)
        self.prevision.x = case_souris[1] * TAILLE_CASE
        self.prevision.y = case_souris[0] * TAILLE_CASE
        self.rotation_aperçu(nombre_colonne, nombre_lignes)














# ------------ Sous-Sous-classes ------------


class Petit(Ship):
    def __init__(self,
                 pv_max: int, attaque: int, port_attaque: int, port_deplacement: int, cout: int, valeur_mort: int,
                 taille: Tuple[int,int], peut_miner: bool, peut_transporter: bool, image: pygame.Surface,
                 tier: int, cordonner: Point, id: Optional[int] = None,
                 path: str = None):
        super().__init__(pv_max, attaque, port_attaque, port_deplacement, cout, valeur_mort,
                         taille, peut_miner, peut_transporter, image,
                         tier, cordonner, id, path)

class Moyen(Ship):
    def __init__(self,
                 pv_max: int, attaque: int, port_attaque: int, port_deplacement: int, cout: int, valeur_mort: int,
                 taille: Tuple[int,int], peut_miner: bool, peut_transporter: bool, image: pygame.Surface,
                 tier: int, cordonner: Point, id: Optional[int] = None,
                 path: str = None):
        super().__init__(pv_max, attaque, port_attaque, port_deplacement, cout, valeur_mort,
                         taille, peut_miner, peut_transporter, image,
                         tier, cordonner, id, path)

class Lourd(Ship):
    def __init__(self,
                 pv_max: int, attaque: int, port_attaque: int, port_deplacement: int, cout: int, valeur_mort: int,
                 taille: Tuple[int,int], peut_miner: bool, peut_transporter: bool, image: pygame.Surface,
                 tier: int, cordonner: Point, id: Optional[int] = None,
                 path: str = None):
        super().__init__(pv_max, attaque, port_attaque, port_deplacement, cout, valeur_mort,
                         taille, peut_miner, peut_transporter, image,
                         tier, cordonner, id, path)

class Foreuse(Ship):
    def __init__(self,
                 pv_max: int, attaque: int, port_attaque: int, port_deplacement: int, cout: int, valeur_mort: int,
                 taille: Tuple[int,int], peut_miner: bool, peut_transporter: bool, image: pygame.Surface,
                 tier: int, cordonner: Point, id: Optional[int] = None,
                 path: str = None):
        super().__init__(pv_max, attaque, port_attaque, port_deplacement, cout, valeur_mort,
                         taille, peut_miner, peut_transporter, image,
                         tier, cordonner, id, path)

class Transport(Ship):
    def __init__(self,
                 pv_max: int, attaque: int, port_attaque: int, port_deplacement: int, cout: int, valeur_mort: int,
                 taille: Tuple[int,int], peut_miner: bool, peut_transporter: bool, image: pygame.Surface,
                 tier: int, cordonner: Point, id: Optional[int] = None,
                 path: str = None):
        super().__init__(pv_max, attaque, port_attaque, port_deplacement, cout, valeur_mort,
                         taille, peut_miner, peut_transporter, image,
                         tier, cordonner, id, path)
        self.cargaison: List[Optional[Ship]] = [None, None, None]

    def ajouter_cargo(self, ship: Ship) -> bool:
        for i in range(len(self.cargaison)):
            if self.cargaison[i] is None:
                self.cargaison[i] = ship
                return True
        return False

    def retirer_cargo(self, index: int, ligne: int, colonne: int, plateau: List[List[int]]) -> bool:
        if 0 <= index < len(self.cargaison):
            Ship = self.cargaison[index]
            if Ship is None:
                return False
            self.cargaison[index] = None
            Ship.cordonner.deplacer(ligne, colonne)
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
        for i, Ship in enumerate(self.cargaison):
            if Ship is None:
                continue
            mini_img = pygame.transform.scale(Ship.image, (20,20))
            x = self.cordonner.y * taille_case + i * 22
            y = self.cordonner.x * taille_case - 22
            fenetre.blit(mini_img, (x, y))

    def positions_debarquement(self, Ship_stocke: Ship, plateau: List[List[int]], nombre_lignes: int, nombre_colonnes: int):
        positions_valides = []
        port = Ship_stocke.port_deplacement

        for dy in range(-port, port+1):
            for dx in range(-port, port+1):
                if abs(dy) + abs(dx) > port:
                    continue
                nl = self.cordonner.x + dy
                nc = self.cordonner.y + dx
                largeur, hauteur = Ship_stocke.donner_dimensions(Ship_stocke.direction)

                if not (0 <= nl <= nombre_lignes - hauteur and 0 <= nc <= nombre_colonnes - largeur):
                    continue

                collision = False
                for l in range(nl, nl+hauteur):
                    for c in range(nc, nc+largeur):
                        if plateau[l][c] != 0:
                            collision = True
                            break
                    if collision:
                        break

                if not collision:
                    positions_valides.append((nl, nc))

        return positions_valides


