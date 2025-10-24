from classes.Ship import *

class IA_Lourd(Lourd):
    def __init__(self, cordonner: Point, id: Optional[int] = None, path: str = None,
                 image: Optional[pygame.Surface] = None, joueur: int = 1):
        stats = SHIP_STATS["Lourd"]
        
        if image is None:
            image = pygame.Surface((stats["taille"][1]*TAILLE_CASE, stats["taille"][0]*TAILLE_CASE))
        
        super().__init__(
            cordonner,
            id,
            path,
            image,
            joueur
        )
    # ==================================
    # MÉTHODE POUR L'INTELLIGENCE ARTIFICIELLE
    # ==================================
    def deplacer_vaisseau_vers(self, vaisseau: Ship, cible: Tuple[int,int], grille: List[List[Point]], ships: List[Ship]):
        """Déplace un vaisseau"""
        cases_possibles = vaisseau.positions_possibles_adjacentes(grille)
        if cases_possibles:
            meilleure_case = min(cases_possibles, key=lambda pos: abs(pos[0]-cible[0]) + abs(pos[1]-cible[1]))
            vaisseau.deplacement(meilleure_case, grille, ships) 
            
    def distance(self, v1, v2): 
        return abs(v1.cordonner.x - v2.cordonner.x) + abs(v1.cordonner.y - v2.cordonner.y)

    def jouer_tour_ia(self, grille, all_ship, ennemis):
        """
        IA du vaisseau Lourd :
        - Attaque si possible.
        - Sinon, se rapproche de l'ennemi le plus proche en utilisant A* pour trouver le chemin le moins coûteux.
        - Si aucune action n'a été faite, tente d'avancer d'une case en haut, sinon d'une case en bas.
        """
        if not ennemis or (self.port_deplacement <= 0 and self.port_attaque <= 0):
            return

        # Stocke la position initiale pour vérifier si un mouvement a eu lieu
        position_initiale = (self.cordonner.x, self.cordonner.y)

        # 1. --- Attaque directe si possible (Sans Mouvement) ---
        if self.port_attaque > 0:
            positions_attaque = self.positions_possibles_attaque(grille, direction=self.direction)
            cibles_dans_portee = [
                e for e in ennemis
                if (e.cordonner.x, e.cordonner.y) in positions_attaque and not e.est_mort()
            ]
            
            if cibles_dans_portee:
                cible = max(cibles_dans_portee, key=lambda e: e.pv_max)
                cible_pos = (cible.cordonner.x, cible.cordonner.y)
                
                # Exécuter l'action d'attaque (qui utilise self.deplacement(...) selon votre règle)
                self.deplacement(cible_pos, grille, all_ship) 
                
                self.port_attaque = 0 
                return # Fin du tour après l'attaque/action

        # 2. --- Déplacement vers l'ennemi le plus proche (via A*) ---
        # ... (le code A* pour trouver la meilleure_destination_a_star) ...
        ennemi_proche = min(ennemis, key=lambda e: abs(self.cordonner.x - e.cordonner.x) + abs(self.cordonner.y - e.cordonner.y))
        cible_pos = (ennemi_proche.cordonner.x, ennemi_proche.cordonner.y)

        nb_lignes, nb_colonnes = len(grille), len(grille[0])
        cout_case = {Type.VIDE: 1, Type.ATMOSPHERE: 2}

        import heapq
        queue = [(0, 0, (self.cordonner.x, self.cordonner.y))] # (f, g, pos)
        g_score = {(self.cordonner.x, self.cordonner.y): 0}
        parent = {}
        
        meilleur_f = float("inf")
        meilleure_destination_a_star = None

        while queue:
            f, g, current_pos = heapq.heappop(queue)
            l, c = current_pos

            if abs(l - cible_pos[0]) + abs(c - cible_pos[1]) <= self.port_attaque:
                if f < meilleur_f:
                    meilleur_f = f
                    meilleure_destination_a_star = current_pos
                # On pourrait break ici pour le premier chemin trouvé, mais continuer peut affiner si plusieurs cibles.
            
            # On itère sur les 4 directions cardinales
            for dl, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nl, nc = l + dl, c + dc
                
                direction_actuelle = self.direction 
                largeur, hauteur = self.donner_dimensions(direction_actuelle)
                
                # Vérification des limites de la grille
                if not (0 <= nl <= nb_lignes - hauteur and 0 <= nc <= nb_colonnes - largeur):
                    continue
                
                # Calcul du coût du mouvement (max cost de la case la plus chère dans l'emprise du vaisseau)
                max_cost = 0
                valide = True
                for yy in range(nl, nl + hauteur):
                    for xx in range(nc, nc + largeur):
                        point = grille[yy][xx]
                        if point.type in cout_case:
                            max_cost = max(max_cost, cout_case[point.type])
                        elif point.type != Type.VAISSEAU: # Collision avec planète/astéroïde/etc.
                            valide = False
                            break
                    if not valide:
                        break
                
                if not valide:
                    continue

                # Vérification de collision avec d'autres vaisseaux (le vaisseau cible doit être ignoré si c'est lui)
                if not self.verifier_collision(grille, nl, nc, direction_actuelle, ignorer_self=True):
                    continue

                g_next = g + max_cost
                h_next = abs(nl - cible_pos[0]) + abs(nc - cible_pos[1]) # Heuristique : Manhattan
                f_next = g_next + h_next

                if (nl, nc) not in g_score or g_next < g_score[(nl, nc)]:
                    g_score[(nl, nc)] = g_next
                    parent[(nl, nc)] = current_pos
                    heapq.heappush(queue, (f_next, g_next, (nl, nc)))
        
        # 3. --- Reconstitution et exécution du DEPLACEMENT MAXIMAL sur le chemin A* ---
        
        if not parent:
            pass
        else:
            if meilleure_destination_a_star is None:
                # Si A* n'a pas atteint la portée d'attaque, on va le plus loin possible vers la cible.
                meilleure_destination_a_star = min(g_score.keys(), 
                                                key=lambda pos: abs(pos[0] - cible_pos[0]) + abs(pos[1] - cible_pos[1]))

            chemin = []
            node = meilleure_destination_a_star
            while node and node != (self.cordonner.x, self.cordonner.y):
                chemin.append(node)
                node = parent.get(node)
            
            if chemin: 
                chemin.reverse()
                
                # NOUVELLE LOGIQUE : Trouver la case la plus éloignée dans la limite de port_deplacement
                case_cible_deplacement = position_initiale
                
                for pos_suivante in chemin:
                    # g_score[pos_suivante] contient le coût TOTAL du mouvement depuis le départ
                    if g_score.get(pos_suivante, float('inf')) <= self.port_deplacement:
                        case_cible_deplacement = pos_suivante
                    else:
                        # On a dépassé le port de déplacement
                        break

                # Si la case cible est la position initiale, aucun mouvement n'est possible (ou elle est trop loin)
                if case_cible_deplacement != position_initiale:
                    # OPTIMISATION DE LA ROTATION : Déterminer la direction en fonction du mouvement global (et non du premier pas)
                    dl = case_cible_deplacement[0] - self.cordonner.x
                    dc = case_cible_deplacement[1] - self.cordonner.y
                    
                    meilleure_direction = self.direction
                    if dl < 0: meilleure_direction = "haut"
                    elif dl > 0: meilleure_direction = "bas"
                    elif dc < 0: meilleure_direction = "gauche"
                    elif dc > 0: meilleure_direction = "droite"
                    # Si dl et dc sont tous deux non nuls, le mouvement est diagonal; la direction prendra l'une des 4.
                    
                    # Exécution du déplacement A*
                    self._derniere_case = (self.cordonner.x, self.cordonner.y)
                    self.aperçu_direction = meilleure_direction
                    # L'appel à deplacement avec case_cible_deplacement exécute le mouvement en une seule fois
                    self.deplacement(case_cible_deplacement, grille, all_ship)

                    # NOUVEAU : Vérification de la possibilité d'attaquer après le mouvement
                    if self.port_attaque > 0:
                        # Ré-évaluer les cibles après le mouvement
                        # Utiliser la direction que le vaisseau a choisie
                        positions_attaque_apres_mouvement = self.positions_possibles_attaque(grille, direction=self.aperçu_direction)
                        cibles_apres_mouvement = [
                            e for e in ennemis
                            if (e.cordonner.x, e.cordonner.y) in positions_attaque_apres_mouvement and not e.est_mort()
                        ]

                        if cibles_apres_mouvement:
                            cible_a_attaquer = max(cibles_apres_mouvement, key=lambda e: e.pv_max)
                            
                            # L'IA est maintenant à portée, elle attaque l'ennemi.
                            self.deplacement((cible_a_attaquer.cordonner.x, cible_a_attaquer.cordonner.y), grille, all_ship)
                            
                            self.port_attaque = 0 
                            return # Fin du tour après le déplacement ET l'attaque.
        
        # 4. --- Mouvement par défaut si aucune action n'a eu lieu ---
        if (self.cordonner.x, self.cordonner.y) == position_initiale:
            
            # Tente d'avancer d'une case en HAUT
            haut_pos = (self.cordonner.x - 1, self.cordonner.y)
            cases_possibles_un_tour = self.positions_possibles_adjacentes(grille, direction="haut")
            
            if haut_pos in cases_possibles_un_tour:
                # Déplacement en haut
                self._derniere_case = position_initiale
                self.aperçu_direction = "haut"
                self.deplacement(haut_pos, grille, all_ship)
                return

            # Si le mouvement en HAUT a échoué, tente de reculer d'une case en BAS
            bas_pos = (self.cordonner.x + 1, self.cordonner.y)
            cases_possibles_un_tour = self.positions_possibles_adjacentes(grille, direction="bas")
            
            if bas_pos in cases_possibles_un_tour:
                # Déplacement en bas
                self._derniere_case = position_initiale
                self.aperçu_direction = "bas"
                self.deplacement(bas_pos, grille, all_ship)
                return

        return