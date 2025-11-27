import math
from typing import Dict, List, Tuple, Optional
from classes.MotherShip import MotherShip
from classes.Ship import Petit, Ship
from classes.Point import Point, Type
from blazyck import PETIT_SCORE
from classes.GlobalVar.ScreenVar import ScreenVar
from classes.GlobalVar.GridVar import GridVar
import random

# ---- Fonctions utilitaires ----

def distance(a: Tuple[int,int], b: Tuple[int,int]) -> float:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# ---- Fonctions d'utilité ----

def utility_attack_pos(ship: Ship, enemies: List[Ship], pos: Tuple[int,int]) -> float:
    score = 0
    for enemy in enemies:
        d = distance(pos, (enemy.cordonner.x, enemy.cordonner.y))
        # Quand le vaisseau peut attaquer l'ennemi il vat vers les ennemis
        if ship.port_attaque != 0:
            if isinstance(enemy, MotherShip): # Score de base qui fait avancer le vaisseau vers la base ennemie
                score += max(0, ((GridVar.nb_cells_x * GridVar.nb_cells_y) - d)/(GridVar.nb_cells_x * GridVar.nb_cells_y))
            if d <= ship.port_attaque:
                score += 200
            else:
                score += max(0, PETIT_SCORE[enemy.__class__.__name__] - 10 * d)
        
        # Quand le vaisseau ne peut pas attaquer l'ennemi il le fuit
        else:
            score += d / (GridVar.nb_cells_x * GridVar.nb_cells_y)
    
    return score

def utility_defend_pos(ship: Ship, allies: List[Ship], enemies: List[Ship], pos: Tuple[int,int]) -> float:
    score : int = 0
    danger_max : int = 0
    for ally in allies:
        if ally == ship or isinstance(ally, Petit):
            continue
        dist = distance(pos, (ally.cordonner.x, ally.cordonner.y))
        if dist <= 2:
            score = 0
        else:
            score += max(0, (PETIT_SCORE[ally.__class__.__name__] * 10 - dist))
        # Vérifie si des ennemis sont proches de l’allié
        for e in enemies:
            danger = distance((ally.cordonner.x, ally.cordonner.y), (e.cordonner.x, e.cordonner.y))
            if danger <= 20:    
                if danger > danger_max:
                    danger_max = danger
        if danger_max:
            score += max(0, PETIT_SCORE[ally.__class__.__name__] - 10 * danger_max)

        # Vérifie si d'autre vaisseau petit sont proches de l'allié
        if not isinstance(ally, Petit):
            for a in allies:
                if a == ally:
                    continue
                dist = distance((ally.cordonner.x, ally.cordonner.y), (a.cordonner.x, a.cordonner.y))
                if dist <= 7:    
                    score = score // 2

    return score

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

def choose_random_best_action(ship: Ship, grille, allies, enemies) -> Tuple[str, Tuple[int, int]]:
    old_pos = (ship.cordonner.x, ship.cordonner.y)
    positions = ship.positions_possibles_adjacentes(grille)
    positions.append(old_pos)

    # Évaluer toutes les positions
    scored_positions = []
    for pos in positions:
        score = evaluate_position(ship, pos, grille, allies, enemies)
        if score != 0:
            scored_positions.append((pos, score))

    # Si aucune position valable → rester sur place
    if not scored_positions:
        return ("stay", old_pos)

    # Trier par score décroissant
    scored_positions.sort(key=lambda x: x[1], reverse=True)

    # Prendre une position aléatoire parmi les 3 meilleures (ou moins si <3)
    top_choices = scored_positions[:3]
    best_pos = random.choice(top_choices)[0]

    # Vérifier si une cible est à portée (attaque prioritaire)
    cible = None
    best_ship_score = -math.inf
    if ship.port_attaque > 0:
        for e in enemies:
            if est_cible_a_portee(ship, e, grille):
                score = score_ship(ship, e)
                if score > best_ship_score:
                    best_ship_score = score
                    cible = e

    # Si une cible est trouvée → attaquer
    if cible:
        return ("attack", (cible.cordonner.x, cible.cordonner.y))

    # Si plus de déplacement possible → ne pas bouger
    if ship.port_deplacement == 0:
        return ("stay", old_pos)

    # Sinon → bouger vers la position choisie
    if best_pos == old_pos:
        return ("stay", best_pos)

    return ("move", best_pos)

def ia_petit_play(ship: Ship, map_obj, tous_les_vaisseaux: List[Ship]) -> bool:


    # Si le vaisseau est mort → tour fini
    if ship.est_mort():

        return True

    # Si le vaisseau ne peut rien faire → tour fini
    if ship.port_deplacement == 0 and ship.port_attaque == 0:

        return True

    sorted_ships = ally_or_enemy(ship, tous_les_vaisseaux)
    move = choose_best_action(ship, map_obj.grille, sorted_ships["allies"], sorted_ships["enemies"])

    # ---- ACTION : Déplacement ----
    if move[0] == "move":
        # print(f"MOVE {ship.cordonner} -> {move[1]}")
        action_ok = ship.deplacement(move[1], map_obj.grille, tous_les_vaisseaux)

        # Si le déplacement a réussi, on attend la fin avant de continuer
        if action_ok:
            ship.port_deplacement = max(0, ship.port_deplacement - 1)
        else:
            # S’il n’a pas pu bouger, il a fini (aucune action possible)
            return True

    # ---- ACTION : Attaque ----
    elif move[0] == "attack":
        if ship.port_attaque > 0:
            cible = get_ship(move[1], tous_les_vaisseaux)
            if cible:
                # print(f"ATTACK {cible} -> {move[1]}")
                ship.attaquer(cible)
                ship.port_attaque = max(0, ship.port_attaque - 1)
        #     else:
        #         print(f"{ship.id} a voulu attaquer, mais cible introuvable")
        # else:
        #     print(f"{ship.id} ne peut plus attaquer")

    # ---- ACTION : Rester ----
    elif move[0] == "stay":
        return True

    # ---- Vérifie s’il peut encore jouer ----
    if ship.port_deplacement == 0 and ship.port_attaque == 0:
        return True

    return False

def ia_petit_play_random(ship : Ship, map_obj, tous_les_vaisseaux : List[Ship]) -> bool:
    
    if ship.port_deplacement == 0 and ship.port_attaque == 0:
        return True
    if not ship.est_mort():
        sorted_ships = ally_or_enemy(ship, tous_les_vaisseaux)
        move = choose_random_best_action(ship, map_obj.grille, sorted_ships["allies"], sorted_ships["enemies"])
        if move[0] == "move":
            ship.deplacement(move[1], map_obj.grille, tous_les_vaisseaux)
        elif move[0] == "stay":
            return True
        elif move[0] == "attack":
            if ship.port_attaque == 0:
                return True
            else:
                cible = get_ship(move[1], tous_les_vaisseaux)
                if cible:
                    # print(f"ATTACK {cible} -> {move[1]}")
                    ship.attaquer(cible)
    return False