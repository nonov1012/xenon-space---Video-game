import pygame
from typing import Tuple, List, Optional
from classes.ShipAnimator import ShipAnimator
from blazyck import *
from classes.Point import Point, Type
import threading
import random

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
            cordonner = Point(0, 0)
        self.cordonner: Point = cordonner

        self.direction = "haut"  # direction par défaut

        # ---- Aperçu (preview avant placement / action) ----
        self.aperçu_direction = self.direction
        self.aperçu_cordonner = Point(cordonner.x, cordonner.y)

        # Initialisation de l'Animator
        # Attention: ShipAnimator attend (y, x) en pixels selon le code
        tile_coord = (cordonner.y, cordonner.x)  # Juste les indices de cases
        self.animator = ShipAnimator(path, taille, tile_coord, PV_max=pv_max, PV_actuelle=pv_max)
        self.prevision = ShipAnimator(path, taille, tile_coord, show_health=False, alpha=100)

        # Charger les animations de base
        base_animations = ["base", "engine", "shield", "destruction"]
        for anim in base_animations:
            self.animator.load_animation(anim, f"{anim}.png")
            self.prevision.load_animation(anim, f"{anim}.png")

        # Charger l'animation weapons seulement si le vaisseau peut attaquer
        if self.attaque > 0 and not isinstance(self, Foreuse):
            self.animator.load_animation("weapons", "weapons.png")
            self.prevision.load_animation("weapons", "weapons.png")

        self.animator.play("base")
        self.prevision.play("base")

    # ------------ UTILITAIRES ------------
    def donner_dimensions(self, direction: str) -> Tuple[int, int]:
        """Retourne (largeur, hauteur) selon l'orientation du vaisseau."""
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
        """Attaque un vaisseau cible."""
        cible.subir_degats(self.attaque)
        
        # Vérifier si ce vaisseau peut tirer (les foreuses n'ont pas d'animation de tir)
        if self.attaque > 0 and not isinstance(self, Foreuse):
            largeur, hauteur = cible.donner_dimensions(cible.direction)

            # Centre de la cible en pixels
            target_x = (cible.cordonner.y + largeur / 2) * TAILLE_CASE + OFFSET_X
            target_y = (cible.cordonner.x + hauteur / 2) * TAILLE_CASE

            self.animator.fire(
                projectile_type="torpedo",
                target=(target_x, target_y),
                is_fired=True,
                projectile_speed=3
            )

    def subir_degats(self, degats):
        """Fait subir des dégâts au vaisseau."""
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
        """Vérifie si le vaisseau est mort."""
        return self.pv_actuel <= 0

    def peut_miner_asteroide(self, grille: List[List[Point]], x: int, y: int) -> bool:
        """Vérifie si le vaisseau peut miner l'astéroïde à la position donnée."""
        if not self.peut_miner:
            return False
        
        if 0 <= x < len(grille[0]) and 0 <= y < len(grille):
            return grille[y][x].type == Type.ASTEROIDE
        return False

    def miner_asteroide(self, grille: List[List[Point]], x: int, y: int) -> bool:
        """Mine un astéroïde et le transforme en case vide."""
        if self.peut_miner_asteroide(grille, x, y):
            grille[y][x].type = Type.VIDE
            # Ici on pourrait ajouter des ressources au vaisseau
            return True
        return False

    # ------------ INTERACTION AVEC LE PLATEAU (grille de Points) ------------
    def occuper_plateau(self, grille: List[List[Point]], nouveau_type: Type, direction=None, ligne: int = None, colonne: int = None):
        """Occupe les cases du plateau avec le type spécifié."""
        if direction is None:
            direction = self.direction
        if ligne is None:
            ligne = self.cordonner.x
        if colonne is None:
            colonne = self.cordonner.y
            
        largeur, hauteur = self.donner_dimensions(direction)
        for l in range(ligne, ligne + hauteur):
            for c in range(colonne, colonne + largeur):
                if 0 <= l < len(grille) and 0 <= c < len(grille[0]):
                    grille[l][c].type = nouveau_type

    def verifier_collision(self, grille: List[List[Point]], ligne: int = 0, colonne: int = 0, direction="haut", ignorer_self=False):
        """Vérifie s'il y a collision avec les objets du plateau."""
        largeur, hauteur = self.donner_dimensions(direction)
        
        # Vérification des limites
        if ligne < 0 or colonne < 0:
            return False
        if ligne + hauteur > len(grille) or colonne + largeur > len(grille[0]):
            return False
            
        # Vérification des collisions
        for l in range(ligne, ligne + hauteur):
            for c in range(colonne, colonne + largeur):
                point = grille[l][c]
                
                # Si on ignore notre propre position actuelle
                if ignorer_self:
                    # Vérifier si cette case fait partie de notre position actuelle
                    if (self.cordonner.x <= l < self.cordonner.x + self.donner_dimensions(self.direction)[1] and
                        self.cordonner.y <= c < self.cordonner.y + self.donner_dimensions(self.direction)[0]):
                        continue
                
                # Types de cases qui bloquent le déplacement
                types_bloquants = [Type.PLANETE, Type.ASTEROIDE, Type.BASE, Type.VAISSEAU]
                if point.type in types_bloquants:
                    return False
        return True

    # ------------ DÉPLACEMENT / ATTAQUE ------------
    def positions_possibles_adjacentes(self, grille: List[List[Point]], direction=None):
        """Calcule les positions de déplacement possibles."""
        if direction is None:
            direction = self.direction
            
        nb_lignes = len(grille)
        nb_colonnes = len(grille[0])
        largeur, hauteur = self.donner_dimensions(direction)
        positions = []
        
        for dy in range(-self.port_deplacement, self.port_deplacement + 1):
            for dx in range(-self.port_deplacement, self.port_deplacement + 1):
                if dy == 0 and dx == 0: 
                    continue
                if abs(dy) + abs(dx) <= self.port_deplacement:
                    nl, nc = self.cordonner.x + dy, self.cordonner.y + dx
                    
                    # Vérification des limites
                    if 0 <= nl <= nb_lignes - hauteur and 0 <= nc <= nb_colonnes - largeur:
                        # Utiliser ignorer_self=True pour éviter l'auto-collision
                        if self.verifier_collision(grille, nl, nc, direction, ignorer_self=True):
                            positions.append((nl, nc))
        return positions

    def positions_possibles_attaque(self, grille: List[List[Point]], direction=None):
        """Calcule les positions d'attaque possibles."""
        if direction is None:
            direction = self.direction
            
        nb_lignes = len(grille)
        nb_colonnes = len(grille[0])
        positions = []
        
        for dy in range(-self.port_attaque, self.port_attaque + 1):
            for dx in range(-self.port_attaque, self.port_attaque + 1):
                if dy == 0 and dx == 0:
                    continue
                if abs(dy) + abs(dx) <= self.port_attaque:
                    nl, nc = self.cordonner.x + dy, self.cordonner.y + dx
                    if 0 <= nl < nb_lignes and 0 <= nc < nb_colonnes:
                        positions.append((nl, nc))
        return positions

    def trouver_vaisseau_a_position(self, ships: List["Ship"], ligne: int, colonne: int) -> Optional["Ship"]:
        """Trouve un vaisseau à la position donnée."""
        for ship in ships:
            largeur, hauteur = ship.donner_dimensions(ship.direction)
            if (ship.cordonner.x <= ligne < ship.cordonner.x + hauteur and
                ship.cordonner.y <= colonne < ship.cordonner.y + largeur):
                return ship
        return None

    def liberer_position(self, grille: List[List[Point]]):
        """Libère la position du vaisseau en restaurant le terrain approprié."""
        largeur, hauteur = self.donner_dimensions(self.direction)
        for l in range(self.cordonner.x, self.cordonner.x + hauteur):
            for c in range(self.cordonner.y, self.cordonner.y + largeur):
                if 0 <= l < len(grille) and 0 <= c < len(grille[0]):
                    # Vérifier si c'est une case d'atmosphère
                    est_atmosphere = False
                    for dl in range(-1, 2):
                        for dc in range(-1, 2):
                            nl, nc = l + dl, c + dc
                            if (0 <= nl < len(grille) and 0 <= nc < len(grille[0]) and 
                                grille[nl][nc].type == Type.PLANETE):
                                est_atmosphere = True
                                break
                        if est_atmosphere:
                            break
                    
                    grille[l][c].type = Type.ATMOSPHERE if est_atmosphere else Type.VIDE

    def deplacement(self, case_cible: Tuple[int, int], grille: List[List[Point]], ships: List["Ship"]):
        """Effectue un déplacement ou une attaque vers la case cible."""
        if self.id is None: 
            raise ValueError("Ship.id non défini")
            
        ligne, colonne = case_cible
        cible_direction = self.aperçu_direction

        # ---- Attaque ----
        positions_attaque = self.positions_possibles_attaque(grille, direction=cible_direction)
        if case_cible in positions_attaque:
            # Chercher un vaisseau ennemi à cette position
            cible_ship = self.trouver_vaisseau_a_position(ships, ligne, colonne)
            if cible_ship and cible_ship.id != self.id:
                self.attaquer(cible_ship)
                if cible_ship.est_mort():
                    # Restaurer le terrain sous le vaisseau détruit
                    cible_ship.liberer_position(grille)
                    ships.remove(cible_ship)
                return True
            
            # Si c'est un astéroïde et qu'on peut miner
            if grille[ligne][colonne].type == Type.ASTEROIDE and self.peut_miner:
                self.miner_asteroide(grille, colonne, ligne)
                return True

        # ---- Déplacement ----
        positions_deplacement = self.positions_possibles_adjacentes(grille, direction=cible_direction)
        if case_cible not in positions_deplacement:
            return False
        
        # Sauvegarder les types de terrain actuels sous le vaisseau
        terrain_sous_vaisseau = []
        ancienne_largeur, ancienne_hauteur = self.donner_dimensions(self.direction)
        for l in range(self.cordonner.x, self.cordonner.x + ancienne_hauteur):
            for c in range(self.cordonner.y, self.cordonner.y + ancienne_largeur):
                if 0 <= l < len(grille) and 0 <= c < len(grille[0]):
                    # Déterminer le type de terrain à restaurer
                    if grille[l][c].type == Type.VAISSEAU:
                        # Vérifier si c'est une case d'atmosphère
                        est_atmosphere = False
                        for dl in range(-1, 2):
                            for dc in range(-1, 2):
                                nl, nc = l + dl, c + dc
                                if (0 <= nl < len(grille) and 0 <= nc < len(grille[0]) and 
                                    grille[nl][nc].type == Type.PLANETE):
                                    est_atmosphere = True
                                    break
                            if est_atmosphere:
                                break
                        
                        terrain_type = Type.ATMOSPHERE if est_atmosphere else Type.VIDE
                    else:
                        terrain_type = grille[l][c].type
                    
                    terrain_sous_vaisseau.append((l, c, terrain_type))
        
        # Libérer l'ancienne position avec les bons types de terrain
        for l, c, terrain_type in terrain_sous_vaisseau:
            grille[l][c].type = terrain_type
        
        # Vérifier la collision à la nouvelle position
        if self.verifier_collision(grille, ligne, colonne, cible_direction, ignorer_self=False):
            # Mettre à jour la position
            self.cordonner._x = ligne
            self.cordonner._y = colonne
            self.direction = cible_direction
            
            # Occuper la nouvelle position
            self.occuper_plateau(grille, Type.VAISSEAU)
            
            # Mise à jour de l'animator
            largeur, hauteur = self.donner_dimensions(self.direction)
            x = colonne * TAILLE_CASE + OFFSET_X
            y = ligne * TAILLE_CASE

            self.animator.x = x
            self.animator.y = y
            self.animator.pixel_w = largeur * TAILLE_CASE
            self.animator.pixel_h = hauteur * TAILLE_CASE

            # Mise à jour des angles
            self.prevision.angle = self.animator.angle
            self.prevision.alpha = 0
            
            angles = {"haut": 0, "droite": -90, "gauche": 90, "bas": 180}
            if cible_direction in angles:
                self.animator.target_angle = angles[cible_direction]
                self.prevision.target_angle = angles[cible_direction]

            self.animator.update_and_draw()
            return True
        else:
            # Remettre l'occupation à l'ancienne position en cas d'échec
            self.occuper_plateau(grille, Type.VAISSEAU)
            return False

    # ------------ ROTATION (aperçu) ------------
    def rotation_aperçu(self, grille: List[List[Point]]):
        """Effectue une rotation de l'aperçu du vaisseau."""
        ordre = ["haut", "droite", "bas", "gauche"]
        idx = ordre.index(self.aperçu_direction) if self.aperçu_direction in ordre else 0
        nouvelle_direction = ordre[(idx + 1) % len(ordre)]

        centre_l, centre_c = self._centre_depuis_coin(
            self.aperçu_cordonner.x, self.aperçu_cordonner.y, self.aperçu_direction
        )
        nouvelle_ligne, nouvelle_col = self._coin_depuis_centre(centre_l, centre_c, nouvelle_direction)
        
        largeur, hauteur = self.donner_dimensions(nouvelle_direction)
        nb_lignes, nb_colonnes = len(grille), len(grille[0])

        # Vérifier si la rotation est possible
        if (0 <= nouvelle_ligne <= nb_lignes - hauteur and 
            0 <= nouvelle_col <= nb_colonnes - largeur):
            
            # Mise à jour de l'aperçu
            self.aperçu_direction = nouvelle_direction
            self.aperçu_cordonner._x = nouvelle_ligne
            self.aperçu_cordonner._y = nouvelle_col
            
            # Mise à jour du visualiseur de prévision
            x = nouvelle_col * TAILLE_CASE + OFFSET_X
            y = nouvelle_ligne * TAILLE_CASE
            w, h = largeur * TAILLE_CASE, hauteur * TAILLE_CASE

            self.prevision.x = x
            self.prevision.y = y
            self.prevision.pixel_w = w
            self.prevision.pixel_h = h

            angles = {"haut": 0, "droite": -90, "gauche": 90, "bas": 180}
            if nouvelle_direction in angles:
                self.prevision.angle = angles[nouvelle_direction]
                self.prevision.target_angle = angles[nouvelle_direction]

    def rotation_aperçu_si_possible(self, case_souris: Tuple[int, int], grille: List[List[Point]]):
        """Met à jour l'aperçu à la position de la souris et effectue une rotation."""
        self.aperçu_cordonner._x = case_souris[0]
        self.aperçu_cordonner._y = case_souris[1]
        
        self.prevision.x = case_souris[1] * TAILLE_CASE + OFFSET_X
        self.prevision.y = case_souris[0] * TAILLE_CASE
        
        self.rotation_aperçu(grille)


