"""
menuParam.py
Menu des paramètres - Version refactorisée
"""
import pygame
import sys
import os
import json
import copy

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from blazyck import *
from classes.Animator import Animator
from classes.PlanetAnimator import PlanetAnimator
from classes.ShipAnimator import ShipAnimator
from classes.Start_Animation.main import create_space_background
from classes.GlobalVar.ScreenVar import ScreenVar

SAVE_FILE = "save_parametre.json"

DEFAULT_SETTINGS = {
    "touches": {
        "rotation_vaisseau": pygame.K_r,
        "terminer_tour": pygame.K_RETURN,
        "afficher_grille": pygame.K_LCTRL,
        "afficher_zones": pygame.K_LSHIFT,
        "menu_pause": pygame.K_ESCAPE
    },
    "audio": {
        "volume_general": 50,
        "volume_musique": 50,
        "volume_sons": 50
    }
}


# =====================================
# FONCTIONS UTILITAIRES
# =====================================

def charger_parametres():
    """Charge les paramètres depuis le fichier de sauvegarde"""
    try:
        with open(SAVE_FILE, 'r') as f:
            return json.load(f)
    except:
        return copy.deepcopy(DEFAULT_SETTINGS)


def sauvegarder_parametres(settings):
    """Sauvegarde les paramètres dans un fichier"""
    with open(SAVE_FILE, 'w') as f:
        json.dump(settings, f, indent=4)


def get_key_name(key_code):
    """Retourne le nom d'une touche"""
    return pygame.key.name(key_code).upper()


# =====================================
# CLASSES
# =====================================

class Couleur:
    """Constantes de couleurs"""
    BLANC = (255, 255, 255)
    GRIS_FONCE = (40, 40, 55)
    GRIS_MOYEN = (90, 90, 110)
    GRIS_CLAIR = (150, 150, 170)
    VERT = (0, 200, 100)
    BLEU_ACCENT = (70, 130, 255)
    ORANGE = (255, 165, 0)
    NOIR = (0, 0, 0)


class Police:
    """Constantes de polices"""
    titre = pygame.font.Font("assets/fonts/SpaceNova.otf", 60)
    param = pygame.font.Font("assets/fonts/SpaceNova.otf", 22)
    bouton = pygame.font.Font("assets/fonts/SpaceNova.otf", 28)


class Slider:
    """Représente un slider pour les volumes"""
    
    def __init__(self, x, y, largeur, hauteur, min_val, max_val, valeur):
        self.rect = pygame.Rect(x, y, largeur, hauteur)
        self.min_val = min_val
        self.max_val = max_val
        self.valeur = valeur
        self.actif = False
        
    def update_valeur(self, mouse_x):
        """Met à jour la valeur selon la position de la souris"""
        rel_x = max(0, min(self.rect.width, mouse_x - self.rect.x))
        self.valeur = int((rel_x / self.rect.width) * (self.max_val - self.min_val) + self.min_val)
        
    def draw(self, surface):
        """Dessine le slider"""
        pygame.draw.rect(surface, Couleur.GRIS_MOYEN, self.rect, border_radius=8)
        
        rel_pos = (self.valeur - self.min_val) / (self.max_val - self.min_val)
        largeur_prog = int(rel_pos * self.rect.width)
        if largeur_prog > 0:
            rect_prog = pygame.Rect(self.rect.x, self.rect.y, largeur_prog, self.rect.height)
            pygame.draw.rect(surface, Couleur.VERT, rect_prog, border_radius=8)
        
        curseur_x = self.rect.x + int(rel_pos * self.rect.width)
        pygame.draw.ellipse(surface, (0, 150, 80), 
                           (curseur_x - 8, self.rect.y - 5, 16, self.rect.height + 10))


class ButtonParam:
    """Bouton pour le menu paramètres"""
    
    def __init__(self, rect, text, font, image, action=None):
        self.rect = rect
        self.text = text
        self.font = font
        self.image = image
        self.zoom = 1.0
        self.action = action
        
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
        text_surf = self.font.render(self.text, True, Couleur.BLANC)
        text_rect = text_surf.get_rect(center=rect_zoom.center)
        surface.blit(text_surf, text_rect)
        
    def is_clicked(self, mouse_pos):
        """Vérifie si le bouton est cliqué"""
        return self.rect.collidepoint(mouse_pos)


