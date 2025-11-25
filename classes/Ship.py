import pygame
from typing import Tuple, List, Optional
from classes.GlobalVar.GridVar import GridVar
from classes.ShipAnimator import ShipAnimator
from blazyck import *
from classes.Point import Point, Type
from classes.Economie import *
from heapq import heappush, heappop
from classes.FloatingText import FloatingText
from menu.modifShips import SHIP_STATS
from collections import deque
import threading


# =======================
# Classe Ship = Vaisseau
# =======================

class Ship:
    def __init__(self,
                 pv_max: int, attaque: int, port_attaque: int, port_deplacement: int, cout: int,
                 taille: Tuple[int,int], peut_miner: bool, peut_transporter: bool, image: pygame.Surface,
                 tier: int, cordonner: Optional[Point] = None, id: Optional[int] = None,
                 path: str = None, joueur : int = 0, isAI: bool = False):
        """
        Classe de base pour tous les vaisseaux.
        
        :param pv_max: Points de vie maximum
        :param attaque: Dégâts infligés par attaque
        :param port_attaque: Portée d’attaque en cases
        :param port_deplacement: Portée de déplacement (points de mouvement)
        :param cout: Coût d’achat
        :param taille: Dimensions du vaisseau (largeur, hauteur en cases)
        :param peut_miner: True si le vaisseau peut miner
        :param peut_transporter: True si le vaisseau peut transporter
        :param image: Sprite de base du vaisseau
        :param tier: Niveau technologique
        :param cordonner: Position initiale (coin haut-gauche du vaisseau)
        :param id: Identifiant unique
        :param path: Chemin vers les assets
        :param joueur: Numéro du joueur propriétaire
        """

        # ---- Caractéristiques ----
        self.pv_max = pv_max
        self.pv_actuel = pv_max
        self.attaque = attaque
        self.port_attaque = port_attaque
        self.port_attaque_max = port_attaque
        self.port_deplacement = port_deplacement
        self.port_deplacement_max = port_deplacement
        self.cout = cout
        self.taille = tuple(taille)
        self.peut_miner = peut_miner
        self.peut_transporter = peut_transporter
        self.joueur = joueur
        self.gain = 0
        self.projectile_type = "laser"
        self.isAI = isAI

        # Inventaire (3 slots si transport possible)
        self.cargaison = [None, None, None]

        # ---- Graphisme & niveau ----
        self.image = image
        self.tier = tier

        # ---- Identifiant ----
        self.id = id

        # ---- Position ----
        if cordonner is None:
            cordonner = Point(0, 0)
        self.cordonner: Point = cordonner
        self.direction = "haut"  # direction initiale

        # ---- Prévisualisation (pour placement/rotation avant validation) ----
        self.aperçu_direction = self.direction
        self.aperçu_cordonner = Point(cordonner.x, cordonner.y)

        # ---- Gestion animations ----
        tile_coord = (cordonner.y, cordonner.x)  # Coordonnées en cases
        self.animator = ShipAnimator(path, taille, tile_coord, PV_max=pv_max, PV_actuelle=pv_max)
        self.prevision = ShipAnimator(path, taille, tile_coord, show_health=False, alpha=100)

        # Charger animations de base
        base_animations = ["base", "engine", "shield", "destruction"]
        for anim in base_animations:
            self.animator.load_animation(anim, f"{anim}.png")
            self.prevision.load_animation(anim, f"{anim}.png")

        # Ajouter animation "weapons" si le vaisseau est armé
        if self.attaque > 0 and not isinstance(self, Foreuse):
            self.animator.load_animation("weapons", "weapons.png")
            self.prevision.load_animation("weapons", "weapons.png")

        self.animator.play("base")
        self.prevision.play("base")


    # ------------ UTILITAIRES ------------
    def donner_dimensions(self, direction: str) -> Tuple[int, int]:
        """Retourne (largeur, hauteur) en fonction de la direction (rotation)."""
        if direction in ("haut", "bas"):
            return self.taille
        elif direction in ("droite", "gauche"):
            return (self.taille[1], self.taille[0])

    def _centre_depuis_coin(self, ligne_coin, colonne_coin, direction):
        """Convertit la position du coin haut-gauche en coordonnées du centre."""
        largeur, hauteur = self.donner_dimensions(direction)
        return ligne_coin + (hauteur-1)/2, colonne_coin + (largeur-1)/2

    def _coin_depuis_centre(self, centre_l, centre_c, direction):
        """Convertit la position du centre en coordonnées du coin haut-gauche."""
        largeur, hauteur = self.donner_dimensions(direction)
        return int(round(centre_l-(hauteur-1)/2)), int(round(centre_c-(largeur-1)/2))
    
    def reset_porters(self):
        self.port_attaque = self.port_attaque_max
        self.port_deplacement = self.port_deplacement_max

    # ------------ COMBAT ------------
    def attaquer(self, cible: "Ship"):
        """
        Attaque un autre vaisseau.
        - inflige des dégâts
        - déclenche animation de tir si le vaisseau est armé
        """
        if self.joueur != cible.joueur:
            if self.attaque > 0 and not isinstance(self, Foreuse):
                # Calcul position centrale de la cible
                largeur, hauteur = cible.donner_dimensions(cible.direction)
                target_x = (cible.cordonner.y * GridVar.cell_size) + (largeur * GridVar.cell_size) / 2 + GridVar.offset_x
                target_y = (cible.cordonner.x * GridVar.cell_size) + (hauteur * GridVar.cell_size) / 2

                self.animator.fire(
                    projectile_type=self.projectile_type,
                    target=(target_x, target_y),
                    is_fired=True,
                    projectile_speed=3
                )

                def appliquer_degats():
                    cible.subir_degats(self.attaque)
                    FloatingText(f"-{self.attaque}", (cible.animator.x + cible.animator.pixel_w, cible.animator.y + cible.animator.pixel_h / 2 ), color=(255, 0, 0))

                threading.Timer(1, appliquer_degats).start()

                self.port_attaque = 0
        if cible.est_mort():
            self.gain += cible.cout * POURCENT_DEATH_REWARD

    def subir_degats(self, degats):
        from classes.Turn import Turn # import fait ici pour eviter boucle import

        self.pv_actuel = max(0, self.pv_actuel - max(0, degats))
        self.animator.PV_actuelle = self.pv_actuel
        if self.pv_actuel > 0:
            self.animator.play("shield", reset=True)
        else:
            self.prevision.remove_from_list()
            self.animator.idle = False
            self.animator.play("destruction", reset=True)
            self.animator.alive = False
            # Supprimer de la liste des vaisseaux vivants
            player_ships = Turn.get_player_with_id(self.joueur).ships
            if self in player_ships:  # ou la liste globale de ships
                player_ships.remove(self)

    def est_mort(self):
        """Retourne True si le vaisseau est détruit."""
        return self.pv_actuel <= 0

    # ------------ MINAGE ------------
    def peut_miner_asteroide(self, grille: List[List[Point]], x: int, y: int) -> bool:
        """Retourne True si le vaisseau peut miner un astéroïde à (x, y)."""
        if not self.peut_miner:
            return False
        if 0 <= x < len(grille[0]) and 0 <= y < len(grille):
            return grille[y][x].type == Type.ASTEROIDE
        return False
    
    def est_autour_asteroide(self, grille: List[List[Point]]) -> bool:
        """Retourne True si le vaisseau est autour d’un astéroïde."""
        largeur, hauteur = self.donner_dimensions(self.direction)
        ligne_start = self.cordonner.x
        colonne_start = self.cordonner.y
        
        # On parcourt toutes les cases autour du vaisseau (bordure 1 case)
        for l in range(ligne_start - 1, ligne_start + hauteur + 1):
            for c in range(colonne_start - 1, colonne_start + largeur + 1):
                # Ignorer les cases à l’intérieur du vaisseau
                if ligne_start <= l < ligne_start + hauteur and colonne_start <= c < colonne_start + largeur:
                    continue
                # Vérifier limites
                if 0 <= l < len(grille) and 0 <= c < len(grille[0]):
                    if grille[l][c].type == Type.ASTEROIDE:
                        return True
        return False

    def miner_asteroide(self, grille: List[List[Point]], x: int, y: int) -> bool:
        """Mine un astéroïde → transforme la case en VIDE, ajoute potentiellement des ressources."""
        if self.peut_miner_asteroide(grille, x, y):
            grille[y][x].type = Type.VIDE
            self.gain = 75
            return True
        return False

     # ------------ INTERACTION PLATEAU ------------
    def occuper_plateau(self, grille: List[List[Point]], nouveau_type: Type, direction=None, ligne: int = None, colonne: int = None):
        """Occupe les cases correspondant à l’emprise du vaisseau avec le type donné (souvent VAISSEAU)."""
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
        """Retourne False si le vaisseau entrerait en collision avec un obstacle (planète, base, autre vaisseau)."""
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
    
    def est_a_cote_planete(self, grille: list[list[Point]]) -> bool:
        """Retourne True si le vaisseau touche une case voisine de type PLANETE."""
        largeur, hauteur = self.donner_dimensions(self.direction)
        ligne_start = self.cordonner.x
        colonne_start = self.cordonner.y
        
        # On parcourt toutes les cases autour du vaisseau (bordure 1 case)
        for l in range(ligne_start - 1, ligne_start + hauteur + 1):
            for c in range(colonne_start - 1, colonne_start + largeur + 1):
                # Ignorer les cases à l’intérieur du vaisseau
                if ligne_start <= l < ligne_start + hauteur and colonne_start <= c < colonne_start + largeur:
                    continue
                # Vérifier limites
                if 0 <= l < len(grille) and 0 <= c < len(grille[0]):
                    if grille[l][c].type == Type.PLANETE:
                        return True
        return False


    # ------------ DÉPLACEMENT / ATTAQUE ------------

    def a_star(self, grille, start, goal, direction, max_portee):
        """
        A* limité à max_portee de déplacement.
        Retourne (chemin, cout_total) ou (None, inf).
        """
        largeur, hauteur = self.donner_dimensions(direction)
        cout_case = {Type.VIDE: 1, Type.ATMOSPHERE: 2, Type.PLANETE: 9999, Type.ASTEROIDE: 9999}

        def heuristique(pos1, pos2):
            return abs(pos1[0]-pos2[0]) + abs(pos1[1]-pos2[1])

        open_set = []
        heappush(open_set, (heuristique(start, goal), 0, start, [start]))
        visited = {}

        while open_set:
            f, g, current, path = heappop(open_set)
            if current in visited and visited[current] <= g:
                continue
            visited[current] = g

            if current == goal:
                return path, g

            l, c = current
            for dl, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
                nl, nc = l + dl, c + dc
                if 0 <= nl <= len(grille)-hauteur and 0 <= nc <= len(grille[0])-largeur:
                    if not self.verifier_collision(grille, nl, nc, direction, ignorer_self=True):
                        continue

                    max_cost = 0
                    valide = True
                    for yy in range(nl, nl+hauteur):
                        for xx in range(nc, nc+largeur):
                            point = grille[yy][xx]
                            if point.type in cout_case:
                                max_cost = max(max_cost, cout_case[point.type])
                            elif point.type == Type.VAISSEAU:
                                continue
                            else:
                                valide = False
                                break
                        if not valide:
                            break

                    if valide:
                        g_next = g + max_cost
                        if g_next > max_portee:  # Limiter A* à la portée du vaisseau
                            continue
                        f_next = g_next + heuristique((nl,nc), goal)
                        heappush(open_set, (f_next, g_next, (nl,nc), path + [(nl,nc)]))

        return None, float('inf')

    def positions_possibles_adjacentes(self, grille, *, direction=None):
        if direction is None:
            direction = self.direction

        reachable = []
        largeur, hauteur = self.donner_dimensions(direction)
        nb_lignes, nb_colonnes = len(grille), len(grille[0])
        cout_case = {Type.VIDE: 1, Type.ATMOSPHERE: 2, Type.PLANETE: 9999, Type.ASTEROIDE: 9999}

        from collections import deque
        queue = deque()
        start = (self.cordonner.x, self.cordonner.y)
        queue.append((start, 0))
        visited = {start: 0}

        while queue:
            (l, c), g = queue.popleft()
            for dl, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
                nl, nc = l + dl, c + dc
                if 0 <= nl <= nb_lignes - hauteur and 0 <= nc <= nb_colonnes - largeur:
                    if not self.verifier_collision(grille, nl, nc, direction, ignorer_self=True):
                        continue

                    max_cost = 0
                    valide = True
                    for yy in range(nl, nl+hauteur):
                        for xx in range(nc, nc+largeur):
                            point = grille[yy][xx]
                            if point.type in cout_case:
                                max_cost = max(max_cost, cout_case[point.type])
                            elif point.type == Type.VAISSEAU:
                                continue
                            else:
                                valide = False
                                break
                        if not valide:
                            break

                    if valide:
                        g_next = g + max_cost
                        if g_next > self.port_deplacement:
                            continue
                        if ((nl, nc) not in visited) or (g_next < visited[(nl,nc)]):
                            visited[(nl,nc)] = g_next
                            queue.append(((nl,nc), g_next))
                            if (nl, nc) != start:
                                reachable.append((nl, nc))

        return reachable

    def positions_possibles_attaque(self, grille: List[List[Point]], direction=None):
        """Retourne toutes les cases dans la portée d’attaque (distance de Manhattan)."""
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
        """Retourne le vaisseau occupant une case donnée (ou None si vide)."""
        for ship in ships:
            largeur, hauteur = ship.donner_dimensions(ship.direction)
            if (ship.cordonner.x <= ligne < ship.cordonner.x + hauteur and
                ship.cordonner.y <= colonne < ship.cordonner.y + largeur):
                return ship
        return None

    def liberer_position(self, grille: List[List[Point]]):
        """Libère les cases occupées par le vaisseau (remet VIDE ou ATMOSPHERE)."""
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

    def est_dans_atmosphere(self, grille, l, c):
        """Retourne True si la case (l, c) est dans ou proche d'une planète."""
        for dl in range(-1, 2):
            for dc in range(-1, 2):
                nl, nc = l + dl, c + dc
                if 0 <= nl < len(grille) and 0 <= nc < len(grille[0]):
                    if grille[nl][nc].type == Type.PLANETE:
                        return True
        return False

    def deplacement(self, case_cible: Tuple[int, int], grille: list[list], ships: list["Ship"]):
        """
        Déplace le vaisseau ou attaque/miner la case cible.
        - Si la case est attaquable → attaque
        - Si la case est un astéroïde minable → mine
        - Sinon, avance vers la case, au maximum selon la portée de déplacement
        """

        if self.id is None:
            raise ValueError("Ship.id non défini")

        if self.port_deplacement <= 0:
            return False

        ligne, colonne = case_cible
        cible_direction = self.aperçu_direction

        # ---------------- Attaque ----------------
        positions_attaque = self.positions_possibles_attaque(grille, direction=cible_direction)
        if case_cible in positions_attaque:
            cible_ship = self.trouver_vaisseau_a_position(ships, ligne, colonne)
            if cible_ship and cible_ship.id != self.id:
                self.attaquer(cible_ship)
                self.port_attaque = 0
                self.prevision.alpha = 0
                if cible_ship.est_mort():
                    cible_ship.liberer_position(grille)
                    ships.remove(cible_ship)
                return True

            if grille[ligne][colonne].type == Type.ASTEROIDE and self.peut_miner:
                self.miner_asteroide(grille, colonne, ligne)
                return True

        # ---------------- Déplacement ----------------
        

        start = (self.cordonner.x, self.cordonner.y)
        queue = deque([start])
        parent = {start: None}
        visited = {start: 0}

        while queue:
            current = queue.popleft()
            l, c = current
            for dl, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
                nl, nc = l + dl, c + dc

                largeur, hauteur = self.donner_dimensions(cible_direction)
                if not (0 <= nl <= len(grille)-hauteur and 0 <= nc <= len(grille[0])-largeur):
                    continue

                if not self.verifier_collision(grille, nl, nc, cible_direction, ignorer_self=True):
                    continue

                max_cost = 0
                valide = True
                for yy in range(nl, nl+hauteur):
                    for xx in range(nc, nc+largeur):
                        point = grille[yy][xx]
                        if point.type == Type.VIDE:
                            max_cost = max(max_cost, 1)
                        elif point.type == Type.ATMOSPHERE:
                            max_cost = max(max_cost, 2)
                        elif point.type == Type.VAISSEAU:
                            continue
                        else:
                            valide = False
                            break
                    if not valide:
                        break

                if valide:
                    g_next = visited[(l,c)] + max_cost
                    if ((nl, nc) not in visited) or (g_next < visited[(nl, nc)]):
                        visited[(nl, nc)] = g_next
                        parent[(nl, nc)] = (l, c)
                        queue.append((nl, nc))

        # ---------------- Reconstituer le chemin ----------------
        node = (ligne, colonne)
        if node not in parent:
            # cible hors portée → prendre le noeud le plus proche
            distances = [(abs(node[0]-n[0]) + abs(node[1]-n[1]), n) for n in parent.keys()]
            node = min(distances)[1]

        chemin = []
        while node:
            chemin.append(node)
            node = parent.get(node)
        chemin.reverse()

        if len(chemin) < 2:
            return False

        # ---------------- Parcours du chemin ----------------
        dernier_ligne, dernier_colonne = chemin[0]
        for nl, nc in chemin[1:]:
            largeur, hauteur = self.donner_dimensions(cible_direction)
            max_cost = 0
            for yy in range(nl, nl + hauteur):
                for xx in range(nc, nc + largeur):
                    point = grille[yy][xx]
                    if point.type == Type.VIDE:
                        max_cost = max(max_cost, 1)
                    elif point.type == Type.ATMOSPHERE:
                        max_cost = max(max_cost, 2)
            if self.port_deplacement - max_cost < 0:
                break
            self.port_deplacement -= max_cost
            dernier_ligne, dernier_colonne = nl, nc

        # ---------------- Mettre à jour la position ----------------
        self.liberer_position(grille)
        self.cordonner._x = dernier_ligne
        self.cordonner._y = dernier_colonne
        self.direction = cible_direction
        self.occuper_plateau(grille, Type.VAISSEAU)

        # ---------------- Animator ----------------
        largeur, hauteur = self.donner_dimensions(self.direction)
        x = colonne * GridVar.cell_size + GridVar.offset_x
        y = ligne * GridVar.cell_size

        self.prevision.x = dernier_ligne
        self.prevision.y = dernier_colonne
        self.animator.set_target((x, y))
        self.animator.pixel_w = largeur * GridVar.cell_size
        self.animator.pixel_h = hauteur * GridVar.cell_size

        angles = {"haut": 0, "droite": -90, "gauche": 90, "bas": 180}
        if cible_direction in angles:
            self.animator.target_angle = angles[cible_direction]
            self.prevision.target_angle = angles[cible_direction]

        self.prevision.angle = self.animator.angle
        self.prevision.alpha = 0

        return True

    # ------------ ROTATION (aperçu) ------------
    def rotation_aperçu(self, grille: List[List[Point]]):
        """Effectue une rotation de l’aperçu du vaisseau (90°)."""
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
            x = nouvelle_col * GridVar.cell_size + GridVar.offset_x
            y = nouvelle_ligne * GridVar.cell_size
            w, h = largeur * GridVar.cell_size, hauteur * GridVar.cell_size

            self.prevision.x = x
            self.prevision.y = y
            self.prevision.pixel_w = w
            self.prevision.pixel_h = h

            angles = {"haut": 0, "droite": -90, "gauche": 90, "bas": 180}
            if nouvelle_direction in angles:
                self.prevision.angle = angles[nouvelle_direction]
                self.prevision.target_angle = angles[nouvelle_direction]

    def rotation_aperçu_si_possible(self, case_souris: Tuple[int, int], grille: List[List[Point]]):
        """Déplace l’aperçu à la souris puis tente une rotation si possible."""
        self.aperçu_cordonner._x = case_souris[0]
        self.aperçu_cordonner._y = case_souris[1]
        
        self.prevision.x = case_souris[1] * GridVar.cell_size + GridVar.offset_x
        self.prevision.y = case_souris[0] * GridVar.cell_size
        
        self.rotation_aperçu(grille)


