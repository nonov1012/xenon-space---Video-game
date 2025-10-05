import pygame
import sys
import os
from blazyck import *

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from classes.Animator import Animator
from classes.PlanetAnimator import PlanetAnimator
from classes.Start_Animation.main import create_space_background
from menu import menuParam  # Assurez-vous que menuParam.main accepte ecran en param

def main_pause(ecran, jeu_surface=None):
    pygame.mouse.set_visible(False)

    # -------------------------------
    # Couleurs et polices
    # -------------------------------
    BLANC = (255, 255, 255)
    NOIR = (0, 0, 0)

    police_bouton = pygame.font.Font("assets/fonts/SpaceNova.otf", 42)
    police_titre = pygame.font.Font("assets/fonts/SpaceNova.otf", 72)

    # -------------------------------
    # Curseur
    # -------------------------------
    curseur_img = pygame.image.load('assets/img/menu/cursor.png')
    curseur_img = pygame.transform.scale(curseur_img, (40, 40))

    # -------------------------------
    # Boutons verticaux
    # -------------------------------
    image_bouton_base = pygame.image.load("assets/img/menu/bouton_menu.png").convert_alpha()
    def creer_image_bouton(largeur, hauteur):
        return pygame.transform.scale(image_bouton_base, (largeur, hauteur))

    labels = ["REPRENDRE", "PARAMÈTRES", "QUITTER"]
    images = [creer_image_bouton(500, 100) for _ in labels]

    largeur_ecran, hauteur_ecran = ecran.get_size()
    espacement = 60
    y_depart = hauteur_ecran // 2 - ((len(labels)-1) * (100 + espacement)) // 2
    rects = [pygame.Rect(largeur_ecran//2 - 250, y_depart + i*(100 + espacement), 500, 100) for i in range(len(labels))]

    boutons = list(zip(images, rects, labels))
    zoom_etats = {label: 1.0 for label in labels}
    vitesse_zoom = 0.08

    # -------------------------------
    # Fond : uniquement étoiles (pas de planètes, pas de vaisseau)
    # -------------------------------
    screen_ratio = (largeur_ecran * 100 / 600) / 100
    stars, _, _ = create_space_background(
        num_stars=100, screen_ratio=screen_ratio
    )

    horloge = pygame.time.Clock()
    en_cours = True

    while en_cours:
        souris = pygame.mouse.get_pos()
        clic = pygame.mouse.get_pressed()[0]

        # -------------------------------
        # Fond animé (juste étoiles)
        # -------------------------------
        ecran.fill(NOIR)
        stars.update()
        stars.draw(ecran)

        # -------------------------------
        # Dessiner boutons
        # -------------------------------
        for image, rect, label in boutons:
            est_hover = rect.collidepoint(souris)
            cible_zoom = 1.1 if est_hover else 1.0
            zoom_etats[label] += (cible_zoom - zoom_etats[label]) * vitesse_zoom

            largeur_zoom = int(image.get_width() * zoom_etats[label])
            hauteur_zoom = int(image.get_height() * zoom_etats[label])
            image_zoom = pygame.transform.scale(image, (largeur_zoom, hauteur_zoom))
            rect_zoom = image_zoom.get_rect(center=rect.center)
            ecran.blit(image_zoom, rect_zoom.topleft) 

            texte_surf = police_bouton.render(label, True, BLANC)
            texte_rect = texte_surf.get_rect(center=rect_zoom.center)
            ecran.blit(texte_surf, texte_rect)

        # -------------------------------
        # Curseur
        # -------------------------------
        ecran.blit(curseur_img, souris)

        # -------------------------------
        # Évènements
        # -------------------------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for _, rect, label in boutons:
                    if rect.collidepoint(event.pos):
                        if label == "REPRENDRE":
                            en_cours = False
                        elif label == "PARAMÈTRES":
                            menuParam.main(ecran, False)
                        elif label == "QUITTER":
                            pygame.quit()
                            sys.exit()

        pygame.display.update()
        horloge.tick(60)

