import pygame
import random
from Point import Point, Type


class Map:
    nb_cases_x = 35
    nb_cases_y = 20

    def __init__(self) -> None:
        # On initialise la grille avec des Points de type VIDE
        self.grille: list[list[Point]] = [
            [Point(x, y, Type.VIDE) for x in range(self.nb_cases_x)]
            for y in range(self.nb_cases_y)
        ]

        # Zone de la base en haut-gauche (5x4)
        for y in range(4):
            for x in range(5):
                self.grille[y][x].type = Type.ASTEROIDE  # zone interdite

        # Zone de la base en bas-droite (5x4)
        for y in range(self.nb_cases_y - 4, self.nb_cases_y):
            for x in range(self.nb_cases_x - 5, self.nb_cases_x):
                self.grille[y][x].type = Type.ASTEROIDE  # zone interdite

    def peut_placer(self, x, y, taille: int) -> bool:
        """
        Vérifie si on peut placer une planète carrée de côté `taille`.
        Les planètes doivent être à 1 case des autres objets et ne pas toucher les bords.
        """
        if x - 1 < 0 or y - 1 < 0 or x + taille >= self.nb_cases_x or y + taille >= self.nb_cases_y:
            return False

        for yy in range(y - 1, y + taille + 1):
            for xx in range(x - 1, x + taille + 1):
                if self.grille[yy][xx].type != Type.VIDE:
                    return False

        return True

    def placer_planete(self, x, y, taille: int) -> None:
        """
        Place une planète carrée de côté = taille.
        """
        for yy in range(y, y + taille):
            for xx in range(x, x + taille):
                self.grille[yy][xx].type = Type.PLANETE

    def generer_planet(self, nb_planet: int) -> None:
        """
        Générer `nb_planet` planètes carrées aléatoires.
        """
        pid = 1
        essais_max = 2000
        essais = 0

        while pid <= nb_planet and essais < essais_max:
            essais += 1
            taille = random.randint(3, 6)  # carré 3x3 à 6x6
            x = random.randint(1, self.nb_cases_x - taille - 1)
            y = random.randint(1, self.nb_cases_y - taille - 1)

            if self.peut_placer(x, y, taille):
                self.placer_planete(x, y, taille)
                pid += 1

        if pid <= nb_planet:
            print(f"/!\\ Seulement {pid-1} planètes placées sur {nb_planet} demandées")


# ==== Test de la classe ====
if __name__ == "__main__":
    pygame.init()

    taille_case = 30
    map_obj = Map()
    map_obj.generer_planet(20)

    screen = pygame.display.set_mode((map_obj.nb_cases_x * taille_case, map_obj.nb_cases_y * taille_case))
    pygame.display.set_caption("Carte avec planètes carrées")

    # couleurs
    COLORS = {
        Type.VIDE: (0, 0, 0),        # noir
        Type.PLANETE: (0, 150, 255), # bleu clair
        Type.ATMOSPHERE: (0, 255, 150),
        Type.ASTEROIDE: (100, 100, 100),  # gris
    }

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))

        for y in range(map_obj.nb_cases_y):
            for x in range(map_obj.nb_cases_x):
                point = map_obj.grille[y][x]
                rect = pygame.Rect(x * taille_case, y * taille_case, taille_case, taille_case)
                pygame.draw.rect(screen, COLORS[point.type], rect)
                pygame.draw.rect(screen, (40, 40, 40), rect, 1)  # contour

        pygame.display.flip()

    pygame.quit()
