"""
- Miner des planètes et astéroïdes
- Éviter les vaisseaux ennemis
- Maximiser les gains tout en survivant
"""

import math
from typing import List, Tuple, Optional
from classes.Ship import Foreuse
from classes.Point import Type, Point
from heapq import heappush, heappop


class ForeuseBehavior:
    """Comportement IA pour une Foreuse"""
    
    def __init__(self, foreuse: Foreuse, grille: List[List[Point]], ships: List):
        self.foreuse = foreuse
        self.grille = grille
        self.ships = ships
        self.danger_radius = 5  # Rayon de détection des ennemis
        self.min_safety_distance = 3  # Distance minimale de sécurité
        
    def evaluate_position_safety(self, ligne: int, colonne: int) -> float:
        """
        Évalue la sécurité d'une position (0 = très dangereux, 1 = très sûr)
        """
        score = 1.0
        
        # Vérifier la présence de vaisseaux ennemis
        for ship in self.ships:
            if ship.joueur == self.foreuse.joueur or ship == self.foreuse:
                continue
                
            # Distance Manhattan entre la position et le vaisseau ennemi
            ship_center_x = ship.cordonner.x + ship.donner_dimensions(ship.direction)[1] / 2
            ship_center_y = ship.cordonner.y + ship.donner_dimensions(ship.direction)[0] / 2
            
            distance = abs(ligne - ship_center_x) + abs(colonne - ship_center_y)
            
            # Pénalité selon la distance et la puissance du vaisseau
            if distance < self.danger_radius:
                threat_level = ship.attaque / 100.0  # Normaliser l'attaque
                danger = (self.danger_radius - distance) / self.danger_radius
                score -= danger * threat_level * 0.5
                
        return max(0.0, min(1.0, score))
    
    def find_mining_targets(self) -> List[Tuple[int, int, float]]:
        """
        Trouve tous les objectifs de minage (planètes et astéroïdes)
        Retourne: Liste de (ligne, colonne, score)
        """
        targets = []
        
        for ligne in range(len(self.grille)):
            for colonne in range(len(self.grille[0])):
                point = self.grille[ligne][colonne]
                
                # Identifier les cibles minables
                if point.type == Type.ASTEROIDE:
                    reward = 100  # Récompense pour astéroïde
                elif point.type == Type.PLANETE:
                    reward = 150  # Récompense pour planète
                else:
                    continue
                
                # Calculer la distance depuis la position actuelle
                distance = abs(ligne - self.foreuse.cordonner.x) + abs(colonne - self.foreuse.cordonner.y)
                
                # Évaluer la sécurité de la position
                safety = self.evaluate_position_safety(ligne, colonne)
                
                # Score composite: récompense / distance * sécurité
                if distance > 0 and safety > 0.3:  # Éviter positions trop dangereuses
                    score = (reward / distance) * safety
                    targets.append((ligne, colonne, score))
        
        # Trier par score décroissant
        targets.sort(key=lambda x: x[2], reverse=True)
        return targets
    
    def find_safe_position_near(self, target_ligne: int, target_colonne: int) -> Optional[Tuple[int, int]]:
        """
        Trouve une position sûre adjacente à la cible de minage
        """
        # Vérifier les cases adjacentes à la cible
        adjacent_positions = []
        for dl in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dl == 0 and dc == 0:
                    continue
                    
                nl, nc = target_ligne + dl, target_colonne + dc
                
                # Vérifier que c'est dans les limites
                if 0 <= nl < len(self.grille) and 0 <= nc < len(self.grille[0]):
                    # Vérifier que c'est accessible
                    if self.foreuse.verifier_collision(self.grille, nl, nc, self.foreuse.direction):
                        safety = self.evaluate_position_safety(nl, nc)
                        adjacent_positions.append((nl, nc, safety))
        
        # Trier par sécurité décroissante
        adjacent_positions.sort(key=lambda x: x[2], reverse=True)
        
        if adjacent_positions and adjacent_positions[0][2] > 0.5:
            return (adjacent_positions[0][0], adjacent_positions[0][1])
        
        return None
    
    def should_flee(self) -> bool:
        """
        Détermine si la Foreuse doit fuir (danger imminent)
        """
        current_safety = self.evaluate_position_safety(
            self.foreuse.cordonner.x, 
            self.foreuse.cordonner.y
        )
        
        # Fuir si la sécurité est très basse ou si les PV sont critiques
        health_ratio = self.foreuse.pv_actuel / self.foreuse.pv_max
        
        return current_safety < 0.3 or health_ratio < 0.3
    
    def find_safest_retreat(self) -> Optional[Tuple[int, int]]:
        """
        Trouve la position la plus sûre pour fuir
        """
        positions_possibles = self.foreuse.positions_possibles_adjacentes(self.grille)
        
        if not positions_possibles:
            return None
        
        # Évaluer la sécurité de chaque position
        safe_positions = []
        for ligne, colonne in positions_possibles:
            safety = self.evaluate_position_safety(ligne, colonne)
            
            # Privilégier les positions loin des ennemis
            distance_to_enemies = 0
            for ship in self.ships:
                if ship.joueur != self.foreuse.joueur and ship != self.foreuse:
                    dist = abs(ligne - ship.cordonner.x) + abs(colonne - ship.cordonner.y)
                    distance_to_enemies += dist
            
            score = safety * distance_to_enemies
            safe_positions.append((ligne, colonne, score))
        
        safe_positions.sort(key=lambda x: x[2], reverse=True)
        
        if safe_positions:
            return (safe_positions[0][0], safe_positions[0][1])
        
        return None
    
    def execute_turn(self) -> bool:
        """
        Exécute le tour de la Foreuse
        Retourne True si une action a été effectuée
        """
        # 1. Vérifier si on doit fuir
        if self.should_flee():
            retreat_pos = self.find_safest_retreat()
            if retreat_pos:
                print(f"[IA Foreuse {self.foreuse.id}] FUITE vers position sûre {retreat_pos}")
                return self.foreuse.deplacement(retreat_pos, self.grille, self.ships)
        
        # 2. Vérifier si on est déjà à côté d'une cible minable
        if self.foreuse.est_a_cote_planete(self.grille):
            # Chercher la planète adjacente
            for dl in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    nl = self.foreuse.cordonner.x + dl
                    nc = self.foreuse.cordonner.y + dc
                    
                    if 0 <= nl < len(self.grille) and 0 <= nc < len(self.grille[0]):
                        if self.grille[nl][nc].type == Type.PLANETE:
                            print(f"[IA Foreuse {self.foreuse.id}] Minage planète en {nc},{nl}")
                            # Pas de méthode directe, on reste en position
                            return True
        
        if self.foreuse.est_autour_asteroide(self.grille):
            # Miner l'astéroïde
            for dl in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    nl = self.foreuse.cordonner.x + dl
                    nc = self.foreu