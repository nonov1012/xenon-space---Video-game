import math
import os
from classes.Ship import Petit, Ship
from blazyck import SHIPS_PATH

class IAPetit(Petit):
    from __future__ import annotations
    from classes.Point import Point
    from classes.Turn import Turn

    def __init__(self : IAPetit, coordonnees : Point, id : int, joueur_id : int) -> None:
        super().__init__(cordonner=coordonnees, id=id, joueur=joueur_id, path=os.path.join(SHIPS_PATH, "petit")) 
        self.vision : int = self.port_deplacement # La vision est le double du port de déplacement

    def get_closest_targets(self, ships: list[Ship]) -> list[Ship]:
        """
        Retourne les `nb` ennemis les plus proches dans le champ de vision.
        Les ennemis trop éloignés (> self.vision) sont exclus.
        """
        closest: dict[str, dict[Ship, float]] = {"ally": {}, "enemy": {}}

        for ship in ships:
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
                score += 1
                continue

            # Plus l'ennemi est proche, plus le score augmente
            if distance < self.port_attaque + self.port_deplacement:
                score += 2  # bonus si à portée d'attaque
            else:
                score += 1 / (distance + 1)

            # Plus l'ennemi a peu de vie, plus le score augmente
            # pour ça on calcule le nombre de coups pour le tuer
            coups_necessaires = math.ceil(ship.pv_actuel / self.attaque) # ceil pour arrondir à l'entier supérieur
            score -= coups_necessaires

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
        score += self.pv_actuel / self.pv_max

        # Compte les alliés proches
        for ship, distance in ships:
            if distance == 0:  # allié
                score -= 1
                continue
            
        score -= len(allies_proches)  # chaque allié proche réduit le score de 1

        # Compte les ennemis à portée d'attaque
        ennemis_proches = [
            s for s in ships 
            if s.joueur != self.joueur 
            and not s.est_mort()
            and abs(s.cordonner.x - self.cordonner.x) + abs(s.cordonner.y - self.cordonner.y) <= self.port_attaque
        ]
        score += len(ennemis_proches) * 2  # chaque ennemi à portée augmente le score de 2

        return score

    def score_repositionner(self, ships: list["Ship"], grille: list[list["Point"]]) -> float:
        """
        Score pour se repositionner / attendre :
        - Élevé si aucun ennemi n'est à portée et aucun allié proche
        - Plus faible si ennemis à portée
        """
        ennemis_proches = [
            s for s in ships 
            if s.joueur != self.joueur 
            and not s.est_mort()
            and abs(s.cordonner.x - self.cordonner.x) + abs(s.cordonner.y - self.cordonner.y) <= self.port_attaque
        ]
        if ennemis_proches:
            return 0.0  # prioriser attaquer ou fuir
        else:
            return 0.5  # score moyen pour se repositionner/attendre
        
    def play(self, ships: list[Ship], grille: list[list["Point"]]) -> None:
        """
        L'IA choisit une seule action par tour :
        - attaquer si un ennemi est proche et le score d'attaque est le plus élevé
        - fuir si elle est menacée
        - se repositionner sinon
        """
        # Récupère les cibles dans le champ de vision
        targets = self.get_closest_targets(ships)

        # Calcul des scores pour chaque comportement
        score_attaque = self.score_attaquer(targets)
        score_fuite = 0
        score_repos = 0

        # Sélectionne l'action prioritaire
        actions = {
            "attaquer": score_attaque,
            "fuir": score_fuite,
            "repositionner": score_repos
        }
        action_choisie = max(actions, key=actions.get)

        # Exécute uniquement l’action choisie
        if action_choisie == "attaquer":
            print(f"[IA] {self.nom} choisit d'attaquer (score={score_attaque:.2f})")
            self.action_attaquer(ships, grille)

        elif action_choisie == "fuir":
            print(f"[IA] {self.nom} choisit de fuir (score={score_fuite:.2f})")
            self.action_fuir(ships, grille)

        elif action_choisie == "repositionner":
            print(f"[IA] {self.nom} se repositionne (score={score_repos:.2f})")
            self.action_repositionner(grille)