# ------------ Sous-classes spécialisées ------------

class Petit(Ship):
    """Vaisseau de petite taille - rapide et agile."""
    def __init__(self, pv_max: int, attaque: int, port_attaque: int, port_deplacement: int, 
                 cout: int, valeur_mort: int, taille: Tuple[int,int], peut_miner: bool, 
                 peut_transporter: bool, image: pygame.Surface, tier: int, 
                 cordonner: Point, id: Optional[int] = None, path: str = None):
        super().__init__(pv_max, attaque, port_attaque, port_deplacement, cout, valeur_mort,
                         taille, peut_miner, peut_transporter, image,
                         tier, cordonner, id, path)

class Moyen(Ship):
    """Vaisseau de taille moyenne - équilibré."""
    def __init__(self, pv_max: int, attaque: int, port_attaque: int, port_deplacement: int,
                 cout: int, valeur_mort: int, taille: Tuple[int,int], peut_miner: bool,
                 peut_transporter: bool, image: pygame.Surface, tier: int,
                 cordonner: Point, id: Optional[int] = None, path: str = None):
        super().__init__(pv_max, attaque, port_attaque, port_deplacement, cout, valeur_mort,
                         taille, peut_miner, peut_transporter, image,
                         tier, cordonner, id, path)

class Lourd(Ship):
    """Vaisseau lourd - résistant mais lent."""
    def __init__(self, pv_max: int, attaque: int, port_attaque: int, port_deplacement: int,
                 cout: int, valeur_mort: int, taille: Tuple[int,int], peut_miner: bool,
                 peut_transporter: bool, image: pygame.Surface, tier: int,
                 cordonner: Point, id: Optional[int] = None, path: str = None):
        super().__init__(pv_max, attaque, port_attaque, port_deplacement, cout, valeur_mort,
                         taille, peut_miner, peut_transporter, image,
                         tier, cordonner, id, path)

