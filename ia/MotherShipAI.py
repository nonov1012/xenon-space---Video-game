import pygame
from typing import Optional, Tuple, List
from classes.MotherShip import MotherShip
from classes.Ship import Ship
from classes.Point import Point

class MotherShipIA(MotherShip):
    """
    Classe MotherShip contrôlée par l'IA.
    Attaque automatiquement les vaisseaux ennemis à portée.
    """
    
    def __init__(self, tier: int, cordonner: Point, id: Optional[int] = None,
                 path: str = None, show_health: bool = False, joueur: int = 1,
                 taille: Optional[Tuple[int, int]] = None):
        """
        Constructeur de la classe MotherShipIA.
        Hérite de MotherShip avec les mêmes paramètres.
        """
        super().__init__(
            tier=tier,
            cordonner=cordonner,
            id=id,
            path=path,
            show_health=show_health,
            joueur=joueur,
            taille=taille
        )
    
    def jouer_tour(self, grille, ships: List[Ship]) -> bool:
        """
        Exécute le tour de l'IA pour le MotherShip.
        
        :param grille: Grille du jeu
        :param ships: Liste de tous les vaisseaux
        :return: True si une action a été effectuée, False sinon
        """
        if self.est_mort():
            return False
        
        if self.port_attaque <= 0:
            print("pas de portée d'attaque")
            return False
        
        # Trouver les cibles potentielles
        cible = self._trouver_meilleure_cible(grille, ships)
        
        if cible:
            # Attaquer la cible
            self.attaquer(cible)
            print("j'attaque le vaisseau:")
            print(cible)
            self.port_attaque = 0  # Consommer l'action d'attaque
            
            # Si la cible est détruite, la retirer
            if cible.est_mort():
                cible.liberer_position(grille)
                if cible in ships:
                    ships.remove(cible)
            
            return True
        
        return False
    
    def _trouver_meilleure_cible(self, grille, ships: List[Ship]) -> Optional[Ship]:
        """
        Trouve le meilleur vaisseau ennemi à attaquer.
        
        Priorités :
        1. Vaisseaux ennemis les plus proches
        2. Vaisseaux avec le moins de PV (pour tuer rapidement)
        3. Vaisseaux avec le plus de valeur (cout élevé)
        
        :param grille: Grille du jeu
        :param ships: Liste de tous les vaisseaux
        :return: Le vaisseau cible ou None
        """
        positions_attaque = self.positions_possibles_attaque(grille, direction=self.direction)
        
        cibles_potentielles = []
        
        # Trouver tous les vaisseaux ennemis à portée
        for ligne, colonne in positions_attaque:
            vaisseau = self.trouver_vaisseau_a_position(ships, ligne, colonne)
            
            if vaisseau and vaisseau.joueur != self.joueur and not vaisseau.est_mort():
                # Calculer la distance de Manhattan
                distance = abs(self.cordonner.x - vaisseau.cordonner.x) + \
                          abs(self.cordonner.y - vaisseau.cordonner.y)
                
                # Calculer un score de priorité
                # Plus le score est élevé, plus la cible est prioritaire
                score = 0
                
                # Priorité 1 : Distance (plus proche = meilleur)
                score += (self.port_attaque - distance) * 100
                
                # Priorité 2 : Vaisseaux presque morts (pour finir rapidement)
                ratio_pv = vaisseau.pv_actuel / vaisseau.pv_max
                if ratio_pv < 0.3:  # Moins de 30% de PV
                    score += 200
                elif vaisseau.pv_actuel <= self.attaque:  # Peut être tué en un coup
                    score += 300
                
                # Priorité 3 : Valeur du vaisseau (cout élevé = cible intéressante)
                score += vaisseau.cout / 10
                
                cibles_potentielles.append((score, vaisseau))
        
        # Trier par score décroissant et retourner la meilleure cible
        if cibles_potentielles:
            cibles_potentielles.sort(key=lambda x: x[0], reverse=True)
            return cibles_potentielles[0][1]
        
        return None
    
    def _est_vaisseau_ennemi_a_position(self, ships: List[Ship], ligne: int, colonne: int) -> bool:
        """
        Vérifie s'il y a un vaisseau ennemi à une position donnée.
        
        :param ships: Liste de tous les vaisseaux
        :param ligne: Ligne de la position
        :param colonne: Colonne de la position
        :return: True si un ennemi est présent
        """
        vaisseau = self.trouver_vaisseau_a_position(ships, ligne, colonne)
        return vaisseau is not None and vaisseau.joueur != self.joueur and not vaisseau.est_mort()