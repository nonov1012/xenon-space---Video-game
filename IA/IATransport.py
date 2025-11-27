from classes.Ship import *
from classes.Turn import Turn
from classes.Point import Point
from typing import List, Tuple, Optional, Dict

class IATransport(Transport):

    def __init__(self, cordonner: Point, id: Optional[int] = None, path: str = None,
                 image: Optional[pygame.Surface] = None, joueur: int = 1):
        # Le vaisseau transport contrôlé par cette IA
    
        # Dictionnaire qui stocke les demandes de transport : {vaisseau: position_destination}
        self.demandes_transport: Dict[Ship, Tuple[int, int]] = {}
        super().__init__(
            cordonner,
            id,
            path,
            image,
            joueur
        )

    # ------------------- Vérifications -------------------
    def est_transportable(self, ship: Ship) -> bool:
        """Vérifie si un vaisseau peut être transporté par ce transport"""
        return isinstance(ship, (Petit, Moyen, Foreuse))  # Seuls ces types sont transportables

    # ------------------- Recherche de vaisseaux -------------------
    def trouver_vaisseaux_proches(self, ships: List[Ship]) -> List[Ship]:
        """Retourne la liste des vaisseaux transportables à distance <= 1 case"""
        transportables = []
        for s in ships:
            if s != self and not s.est_mort() and self.est_transportable(s):
                distance = abs(s.cordonner.x - self.cordonner.x) + abs(s.cordonner.y - self.cordonner.y)
                if distance <= 1:
                    transportables.append(s)
        return transportables

    def trouver_vaisseaux_allies(self, ships: List[Ship]) -> List[Ship]:
        """Retourne tous les vaisseaux alliés transportables sur la carte"""
        return [s for s in ships if s != self and not s.est_mort() and self.est_transportable(s)]

    # ------------------- Embarquement -------------------
    def embarquer_vaisseaux(self, vaisseaux: List[Ship], grille: List[List[Point]]) -> int:
        """Tente d'embarquer les vaisseaux fournis et retourne le nombre embarqué"""
        embarques = 0
        for vaisseau in vaisseaux:
            if self.ajouter_cargo(vaisseau, grille):
                # Ne pas supprimer la demande ici, on la garde pour la livraison
                embarques += 1
        return embarques

    # ------------------- Débarquement -------------------
    def debarquer_vaisseau(self, vaisseau_embarque: Ship, destination: Tuple[int, int], 
                          grille: List[List[Point]], ships: List[Ship]) -> bool:
        """
        Tente de débarquer un vaisseau à sa destination.
        Retourne True si le débarquement a réussi, False sinon.
        """
        
        # Trouver les positions de débarquement disponibles
        positions_debarquement = self.positions_debarquement(vaisseau_embarque, grille)
        
        if not positions_debarquement:
            return False
        
        # Choisir la position la plus proche de la destination
        meilleure_position = min(positions_debarquement, 
                                key=lambda pos: abs(pos[0]-destination[0]) + abs(pos[1]-destination[1]))
        
        
        # Tenter le débarquement
        try:
            index = self.cargaison.index(vaisseau_embarque)
        except ValueError:
            return False # Ne devrait pas arriver dans la logique normale
            
        success = self.retirer_cargo(index, meilleure_position[0], 
                                         meilleure_position[1], grille, ships)
        
        
        if success:
            # Supprimer la demande de transport
            if vaisseau_embarque in self.demandes_transport:
                del self.demandes_transport[vaisseau_embarque]
            return True
        else:
            return False

    # ------------------- Calcul de position -------------------
    def calculer_position_moyenne(self, vaisseaux: List[Ship]) -> Tuple[int, int]:
        """Retourne la position moyenne (x, y) d'une liste de vaisseaux"""
        if not vaisseaux:
            return (self.cordonner.x, self.cordonner.y)
        avg_x = round(sum(s.cordonner.x for s in vaisseaux) / len(vaisseaux))
        avg_y = round(sum(s.cordonner.y for s in vaisseaux) / len(vaisseaux))
        return (avg_x, avg_y)

    # NOUVELLE MÉTHODE pour calculer une position de fuite
    def calculer_position_fuite(self, cible: Tuple[int, int], grille: List[List[Point]]) -> Tuple[int, int]:
        """
        Calcule une position opposée à la cible (destination).
        Taille de la grille est supposée être (len(grille[0]), len(grille)).
        """
        largeur = len(grille[0]) - 1 
        hauteur = len(grille) - 1
        
        # Vecteur de déplacement actuel (cible - transport)
        dx = cible[0] - self.cordonner.x
        dy = cible[1] - self.cordonner.y
        
        # Position opposée : fuir dans la direction opposée (symétrie par rapport au transport)
        # Mais pour plus simple, on inverse la direction du mouvement
        
        # Si le transport se dirigeait vers la cible, on s'éloigne
        # Pour simplifier, on prend l'opposé de la coordonnée la plus éloignée du bord
        
        # On calcule le "point miroir" de la cible par rapport au transport, puis on le contraint aux bords
        
        # Décalage par rapport au centre de la carte (largeur/2, hauteur/2)
        centre_x = largeur / 2
        centre_y = hauteur / 2
        
        # Si le transport est à gauche du centre, on fuit vers la droite (et inversement)
        # Si le transport est en haut, on fuit vers le bas (et inversement)
        
        fuite_x = largeur - self.cordonner.x # "Miroir" par rapport à l'axe X
        fuite_y = hauteur - self.cordonner.y # "Miroir" par rapport à l'axe Y
        
        # On contraint aux limites de la carte
        fuite_x = max(0, min(largeur, fuite_x))
        fuite_y = max(0, min(hauteur, fuite_y))
        
        return (round(fuite_x), round(fuite_y))

    # ------------------- Déplacement -------------------
    def trouver_meilleure_case_adjacente(self, cible: Tuple[int, int], grille: List[List[Point]], ships: List[Ship]) -> Optional[Tuple[int, int]]:
        """Retourne la meilleure case adjacente pour se rapprocher de la cible"""
        cases_possibles = self.positions_possibles_adjacentes(grille)
        if not cases_possibles:
            return None
        return min(cases_possibles, key=lambda pos: abs(pos[0]-cible[0]) + abs(pos[1]-cible[1]))

    def deplacer_vers(self, cible: Tuple[int, int], grille: List[List[Point]], ships: List[Ship]) -> bool:
        """Déplace le transport vers la position cible"""
        case = self.trouver_meilleure_case_adjacente(cible, grille, ships)
        if case:
            resultat = self.deplacement(case, grille, ships)
            return resultat
        return False

    # ------------------- Déplacer vaisseau allié vers le transport -------------------
    def deplacer_vaisseau_vers(self, vaisseau: Ship, cible: Tuple[int,int], grille: List[List[Point]], ships: List[Ship]):
        """Déplace un vaisseau allié vers la cible (transport)"""
        cases_possibles = vaisseau.positions_possibles_adjacentes(grille)
        if cases_possibles:
            meilleure_case = min(cases_possibles, key=lambda pos: abs(pos[0]-cible[0]) + abs(pos[1]-cible[1]))
            vaisseau.deplacement(meilleure_case, grille, ships)

    # ------------------- Gestion des appels -------------------
    def appel_transport(self, vaisseau_appelant: Ship, position_destination: Tuple[int, int] = [15, 15]):
        """Enregistre une demande de transport pour un vaisseau"""
        if self.est_transportable(vaisseau_appelant):
            self.demandes_transport[vaisseau_appelant] = position_destination

    def calculer_priorite_appel(self, vaisseau_appelant: Ship) -> float:
        """Calcule la priorité d'un appel (distance au transport)"""
        return abs(vaisseau_appelant.cordonner.x - self.cordonner.x) + \
               abs(vaisseau_appelant.cordonner.y - self.cordonner.y)

    def choisir_meilleur_appel(self) -> Optional[Ship]:
        """Choisit l'appel le plus pertinent à traiter"""
        candidats = {}
        for vaisseau, destination in self.demandes_transport.items():
            distance_restante = abs(vaisseau.cordonner.x - destination[0]) + abs(vaisseau.cordonner.y - destination[1])
            distance_transport = abs(vaisseau.cordonner.x - self.cordonner.x) + abs(vaisseau.cordonner.y - self.cordonner.y)
            if distance_transport < distance_restante:
                candidats[vaisseau] = distance_transport
        if not candidats:
            return None
        return min(candidats.keys(), key=lambda v: candidats[v])

    # ------------------- Tour de l'IA -------------------
    def jouer_tour(self, grille: List[List[Point]], ships: List[Ship]):
        """Logique principale du tour de l'IA Transport"""
        
        # ⚠️ NOUVEAU : Vérification des PV faibles (moins de 15%)
        pv_faibles = self.pv_actuel < 0.15 * self.pv_max
        
        if pv_faibles and self.cargaison:
            
            derniere_destination = None # Pour calculer la fuite
            
            # Tenter de débarquer TOUS les vaisseaux immédiatement
            for i, vaisseau_embarque in reversed(list(enumerate(self.cargaison))): 
                if vaisseau_embarque is None:
                    continue
                
                # Prendre la destination du vaisseau s'il en a une
                if vaisseau_embarque in self.demandes_transport:
                    destination = self.demandes_transport[vaisseau_embarque]
                    derniere_destination = destination
                else:
                    # Destination par défaut pour le débarquement (sa position actuelle)
                    destination = (self.cordonner.x, self.cordonner.y)
                
                # Tenter le débarquement
                # On utilise la destination actuelle du transport comme "cible" pour trouver la meilleure case adjacente
                self.debarquer_vaisseau(vaisseau_embarque, destination, grille, ships)
            
            # ➡️ FUITE : Va au point opposé qu'il devait aller (si une destination existait)
            if derniere_destination:
                position_fuite = self.calculer_position_fuite(derniere_destination, grille)
                self.deplacer_vers(position_fuite, grille, ships)
            else:
                # Si pas de destination connue, fuir loin des bords (vers le centre) ou rester immobile
                centre_x = len(grille[0]) // 2
                centre_y = len(grille) // 2
                self.deplacer_vers((centre_x, centre_y), grille, ships)

            return # Fin du tour en cas d'urgence

        # 1️⃣ Vérifier si on transporte quelqu'un avec une destination
        for vaisseau_embarque in self.cargaison:
            if vaisseau_embarque is None:
                continue
            
            # Vérifier si ce vaisseau avait une demande de transport
            if vaisseau_embarque in self.demandes_transport:
                destination = self.demandes_transport[vaisseau_embarque]
                distance_destination = abs(self.cordonner.x - destination[0]) + \
                                     abs(self.cordonner.y - destination[1])
                
                
                # Si on est arrivé à destination (distance <= 1)
                if distance_destination <= 1:
                    # Tenter le débarquement
                    if self.debarquer_vaisseau(vaisseau_embarque, destination, grille, ships):
                        # Si le débarquement du premier vaisseau en cargaison réussi, on arrête le tour 
                        # pour que le vaisseau débarqué puisse potentiellement jouer (même si dans l'implémentation
                        # typique, les actions sont séquentielles, on s'arrête ici pour une logique simple).
                        return 
                    else:
                        # Pas de place pour débarquer, continuer d'avancer
                        self.deplacer_vers(destination, grille, ships)
                        return
                else:
                    # Continuer vers la destination
                    self.deplacer_vers(destination, grille, ships)
                    return
    
        # 2️⃣ Embarquer vaisseaux proches
        vaisseaux_proches = self.trouver_vaisseaux_proches(ships)
        if vaisseaux_proches:
            nb_embarques = self.embarquer_vaisseaux(vaisseaux_proches, grille)
            return
    
        # 3️⃣ Répondre aux appels
        if self.demandes_transport:
            vaisseau_cible = self.choisir_meilleur_appel()
            if vaisseau_cible:
                # Déplacer le vaisseau allié vers le transport
                self.deplacer_vaisseau_vers(vaisseau_cible, (self.cordonner.x, self.cordonner.y), grille, ships)
                # Déplacer le transport vers le vaisseau allié
                position_cible = (vaisseau_cible.cordonner.x, vaisseau_cible.cordonner.y)
                self.deplacer_vers(position_cible, grille, ships)
                return
    
        # 4️⃣ Se rapprocher des alliés restants
        vaisseaux_allies = self.trouver_vaisseaux_allies(ships)
        if not vaisseaux_allies:
            return
    
        position_cible = self.calculer_position_moyenne(vaisseaux_allies)
        distance = abs(position_cible[0]-self.cordonner.x) + abs(position_cible[1]-self.cordonner.y)
        self.deplacer_vers(position_cible, grille, ships)