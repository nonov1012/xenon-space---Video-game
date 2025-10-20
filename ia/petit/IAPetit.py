from __future__ import annotations
import math
import os
from classes import MotherShip, Turn
from classes.Point import Type
from classes.Ship import Petit, Ship
from blazyck import NB_CASE_X, NB_CASE_Y, SHIPS_PATH

class IAPetit(Petit):
    from classes.Point import Point
    from classes.Turn import Turn

    def __init__(self : IAPetit, coordonnees : Point, id : int, joueur_id : int) -> None:
        super().__init__(cordonner=coordonnees, id=id, joueur=joueur_id, path=os.path.join(SHIPS_PATH, "petit")) 
        self.vision : int = self.port_deplacement + self.port_attaque # La vision est le double du port de déplacement

    def value_ship(ship: Ship) -> float:
        """ Calcule une valeur pour un vaisseau en fonction de ses caractéristiques. """
        valeur = (ship.pv_actuel / ship.pv_max) + ship.attaque + ship.port_attaque_max * 100 + ship.port_deplacement_max * 100
        return valeur

    def get_closest_targets(self, ships: list[Ship]) -> list[tuple[Ship, float]]:
        """Retourne les ennemis dans le champ de vision sous forme [(ship, distance)]."""
        results = []
        for ship in ships:
            if ship.est_mort() or ship.joueur == self.joueur:
                continue

            distance = abs(ship.cordonner.x - self.cordonner.x) + abs(ship.cordonner.y - self.cordonner.y)
            if distance < self.vision:
                results.append((ship, distance))
        return results

        
    def score_attaquer(self, ships: list[tuple[Ship, float]]) -> float:
        """ 
        Calcule un score pour l'action d'attaquer un ennemi.
        Le score est plus élevé si :
        - les ennemis sont proches,
        - les ennemis ont peu de vie.
        - le nombre de déplacement de ce vaisseau est élevé.
        le score est réduit proportionnellement au nombre d'ennemis visibles.
        """
        if not ships:
            return 0.0

        score = 0.0

        for ship, distance in ships:
            if distance == 0:  # allié
                score += IAPetit.value_ship(ship)
                continue

            # Plus l'ennemi est proche, plus le score augmente
            if distance < self.port_attaque + self.port_deplacement:
                score += IAPetit.value_ship(ship)  # bonus si à portée d'attaque
            else:
                score += IAPetit.value_ship(ship) / (distance + 1)

            # Plus l'ennemi a peu de vie, plus le score augmente
            # pour ça on calcule le nombre de coups pour le tuer
            coups_necessaires = math.ceil(ship.pv_actuel / self.attaque) # ceil pour arrondir à l'entier supérieur
            score -= coups_necessaires * 100

        return score

    def score_fuir(self, ships: list[tuple[Ship, float]]) -> float:
        """
            On définit un score pour l'action de fuir un ennemi.
            Plus le score est élevé, plus l'action est prioritaire.
            Le score est basé : 
             - la vie du vaisseau (plus la vie est basse, plus le score est élevé)
             - le d'alliés proches (fait baisser le score)
             - le nombre d'ennemis qui on l'a portée de l'attaquer (fait augmenter le score)
        """
        score = 0.0

        # Plus la vie est basse, plus le score augmente
        score += IAPetit.value_ship(self)

        # Compte les alliés proches
        for ship, distance in ships:
            if distance == 0:  # allié
                score -= IAPetit.value_ship(ship)  # chaque allié proche fait baisser le score
                continue

            if distance + ship.port_attaque >= self.port_deplacement:
                score += 1.25 * IAPetit.value_ship(ship)  # chaque ennemi qui peut nous attaquer augmente le score de 2
            elif distance > self.port_deplacement:
                score += IAPetit.value_ship(ship)  # chaque ennemi qui peut nous atteindre augmente le score de 1

        return score
    
    def valuation_attack(self, ships: list[Ship]) -> float:
        """
        - Plus le vaisseau est proche de la base ennemie ou d'un vaisseau ennemi, plus le score augmente
        """
        valuation : int = 0
        
        for ship in ships:
            if ship.joueur != self.joueur:
                valuation += (abs(ship.cordonner.x - self.cordonner.x) * NB_CASE_X) + (abs(ship.cordonner.y - self.cordonner.y) * NB_CASE_Y)
            
        return valuation
    
    def prevision_move_attack(self, ships: list[Ship], grille: list[list["Point"]]):
        """Se déplace vers l’ennemi le plus proche, en anticipant légèrement son mouvement."""
        enemies = [s for s in ships if s.joueur != self.joueur and not s.est_mort()]
        if not enemies:
            return

        # Trouver la cible la plus proche
        cible = min(enemies, key=lambda s: abs(s.cordonner.x - self.cordonner.x) + abs(s.cordonner.y - self.cordonner.y))

        # Prédiction simple du déplacement futur de la cible
        dx = 0
        dy = 0
        if cible.direction == "haut":
            dx = -1
        elif cible.direction == "bas":
            dx = 1
        elif cible.direction == "gauche":
            dy = -1
        elif cible.direction == "droite":
            dy = 1

        x_pred = cible.cordonner.x + dx
        y_pred = cible.cordonner.y + dy

        # Trouve un chemin avec A*
        path, cost = self.a_star(grille,
                                (self.cordonner.x, self.cordonner.y),
                                (x_pred, y_pred),
                                self.direction,
                                self.port_deplacement)
        if path:
            next_pos = path[min(self.port_deplacement, len(path) - 1)]
            self.deplacement(next_pos, grille, ships)

    def play_flee_mode(self, ships: list[Ship], grille: list[list["Point"]]):
        """Fuit dans la direction opposée à la moyenne des ennemis visibles."""
        enemies = [s for s in ships if s.joueur != self.joueur and not s.est_mort()]
        if not enemies:
            return

        avg_x = sum(s.cordonner.x for s in enemies) / len(enemies)
        avg_y = sum(s.cordonner.y for s in enemies) / len(enemies)

        # Direction opposée
        dx = -1 if avg_x > self.cordonner.x else 1 if avg_x < self.cordonner.x else 0
        dy = -1 if avg_y > self.cordonner.y else 1 if avg_y < self.cordonner.y else 0

        # Déplacement limité par la portée
        new_x = self.cordonner.x + dx * self.port_deplacement
        new_y = self.cordonner.y + dy * self.port_deplacement

        path, cost = self.a_star(grille,
                                (self.cordonner.x, self.cordonner.y),
                                (new_x, new_y),
                                self.direction,
                                self.port_deplacement)
        if path:
            next_pos = path[min(self.port_deplacement, len(path) - 1)]
            self.deplacement(next_pos, grille, ships)

    def play(self, ships: list[Ship], grille: list[list["Point"]]) -> None:
        """
        L'IA choisit une seule action par tour :
        - attaquer si un ennemi est proche et le score d'attaque est le plus élevé
        - fuir si elle est menacée
        - aller vers la base adverse sinon
        Elle peut se déplacer de plusieurs cases tant qu'il lui reste du déplacement.
        """
        # Récupère les cibles dans le champ de vision
        targets = self.get_closest_targets(ships)

        if not targets:
            for ship in ships:
                if ship.joueur != self.joueur and isinstance(ship, MotherShip):
                    self.deplacement(MotherShip.cordonner, grille, ships)
            return

        # Calcul des scores pour chaque comportement
        score_attaque = self.score_attaquer(targets)
        score_fuite = self.score_fuir(targets)

        # Sélectionne l'action prioritaire
        etat = {
            "attaquer": score_attaque,
            "fuir": score_fuite,
        }
        etat_choisis = max(etat, key=etat.get)

        # Boucle principale : le vaisseau agit tant qu'il peut encore se déplacer ou attaquer
        passed = False
        while not passed:
            # Met à jour les cibles visibles
            targets = self.get_closest_targets(ships)

            # Si aucune cible visible -> fin de tour
            if not targets:
                passed = True
                continue

            # Trie les cibles : plus faible valeur en premier (ennemi "intéressant")
            targets.sort(key=lambda x: IAPetit.value_ship(x[0]) / (x[1] + 1))
            cible, distance_to_target = targets[0]

            # Si la cible est à portée d’attaque, on attaque
            if distance_to_target <= self.port_attaque and self.port_attaque > 0:
                self.attaquer(cible)
                passed = True  # Fin du tour après attaque
                continue

            # Sinon, on se déplace selon la stratégie choisie
            if self.deplacement > 0:
                if etat_choisis == "attaquer":
                    self.prevision_move_attack(ships, grille)
                elif etat_choisis == "fuir":
                    self.play_flee_mode(ships, grille)
            else:
                passed = True  # Plus de déplacement possible → fin du tour
