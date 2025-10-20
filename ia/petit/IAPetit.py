from __future__ import annotations
import math
import os
from classes.FloatingText import FloatingText
from classes.MotherShip import MotherShip
from classes.Turn import Turn
from classes.Point import Type, Point
from classes.Ship import Petit, Ship
from blazyck import NB_CASE_X, NB_CASE_Y, SHIPS_PATH

class IAPetit(Petit):

    def __init__(self : IAPetit, coordonnees : Point, id : int, joueur_id : int) -> None:
        super().__init__(cordonner=coordonnees, id=id, joueur=joueur_id, path=os.path.join(SHIPS_PATH, "petit")) 

    def value_ship(ship: Ship) -> float:
        """Calcule la dangerosité d'un vaisseau."""
        # Normalisation : ramène tout sur une base comparable (environ 0–10)
        pv_norm = (ship.pv_actuel / ship.pv_max) * 5          # santé : jusqu’à 5
        attaque_norm = (ship.attaque / 200) * 5               # attaque : jusqu’à 5
        port_attaque_norm = (ship.port_attaque_max / 10) * 3  # portée : jusqu’à 3
        port_dep_norm = (ship.port_deplacement_max / 10) * 2  # mobilité : jusqu’à 2

        return pv_norm + attaque_norm + port_attaque_norm + port_dep_norm

    def get_closest_targets(self, ships: list[Ship]) -> list[tuple[Ship, float]]:
        """Retourne les ennemis dans le champ de vision sous forme [(ship, distance)]."""
        results = []
        for ship in ships:
            if ship.est_mort() or ship.joueur == self.joueur:
                continue

            distance = abs(ship.cordonner.x - self.cordonner.x) + abs(ship.cordonner.y - self.cordonner.y)

            results.append((ship, distance))
        return results

        
    def score_attaquer(self, ships: list[tuple[Ship, float]]) -> float:
        if not ships:
            return 0.0

        score = 0.0

        for ship, distance in ships:
            if ship.joueur == self.joueur or isinstance(ship, MotherShip):
                continue

            # Plus la cible est faible, plus le score monte
            faiblesse = max(0, (1 - ship.pv_actuel / ship.pv_max) * 10)

            # Plus elle est proche, plus le score monte
            proximity = max(0, self.port_deplacement + self.port_attaque - distance)

            # La valeur de l'ennemi réduit légèrement le score (attaquer un tank est risqué)
            danger = min(5, IAPetit.value_ship(ship))

            score += faiblesse + proximity - danger

        # Bonus selon la santé et la mobilité de l'IA elle-même
        score += (self.pv_actuel / self.pv_max) * 8
        score += self.port_deplacement_max

        FloatingText(f"{max(score, 0)}", pos=(self.animator.x + self.animator.pixel_w, self.animator.y + self.animator.pixel_h / 2 + 20), color=(255, 120, 120))

        return max(score, 0)

    def score_fuir(self, ships: list[tuple[Ship, float]]) -> float:
        if not ships:
            return 0.0

        allies_proches = 0
        ennemis_proches = 0

        for ship, distance in ships:
            if isinstance(ship, MotherShip):
                continue
            if ship.joueur == self.joueur:
                if distance <= 3:
                    allies_proches += 1
            else:
                if distance <= ship.port_attaque + 1:
                    ennemis_proches += 1

        # Vie faible => forte envie de fuir
        vie_ratio = 1 - (self.pv_actuel / self.pv_max)
        score = vie_ratio * 15

        # Beaucoup d’ennemis proches => on fuit
        score += ennemis_proches

        # Beaucoup d’alliés => on est rassuré
        score -= allies_proches
        FloatingText(f"{int(score)}", pos=(self.animator.x + self.animator.pixel_w, self.animator.y + self.animator.pixel_h / 2), color=(120, 120, 255))

        return max(score, 0)

    def prevision_move_attack(self, ships: list[Ship], grille: list[list["Point"]]):
        """Se déplace vers l'ennemi le plus proche."""
        enemies = [s for s in ships if s.joueur != self.joueur and not s.est_mort()]
        if not enemies:
            print(f"    DEBUG: Pas d'ennemis")
            return

        # Trouver la cible la plus proche
        cible = min(enemies, key=lambda s: abs(s.cordonner.x - self.cordonner.x) + abs(s.cordonner.y - self.cordonner.y))
        target_pos = (cible.cordonner.x, cible.cordonner.y)

        # Récupérer toutes les positions atteignables
        reachable = self.positions_possibles_adjacentes(grille, direction=self.direction)
        
        if not reachable:
            print(f"    DEBUG: Aucune position atteignable")
            return

        # Trouver la position atteignable la plus proche de la cible
        closest_reachable = min(
            reachable,
            key=lambda pos: abs(pos[0] - target_pos[0]) + abs(pos[1] - target_pos[1])
        )

        print(f"    DEBUG: Déplacement vers {closest_reachable}")
        self.deplacement(closest_reachable, grille, ships)


    def play_flee_mode(self, ships: list[Ship], grille: list[list["Point"]]):
        """Fuit dans la direction opposée à la moyenne des ennemis visibles."""
        enemies = [s for s in ships if s.joueur != self.joueur and not s.est_mort()]
        if not enemies:
            return

        avg_x = sum(s.cordonner.x for s in enemies) / len(enemies)
        avg_y = sum(s.cordonner.y for s in enemies) / len(enemies)

        # Direction opposée normalisée
        dx = self.cordonner.x - avg_x
        dy = self.cordonner.y - avg_y
        
        if dx == 0 and dy == 0:
            return

        # Normaliser
        if dx != 0:
            dx = int(dx / abs(dx))
        if dy != 0:
            dy = int(dy / abs(dy))

        # Récupérer toutes les positions atteignables
        reachable = self.positions_possibles_adjacentes(grille, direction=self.direction)
        
        if not reachable:
            return

        # Trouver la position atteignable dans la direction de fuite (la plus loin)
        best_flee = max(
            reachable,
            key=lambda pos: (pos[0] - self.cordonner.x) * dx + (pos[1] - self.cordonner.y) * dy
        )

        self.deplacement(best_flee, grille, ships)

    def est_cible_a_portee(self, cible: Ship, grille: list[list["Point"]]) -> bool:
        """Vérifie si AU MOINS une case du vaisseau cible est dans la portée d'attaque."""
        positions_portee = self.positions_possibles_attaque(grille, direction=self.direction)

        largeur, hauteur = cible.donner_dimensions(cible.direction)

        # Vérifie chaque case occupée par le vaisseau cible
        for dy in range(hauteur):
            for dx in range(largeur):
                case_x = cible.cordonner.x + dy
                case_y = cible.cordonner.y + dx
                if (case_x, case_y) in positions_portee:
                    return True

        return False

    def play(self, ships: list[Ship], grille: list[list["Point"]]) -> None:
        """
        L'IA choisit une seule action par tour :
        - attaquer si un ennemi est proche et le score d'attaque est le plus élevé
        - fuir si elle est menacée
        - aller vers la base adverse sinon
        """
        print(f"Tour de l'IA {self.joueur} : {self}")

        # Récupère les cibles dans le champ de vision
        targets = self.get_closest_targets(ships)

        # Cas 1 : Aucune cible visible -> Aller vers la base adverse
        if not targets:
            print(f"- Pas de cibles visibles")
            for ship in ships:
                if ship.joueur != self.joueur and isinstance(ship, MotherShip):
                    self.deplacement((ship.cordonner.x, ship.cordonner.y), grille, ships)
                    print(f"- Déplacement vers la base : {ship.cordonner}")
            return

        # Cas 2 : Cibles visibles -> Calculer les scores
        score_attaque = self.score_attaquer(targets)
        score_fuite = self.score_fuir(targets)

        # Sélectionne l'action prioritaire
        etat_choisi = "attaquer" if score_attaque >= score_fuite else "fuir"
        print(f"- Action choisie : {etat_choisi} (attaque: {score_attaque:.1f}, fuite: {score_fuite:.1f})")

        # Boucle principale : le vaisseau agit tant qu'il a des points de mouvement
        iterations = 0
        max_iterations = 20
        
        while self.port_deplacement > 0 and iterations < max_iterations:
            iterations += 1

            # Met à jour les cibles visibles
            targets = self.get_closest_targets(ships)

            # Si aucune cible visible -> fin de tour
            if not targets:
                print(f"  - Aucune cible visible")
                break

            # Trie les cibles : plus intéressante en premier
            targets.sort(key=lambda x: IAPetit.value_ship(x[0]) / (x[1] + 1))

            print(f"  - Position cible: {targets}")

            # Si la cible est à portée d'attaque, on attaque
            for target, dist in targets:
                if self.port_attaque > 0:
                    if self.est_cible_a_portee(target, grille):
                        print(f"  - Attaque de {target} à distance {dist}")
                        self.attaquer(target)
                        self.port_attaque = 0
                        break  # Fin du tour après attaque

            # Sinon, on se déplace selon la stratégie choisie
            deplacement_avant = self.port_deplacement
            
            if etat_choisi == "attaquer":
                self.prevision_move_attack(ships, grille)
            elif etat_choisi == "fuir":
                self.play_flee_mode(ships, grille)
            
            deplacement_apres = self.port_deplacement
            
            # Vérifier que le déplacement a bien consommé des points
            if deplacement_avant == deplacement_apres:
                print(f"  ⚠️ Aucun déplacement effectué, sortie de boucle")
                break

        if iterations >= max_iterations:
            print(f"⚠️ Max itérations atteint ({max_iterations})")
        
        print(f"- Fin du tour: Déplacement restant: {self.port_deplacement}")