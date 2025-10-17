from classes.Ship import *

class IA_Lourd(Lourd):
    # ==================================
    # MÉTHODE POUR L'INTELLIGENCE ARTIFICIELLE
    # ==================================
    def jouer_tour_ia(self, grille: List[List[Point]], tous_les_vaisseaux: List["Ship"], ennemis: List["Ship"]):
        """
        Exécute le tour d'un vaisseau contrôlé par l'IA selon une logique de priorités.
        1. Attaquer l'ennemi à portée avec le plus de PV MAX.
        2. Si personne à portée, se déplacer vers l'ennemi le plus proche.
        3. Après le déplacement, vérifier à nouveau si une attaque est possible.
        """        


        # --- PRIORITÉ 1 : ATTAQUER SANS SE DÉPLACER ---

        # 1.1. Trouver tous les ennemis à portée d'attaque
        cibles_a_portee = []
        cases_attaquables = self.positions_possibles_attaque(grille)
        
        for ennemi in ennemis:
            # On vérifie si n'importe quelle case de l'ennemi est dans notre portée
            largeur_ennemi, hauteur_ennemi = ennemi.donner_dimensions(ennemi.direction)
            ennemi_occupe_cases = False
            for l in range(ennemi.cordonner.x, ennemi.cordonner.x + hauteur_ennemi):
                for c in range(ennemi.cordonner.y, ennemi.cordonner.y + largeur_ennemi):
                    if (l, c) in cases_attaquables:
                        cibles_a_portee.append(ennemi)
                        ennemi_occupe_cases = True
                        break
                if ennemi_occupe_cases:
                    break
        
        # 1.2. Si des cibles sont à portée, choisir la meilleure et attaquer
        if cibles_a_portee:
            # Cible = celle avec le plus de PV MAX
            cible_finale = max(cibles_a_portee, key=lambda ship: ship.pv_max)
                        
            # On utilise la méthode `deplacement` qui gère aussi les attaques
            # On cible la case "coin" du vaisseau ennemi
            self.deplacement((cible_finale.cordonner.x, cible_finale.cordonner.y), grille, tous_les_vaisseaux)
            return # L'action est terminée pour ce tour

        # --- PRIORITÉ 2 : SE DÉPLACER VERS L'ENNEMI LE PLUS PROCHE ---

        # 2.1. Trouver l'ennemi le plus proche
        ennemi_le_plus_proche = min(ennemis, key=lambda e: abs(e.cordonner.x - self.cordonner.x) + abs(e.cordonner.y - self.cordonner.y))

        # 2.2. Trouver la meilleure case où se déplacer
        # On cherche la case atteignable qui nous rapproche le plus de la cible
        cases_deplacement_possibles = self.positions_possibles_adjacentes(grille)
        
        if not cases_deplacement_possibles:
            return # Aucune case n'est accessible

        meilleure_case = None
        distance_minimale = float('inf')

        for case in cases_deplacement_possibles:
            l, c = case
            # Calcul de la distance depuis la case de destination potentielle vers l'ennemi
            dist = abs(l - ennemi_le_plus_proche.cordonner.x) + abs(c - ennemi_le_plus_proche.cordonner.y)
            if dist < distance_minimale:
                distance_minimale = dist
                meilleure_case = case

        # 2.3. Exécuter le déplacement vers la meilleure case trouvée
        if meilleure_case:
            self.deplacement(meilleure_case, grille, tous_les_vaisseaux)

            # --- PRIORITÉ 3 : ATTAQUER APRÈS S'ÊTRE DÉPLACÉ ---
            # Après avoir bougé, on revérifie si une cible est à portée
            
            # On met à jour les cibles potentielles depuis la nouvelle position
            cibles_a_portee_apres_mvt = []
            cases_attaquables_apres_mvt = self.positions_possibles_attaque(grille)
            for ennemi in ennemis:
                largeur_ennemi, hauteur_ennemi = ennemi.donner_dimensions(ennemi.direction)
                ennemi_occupe_cases = False
                for l in range(ennemi.cordonner.x, ennemi.cordonner.x + hauteur_ennemi):
                    for c in range(ennemi.cordonner.y, ennemi.cordonner.y + largeur_ennemi):
                        if (l, c) in cases_attaquables_apres_mvt:
                            cibles_a_portee_apres_mvt.append(ennemi)
                            ennemi_occupe_cases = True
                            break
                    if ennemi_occupe_cases:
                        break

            if cibles_a_portee_apres_mvt:
                # Si on peut attaquer, on choisit la meilleure cible et on attaque
                cible_finale_apres_mvt = max(cibles_a_portee_apres_mvt, key=lambda ship: ship.pv_max)
                self.deplacement((cible_finale_apres_mvt.cordonner.x, cible_finale_apres_mvt.cordonner.y), grille, tous_les_vaisseaux)