# ------------ Sous-classes spécialisées ------------

class Petit(Ship):
    """Vaisseau rapide et fragile."""
    def __init__(self, cordonner: Point, id: Optional[int] = None, 
                 image: Optional[pygame.Surface] = None, joueur: int = 1):
        stats = SHIP_STATS["Petit"]
        
        # Créer l'image si non fournie
        if image is None:
            image = pygame.Surface((stats["taille"][1]*GridVar.cell_size, stats["taille"][0]*GridVar.cell_size))
            
        path = os.path.join(SHIPS_PATH, "petit")

        super().__init__(
            pv_max=stats["pv_max"],
            attaque=stats["attaque"],
            port_attaque=stats["port_attaque"],
            port_deplacement=stats["port_deplacement"],
            cout=stats["cout"],
            taille=stats["taille"],
            peut_miner=stats["peut_miner"],
            peut_transporter=stats["peut_transporter"],
            image=os.path.join(path, "base.png"),
            tier=1,
            cordonner=cordonner,
            id=id,
            path=path,
            joueur=joueur
        )
        self.animator.speed = 10
        self.projectile_type = "bullet"


class Moyen(Ship):
    """Vaisseau équilibré."""
    def __init__(self, cordonner: Point, id: Optional[int] = None, path: str = None,
                 image: Optional[pygame.Surface] = None, joueur: int = 1):
        stats = SHIP_STATS["Moyen"]
        
        if image is None:
            image = pygame.Surface((stats["taille"][1]*GridVar.cell_size, stats["taille"][0]*GridVar.cell_size))
        
        super().__init__(
            pv_max=stats["pv_max"],
            attaque=stats["attaque"],
            port_attaque=stats["port_attaque"],
            port_deplacement=stats["port_deplacement"],
            cout=stats["cout"],
            taille=stats["taille"],
            peut_miner=stats["peut_miner"],
            peut_transporter=stats["peut_transporter"],
            image=image,
            tier=1,
            cordonner=cordonner,
            id=id,
            path=path,
            joueur=joueur
        )
        self.animator.speed = 7
        self.projectile_type = "bullet"