class Foreuse(Ship):
    """Vaisseau spécialisé dans le minage d'astéroïdes."""
    def __init__(self, pv_max: int, attaque: int, port_attaque: int, port_deplacement: int,
                 cout: int, valeur_mort: int, taille: Tuple[int,int], peut_miner: bool,
                 peut_transporter: bool, image: pygame.Surface, tier: int,
                 cordonner: Point, id: Optional[int] = None, path: str = None):
        super().__init__(pv_max, attaque, port_attaque, port_deplacement, cout, valeur_mort,
                         taille, peut_miner, peut_transporter, image,
                         tier, cordonner, id, path)
        # Les foreuses peuvent toujours miner
        self.peut_miner = True

    def miner_asteroide(self, grille: List[List[Point]], x: int, y: int) -> bool:
        """Version améliorée du minage pour les foreuses."""
        if super().miner_asteroide(grille, x, y):
            # Les foreuses récupèrent plus de ressources
            # Ici on pourrait ajouter bonus de ressources
            return True
        return False

class Transport(Ship):
    """Vaisseau de transport - peut transporter d'autres vaisseaux."""
    def __init__(self, pv_max: int, attaque: int, port_attaque: int, port_deplacement: int,
                 cout: int, valeur_mort: int, taille: Tuple[int,int], peut_miner: bool,
                 peut_transporter: bool, image: pygame.Surface, tier: int,
                 cordonner: Point, id: Optional[int] = None, path: str = None):
        super().__init__(pv_max, attaque, port_attaque, port_deplacement, cout, valeur_mort,
                         taille, peut_miner, peut_transporter, image,
                         tier, cordonner, id, path)
        # Cargaison pour transporter d'autres vaisseaux
        self.cargaison: List[Optional[Ship]] = [None, None, None]
        self.peut_transporter = True

    def ajouter_cargo(self, ship: Ship) -> bool:
        """Ajoute un vaisseau à la cargaison."""
        if not self.peut_transporter:
            return False
            
        for i in range(len(self.cargaison)):
            if self.cargaison[i] is None:
                self.cargaison[i] = ship
                return True
        return False

    def retirer_cargo(self, index: int, ligne: int, colonne: int, grille: List[List[Point]], ships: List[Ship]) -> bool:
        """Retire un vaisseau de la cargaison et le place sur la grille."""
        if 0 <= index < len(self.cargaison):
            ship = self.cargaison[index]
            if ship is None:
                return False
                
            # Vérifier si la position est libre
            if not ship.verifier_collision(grille, ligne, colonne, ship.direction):
                return False
                
            self.cargaison[index] = None
            ship.cordonner._x = ligne
            ship.cordonner._y = colonne
            ship.direction = "haut"
            ship.occuper_plateau(grille, Type.VAISSEAU)
            
            # Remettre le vaisseau dans la liste des vaisseaux actifs
            if ship not in ships:
                ships.append(ship)
            return True
        return False

    def _taille_vaisseau(self, ship: Ship) -> int:
        """Détermine la taille d'un vaisseau pour l'affichage."""
        if isinstance(ship, Petit):
            return 1
        elif isinstance(ship, Moyen):
            return 2
        else:
            return 3

    def afficher_cargaison(self, fenetre: pygame.Surface):
        """Affiche les vaisseaux transportés."""
        for i, ship in enumerate(self.cargaison):
            if ship is None:
                continue
            mini_img = pygame.transform.scale(ship.image, (20, 20))
            x = (self.cordonner.y * TAILLE_CASE) + OFFSET_X + (i * 22)
            y = self.cordonner.x * TAILLE_CASE - 22
            fenetre.blit(mini_img, (x, y))

    def positions_debarquement(self, ship_stocke: Ship, grille: List[List[Point]]) -> List[Tuple[int, int]]:
        """Trouve les positions valides pour débarquer un vaisseau."""
        positions_valides = []
        port = ship_stocke.port_deplacement
        nb_lignes = len(grille)
        nb_colonnes = len(grille[0])

        for dy in range(-port, port + 1):
            for dx in range(-port, port + 1):
                if abs(dy) + abs(dx) > port:
                    continue
                    
                nl = self.cordonner.x + dy
                nc = self.cordonner.y + dx
                
                if ship_stocke.verifier_collision(grille, nl, nc, ship_stocke.direction):
                    positions_valides.append((nl, nc))

        return positions_valides