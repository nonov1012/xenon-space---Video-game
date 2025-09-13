import heapq  # Import pour une file de priorite pour A*

class Deplacement:
    def __init__(self, vaisseau, grille, rayon=3):
        """
        Initialise la classe de gestion du déplacement du vaisseau.

        Args:
            vaisseau: instance de la classe Vaisseau
            grille: liste 2D représentant la grille (0 = libre, 1 = obstacle)
            rayon: distance maximale autour du vaisseau pour calculer les positions accessibles
        """
        self.vaisseau = vaisseau  # Le vaisseau a deplacer
        self.grille = grille      # La grille de jeu avec obstacles
        self.rayon = rayon        # Rayon autour du vaisseau pour calculer déplacements possibles
        self.cases_accessibles = []  # Liste des cases accessibles autour du vaisseau

    def mettre_a_jour_cases_accessibles(self):
        """
        Calcule toutes les positions accessibles autour du vaisseau.

        Le calcul se fait sur un rayon donné et utilise la distance de Manhattan
        pour limiter les déplacements à l'intérieur du rayon. Les positions qui 
        entreraient en collision avec un obstacle ou hors de la grille sont exclues.
        """
        positions = []
        for dx in range(-self.rayon, self.rayon + 1):
            for dy in range(-self.rayon, self.rayon + 1):
                if abs(dx) + abs(dy) <= self.rayon:  # limite par distance de Manhattan
                    nouvelle_x = self.vaisseau.x + dx
                    nouvelle_y = self.vaisseau.y + dy
                    if self.peut_aller(nouvelle_x, nouvelle_y):
                        positions.append((nouvelle_x, nouvelle_y))
        self.cases_accessibles = positions

    def peut_aller(self, x, y):
        """
        Vérifie si le vaisseau peut aller à la position (x, y) sans collision.

        Conditions :
            - Le vaisseau ne sort pas de la grille.
            - Le vaisseau ne touche pas un obstacle (valeur 1 dans la grille).

        Returns:
            True si la position est accessible, False sinon.
        """
        # Vérifie si le vaisseau sort de la grille
        if x < 0 or y < 0 or x + self.vaisseau.largeur > len(self.grille) or y + self.vaisseau.hauteur > len(self.grille):
            return False

        # Vérifie la presence d'obstacles dans l'espace que le vaisseau occuperait
        for dx in range(self.vaisseau.largeur):
            for dy in range(self.vaisseau.hauteur):
                if self.grille[y + dy][x + dx] == 1:
                    return False
        return True

    def heuristique(self, case_a, case_b):
        """
        Calcule la distance de Manhattan entre deux cases.

        Args:
            case_a: tuple (x, y) première position
            case_b: tuple (x, y) deuxième position

        Returns:
            Distance en nombre de cases à parcourir horizontalement et verticalement
        """
        return abs(case_a[0] - case_b[0]) + abs(case_a[1] - case_b[1])

    def astar(self, depart, cible):
        """
        Algorithme A* pour trouver le chemin le plus court entre deux positions.

        Args:
            depart: tuple (x, y) position de départ
            cible: tuple (x, y) position cible

        Returns:
            Liste de tuples (x, y) représentant le chemin à suivre.
            Retourne une liste vide si aucun chemin n'est trouvé.
        """
        file_priorite = []
        heapq.heappush(file_priorite, (0, depart))

        chemin_fait = {}
        score_g = {depart: 0}
        cases_visitees = set()

        while file_priorite:
            #la case avec le plus petit score
            _, case_courante = heapq.heappop(file_priorite)

            if case_courante in cases_visitees:
                continue
            cases_visitees.add(case_courante)

            # Si la case courante est la cible reconstruire le chemin
            if case_courante == cible:
                chemin = []
                while case_courante in chemin_fait:
                    chemin.append(case_courante)
                    case_courante = chemin_fait[case_courante]
                chemin.reverse()
                return chemin

            # Explorer les voisins (droite, gauche, bas, haut)
            for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
                voisin = (case_courante[0] + dx, case_courante[1] + dy)
                if self.peut_aller(voisin[0], voisin[1]):
                    cout_temporaire = score_g[case_courante] + 1
                    if voisin not in score_g or cout_temporaire < score_g[voisin]:
                        score_g[voisin] = cout_temporaire
                        f = cout_temporaire + self.heuristique(voisin, cible)
                        heapq.heappush(file_priorite, (f, voisin))
                        chemin_fait[voisin] = case_courante

        return []


    def deplacer_vaisseau(self):
        """
        Déplace le vaisseau pas à pas le long du chemin calculé.

        Cette fonction doit être appelée à chaque frame pour animer le mouvement
        et retire la première case de la liste de chemin à chaque appel.
        """
        if self.vaisseau.chemin:
            nouvelle_x, nouvelle_y = self.vaisseau.chemin.pop(0)
            self.vaisseau.mettre_a_jour_position(nouvelle_x, nouvelle_y)
