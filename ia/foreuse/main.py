# classes/ForeuseBehavior.py
from typing import Optional, Tuple, List
from classes.Point import Type, Point
from classes.Ship import Ship, Foreuse
import random

class ForeuseBehavior:
    """
    Gère le comportement automatique d'une Foreuse.
    
    Stratégie :
    1. Chercher un astéroïde ou une planète à proximité
    2. Se déplacer vers la cible
    3. Rester à côté pour que Turn gère le minage
    """
    
    def __init__(self, foreuse: Foreuse):
        self.foreuse = foreuse
        self.cible_actuelle: Optional[Tuple[int, int]] = None
        self.mode = "recherche"  # "recherche", "deplacement", "attente"
        print(f"[IA Foreuse {self.foreuse.id}] Initialisation")
        
    def trouver_ressource_proche(self, grille: List[List[Point]], 
                                  rayon_recherche: int = 15) -> Optional[Tuple[int, int]]:
        """
        Trouve l'astéroïde ou la planète la plus proche dans un rayon donné.
        Priorité : astéroïdes > planètes
        """
        pos_foreuse = (self.foreuse.cordonner.x, self.foreuse.cordonner.y)
        print(f"[IA Foreuse {self.foreuse.id}] Position actuelle: {pos_foreuse}")
        
        # Listes pour stocker les ressources trouvées
        asteroides = []
        planetes = []
        
        # Parcourir la zone autour de la foreuse
        for dl in range(-rayon_recherche, rayon_recherche + 1):
            for dc in range(-rayon_recherche, rayon_recherche + 1):
                ligne = pos_foreuse[0] + dl
                col = pos_foreuse[1] + dc
                
                # Vérifier les limites
                if 0 <= ligne < len(grille) and 0 <= col < len(grille[0]):
                    case = grille[ligne][col]
                    
                    # Distance de Manhattan
                    distance = abs(dl) + abs(dc)
                    
                    if case.type == Type.ASTEROIDE:
                        asteroides.append((ligne, col, distance))
                        print(f"[IA Foreuse {self.foreuse.id}] Astéroïde trouvé à ({ligne}, {col}), distance: {distance}")
                    elif case.type == Type.PLANETE:
                        planetes.append((ligne, col, distance))
        
        print(f"[IA Foreuse {self.foreuse.id}] Trouvé {len(asteroides)} astéroïdes et {len(planetes)} planètes")
        
        # Priorité aux astéroïdes (plus rentables)
        if asteroides:
            asteroides.sort(key=lambda x: x[2])
            cible = (asteroides[0][0], asteroides[0][1])
            print(f"[IA Foreuse {self.foreuse.id}] Cible choisie (astéroïde): {cible}")
            return cible
        
        if planetes:
            planetes.sort(key=lambda x: x[2])
            cible = (planetes[0][0], planetes[0][1])
            print(f"[IA Foreuse {self.foreuse.id}] Cible choisie (planète): {cible}")
            return cible
        
        print(f"[IA Foreuse {self.foreuse.id}] Aucune ressource trouvée dans le rayon {rayon_recherche}")
        return None
    
    def trouver_case_adjacente_libre(self, cible: Tuple[int, int], 
                                      grille: List[List[Point]]) -> Optional[Tuple[int, int]]:
        """
        Trouve une case libre adjacente à la cible pour se positionner.
        """
        ligne_cible, col_cible = cible
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # haut, bas, gauche, droite
        
        cases_libres = []
        
        print(f"[IA Foreuse {self.foreuse.id}] Recherche case adjacente à ({ligne_cible}, {col_cible})")
        
        for dl, dc in directions:
            ligne = ligne_cible + dl
            col = col_cible + dc
            
            # Vérifier si la case est dans les limites
            if (0 <= ligne < len(grille) and 0 <= col < len(grille[0])):
                print(f"[IA Foreuse {self.foreuse.id}] Test case ({ligne}, {col})")
                
                # Vérifier collision
                if self.foreuse.verifier_collision(grille, ligne, col, 
                                                   self.foreuse.direction, 
                                                   ignorer_self=True):
                    cases_libres.append((ligne, col))
                    print(f"[IA Foreuse {self.foreuse.id}] Case ({ligne}, {col}) est LIBRE")
                else:
                    print(f"[IA Foreuse {self.foreuse.id}] Case ({ligne}, {col}) est OCCUPÉE")
        
        if cases_libres:
            print(f"[IA Foreuse {self.foreuse.id}] {len(cases_libres)} cases libres trouvées")
            return cases_libres[0]
        else:
            print(f"[IA Foreuse {self.foreuse.id}] AUCUNE case libre trouvée")
            return None
    
    def est_adjacent_a_cible(self, cible: Tuple[int, int]) -> bool:
        """
        Vérifie si la foreuse est adjacente à la cible.
        """
        pos = (self.foreuse.cordonner.x, self.foreuse.cordonner.y)
        distance = abs(pos[0] - cible[0]) + abs(pos[1] - cible[1])
        est_adjacent = distance == 1
        
        print(f"[IA Foreuse {self.foreuse.id}] Distance à cible {cible}: {distance}, adjacent: {est_adjacent}")
        return est_adjacent
    
    def executer_tour(self, grille: List[List[Point]], ships: List[Ship]) -> bool:
        """
        Exécute le comportement de la foreuse pour un tour.
        UNIQUEMENT LE DÉPLACEMENT, pas le minage.
        """
        print(f"\n{'='*60}")
        print(f"[IA Foreuse {self.foreuse.id}] === DÉBUT DU TOUR ===")
        print(f"[IA Foreuse {self.foreuse.id}] Portée déplacement: {self.foreuse.port_deplacement}")
        print(f"[IA Foreuse {self.foreuse.id}] Mode: {self.mode}")
        print(f"[IA Foreuse {self.foreuse.id}] Cible actuelle: {self.cible_actuelle}")
        
        # Si plus de portée de déplacement, ne rien faire
        if self.foreuse.port_deplacement <= 0:
            print(f"[IA Foreuse {self.foreuse.id}] ❌ Plus de portée de déplacement")
            return False
        
        # === MODE RECHERCHE ===
        if self.mode == "recherche" or self.cible_actuelle is None:
            print(f"[IA Foreuse {self.foreuse.id}] 🔍 MODE RECHERCHE")
            self.cible_actuelle = self.trouver_ressource_proche(grille)
            
            if self.cible_actuelle is None:
                print(f"[IA Foreuse {self.foreuse.id}] ⚠️ Aucune ressource trouvée, déplacement aléatoire")
                return self.deplacer_aleatoirement(grille, ships)
            
            self.mode = "deplacement"
            print(f"[IA Foreuse {self.foreuse.id}] ✓ Passage en mode DÉPLACEMENT")
        
        # === VÉRIFIER SI DÉJÀ ADJACENT ===
        if self.est_adjacent_a_cible(self.cible_actuelle):
            print(f"[IA Foreuse {self.foreuse.id}] ✓ DÉJÀ ADJACENT à la cible {self.cible_actuelle}")
            
            # Vérifier si la cible existe encore
            ligne_cible, col_cible = self.cible_actuelle
            type_case = grille[ligne_cible][col_cible].type
            
            print(f"[IA Foreuse {self.foreuse.id}] Type de case cible: {type_case}")
            
            if type_case in [Type.ASTEROIDE, Type.PLANETE]:
                # Rester en place, Turn gérera le minage
                print(f"[IA Foreuse {self.foreuse.id}] 💎 Reste en place pour minage automatique")
                self.mode = "attente"
                return False  # Pas de déplacement
            else:
                # La cible n'existe plus, chercher une nouvelle cible
                print(f"[IA Foreuse {self.foreuse.id}] ⚠️ Cible disparue, nouvelle recherche")
                self.cible_actuelle = None
                self.mode = "recherche"
                return False
        
        # === MODE DÉPLACEMENT ===
        print(f"[IA Foreuse {self.foreuse.id}] 🚀 MODE DÉPLACEMENT vers {self.cible_actuelle}")
        
        # Trouver une case adjacente à la cible
        case_adjacente = self.trouver_case_adjacente_libre(self.cible_actuelle, grille)
        
        if case_adjacente is None:
            print(f"[IA Foreuse {self.foreuse.id}] ❌ Cible inatteignable, nouvelle recherche")
            self.cible_actuelle = None
            self.mode = "recherche"
            return False
        
        print(f"[IA Foreuse {self.foreuse.id}] 🎯 Tentative de déplacement vers {case_adjacente}")
        
        # Se déplacer vers la case adjacente
        success = self.foreuse.deplacement(case_adjacente, grille, ships)
        
        if success:
            print(f"[IA Foreuse {self.foreuse.id}] ✅ DÉPLACEMENT RÉUSSI vers {case_adjacente}")
            print(f"[IA Foreuse {self.foreuse.id}] Nouvelle position: ({self.foreuse.cordonner.x}, {self.foreuse.cordonner.y})")
            print(f"[IA Foreuse {self.foreuse.id}] Portée restante: {self.foreuse.port_deplacement}")
            return True
        else:
            print(f"[IA Foreuse {self.foreuse.id}] ❌ DÉPLACEMENT ÉCHOUÉ")
            # Déplacement impossible, chercher une autre cible
            self.cible_actuelle = None
            self.mode = "recherche"
            return False
    
    def deplacer_aleatoirement(self, grille: List[List[Point]], ships: List[Ship]) -> bool:
        """
        Déplace la foreuse vers une position aléatoire accessible.
        """
        print(f"[IA Foreuse {self.foreuse.id}] 🎲 Déplacement aléatoire")
        
        positions = self.foreuse.positions_possibles_adjacentes(grille)
        print(f"[IA Foreuse {self.foreuse.id}] {len(positions)} positions possibles")
        
        if positions:
            position_aleatoire = random.choice(positions)
            print(f"[IA Foreuse {self.foreuse.id}] Position choisie: {position_aleatoire}")
            
            success = self.foreuse.deplacement(position_aleatoire, grille, ships)
            
            if success:
                print(f"[IA Foreuse {self.foreuse.id}] ✅ Déplacement aléatoire RÉUSSI")
                return True
            else:
                print(f"[IA Foreuse {self.foreuse.id}] ❌ Déplacement aléatoire ÉCHOUÉ")
        else:
            print(f"[IA Foreuse {self.foreuse.id}] ❌ Aucune position accessible")
        
        return False
    
    def reset(self):
        """Réinitialise l'état de l'IA (appelé en début de tour)."""
        print(f"[IA Foreuse {self.foreuse.id}] 🔄 RESET de l'IA")
        if self.mode == "attente":
            # Si on était en attente de minage, on reste sur la même cible
            self.mode = "deplacement"
            print(f"[IA Foreuse {self.foreuse.id}] Mode attente -> déplacement")
        # Ne pas réinitialiser la cible si on est déjà en cours