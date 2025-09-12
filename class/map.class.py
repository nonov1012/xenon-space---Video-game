class Map:
    grille = []
    nb_cases_x = 35
    nb_cases_y = 20
    def __init__(self) -> None:
        self.grille = [[None for _ in range(self.nb_cases_x)] for _ in range(self.nb_cases_y)]

    def generer_planet(nb_planet):
        """
        Générer n planet sur la map
        """
        pass