class Lourd(Ship):
    """Vaisseau résistant mais lent."""
    def __init__(self, cordonner: Point, id: Optional[int] = None, path: str = None,
                 image: Optional[pygame.Surface] = None, joueur: int = 1):
        stats = SHIP_STATS["Lourd"]
        
        if image is None:
            image = pygame.Surface((stats["taille"][1]*GridVar.cell_size, stats["taille"][0]*GridVar.cell_size))
        
        super().__init__(
            pv_max=stats["pv_max"],
            attaque=stats["attaque"],
            port_attaque=stats["port_attaque"],
            port_deplacement=stats["port_deplacement"],
            cout=stats["cout"],
            taille=stats["taille"],
            peut_miner=stats["peut_miner"],
            peut_transporter=stats["peut_transporter"],
            image=image,
            tier=1,
            cordonner=cordonner,
            id=id,
            path=path,
            joueur=joueur
        )
        self.animator.speed = 5
        self.projectile_type = "torpedo"


class Foreuse(Ship):
    """Vaisseau spécialisé dans le minage."""
    def __init__(self, cordonner: Point, id: Optional[int] = None, path: str = None,
                 image: Optional[pygame.Surface] = None, joueur: int = 1):
        stats = SHIP_STATS["Foreuse"]
        
        if image is None:
            image = pygame.Surface((stats["taille"][1]*GridVar.cell_size, stats["taille"][0]*GridVar.cell_size))
        
        super().__init__(
            pv_max=stats["pv_max"],
            attaque=0,
            port_attaque=0,
            port_deplacement=stats["port_deplacement"],
            cout=stats["cout"],
            taille=stats["taille"],
            peut_miner=True,  # Toujours True pour les foreuses
            peut_transporter=stats["peut_transporter"],
            image=image,
            tier=1,
            cordonner=cordonner,
            id=id,
            path=path,
            joueur=joueur
        )
        self.animator.speed = 10

