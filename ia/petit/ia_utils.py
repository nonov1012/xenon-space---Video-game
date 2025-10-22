import math
from typing import Dict, List, Tuple, Optional
from classes.MotherShip import MotherShip
from classes.Ship import Petit, Ship
from classes.Point import Point, Type
from blazyck import NB_CASE_X, NB_CASE_Y, PETIT_SCORE

# ---- Fonctions utilitaires ----

def distance(a: Tuple[int,int], b: Tuple[int,int]) -> float:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# ---- Fonctions d'utilité ----

def utility_attack_pos(ship: Ship, enemies: List[Ship], pos: Tuple[int,int]) -> float:
    score = 0
    for enemy in enemies:
        d = distance(pos, (enemy.cordonner.x, enemy.cordonner.y))
        if isinstance(enemy, MotherShip): # Score de base qui fait avancer le vaisseau vers la base ennemie
            score += max(0, ((NB_CASE_X * NB_CASE_Y) - d)/(NB_CASE_X * NB_CASE_Y))
        if d <= ship.port_attaque:
            score += 200
        else:
            score += max(0, PETIT_SCORE[enemy.__class__.__name__] - 10 * d)
    
    return score

def utility_defend_pos(ship: Ship, allies: List[Ship], enemies: List[Ship], pos: Tuple[int,int]) -> float:
    score : int = 0
    danger_max : int = 0
    for ally in allies:
        if ally == ship:
            continue
        dist = distance(pos, (ally.cordonner.x, ally.cordonner.y))
        # Vérifie si des ennemis sont proches de l’allié
        for e in enemies:
            danger = distance((ally.cordonner.x, ally.cordonner.y), (e.cordonner.x, e.cordonner.y))
            if danger <= 20:    
                if danger > danger_max:
                    danger_max = danger
        if danger_max:
            score += max(0, PETIT_SCORE[ally.__class__.__name__] - 10 * dist)

    return score

"""
def utility_mine(ship: Ship, grille: List[List[Point]]) -> float:
    if not ship.peut_miner:
        return 0
    score = 0
    for dy in range(-ship.port_deplacement, ship.port_deplacement + 1):
        for dx in range(-ship.port_deplacement, ship.port_deplacement + 1):
            y = ship.cordonner.x + dy
            x = ship.cordonner.y + dx
            if 0 <= y < len(grille) and 0 <= x < len(grille[0]):
                if grille[y][x].type == Type.ASTEROIDE:
                    score += 100 / (1 + abs(dx) + abs(dy))
    return score
"""

# ---- Évaluation globale ----

def evaluate_position(ship: Ship, pos: Tuple[int,int], grille, allies, enemies) -> float:
    # On ne bouge plus le vrai vaisseau, on simule simplement ses coordonnées
    x, y = pos
    if ship.port_deplacement <= 0:
        return 0
    else:
        score = (
            1.0 * utility_attack_pos(ship, enemies, (x, y))
            + 0.8 * utility_defend_pos(ship, allies, enemies, (x, y))
        )

        return score

# ---- Choix de l’action ----

def ally_or_enemy(ur_ship: Ship, all_ships: List[Ship], res: Dict[str, List[Ship]] = None) -> Dict[str, List[Ship]]:
    if res is None:
        res = {"allies": [], "enemies": []}

    if not all_ships:
        return res

    a_ship: Ship = all_ships[0]
    ur_id = ur_ship.joueur
    ship_id = a_ship.joueur

    if ship_id == ur_id:
        res["allies"].append(a_ship)
    else:
        res["enemies"].append(a_ship)

    return ally_or_enemy(ur_ship, all_ships[1:], res)

def get_ship(coord: Tuple[int,int], ships: List[Ship]) -> Ship:
    for s in ships:
        if s.cordonner.x == coord[0] and s.cordonner.y == coord[1]:
            return s
    return None

def score_ship(ship: Ship, cible: Ship) -> float:
    diviseur = cible.pv_actuel // ship.attaque if ship.attaque > 0 else 1
    if diviseur <= 0:
        diviseur = 1
    return PETIT_SCORE[cible.__class__.__name__] / diviseur


def est_cible_a_portee(ship: Ship, cible: Ship, grille: list[list["Point"]]) -> bool:
        """Vérifie si AU MOINS une case du vaisseau cible est dans la portée d'attaque."""
        positions_portee = ship.positions_possibles_attaque(grille, direction=ship.direction)

        largeur, hauteur = cible.donner_dimensions(cible.direction)

        # Vérifie chaque case occupée par le vaisseau cible
        for dy in range(hauteur):
            for dx in range(largeur):
                case_x = cible.cordonner.x + dy
                case_y = cible.cordonner.y + dx
                if (case_x, case_y) in positions_portee:
                    return True

        return False

def choose_best_action(ship: Ship, grille, allies, enemies) -> Tuple[str, Tuple[int,int]]:
    old_pos = (ship.cordonner.x, ship.cordonner.y)
    positions = ship.positions_possibles_adjacentes(grille)
    positions.append((ship.cordonner.x, ship.cordonner.y))

    best_pos = (ship.cordonner.x, ship.cordonner.y)
    best_score = -math.inf
    for pos in positions:
        score = evaluate_position(ship, pos, grille, allies, enemies)
        if score == 0:
            continue
        if score > best_score:
            best_score = score
            best_pos = pos
    
    cible = None
    best_ship = 0
    if ship.port_attaque > 0:
        for e in enemies:
            if est_cible_a_portee(ship, e, grille):
                score = score_ship(ship, e)
                if best_ship < score:
                    best_ship = score
                    cible = e
    
    if cible:
        return ("attack", (cible.cordonner.x, cible.cordonner.y))
    if ship.port_deplacement == 0:
        return ("stay", old_pos)
    if best_pos == (ship.cordonner.x, ship.cordonner.y):
        return ("stay", best_pos)

    # Sinon, se déplacer vers la meilleure position choisie
    return ("move", best_pos)