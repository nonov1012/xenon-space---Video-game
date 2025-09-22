import sys
import os

import pygame
import random
from classes.Point import Point, Type
from classes.Start_Animation.StarField import StarField

from blazyck import NB_CASE_X, NB_CASE_Y, PLANETES_PATH, TAILLE_CASE, ASTEROIDES_PATH

from PIL import Image

def load_image(path):
    pil_img = Image.open(path).convert("RGBA")
    mode = pil_img.mode
    size = pil_img.size
    data = pil_img.tobytes()

    return pygame.image.fromstring(data, size, mode)


class Map:
    nb_cases_x = NB_CASE_X
    nb_cases_y = NB_CASE_Y

    def __init__(self) -> None:
        # On initialise la grille avec des Points de type VIDE
        self.grille: list[list[Point]] = [
            [Point(x, y, Type.VIDE) for x in range(self.nb_cases_x)]
            for y in range(self.nb_cases_y)
        ]
        
        self.planete_img_map: dict[tuple[int, int], pygame.Surface] = {}
        self.asteroide_img_map: dict[tuple[int, int], pygame.Surface] = {}

        # Zone de la base en haut a gauche (5x4)
        for y in range(4):
            for x in range(5):
                self.grille[y][x].type = Type.BASE  # zone interdite

        # Zone de la base en bas a droite (5x4)
        for y in range(self.nb_cases_y - 4, self.nb_cases_y):
            for x in range(self.nb_cases_x - 5, self.nb_cases_x):
                self.grille[y][x].type = Type.BASE  # zone interdite

        # === Chargement des images de planètes ===
        self.planete_images = []
        for i in range(1, 6):
            path = os.path.join(PLANETES_PATH, f"planet{i}.gif")
            if os.path.exists(path):
                try:
                    img = load_image(path)
                    self.planete_images.append(img)
                except pygame.error as e:
                    print(f"Erreur chargement {path} : {e}")
            else:
                print(f"[!] Fichier introuvable : {path}")
        
        # === Chargement des images d’astéroïdes ===
        self.asteroide_images = []
        for i in range(1, 6):  # imaginons aste1.png → aste5.png
            path = os.path.join(ASTEROIDES_PATH, f"aste{i}.png")
            if os.path.exists(path):
                try:
                    img = load_image(path)
                    # on redimensionne à la taille d’une case
                    img = pygame.transform.scale(img, (TAILLE_CASE, TAILLE_CASE))
                    self.asteroide_images.append(img)
                except pygame.error as e:
                    print(f"Erreur chargement {path} : {e}")
            else:
                print(f"[!] Fichier introuvable : {path}")

        if not self.asteroide_images:
            print("⚠️ Aucune image d’astéroïde trouvée ! Vérifie ASTEROIDE_PATH.")

        if not self.planete_images:
            print("⚠️ Aucune image de planète trouvée ! Vérifie PLANETES_PATH.")


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
        Associe une image aléatoire à cette planète.
        """
        # Choisir une image aléatoire pour cette planète
        if self.planete_images:
            chosen_img = random.choice(self.planete_images)
            # Redimensionner l’image pour coller à la taille
            img_resized = pygame.transform.scale(chosen_img, (TAILLE_CASE * taille, TAILLE_CASE * taille))
        else:
            img_resized = None

        for yy in range(y, y + taille):
            for xx in range(x, x + taille):
                self.grille[yy][xx].type = Type.PLANETE
        
        for yy in range(y - 1, y + taille + 1):
            for xx in range(x - 1, x + taille + 1):
                if 0 <= xx < self.nb_cases_x and 0 <= yy < self.nb_cases_y:
                    if self.grille[yy][xx].type == Type.VIDE:
                        self.grille[yy][xx].type = Type.ATMOSPHERE

        if img_resized:
            # On stocke l’image à la position d’origine de la planète
            self.planete_img_map[(x, y)] = img_resized
    
    def placer_asteroide(self, x, y) -> None:
        """
        Place un astéroïde 1x1 à la position (x, y).
        """
        if self.grille[y][x].type == Type.VIDE and self.asteroide_images:
            chosen_img = random.choice(self.asteroide_images)
            self.grille[y][x].type = Type.ASTEROIDE
            self.asteroide_img_map[(x, y)] = chosen_img

    def generer_asteroides(self, nb_asteroides: int) -> None:
        """
        Générer des astéroïdes 1x1 aléatoires.
        """
        essais = 0
        max_essais = 2000
        placed = 0

        while placed < nb_asteroides and essais < max_essais:
            essais += 1
            x = random.randint(0, self.nb_cases_x - 1)
            y = random.randint(0, self.nb_cases_y - 1)

            if self.grille[y][x].type == Type.VIDE:
                self.placer_asteroide(x, y)
                placed += 1

        if placed < nb_asteroides:
            print(f"/!\\ Seulement {placed} astéroïdes placés sur {nb_asteroides} demandés")


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

    screen = pygame.display.set_mode((NB_CASE_X * TAILLE_CASE, NB_CASE_Y * TAILLE_CASE), pygame.SRCALPHA)
    pygame.display.set_caption("Génération de la map aléatoire")
    
    screen_width, screen_height = screen.get_size()
    num_stars=100
    screen_ratio=1.0
    stars = StarField(
        screen_width,
        screen_height,
        num_stars=int(num_stars * screen_ratio),
        min_radius=1,
        max_radius=3,
        min_distance=15,
        size_distribution="small-biased",
        move_amplitude=3
    )    
    
    map_obj = Map()
    map_obj.generer_planet(6)
    map_obj.generer_asteroides(20)


    # couleurs
    COLORS = {
        Type.VIDE: (0, 0, 0, 10),               # noir
        Type.PLANETE: (0, 150, 255),            # bleu clair
        Type.ATMOSPHERE: (0, 255, 150, 125),    # vert clair
        Type.ASTEROIDE: (200, 200, 200),        # gris
        Type.BASE: (100, 100, 100),             # gris foncé
    }

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))
        stars.update()
        stars.draw(screen)

        # Dessin de la grille
        for y in range(map_obj.nb_cases_y):
            for x in range(map_obj.nb_cases_x):
                point = map_obj.grille[y][x]
                rect = pygame.Rect(x * TAILLE_CASE, y * TAILLE_CASE, TAILLE_CASE, TAILLE_CASE)
                if point.type != Type.VIDE:
                    pygame.draw.rect(screen, COLORS[point.type], rect)  # fond
                pygame.draw.rect(screen, (40, 40, 40), rect, 1)  # contour

        # Dessin des images des planètes
        for (px, py), img in map_obj.planete_img_map.items():
            screen.blit(img, (px * TAILLE_CASE, py * TAILLE_CASE))
            
        for (ax, ay), img in map_obj.asteroide_img_map.items():
            screen.blit(img, (ax * TAILLE_CASE, ay * TAILLE_CASE))

        pygame.display.flip()

    pygame.quit()