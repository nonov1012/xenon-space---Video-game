# credit.py
import pygame
import sys
import os
import random
from classes.Sounds import SoundManager
from blazyck import *

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from classes.Animator import Animator
from classes.PlanetAnimator import PlanetAnimator
from classes.ShipAnimator import ShipAnimator
from classes.Start_Animation.main import create_space_background

credits = [
    "NOEL CLEMENT",
    "VOITURIER NOA",
    "DAVID GABRIEL",
    "CAVEL UGO",
    "DUPUIS BRIAN",
    "VANHOVE TOM",
    "IUT du Littoral Cote d'Opale"
]

credit_colors = [
    (255, 100, 100),
    (100, 255, 100),
    (100, 100, 255),
    (255, 255, 100),
    (255, 100, 255),
    (100, 255, 255),
    (200, 200, 200)
]

class Particle:
    def __init__(self, x, y, color, vx, vy):
        self.x = x
        self.y = y
        self.color = color
        self.vx = vx
        self.vy = vy
        self.life = 60

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.2
        self.life -= 1

    def draw(self, surface):
        if self.life > 0:
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), 3)


def main(ecran):
    largeur_ecran, hauteur_ecran = ecran.get_size()
    horloge = pygame.time.Clock()

    # Fond animé
    screen_ratio = (largeur_ecran * 100 / 600) / 100
    stars, planet_manager, _ = create_space_background(num_stars=100, screen_ratio=screen_ratio)

    police = pygame.font.Font("assets/fonts/SpaceNova.otf", 40)
    police_info = pygame.font.Font("assets/fonts/SpaceNova.otf", 22)
    credit_y = hauteur_ecran
    vitesse_defilement = 1
    vitesse_acceleree = 4

    particles = []
    en_cours = True
    espace_enfonce = False

    curseur_img = pygame.image.load('assets/img/menu/cursor.png')
    curseur_img = pygame.transform.scale(curseur_img, (40, 40))

    while en_cours:
        souris = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                en_cours = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    en_cours = False  # quitter crédits
                elif event.key == pygame.K_SPACE:
                    espace_enfonce = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    espace_enfonce = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Clic gauche sur une ligne de crédit → explosion en particules
                y_offset_click = credit_y
                for idx, line in enumerate(credits):
                    text_surf_click = police.render(line, True, credit_colors[idx])
                    rect_click = text_surf_click.get_rect(center=(largeur_ecran // 2, y_offset_click))
                    if rect_click.collidepoint(event.pos):
                        w, h = text_surf_click.get_size()
                        step = 6  # taille de l’échantillonnage des pixels
                        for i in range(0, w, step):
                            for j in range(0, h, step):
                                color = text_surf_click.get_at((i, j))
                                if len(color) >= 4 and color[3] > 0:  # pixel visible
                                    vx = random.uniform(-3, 3)
                                    vy = random.uniform(-5, 0)
                                    particles.append(Particle(rect_click.x + i, rect_click.y + j, color, vx, vy))
                        break  # on explose seulement une ligne par clic
                    y_offset_click += 60

        # Fond animé
        ecran.fill((0, 0, 0))
        stars.update()
        stars.draw(ecran)
        planet_manager.update_and_draw()
        Animator.update_all()
        PlanetAnimator.update_all()
        ShipAnimator.update_all()

        # Défilement et affichage des crédits
        vitesse = vitesse_acceleree if espace_enfonce else vitesse_defilement
        credit_y -= vitesse
        y_offset = credit_y
        for idx, line in enumerate(credits):
            text_surf = police.render(line, True, credit_colors[idx])
            rect = text_surf.get_rect(center=(largeur_ecran // 2, y_offset))
            ecran.blit(text_surf, rect)
            y_offset += 60

        # Vérification : si le dernier crédit est sorti de l’écran → retour auto
        if y_offset < 0:
            en_cours = False

        # Particules
        for p in particles[:]:
            p.update()
            p.draw(ecran)
            if p.life <= 0:
                particles.remove(p)

        # Texte info
        info_texte = police_info.render("ESPACE = accelerer, ECHAP = quitter", True, (200, 200, 200))
        rect_info = info_texte.get_rect(bottomright=(largeur_ecran - 20, hauteur_ecran - 20))
        ecran.blit(info_texte, rect_info)

        # Curseur
        ecran.blit(curseur_img, souris)

        pygame.display.flip()
        horloge.tick(60)

    return


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    main(screen)
    pygame.quit()
    sys.exit()
