import pygame
import sys
import menu.menuParam
import menu.menuJouer
from classes.Sounds import SoundManager

class PauseMenu:
    def __init__(self, screen: pygame.Surface, sound_manager: SoundManager):
        self.screen = screen
        self.sm = sound_manager
        self.clock = pygame.time.Clock()
        self.screen_width, self.screen_height = screen.get_size()

        # Couleurs et polices
        self.white = (255, 255, 255)
        self.title_font = pygame.font.Font("assets/fonts/SpaceNova.otf", 80)
        self.button_font = pygame.font.Font("assets/fonts/SpaceNova.otf", 30)

        # Fond noir transparent
        self.overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        self.overlay.fill((0, 0, 0, 180))

        # Titre
        self.title_text = self.title_font.render("PAUSE", True, self.white)
        self.title_rect = self.title_text.get_rect(center=(self.screen_width // 2, 100))

        # Boutons
        self.image_bouton = pygame.image.load("assets/img/menu/bouton_menu.png").convert_alpha()
        self.image_bouton = pygame.transform.scale(self.image_bouton, (400, 100))
        self.largeur_bouton, self.hauteur_bouton = self.image_bouton.get_size()
        y_bouton = 250
        espace = 120
        self.texts = ["REPRENDRE", "PARAMETRES", "QUITTER", "RETOUR AU MENU"]
        self.buttons = [pygame.Rect(self.screen_width//2 - self.largeur_bouton//2, y_bouton + i*espace,
                                     self.largeur_bouton, self.hauteur_bouton) for i in range(len(self.texts))]

        # Zoom et hover
        self.zoom_states = {}
        self.hover_states = {}
        self.zoom_speed = 0.08

    def run(self):
        pygame.mouse.set_visible(True)
        running = True
        while running:
            souris = pygame.mouse.get_pos()
            self.screen.blit(self.overlay, (0,0))
            self.screen.blit(self.title_text, self.title_rect.topleft)

            # Dessin des boutons
            for i, bouton in enumerate(self.buttons):
                if i not in self.zoom_states:
                    self.zoom_states[i] = 1.0
                if i not in self.hover_states:
                    self.hover_states[i] = False

                zone_survol = bouton.inflate(0, -20)
                est_survol = zone_survol.collidepoint(souris)
                if est_survol and not self.hover_states[i]:
                    self.sm.play_sfx("son_hover")
                self.hover_states[i] = est_survol

                zoom_cible = 1.1 if est_survol else 1.0
                self.zoom_states[i] += (zoom_cible - self.zoom_states[i]) * self.zoom_speed

                bouton_zoom = pygame.transform.scale(
                    self.image_bouton,
                    (int(self.largeur_bouton * self.zoom_states[i]),
                     int(self.hauteur_bouton * self.zoom_states[i]))
                )
                rect_zoom = bouton_zoom.get_rect(center=bouton.center)
                self.screen.blit(bouton_zoom, rect_zoom.topleft)

                texte_render = self.button_font.render(self.texts[i], True, self.white)
                rect_texte = texte_render.get_rect(center=rect_zoom.center)
                self.screen.blit(texte_render, rect_texte.topleft)

            pygame.display.flip()
            self.clock.tick(30)

            # Gestion des événements
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.buttons[0].collidepoint(event.pos):  # REPRENDRE
                        self.sm.play_sfx("son_click")
                        running = False
                    elif self.buttons[1].collidepoint(event.pos):  # PARAMETRES
                        self.sm.play_sfx("son_click")
                        menuParam.main(self.screen)
                    elif self.buttons[2].collidepoint(event.pos):  # QUITTER
                        self.sm.play_sfx("son_click")
                        pygame.quit()
                        sys.exit()
                    elif self.buttons[3].collidepoint(event.pos):  # RETOUR AU MENU
                        self.sm.play_sfx("son_click")
                        menuJouer.main(self.screen)
                        running = False
