"""
menuPause.py
Menu de pause - Version restructurée
"""
from asyncio import wait
import pygame
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from blazyck import *
from classes.Animator import Animator
from classes.PlanetAnimator import PlanetAnimator
from classes.Start_Animation.main import create_space_background
from menu import menuParam
import classes.ShipAnimator


# =====================================
# CLASSES
# =====================================

class PauseButton:
    """Bouton pour le menu pause"""
    
    def __init__(self, rect, text, font, image, action=None):
        """
        Initialise un bouton de pause
        
        Args:
            rect: Rectangle de position
            text: Texte du bouton
            font: Police du texte
            image: Image de fond
            action: Fonction à appeler au clic
        """
        self.rect = rect
        self.text = text
        self.font = font
        self.image = image
        self.action = action
        self.zoom = 1.0
        
    def update(self, mouse_pos):
        """Met à jour l'animation du bouton"""
        is_hover = self.rect.collidepoint(mouse_pos)
        target_zoom = 1.1 if is_hover else 1.0
        self.zoom += (target_zoom - self.zoom) * 0.08
        
    def draw(self, surface):
        """Dessine le bouton"""
        width = int(self.image.get_width() * self.zoom)
        height = int(self.image.get_height() * self.zoom)
        scaled = pygame.transform.scale(self.image, (width, height))
        rect_zoom = scaled.get_rect(center=self.rect.center)
        
        surface.blit(scaled, rect_zoom.topleft)
        text_surf = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=rect_zoom.center)
        surface.blit(text_surf, text_rect)
        
    def is_clicked(self, mouse_pos):
        """Vérifie si le bouton est cliqué"""
        return self.rect.collidepoint(mouse_pos)


class MenuPause:
    """Menu de pause du jeu"""
    
    def __init__(self, ecran, jeu_surface=None):
        """
        Initialise le menu de pause
        
        Args:
            ecran: Surface Pygame
            jeu_surface: Surface du jeu en cours (pour overlay)
        """
        self.ecran = ecran
        self.jeu_surface = jeu_surface
        self.largeur_ecran, self.hauteur_ecran = ecran.get_size()
        
        # État
        self.running = True
        self.action_result = "continue" # Initialise le résultat de l'action
        
        # Initialisation
        self._init_colors()
        self._init_fonts()
        self._init_background()
        self._init_buttons()
        
        self.clock = pygame.time.Clock()
        
    # =====================================
    # INITIALISATION
    # =====================================
    
    def _init_colors(self):
        """Initialise les couleurs"""
        self.BLANC = (255, 255, 255)
        self.NOIR = (0, 0, 0)
        
    def _init_fonts(self):
        """Initialise les polices"""
        self.police_bouton = pygame.font.Font("assets/fonts/SpaceNova.otf", 42)
        self.police_titre = pygame.font.Font("assets/fonts/SpaceNova.otf", 72)
        
    def _init_background(self):
        """Initialise le fond animé (étoiles uniquement)"""
        self.stars, _, ship = create_space_background()
        ship.animator.remove_from_list()
        
    def _init_buttons(self):
        """Initialise les boutons"""
        image_base = pygame.image.load("assets/img/menu/bouton_menu.png").convert_alpha()
        button_width, button_height = 500, 100
        
        # Configuration des boutons
        button_configs = [
            ("REPRENDRE", self._action_reprendre),
            ("PARAMETRES", self._action_parametres),
            ("RETOUR AU MENU PRINCIPAL", self._action_retour_menu),
            ("QUITTER", self._action_quitter)
        ]
        
        # Calcul des positions verticales
        espacement = 60
        total_height = len(button_configs) * button_height + (len(button_configs) - 1) * espacement
        y_start = (self.hauteur_ecran - total_height) // 2
        
        # Création des boutons
        self.buttons = []
        for i, (text, action) in enumerate(button_configs):
            image = pygame.transform.scale(image_base, (button_width, button_height))
            y = y_start + i * (button_height + espacement)
            rect = pygame.Rect(
                self.largeur_ecran // 2 - button_width // 2,
                y,
                button_width,
                button_height
            )
            button = PauseButton(rect, text, self.police_bouton, image, action)
            self.buttons.append(button)
            
    # =====================================
    # ACTIONS DES BOUTONS
    # =====================================
    
    def _action_reprendre(self):
        """Reprend le jeu"""
        self.running = False
        self.action_result = "continue"
        
    def _action_parametres(self):
        """Ouvre le menu des paramètres"""
        menuParam.main(self.ecran, animation=False)
        
    def _action_retour_menu(self):
        """Quitte la partie pour retourner au menu principal"""
        classes.ShipAnimator.ShipAnimator.clear_list()
        PlanetAnimator.clear_list()
        self.running = False
        self.action_result = "go_to_main_menu"
        
    def _action_quitter(self):
        """Quitte le jeu"""
        pygame.quit()
        sys.exit()
        
    # =====================================
    # GESTION DES ÉVÉNEMENTS
    # =====================================
    
    def _handle_events(self):
        """Gère les événements"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            elif event.type == pygame.KEYDOWN:
                self._handle_keydown(event.key)
                
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self._handle_click(event.pos)
                
    def _handle_keydown(self, key):
        """Gère les touches pressées"""
        if key == pygame.K_ESCAPE:
            self._action_reprendre()
            
    def _handle_click(self, mouse_pos):
        """Gère les clics de souris"""
        for button in self.buttons:
            if button.is_clicked(mouse_pos):
                if button.action:
                    button.action()
                    
                    if not self.running:
                        break
    # =====================================
    # MISE À JOUR
    # =====================================
    
    def _update(self):
        """Met à jour la logique du menu"""
        mouse_pos = pygame.mouse.get_pos()
        
        # Mise à jour des boutons
        for button in self.buttons:
            button.update(mouse_pos)
            
    # =====================================
    # RENDU
    # =====================================
    
    def _draw_background(self):
        """Dessine le fond"""
        self.ecran.fill(self.NOIR)
        
        # Étoiles animées
        self.stars.update()
        self.stars.draw(self.ecran)

        
    def _draw_buttons(self):
        """Dessine les boutons"""
        for button in self.buttons:
            button.draw(self.ecran)
        
    def _render(self):
        """Effectue le rendu complet"""
        self._draw_background()
        self._draw_buttons()
        
        pygame.display.update()
        
    # =====================================
    # BOUCLE PRINCIPALE
    # =====================================
    
    def run(self):
        """Lance la boucle principale du menu de pause"""
        while self.running:
            self._handle_events()
            self._update()
            self._render()
            self.clock.tick(60)
            
        return self.action_result


# =====================================
# FONCTION PRINCIPALE
# =====================================

def main_pause(ecran, jeu_surface=None):
    """
    Lance le menu de pause et retourne l'action choisie.
    
    Args:
        ecran: Surface Pygame
        jeu_surface: Surface du jeu en cours (optionnel)
        
    Returns:
        str: "continue" (reprendre le jeu) ou "go_to_main_menu" (retour au menu principal).
    """
    menu = MenuPause(ecran, jeu_surface)
    return menu.run() 