class MenuParametres:
    """Menu des paramètres du jeu"""
    
    def __init__(self):
        """Initialise le menu des paramètres"""
        self.image_bouton_base = pygame.image.load("assets/img/menu/bouton_menu.png").convert_alpha()
        
        # État
        self.en_cours = False
        self.settings = charger_parametres()
        self.capture_touche = None
        self.slider_actif = None
        self.onglet_actif = "Touches"
        
        # Configuration des touches
        self.touches_config = [
            ("Rotation vaisseau", "rotation_vaisseau"),
            ("Terminer tour", "terminer_tour"),
            ("Afficher grille", "afficher_grille"),
            ("Afficher zones", "afficher_zones"),
            ("Menu pause", "menu_pause")
        ]
        
    def update(self):
        """Initialise ou met à jour le menu"""
        self.screen = ScreenVar.screen
        self.screen_width, self.screen_height = self.screen.get_size()
        
        # Curseur personnalisé
        self.curseur_img = pygame.image.load('assets/img/menu/cursor.png')
        self.curseur_img = pygame.transform.scale(self.curseur_img, (40, 40))
        pygame.mouse.set_visible(False)
        
        # Panneau principal
        self.panneau_largeur = 800
        self.panneau_hauteur = 500
        self.panneau_x = (self.screen_width - self.panneau_largeur) // 2
        self.panneau_y = 120
        
        # Onglets
        self.onglets = ["Touches", "Audio"]
        
        # Initialiser sliders et boutons
        self._init_sliders()
        self._init_buttons()
        
    def _init_sliders(self):
        """Initialise les sliders audio"""
        slider_largeur = 400
        slider_hauteur = 15
        slider_x = self.panneau_x + (self.panneau_largeur - slider_largeur) // 2
        y_offset = 80
        
        self.sliders = {}
        audio_params = [
            ("Volume general", "volume_general"),
            ("Volume musique", "volume_musique"),
            ("Volume sons", "volume_sons")
        ]
        
        for idx, (label, param_id) in enumerate(audio_params):
            y = self.panneau_y + y_offset + idx * 100 + 10
            self.sliders[param_id] = Slider(
                slider_x, y, slider_largeur, slider_hauteur,
                0, 100, self.settings["audio"][param_id]
            )
            
    def _init_buttons(self):
        """Initialise les boutons"""
        button_configs = [
            ("SAUVEGARDER", self._action_sauvegarder),
            ("RESET", self._action_reset),
            ("RETOUR", self._action_retour)
        ]
        
        self.buttons = []
        espacement = 50
        y_boutons = self.screen_height - 170
        
        # Calcul des positions
        total_width = sum(len(text) * 15 + 160 for text, _ in button_configs)
        total_width += espacement * (len(button_configs) - 1)
        x = (self.screen_width - total_width) // 2
        
        for text, action in button_configs:
            text_surf = Police.bouton.render(text, True, Couleur.BLANC)
            image = pygame.transform.scale(
                self.image_bouton_base,
                (text_surf.get_width() + 160, text_surf.get_height() + 130)
            )
            rect = pygame.Rect(x, y_boutons, image.get_width(), image.get_height())
            
            button = ButtonParam(rect, text, Police.bouton, image, action)
            self.buttons.append(button)
            
            x += image.get_width() + espacement
            
    # =====================================
    # ACTIONS DES BOUTONS
    # =====================================
    
    def _action_sauvegarder(self):
        """Sauvegarde les paramètres"""
        sauvegarder_parametres(self.settings)
        print("Parametres sauvegardes dans", SAVE_FILE)
        
    def _action_reset(self):
        """Réinitialise les paramètres"""
        self.settings = copy.deepcopy(DEFAULT_SETTINGS)
        self.capture_touche = None
        self._init_sliders() 
        print("Paramètres réinitialisés")
        
    def _action_retour(self):
        """Retour au menu principal"""
        self.en_cours = False
        
    # =====================================
    # GESTION DES ÉVÉNEMENTS
    # =====================================
    
    def handle_events(self, event):
        """Gère les événements"""
        if event.type == pygame.QUIT:
            self.en_cours = False
            
        elif event.type == pygame.KEYDOWN:
            if self.capture_touche:
                self.settings["touches"][self.capture_touche] = event.key
                self.capture_touche = None
                
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self._handle_click(event.pos)
                
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.slider_actif = None
                
    def _handle_click(self, mouse_pos):
        """Gère les clics de souris"""
        # Clic sur onglets
        self._check_tab_click(mouse_pos)
        
        # Clic selon l'onglet actif
        if self.onglet_actif == "Touches":
            self._check_key_button_click(mouse_pos)
        elif self.onglet_actif == "Audio":
            self._check_slider_click(mouse_pos)
            
        # Clic sur boutons principaux
        for button in self.buttons:
            if button.is_clicked(mouse_pos):
                button.action()
                
    def _check_tab_click(self, mouse_pos):
        """Vérifie le clic sur les onglets"""
        onglet_largeur = self.panneau_largeur // len(self.onglets)
        for i, nom in enumerate(self.onglets):
            rect = pygame.Rect(
                self.panneau_x + i * onglet_largeur,
                self.panneau_y - 50,
                onglet_largeur, 40
            )
            if rect.collidepoint(mouse_pos):
                self.onglet_actif = nom
                self.capture_touche = None
                
    def _check_key_button_click(self, mouse_pos):
        """Vérifie le clic sur les boutons de touches"""
        y_offset = self.panneau_y + 40
        espacement_ligne = 70
        
        for i, (_, key_id) in enumerate(self.touches_config):
            y = y_offset + i * espacement_ligne
            rect = pygame.Rect(
                self.panneau_x + self.panneau_largeur - 150 - 40,
                y - 5, 150, 40
            )
            if rect.collidepoint(mouse_pos):
                self.capture_touche = key_id
                
    def _check_slider_click(self, mouse_pos):
        """Vérifie le clic sur les sliders"""
        for param_id, slider in self.sliders.items():
            if slider.rect.collidepoint(mouse_pos):
                self.slider_actif = param_id
                
    # =====================================
    # MISE À JOUR
    # =====================================
    
    def update_slider(self):
        """Met à jour le slider actif"""
        if self.slider_actif and pygame.mouse.get_pressed()[0]:
            mouse_pos = pygame.mouse.get_pos()
            slider = self.sliders[self.slider_actif]
            slider.update_valeur(mouse_pos[0])
            self.settings["audio"][self.slider_actif] = slider.valeur
            
    # =====================================
    # RENDU
    # =====================================
    
    def draw_titre(self):
        """Dessine le titre"""
        titre_surf = Police.titre.render("Parametres", True, Couleur.BLANC)
        rect = titre_surf.get_rect(center=(self.screen_width // 2, 50))
        self.screen.blit(titre_surf, rect)
        
    def draw_panneau(self):
        """Dessine le panneau principal"""
        pygame.draw.rect(
            self.screen, Couleur.GRIS_FONCE,
            (self.panneau_x, self.panneau_y, self.panneau_largeur, self.panneau_hauteur),
            border_radius=15
        )
        pygame.draw.rect(
            self.screen, Couleur.GRIS_MOYEN,
            (self.panneau_x, self.panneau_y, self.panneau_largeur, self.panneau_hauteur),
            2, border_radius=15
        )
        
    def draw_onglets(self):
        """Dessine les onglets"""
        onglet_largeur = self.panneau_largeur // len(self.onglets)
        for i, nom in enumerate(self.onglets):
            rect = pygame.Rect(
                self.panneau_x + i * onglet_largeur,
                self.panneau_y - 50,
                onglet_largeur, 40
            )
            couleur = Couleur.BLEU_ACCENT if nom == self.onglet_actif else Couleur.GRIS_CLAIR
            pygame.draw.rect(self.screen, couleur, rect, border_radius=8)
            
            texte = Police.param.render(
                nom, True,
                Couleur.BLANC if nom == self.onglet_actif else Couleur.GRIS_FONCE
            )
            text_rect = texte.get_rect(center=rect.center)
            self.screen.blit(texte, text_rect)
            
    def draw_onglet_touches(self):
        """Dessine l'onglet des touches"""
        y_offset = self.panneau_y + 40
        espacement_ligne = 70
        
        for i, (label, key_id) in enumerate(self.touches_config):
            y = y_offset + i * espacement_ligne
            
            # Label
            text_label = Police.param.render(label + ":", True, Couleur.BLANC)
            self.screen.blit(text_label, (self.panneau_x + 40, y))
            
            # Bouton de touche
            rect_bouton = pygame.Rect(
                self.panneau_x + self.panneau_largeur - 150 - 40,
                y - 5, 150, 40
            )
            
            if self.capture_touche == key_id:
                couleur = Couleur.ORANGE
                texte = "Appuyez..."
            else:
                couleur = Couleur.GRIS_MOYEN
                texte = get_key_name(self.settings["touches"][key_id])
                
            pygame.draw.rect(self.screen, couleur, rect_bouton, border_radius=8)
            text_surf = Police.param.render(texte, True, Couleur.BLANC)
            text_rect = text_surf.get_rect(center=rect_bouton.center)
            self.screen.blit(text_surf, text_rect)
            
    def draw_onglet_audio(self):
        """Dessine l'onglet audio"""
        y_offset = 80
        audio_labels = [
            "Volume general",
            "Volume musique",
            "Volume sons"
        ]
        param_ids = ["volume_general", "volume_musique", "volume_sons"]
        
        for idx, (label, param_id) in enumerate(zip(audio_labels, param_ids)):
            y = self.panneau_y + y_offset + idx * 100
            slider = self.sliders[param_id]
            
            # Label
            text = Police.param.render(label, True, Couleur.BLANC)
            self.screen.blit(text, (slider.rect.x, y - 25))
            
            # Valeur
            valeur_text = Police.param.render(f"{slider.valeur}%", True, Couleur.BLEU_ACCENT)
            self.screen.blit(valeur_text, (slider.rect.x + slider.rect.width + 20, y - 25))
            
            # Slider
            slider.draw(self.screen)
            
    def draw_boutons(self):
        """Dessine les boutons"""
        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons:
            button.update(mouse_pos)
            button.draw(self.screen)
            
    def draw(self):
        """Dessine tout le menu"""
        self.souris = pygame.mouse.get_pos()
        
        self.draw_titre()
        self.draw_panneau()
        self.draw_onglets()
        
        if self.onglet_actif == "Touches":
            self.draw_onglet_touches()
        elif self.onglet_actif == "Audio":
            self.draw_onglet_audio()
            
        self.draw_boutons()
        
        # Curseur
        self.screen.blit(self.curseur_img, self.souris)


# =====================================
# FONCTION PRINCIPALE
# =====================================

def main(ecran):
    """
    Lance le menu des paramètres
    
    Args:
        ecran: Surface Pygame
    """
    # Création du fond spatial animé
    stars, planet_manager, vaisseau_fond = create_space_background()
    
    # Création de l'instance du menu
    menu = MenuParametres()
    menu.update()
    menu.en_cours = True
    
    horloge = pygame.time.Clock()

    while menu.en_cours:
        # Fond animé
        ecran.fill((0, 0, 0))
        stars.update()
        stars.draw(ecran)
        planet_manager.update_and_draw()
        Animator.update_all()
        PlanetAnimator.update_all()
        ShipAnimator.update_all()
        
        # Gestion des événements
        for event in pygame.event.get():
            menu.handle_events(event)
        
        # Mise à jour du slider
        menu.update_slider()
        
        # Dessin du menu
        menu.draw()
        
        pygame.display.flip()
        horloge.tick(60)
    
    # Nettoyage
    ShipAnimator.clear_list()
    PlanetAnimator.clear_list()