import math
from typing import List, Tuple, Optional
from classes.Ship import Foreuse
from classes.Point import Point, Type
from classes.Map import Map


class ForeuseIA:
    """
    IA pour le vaisseau Foreuse.
    Stratégie : Maximiser la collecte de ressources (astéroïdes et planètes)
    tout en évitant les dangers.
    """
    
    def __init__(self, foreuse: Foreuse, grille: List[List[Point]], ships: List):
        """
        Initialise le comportement de la Foreuse.
        
        :param foreuse: Instance du vaisseau Foreuse
        :param grille: Grille de jeu
        :param ships: Liste de tous les vaisseaux
        """
        self.foreuse = foreuse
        self.grille = grille
        self.ships = ships
        self.nb_lignes = len(grille)
        self.nb_colonnes = len(grille[0])
        
    def valuer_position(self, position: Tuple[int, int]) -> float:
        """
        Value la valeur d'une position selon plusieurs critères.
        
        :param position: Tuple (ligne, colonne)
        :return: Score de la position (plus élevé = meilleur)
        """
        ligne, colonne = position
        score = 0.0
        
        # Vérifier si la position est valide
        if not (0 <= ligne < self.nb_lignes and 0 <= colonne < self.nb_colonnes):
            return float('-inf')
        
        # 1. PRIORITÉ MAXIMALE : Proximité aux astéroïdes (minables immédiatement)
        nb_asteroides_adjacents = self._compter_asteroides_adjacents(ligne, colonne)
        score += nb_asteroides_adjacents * 1000  # Bonus énorme pour astéroïdes adjacents
        
        # 2. PRIORITÉ HAUTE : Proximité aux planètes (bonus passif)
        nb_planetes_adjacentes = self._compter_planetes_adjacentes(ligne, colonne)
        score += nb_planetes_adjacentes * 500  # Bonus important pour planètes
        
        # 3. Proximité aux astéroïdes proches (pas adjacents)
        distance_asteroide_proche = self._distance_ressource_proche(ligne, colonne, Type.ASTEROIDE)
        if distance_asteroide_proche > 0:
            score += 200 / distance_asteroide_proche  # Plus proche = meilleur
        
        # 4. Proximité aux planètes proches
        distance_planete_proche = self._distance_ressource_proche(ligne, colonne, Type.PLANETE)
        if distance_planete_proche > 0:
            score += 100 / distance_planete_proche
        
        # 5. MALUS : Danger des vaisseaux ennemis
        danger = self._evaluer_danger(ligne, colonne)
        score -= danger * 300  # Pénalité importante si danger
        
        # 6. MALUS : Distance à la base alliée (pour éviter de trop s'éloigner)
        distance_base = self._distance_base_alliee(ligne, colonne)
        score -= distance_base * 2  # Petit malus pour éloignement
        
        # 7. Bonus si dans l'atmosphère (zone safe proche planète)
        # if self.grille[ligne][colonne].type == Type.ATMOSPHERE:
        #     score += 50
        
        return score
    
    def _compter_asteroides_adjacents(self, ligne: int, colonne: int) -> int:
        """Compte le nombre d'astéroïdes adjacents à une position."""
        count = 0
        for dl in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dl == 0 and dc == 0:
                    continue
                nl, nc = ligne + dl, colonne + dc
                if (0 <= nl < self.nb_lignes and 0 <= nc < self.nb_colonnes and
                    self.grille[nl][nc].type == Type.ASTEROIDE):
                    count += 1
        return count
    
    def _compter_planetes_adjacentes(self, ligne: int, colonne: int) -> int:
        """Compte le nombre de cases de planètes adjacentes."""
        count = 0
        for dl in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dl == 0 and dc == 0:
                    continue
                nl, nc = ligne + dl, colonne + dc
                if (0 <= nl < self.nb_lignes and 0 <= nc < self.nb_colonnes and
                    self.grille[nl][nc].type == Type.PLANETE):
                    count += 1
        return count
    
    def _distance_ressource_proche(self, ligne: int, colonne: int, type_ressource: Type) -> float:
        """
        Trouve la distance à la ressource la plus proche du type spécifié.
        
        :return: Distance Manhattan à la ressource la plus proche
        """
        min_distance = float('inf')
        
        # Recherche dans un rayon limité pour optimiser
        rayon = int(min(15, self.foreuse.port_deplacement * 3))
        
        for l in range(max(0, ligne - rayon), min(self.nb_lignes, ligne + rayon + 1)):
            for c in range(max(0, colonne - rayon), min(self.nb_colonnes, colonne + rayon + 1)):
                if self.grille[l][c].type == type_ressource:
                    distance = abs(l - ligne) + abs(c - colonne)
                    min_distance = min(min_distance, distance)
        
        return min_distance if min_distance != float('inf') else 0
    
    def _evaluer_danger(self, ligne: int, colonne: int) -> float:
        """
        Évalue le niveau de danger d'une position selon les vaisseaux ennemis.
        
        :return: Score de danger (plus élevé = plus dangereux)
        """
        danger = 0.0
        
        for ship in self.ships:
            # Ignorer les vaisseaux alliés et la foreuse elle-même
            if ship.joueur == self.foreuse.joueur or ship.id == self.foreuse.id:
                continue
            
            # Ignorer les foreuses ennemies (pas de danger ça tire pas)
            if isinstance(ship, Foreuse):
                continue
            
            # Calculer la distance au vaisseau ennemi
            distance = abs(ship.cordonner.x - ligne) + abs(ship.cordonner.y - colonne)
            
            # Si dans la portée d'attaque de l'ennemi : DANGER !
            if distance <= ship.port_attaque and ship.attaque > 0:
                # Danger proportionnel à la puissance d'attaque
                danger += (ship.attaque / 50) * (1 + 1.0 / max(1, distance))
            
            # Si très proche : danger même sans attaque
            elif distance <= 3:
                danger += 0.5
        
        return danger
    
    def _distance_base_alliee(self, ligne: int, colonne: int) -> float:
        """Calcule la distance à la base alliée."""
        # Trouver la base alliée
        base_pos = None
        for ship in self.ships:
            if ship.joueur == self.foreuse.joueur and hasattr(ship, '__class__') and ship.__class__.__name__ == 'MotherShip':
                base_pos = (ship.cordonner.x, ship.cordonner.y)
                break
        
        if base_pos is None:
            return 0
        
        return abs(base_pos[0] - ligne) + abs(base_pos[1] - colonne)
    
    def _est_position_optimale(self) -> bool:
        """
        Vérifie si la foreuse est déjà dans une position optimale
        (à côté d'une planète OU d'un astéroïde).
        
        :return: True si position optimale, False sinon
        """
        ligne_actuelle = self.foreuse.cordonner.x
        colonne_actuelle = self.foreuse.cordonner.y
        
        # Vérifier s'il y a un astéroïde adjacent
        if self._compter_asteroides_adjacents(ligne_actuelle, colonne_actuelle) > 0:
            return True
        
        # Vérifier s'il y a une planète adjacente
        if self._compter_planetes_adjacentes(ligne_actuelle, colonne_actuelle) > 0:
            return True
        
        return False
    
    def trouver_meilleure_action(self) -> Optional[Tuple[int, int]]:
        """
        Trouve la meilleure action pour la Foreuse.
        
        :return: Position cible (ligne, colonne) ou None si aucune action
        """
        # NOUVEAU : Vérifier si on est déjà dans une position optimale
        if self._est_position_optimale():
            # On reste sur place, on ne bouge pas
            return None
        
        # 1. Vérifier si on peut miner un astéroïde adjacent
        action_minage = self._verifier_minage_immediat()
        if action_minage:
            return action_minage
        
        # 2. Trouver toutes les positions accessibles
        positions_possibles = self.foreuse.positions_possibles_adjacentes(
            self.grille, 
            direction=self.foreuse.direction
        )
        
        if not positions_possibles:
            return None
        
        # 3. Évaluer toutes les positions et choisir la meilleure
        meilleure_position = None
        meilleur_score = float('-inf')
        
        for position in positions_possibles:
            score = self.valuer_position(position)
            
            if score > meilleur_score:
                meilleur_score = score
                meilleure_position = position
        
        return meilleure_position
    
    def _verifier_minage_immediat(self) -> Optional[Tuple[int, int]]:
        """
        Vérifie s'il y a un astéroïde minable adjacent.
        
        :return: Position de l'astéroïde ou None
        """
        ligne_actuelle = self.foreuse.cordonner.x
        colonne_actuelle = self.foreuse.cordonner.y
        
        # Chercher un astéroïde adjacent
        for dl in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dl == 0 and dc == 0:
                    continue
                
                nl = ligne_actuelle + dl
                nc = colonne_actuelle + dc
                
                if (0 <= nl < self.nb_lignes and 0 <= nc < self.nb_colonnes and
                    self.grille[nl][nc].type == Type.ASTEROIDE):
                    # Retourner la position de l'astéroïde pour minage
                    return (nl, nc)
        
        return None
    
    def executer_action(self) -> bool:
        """
        Exécute la meilleure action pour la Foreuse.
        
        :return: True si une action a été effectuée
        """
        # Trouver la meilleure action
        action = self.trouver_meilleure_action()
        
        if action is None:
            # Aucune action à effectuer (déjà en position optimale ou aucun mouvement possible)
            return False
        
        # Exécuter le déplacement/minage
        success = self.foreuse.deplacement(action, self.grille, self.ships)
        
        return success


def jouer_tour_foreuse(foreuse: Foreuse, grille: List[List[Point]], ships: List) -> bool:
    """
    Fonction principale pour faire jouer un tour à une Foreuse.
    
    :param foreuse: Instance de la Foreuse
    :param grille: Grille de jeu
    :param ships: Liste de tous les vaisseaux
    :return: True si une action a été effectuée
    """
    if foreuse.est_mort():
        return False
    
    # Créer le comportement IA
    ia = ForeuseIA(foreuse, grille, ships)
    
    # Exécuter l'action
    return ia.executer_action()