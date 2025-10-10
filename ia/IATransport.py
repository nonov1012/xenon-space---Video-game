from classes.Ship import *
from classes.Turn import Turn
from classes.Point import Point

class IATransport(Transport):

    def __init__(self, id: int, pos: tuple[int, int], equipe: str):
        super().__init__(cordonner=Point(pos[0], pos[1]), id=id, joueur=equipe)

    def recuperer_vaisseaux_transportables(self):
        """Récupère tous les vaisseaux alliés transportables : Petit, Moyen, Foreuse"""
        return [
            ship for ship in Turn.get_players_ships()
            if ship.joueur == self.joueur and isinstance(ship, (Petit, Moyen, Foreuse))
        ]

    def calculer_position_moyenne(self, ships: list):
        """Calcule la position centrale des vaisseaux donnés"""
        if not ships:
            return self.cordonner
        somme_x = sum(ship.cordonner.x for ship in ships)
        somme_y = sum(ship.cordonner.y for ship in ships)
        nb = len(ships)
        return Point(int(somme_x / nb), int(somme_y / nb))

    def se_positionner_milieu_allies(self):
        """Place le transport au centre des vaisseaux alliés transportables"""
        ships_transportables = self.recuperer_vaisseaux_transportables()
        point_milieu = self.calculer_position_moyenne(ships_transportables)
        self.cordonner = point_milieu

    # ---------------- MAIN IA (déplacement seulement) ----------------
    def jouer_tour(self, grille: List[List[Point]]):
        """
        Tour complet de l'IA Transport :
        1️⃣ Se placer au centre des vaisseaux alliés transportables
        2️⃣ Se déplacer vers cette position si nécessaire
        """
        
        ships_transportables = self.recuperer_vaisseaux_transportables()
        cible = self.calculer_position_moyenne(ships_transportables)

        self.deplacement((cible.x, cible.y), grille, Turn.get_players_ships())
