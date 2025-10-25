import random
from typing import List, Tuple, Optional, Dict
import heapq
import pygame
from classes.Point import Point, Type
from classes.Ship import Ship, Moyen
from classes.MotherShip import MotherShip


class AIShip:
    """Représente un vaisseau contrôlé par l'IA"""
    
    def __init__(self, ship: Ship):
        self.ship = ship
        self.target_position: Optional[Tuple[int, int]] = None
        self.last_update = 0
        self.update_interval = 500  # Mise à jour plus rapide
        self.state = "seeking"  # seeking, attacking, waiting
        
    def is_ready_for_update(self, current_time: int) -> bool:
        """Vérifie si le vaisseau est prêt pour une nouvelle action"""
        return current_time - self.last_update >= self.update_interval


class AIManager:
    """Gestionnaire principal de l'intelligence artificielle"""
    
    def __init__(self):
        self.ai_ships: List[AIShip] = []
        
    def add_ai_ship(self, ship: Ship):
        """Ajoute un vaisseau à l'IA"""
        if isinstance(ship, Moyen):
            ai_ship = AIShip(ship)
            self.ai_ships.append(ai_ship)
            print(f"Vaisseau IA ajouté: ID {ship.id}")
    
    def remove_ai_ship(self, ship: Ship):
        """Retire un vaisseau de l'IA"""
        self.ai_ships = [ai for ai in self.ai_ships if ai.ship.id != ship.id]
        
    def update_all(self, grille: List[List[Point]], all_ships: List[Ship], delta_time: int):
        """Met à jour tous les vaisseaux IA"""
        current_time = pygame.time.get_ticks()
        
        for ai_ship in self.ai_ships[:]:
            # Vérifier si le vaisseau est encore vivant
            if ai_ship.ship.est_mort():
                self.remove_ai_ship(ai_ship.ship)
                continue
                
            # Mettre à jour le vaisseau s'il est prêt
            if ai_ship.is_ready_for_update(current_time):
                self.update_ai_ship(ai_ship, grille, all_ships)
                ai_ship.last_update = current_time
    
    def update_ai_ship(self, ai_ship: AIShip, grille: List[List[Point]], all_ships: List[Ship]):
        """Met à jour un vaisseau IA spécifique - Version simplifiée"""
        ship = ai_ship.ship
        
        # Si pas de points d'action, skip
        if ship.port_deplacement <= 0 and ship.port_attaque <= 0:
            return
            
        # Trouver la base ennemie
        enemy_base = self.find_enemy_base(ship, all_ships)
        if not enemy_base:
            return
            
        # PRIORITÉ 1: Attaquer la base si possible
        if ship.port_attaque > 0:
            positions_attaque = ship.positions_possibles_attaque(grille)
            base_positions = []
            
            # Toutes les cases occupées par la base
            base_largeur, base_hauteur = enemy_base.donner_dimensions(enemy_base.direction)
            for by in range(enemy_base.cordonner.x, enemy_base.cordonner.x + base_hauteur):
                for bx in range(enemy_base.cordonner.y, enemy_base.cordonner.y + base_largeur):
                    base_positions.append((by, bx))
            
            # Si on peut attaquer la base, on attaque !
            for pos in positions_attaque:
                if pos in base_positions:
                    print(f"IA {ship.id}: ATTAQUE LA BASE !")
                    ship.deplacement(pos, grille, all_ships)
                    return
        
        # PRIORITÉ 2: Se déplacer vers la base
        if ship.port_deplacement > 0:
            self.move_straight_to_base(ship, enemy_base, grille, all_ships)
    
    def find_enemy_base(self, ship: Ship, all_ships: List[Ship]) -> Optional[MotherShip]:
        """Trouve la base ennemie"""
        for other_ship in all_ships:
            if (isinstance(other_ship, MotherShip) and 
                other_ship.joueur != ship.joueur and 
                not other_ship.est_mort()):
                return other_ship
        return None
    
    def move_straight_to_base(self, ship: Ship, target: MotherShip, grille: List[List[Point]], all_ships: List[Ship]):
        """Déplace le vaisseau directement vers la base ennemie - Version ultra simple"""
        
        # Position actuelle et cible
        current_y, current_x = ship.cordonner.x, ship.cordonner.y
        target_y, target_x = target.cordonner.x, target.cordonner.y
        
        # Calculer les directions
        dy = target_y - current_y
        dx = target_x - current_x
        
        # Liste des mouvements possibles par ordre de priorité
        moves_to_try = []
        
        # Priorité à la direction qui rapproche le plus
        if abs(dy) > abs(dx):
            # Mouvement vertical prioritaire
            if dy > 0:
                moves_to_try.append((current_y + 1, current_x))  # Descendre
            else:
                moves_to_try.append((current_y - 1, current_x))  # Monter
            
            # Puis mouvement horizontal
            if dx > 0:
                moves_to_try.append((current_y, current_x + 1))  # Droite
            else:
                moves_to_try.append((current_y, current_x - 1))  # Gauche
        else:
            # Mouvement horizontal prioritaire
            if dx > 0:
                moves_to_try.append((current_y, current_x + 1))  # Droite
            else:
                moves_to_try.append((current_y, current_x - 1))  # Gauche
                
            # Puis mouvement vertical
            if dy > 0:
                moves_to_try.append((current_y + 1, current_x))  # Descendre
            else:
                moves_to_try.append((current_y - 1, current_x))  # Monter
        
        # Ajouter mouvements diagonaux comme alternatives
        if dy != 0 and dx != 0:
            moves_to_try.extend([
                (current_y + (1 if dy > 0 else -1), current_x + (1 if dx > 0 else -1)),
                (current_y + (1 if dy > 0 else -1), current_x - (1 if dx > 0 else -1)),
                (current_y - (1 if dy > 0 else -1), current_x + (1 if dx > 0 else -1))
            ])
        
        # Essayer chaque mouvement
        for new_y, new_x in moves_to_try:
            # Vérifier limites
            if 0 <= new_y < len(grille) and 0 <= new_x < len(grille[0]):
                # Vérifier si le mouvement est possible
                positions_possibles = ship.positions_possibles_adjacentes(grille)
                if (new_y, new_x) in positions_possibles:
                    success = ship.deplacement((new_y, new_x), grille, all_ships)
                    if success:
                        print(f"IA {ship.id}: Se déplace vers la base ({new_y}, {new_x})")
                        return
        
        print(f"IA {ship.id}: Aucun mouvement possible vers la base") 