class Transport(Ship):
    """Vaisseau pouvant transporter d'autres vaisseaux."""
    def __init__(self, cordonner: Point, id: Optional[int] = None, path: str = None,
                 image: Optional[pygame.Surface] = None, joueur: int = 1):
        stats = SHIP_STATS["Transport"]
        
        if image is None:
            image = pygame.Surface((stats["taille"][1]*GridVar.cell_size, stats["taille"][0]*GridVar.cell_size))
        
        super().__init__(
            pv_max=stats["pv_max"],
            attaque=stats["attaque"],
            port_attaque=stats["port_attaque"],
            port_deplacement=stats["port_deplacement"],
            cout=stats["cout"],
            taille=stats["taille"],
            peut_miner=stats["peut_miner"],
            peut_transporter=True,  # Toujours True pour les transports
            image=image,
            tier=1,
            cordonner=cordonner,
            id=id,
            path=path,
            joueur=joueur
        )
        # Nombre de slots selon les stats
        nb_slots = stats.get("nb_vaisseaux", 3)
        self.cargaison: List[Optional[Ship]] = [None] * nb_slots
        self.projectile_type = "torpedo"
        self.animator.speed = 7


    def ajouter_cargo(self, ship: Ship, grille: List[List[Point]]) -> bool:
        """
        Ajoute un vaisseau à la cargaison :
        - Vérifie qu’il reste un slot libre
        - Vérifie que le vaisseau est à portée d’embarquement
        - Retire le vaisseau de la grille et de la liste des vaisseaux actifs
        - Supprime son animation du rendu
        """
        if not self.peut_transporter:
            return False

        for i in range(len(self.cargaison)):
            if self.cargaison[i] is None:
                if ship.est_mort():
                    return False

                # Libérer les cases sur la grille
                ship.liberer_position(grille)
                
                ship.animator.alpha = 0  # totalement transparent
                ship.animator.show_health = False
                

                # Ajouter dans la cargaison
                self.cargaison[i] = ship

                return True

        return False


    def retirer_cargo(self, index: int, ligne: int, colonne: int, grille: List[List[Point]], ships: List[Ship]) -> bool:
        """
        Retire un vaisseau de la cargaison et le replace sur la grille :
        - Vérifie la validité de la position
        - Réactive l’animation et le rend visible
        - Réinsère dans la liste des vaisseaux actifs
        """
        if 0 <= index < len(self.cargaison):
            ship = self.cargaison[index]
            if ship is None:
                return False

            # Vérifier que la position est valide
            if not ship.verifier_collision(grille, ligne, colonne, ship.direction):
                return False

            # Placer le vaisseau sur la carte
            ship.cordonner._x = ligne
            ship.cordonner._y = colonne
            ship.direction = "haut"
            ship.occuper_plateau(grille, Type.VAISSEAU)

            # Réactiver animations
            ship.animator.alpha = 255  # totalement transparent*
            ship.animator.show_health = True

            ship.port_deplacement = 0


            # Repositionner le sprite
            largeur, hauteur = ship.donner_dimensions(ship.direction)
            ship.animator.x = colonne * GridVar.cell_size + GridVar.offset_x
            ship.animator.y = ligne * GridVar.cell_size
            ship.animator.pixel_w = largeur * GridVar.cell_size
            ship.animator.pixel_h = hauteur * GridVar.cell_size

            # Retirer du cargo
            self.cargaison[index] = None

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
            x = (self.cordonner.y * GridVar.cell_size) + GridVar.offset_x + (i * 22)
            y = self.cordonner.x * GridVar.cell_size - 22
            fenetre.blit(mini_img, (x, y))

    def positions_debarquement(self, ship_stocke: Ship, grille: List[List[Point]]) -> List[Tuple[int, int]]:
        """Trouve les positions valides pour débarquer un vaisseau."""
        positions_valides = []
        port_entier = int(ship_stocke.port_deplacement)
        nb_lignes = len(grille)
        nb_colonnes = len(grille[0])

        for dy in range(port, port + 1):
            for dx in range(port, port + 1):
                if abs(dy) + abs(dx) > port:
                    continue
                    
                nl = self.cordonner.x + dy
                nc = self.cordonner.y + dx
                
                if ship_stocke.verifier_collision(grille, nl, nc, ship_stocke.direction):
                    positions_valides.append((nl, nc))

        return positions_valides