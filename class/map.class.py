import pygame
import random

class Map:
    nb_cases_x = 35
    nb_cases_y = 20

    def __init__(self) -> None:
        self.grille = [[None for _ in range(self.nb_cases_x)] for _ in range(self.nb_cases_y)]

        # marquer zones interdites (haut gauche 5x4 et bas droite 5x4)
        for y in range(4):
            for x in range(5):
                self.grille[y][x] = "X"  # zone interdite

        for y in range(self.nb_cases_y - 4, self.nb_cases_y):
            for x in range(self.nb_cases_x - 5, self.nb_cases_x):
                self.grille[y][x] = "X"  # zone interdite

    def peut_placer(self, x, y, taille):
        """
        Vérifie si on peut placer une planète carrée de côté = taille
        """
        # vérifier si la planète dépasse les bords
        if x - 1 < 0 or y - 1 < 0 or x + taille >= self.nb_cases_x or y + taille >= self.nb_cases_y:
            return False

        # vérifier si la zone est libre + 1 case autour
        for yy in range(y - 1, y + taille + 1):
            for xx in range(x - 1, x + taille + 1):
                if self.grille[yy][xx] is not None:
                    return False

        return True

    def placer_planete(self, x, y, taille, pid):
        """
        Place une planète carrée de côté = taille
        """
        for yy in range(y, y + taille):
            for xx in range(x, x + taille):
                self.grille[yy][xx] = f"P{pid}"

    def generer_planet(self, nb_planet):
        """
        Générer nb_planet planètes carrées
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
                self.placer_planete(x, y, taille, pid)
                pid += 1

        if pid <= nb_planet:
            print(f"/!\ Seulement {pid-1} planètes placées sur {nb_planet} demandées")



# ==== Test de la class ====
pygame.init()

taille_case = 30
map_obj = Map()
map_obj.generer_planet(200)  # on veut 6 planètes carrées

screen = pygame.display.set_mode((map_obj.nb_cases_x * taille_case, map_obj.nb_cases_y * taille_case))
pygame.display.set_caption("Carte avec planètes carrées")

# couleurs
BLACK = (0, 0, 0)
GREY = (60, 60, 60)

# couleurs aléatoires pour planètes
planet_colors = {}

# boucle principale
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BLACK)

    for y in range(map_obj.nb_cases_y):
        for x in range(map_obj.nb_cases_x):
            val = map_obj.grille[y][x]
            rect = pygame.Rect(x * taille_case, y * taille_case, taille_case, taille_case)

            if val is None:
                pygame.draw.rect(screen, BLACK, rect)
                pygame.draw.rect(screen, (40, 40, 40), rect, 1)  # contour grille
            elif val == "X":
                pygame.draw.rect(screen, GREY, rect)
            else:
                # couleur unique par planète
                if val not in planet_colors:
                    planet_colors[val] = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
                pygame.draw.rect(screen, planet_colors[val], rect)

    pygame.display.flip()

pygame.quit()
