from classes.Ship import *
from classes.Turn import Turn
from classes.Point import Point

class IATransport:
    """Classe utilitaire pour gérer l'IA d'un vaisseau Transport"""
    
    def __init__(self, transport_ship: Transport):
        """
        Initialise l'IA avec un vaisseau Transport existant
        
        Args:
            transport_ship: Instance de Transport à contrôler
        """
        self.ship = transport_ship
    
    def recuperer_vaisseaux_transportables(self):
        """Récupère tous les vaisseaux alliés transportables : Petit, Moyen, Foreuse"""
        return [
            ship for ship in Turn.get_players_ships()
            if ship.joueur == self.ship.joueur and isinstance(ship, (Petit, Moyen, Foreuse))
        ]
    
    def calculer_position_moyenne(self, ships: list):
        """Calcule la position centrale des vaisseaux donnés"""
        if not ships:
            return self.ship.cordonner
        somme_x = sum(ship.cordonner.x for ship in ships)
        somme_y = sum(ship.cordonner.y for ship in ships)
        nb = len(ships)
        return Point(int(somme_x / nb), int(somme_y / nb))
    
    def jouer_tour(self, grille: List[List[Point]]):
        """
        Tour complet de l'IA Transport :
        1️⃣ Récupérer les vaisseaux alliés transportables
        2️⃣ Calculer leur position moyenne
        3️⃣ Se déplacer vers cette position
        """
        ships_transportables = self.recuperer_vaisseaux_transportables()
        
        if not ships_transportables:
            # Pas de vaisseaux à transporter, ne rien faire
            return
        
        cible = self.calculer_position_moyenne(ships_transportables)
        
        # Déplacer le vaisseau Transport vers la cible
        self.ship.deplacement((cible.x, cible.y), grille, Turn.get_players_ships())