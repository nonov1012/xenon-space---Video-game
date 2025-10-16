import math
import os
from classes import Turn
from classes.Ship import Petit, Ship
from blazyck import SHIPS_PATH

class IAPetit(Petit):
    from __future__ import annotations
    from classes.Point import Point
    from classes.Turn import Turn

    def __init__(self : IAPetit, coordonnees : Point, id : int, joueur_id : int) -> None:
        super().__init__(cordonner=coordonnees, id=id, joueur=joueur_id, path=os.path.join(SHIPS_PATH, "petit")) 
        self.vision : int = self.port_deplacement + self.port_attaque # La vision est le double du port de déplacement

    def value_ship(ship: Ship) -> float:
        """ Calcule une valeur pour un vaisseau en fonction de ses caractéristiques. """
        valeur = (ship.pv_actuel / ship.pv_max) + ship.attaque + ship.port_attaque_max * 100 + ship.port_deplacement_max * 100
        return valeur

    def get_closest_targets(self, ships: list[Ship], ally : bool = True) -> list[Ship]:
        """
        Retourne les `nb` ennemis les plus proches dans le champ de vision.
        Les ennemis trop éloignés (> self.vision) sont exclus.
        """
        closest: dict[str, dict[Ship, float]] = {"ally": {}, "enemy": {}}

        for ship in ships:
            if ally:
                if ship.joueur == self.joueur:
                    closest["ally"][ship] = 0 # on ignore la distance de l'allié
                    continue  # on ignore les alliés
            if ship.est_mort():
                continue

            distance_to_ship = abs(ship.cordonner.x - self.cordonner.x) + abs(ship.cordonner.y - self.cordonner.y)
            if distance_to_ship >= self.vision:
                continue  # hors de vision, on ignore

            closest["enemy"][ship] = distance_to_ship

        return list(closest)
        
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
    
    def play_attack_mode(self, ships: list[Ship], grille: list[list[Point]]) -> None:
            passed = False
            while not passed:
                if self.port_attaque > 0:
                    targets = self.get_closest_targets(ships, False)
                    if targets:
                        # Trie les cibles par score puis par distance
                        targets.sort(key=lambda x: (IAPetit.value_ship(x[0]) * x[1]))

                        cible = targets[0][0]  # cible la plus faible et la plus proche

                        distance_to_target = targets[0][1]

                        if distance_to_target <= self.port_attaque:
                            # Attaque la cible
                            self.attaquer(cible)
                            passed = True  # Sortir de la boucle une fois que l'attaque est effectuée

                        # Move towards the target
                        if self.deplacement > 0:
                            direction = self.deplacement(cible.cordonner, grille, Turn.get_players_ships())
                else:
                    passed = True  

            
    def play(self, ships: list[Ship], grille: list[list["Point"]]) -> None:
        """
        L'IA choisit une seule action par tour :
        - attaquer si un ennemi est proche et le score d'attaque est le plus élevé
        - fuir si elle est menacée
        - aller vers la base adverse sinon
        """
        # Récupère les cibles dans le champ de vision
        targets = self.get_closest_targets(ships)

        if not targets:
            pass # TODO : aller vers la base ennemie
        else:
            # Calcul des scores pour chaque comportement
            score_attaque = self.score_attaquer(targets)
            score_fuite = self.score_fuir(targets)

            # Sélectionne l'action prioritaire
            etat = {
                "attaquer": score_attaque,
                "fuir": score_fuite,
            }
            etat_choisis = max(etat, key=etat.get)

            if etat_choisis == "attaquer":
                self.play_attack_mode(ships, grille)
            elif etat_choisis == "fuir":
                self.play_flee_mode(ships, grille)
                
            
