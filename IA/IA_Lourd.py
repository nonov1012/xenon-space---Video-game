from classes.Ship import *
from classes.GlobalVar.ScreenVar import ScreenVar
from classes.GlobalVar.GridVar import GridVar

class IA_Lourd(Lourd):
    def __init__(self, cordonner: Point, id: Optional[int] = None, path: str = None,
                 image: Optional[pygame.Surface] = None, joueur: int = 1):
        stats = SHIP_STATS["Lourd"]
        
        if image is None:
            image = pygame.Surface((stats["taille"][1]*GridVar.cell_size, stats["taille"][0]*GridVar.cell_size))
        
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
        """
        if not ennemis or (self.port_deplacement <= 0 and self.port_attaque <= 0):
            return

        # 1. --- Attaque directe si possible ---
        positions_attaque = self.positions_possibles_attaque(grille, direction=self.direction)
        cibles_dans_portee = [
            e for e in ennemis
            if (e.cordonner.x, e.cordonner.y) in positions_attaque and not e.est_mort()
        ]
        if cibles_dans_portee:
            cible = max(cibles_dans_portee, key=lambda e: e.pv_max)
            self.deplacement((cible.cordonner.x, cible.cordonner.y), grille, all_ship)
            return

        # 2. --- Déplacement vers l'ennemi le plus proche (via A*) ---
        ennemi_proche = min(ennemis, key=lambda e: abs(self.cordonner.x - e.cordonner.x) + abs(self.cordonner.y - e.cordonner.y))
        cible_pos = (ennemi_proche.cordonner.x, ennemi_proche.cordonner.y)

        # Récupérer les informations de la grille
        nb_lignes, nb_colonnes = len(grille), len(grille[0])
        cout_case = {Type.VIDE: 1, Type.ATMOSPHERE: 2}

        # Structure A* : (f_score, g_score, position)
        import heapq
        queue = [(0, 0, (self.cordonner.x, self.cordonner.y))] # (f, g, pos)
        g_score = {(self.cordonner.x, self.cordonner.y): 0}
        parent = {}
        
        meilleur_f = float("inf")
        meilleure_destination_a_star = None

        while queue:
            f, g, current_pos = heapq.heappop(queue)
            l, c = current_pos

            # Si l'on est dans la portée d'attaque de la cible (Manhattan), c'est une destination viable pour l'A*
            if abs(l - cible_pos[0]) + abs(c - cible_pos[1]) <= self.port_attaque:
                # On a trouvé la case la plus proche de l'ennemi qui permet d'attaquer ou d'être le plus proche possible.
                # Si l'ennemi est atteint, on peut s'arrêter.
                if f < meilleur_f:
                    meilleur_f = f
                    meilleure_destination_a_star = current_pos
                # break # On pourrait break ici pour le premier chemin trouvé, mais continuer peut affiner si plusieurs cibles.
                
            # On arrête de chercher si le coût g (coût réel) dépasse notre portée de déplacement maximale
            # (Bien que cela devrait déjà être géré par la boucle elle-même)
            # On continue la recherche sur l'intégralité de la grille pour trouver le meilleur chemin global.

            # On itère sur les 4 directions cardinales
            for dl, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nl, nc = l + dl, c + dc
                
                # Pour la simplicité de l'A* qui trouve le chemin optimal, on ne considère que l'orientation actuelle
                # lors du déplacement (l'orientation peut être changée après la sélection de la case cible).
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
        
        # 3. --- Reconstitution et exécution du premier pas ---

        # Si l'A* a trouvé un chemin (même partiel, si l'ennemi est trop loin)
        if not parent:
            # Aucune case adjacente accessible. On ne peut rien faire.
            return
        
        # S'il n'y a pas de meilleure_destination_a_star (trop loin), on choisit la case la plus proche de l'ennemi trouvée par A*
        if meilleure_destination_a_star is None:
            # On prend la case finale du g_score qui minimise la distance de Manhattan
            meilleure_destination_a_star = min(g_score.keys(), 
                                            key=lambda pos: abs(pos[0] - cible_pos[0]) + abs(pos[1] - cible_pos[1]))


        # Reconstituer le chemin depuis la meilleure destination A* jusqu'au départ
        chemin = []
        node = meilleure_destination_a_star
        while node and node != (self.cordonner.x, self.cordonner.y):
            chemin.append(node)
            node = parent.get(node)
        
        # Si le chemin est juste le point de départ ou si A* a échoué complètement
        if not chemin: 
            return

        chemin.reverse()
        
        # Le premier pas est la première case après la case de départ
        if len(chemin) >= 3 :
            premier_pas = chemin[2]
        elif len(chemin) == 2 :
            premier_pas = chemin[1]
        elif len(chemin) == 1 :
            premier_pas = chemin[0]
        
        # Vérifier si ce premier pas est dans la portée de déplacement
        # Note : Le calcul de coût est déjà dans l'A*, mais vérifions
        
        # La case cible pour le déplacement est le premier pas du chemin A*
        case_cible_deplacement = premier_pas

        # Tenter de déterminer la meilleure direction pour se rendre à cette case (simplifié : la direction du mouvement)
        dl = case_cible_deplacement[0] - self.cordonner.x
        dc = case_cible_deplacement[1] - self.cordonner.y
        
        meilleure_direction = self.direction
        if dl == -1: meilleure_direction = "haut"
        elif dl == 1: meilleure_direction = "bas"
        elif dc == -1: meilleure_direction = "gauche"
        elif dc == 1: meilleure_direction = "droite"

        # Anti-boucle : on évite de faire le premier pas si son coût dépasse le port_deplacement actuel.
        # L'A* est fait sur la grille entière, donc il faut vérifier si le premier pas est atteignable.
        
        # On doit vérifier si la case cible est atteignable en un seul tour (similaire à positions_possibles_adjacentes)
        cases_possibles_un_tour = self.positions_possibles_adjacentes(grille, direction=meilleure_direction)
        if case_cible_deplacement not in cases_possibles_un_tour:
            # Si le premier pas A* n'est pas atteignable ce tour-ci (portée insuffisante), on choisit la meilleure
            # case parmi celles qui sont atteignables et qui minimisent la distance de Manhattan.
            if cases_possibles_un_tour:
                case_cible_deplacement = min(cases_possibles_un_tour, 
                                            key=lambda pos: abs(pos[0] - cible_pos[0]) + abs(pos[1] - cible_pos[1]))
                
                # Mettre à jour la direction pour ce choix de secours
                dl_s = case_cible_deplacement[0] - self.cordonner.x
                dc_s = case_cible_deplacement[1] - self.cordonner.y
                if dl_s == -1: meilleure_direction = "haut"
                elif dl_s == 1: meilleure_direction = "bas"
                elif dc_s == -1: meilleure_direction = "gauche"
                elif dc_s == 1: meilleure_direction = "droite"
            else:
                return

        # Exécution du déplacement
        self._derniere_case = (self.cordonner.x, self.cordonner.y)
        self.aperçu_direction = meilleure_direction
        self.deplacement(case_cible_deplacement, grille, all_ship)