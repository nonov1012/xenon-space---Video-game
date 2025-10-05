import pygame
import sys
import os
# Ajouter le répertoire parent au path pour les imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from classes.PlanetAnimator import PlanetAnimator
from classes.ShipAnimator import ShipAnimator
import menuJouer
import menuParam
import menuSucces
import menuPause
from classes.TitreAnime import TitreAnime
from classes.Sounds import SoundManager
from classes.Start_Animation.StarField import StarField
from classes.Start_Animation.PlanetManager import PlanetManager
from classes.MotherShip import MotherShip
from classes.Point import Point
from blazyck import *
from classes.Achievements import AchievementManager
from classes.Animator import Animator
from classes.Start_Animation.main import create_space_background


class MenuPrincipal:
    def __init__(self):
        """
        Initialise le menu principal
        """
        # -------------------------------
        # Initialisation Pygame
        # -------------------------------
        pygame.init()
        screen_info = pygame.display.Info()
        self.screen_width, self.screen_height = screen_info.current_w, screen_info.current_h
        self.ecran = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()

        Animator.set_screen(self.ecran)  # initialisation de la classe Animator

        # Curseur personnalise
        self.new_cursor = pygame.image.load('../assets/img/menu/cursor.png')
        self.new_cursor = pygame.transform.scale(self.new_cursor, (40, 40))
        pygame.mouse.set_visible(False)

        # Sons
        self.sm = SoundManager()
        # self.sm.play_music("../assets/sounds/musics/music_ingame.mp3")
        self.sm.load_sfx("son_hover", "../assets/sounds/menu/buttons/button_hover.mp3")
        self.sm.load_sfx("son_click", "../assets/sounds/menu/buttons/button_pressed.mp3")

        # Icone
        icone = pygame.image.load("../assets/img/menu/logo.png")
        pygame.display.set_icon(icone)

        # -------------------------------
        # Fond anime avec planetes et vaisseau
        # -------------------------------
        self.screen_ratio = (self.screen_width * 100 / 600) / 100

        # Création du fond spatial et du vaisseau
        self.stars, self.planet_manager, self.B1 = create_space_background(
            num_stars=100, screen_ratio=self.screen_ratio
        )

        # -------------------------------
        # Titre centre
        # -------------------------------
        police_titre = pygame.font.Font("../assets/fonts/SpaceNova.otf", 100)
        titre_position = (self.screen_width // 2, 200)
        self.titre = TitreAnime(
            "XENON-SPACE", police_titre, titre_position,
            couleur_haut=(255, 255, 0), couleur_bas=(255, 0, 255)
        )

        # -------------------------------
        # Boutons decales a gauche
        # -------------------------------
        self.blanc = (255, 255, 255)
        police = pygame.font.Font("../assets/fonts/SpaceNova.otf", 25)
        self.image_bouton = pygame.image.load("../assets/img/menu/bouton_menu.png").convert_alpha()
        self.image_bouton = pygame.transform.scale(self.image_bouton, (500, 150))
        self.largeur_bouton, self.hauteur_bouton = self.image_bouton.get_size()

        decalage_boutons = -500  # boutons a gauche
        x_bouton = self.screen_width // 2 - self.largeur_bouton // 2 + decalage_boutons
        y_bouton = self.screen_height // 2

        # Textes des boutons
        self.texte_jouer = police.render("Jouer", True, self.blanc)
        self.texte_param = police.render("Parametres", True, self.blanc)
        self.texte_succes = police.render("Succes", True, self.blanc)
        self.texte_quitter = police.render("Quitter", True, self.blanc)
        self.texte_credit = police.render("Credits", True, self.blanc)

        # Rectangles des boutons
        self.bouton_jouer = pygame.Rect(x_bouton, y_bouton - 200, self.largeur_bouton, self.hauteur_bouton)
        self.bouton_param = pygame.Rect(x_bouton, y_bouton - 100, self.largeur_bouton, self.hauteur_bouton)
        self.bouton_succes = pygame.Rect(x_bouton, y_bouton, self.largeur_bouton, self.hauteur_bouton)
        self.bouton_quitter = pygame.Rect(x_bouton, y_bouton + 100, self.largeur_bouton, self.hauteur_bouton)

        # Bouton credit reste a sa position originale
        self.bouton_credit = pygame.Rect(
            self.screen_width - self.largeur_bouton - 30,
            self.screen_height - self.hauteur_bouton - 30,
            self.largeur_bouton, self.hauteur_bouton
        )

        # États des animations
        self.zoom_states = {}
        self.zoom_speed = 0.08
        self.hover_states = {}

        # État de la boucle
        self.en_cours = True

    def handle_events(self):
        """
        Gère les événements du menu
        """
        for evenement in pygame.event.get():
            if evenement.type == pygame.QUIT:
                self.en_cours = False
            elif evenement.type == pygame.KEYDOWN:
                if evenement.key == pygame.K_ESCAPE:
                    # Appelle le menu pause
                    pause_menu = menuPause.PauseMenu(self.ecran, self.sm)
                    pause_menu.run()
            elif evenement.type == pygame.MOUSEBUTTONDOWN:
                if self.bouton_jouer.collidepoint(evenement.pos):
                    self.sm.play_sfx("son_click")
                    menuJouer.main(self.ecran)
                elif self.bouton_param.collidepoint(evenement.pos):
                    self.sm.play_sfx("son_click")
                    menuParam.main(self.ecran)
                elif self.bouton_succes.collidepoint(evenement.pos):
                    self.sm.play_sfx("son_click")
                    menuSucces.main(self.ecran)
                elif self.bouton_quitter.collidepoint(evenement.pos):
                    self.sm.play_sfx("son_click")
                    pygame.quit()
                    sys.exit()

    def update_buttons(self):
        """
        Met à jour les états des boutons (zoom et survol)
        """
        souris = pygame.mouse.get_pos()

        boutons = [
            (self.bouton_jouer, self.texte_jouer),
            (self.bouton_param, self.texte_param),
            (self.bouton_succes, self.texte_succes),
            (self.bouton_quitter, self.texte_quitter),
            (self.bouton_credit, self.texte_credit)
        ]

        for i, (bouton, texte) in enumerate(boutons):
            if i not in self.zoom_states:
                self.zoom_states[i] = 1.0
            if i not in self.hover_states:
                self.hover_states[i] = False

            zone_survol = bouton.inflate(0, -100)
            est_survol = zone_survol.collidepoint(souris)
            
            if est_survol and not self.hover_states[i]:
                self.sm.play_sfx("son_hover")
            
            self.hover_states[i] = est_survol

            zoom_cible = 1.1 if est_survol else 1.0
            self.zoom_states[i] += (zoom_cible - self.zoom_states[i]) * self.zoom_speed

    def draw(self):
        """
        Dessine le menu principal à l'écran
        """
        # --- Fond + planetes + vaisseau ---
        self.ecran.fill((0, 0, 0))

        self.stars.update()
        self.stars.draw(self.ecran)
        self.planet_manager.update_and_draw()
        Animator.update_all()
        PlanetAnimator.update_all()
        ShipAnimator.update_all()

        # --- Titre ---
        self.titre.draw(self.ecran)

        # --- Boutons ---
        boutons = [
            (self.bouton_jouer, self.texte_jouer),
            (self.bouton_param, self.texte_param),
            (self.bouton_succes, self.texte_succes),
            (self.bouton_quitter, self.texte_quitter),
            (self.bouton_credit, self.texte_credit)
        ]

        for i, (bouton, texte) in enumerate(boutons):
            bouton_zoom = pygame.transform.scale(
                self.image_bouton,
                (int(self.largeur_bouton * self.zoom_states[i]), 
                 int(self.hauteur_bouton * self.zoom_states[i]))
            )
            rect_zoom = bouton_zoom.get_rect(center=bouton.center)
            self.ecran.blit(bouton_zoom, rect_zoom.topleft)
            rect_texte = texte.get_rect(center=rect_zoom.center)
            self.ecran.blit(texte, rect_texte.topleft)

        # --- Curseur ---
        souris = pygame.mouse.get_pos()
        self.ecran.blit(self.new_cursor, souris)

        # Mise à jour de l'affichage
        pygame.display.flip()

    def run(self):
        """
        Boucle principale du menu
        """
        while self.en_cours:
            self.handle_events()
            self.update_buttons()
            self.draw()
            self.clock.tick(30)


# -------------------------------
# Fonction principale 
# -------------------------------
def main():
    """
    Fonction principale pour lancer le menu principal
    """
    menu = MenuPrincipal()
    menu.run()


# -------------------------------
# Boucle principale 
# -------------------------------
if __name__ == "__main__":
    main()