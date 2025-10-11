"""
menuFin.py
Menu de fin de partie - Version restructurée
"""
import pygame
import sys

from classes.ShipAnimator import ShipAnimator
from classes.PlanetAnimator import PlanetAnimator
from classes.Animator import Animator
from classes.Start_Animation.main import create_space_background
from classes.Sounds import SoundManager

# =====================================
# CLASSES
# =====================================

class EndButton:
    """Bouton pour le menu de fin"""
    
    def __init__(self, rect, text, text_surf, image, action=None):
        """
        Initialise un bouton de fin
        
        Args:
            rect: Rectangle de position
            text: Texte du bouton (identifiant)
            text_surf: Surface texte prérendue
            image: Image de fond
            action: Fonction à appeler au clic
        """
        self.rect = rect
        self.text = text
        self.text_surf = text_surf
        self.image = image
        self.action = action
        self.zoom = 1.0
        self.is_hovered = False
        
    def update(self, mouse_pos):
        """Met à jour l'animation du bouton"""
        was_hovered = self.is_hovered
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        
        target_zoom = 1.1 if self.is_hovered else 1.0
        self.zoom += (target_zoom - self.zoom) * 0.08
        
        return self.is_hovered and not was_hovered # True si début du survol
        
    def draw(self, surface):
        """Dessine le bouton"""
        width = int(self.image.get_width() * self.zoom)
        height = int(self.image.get_height() * self.zoom)
        scaled = pygame.transform.scale(self.image, (width, height))
        rect_zoom = scaled.get_rect(center=self.rect.center)
        
        surface.blit(scaled, rect_zoom.topleft)
        text_rect = self.text_surf.get_rect(center=rect_zoom.center)
        surface.blit(self.text_surf, text_rect)
        
    def is_clicked(self, mouse_pos):
        """Vérifie si le bouton est cliqué"""
        return self.rect.collidepoint(mouse_pos)


class MenuFin:
    """Menu de fin de partie"""
    
    def __init__(self, ecran, player, victoire=True, sound_manager=None):
        """
        Initialise le menu de fin
        
        Args:
            ecran: Surface Pygame
            player: Instance de Player avec les stats
            victoire: True si victoire, False si défaite
            sound_manager: Gestionnaire de sons (optionnel)
        """
        self.ecran = ecran
        self.player = player
        self.victoire = victoire
        self.largeur_ecran, self.hauteur_ecran = ecran.get_size()
        
        # État
        self.running = True
        self.choix = None
        
        # Nettoyage des animateurs
        ShipAnimator.clear_list()
        PlanetAnimator.clear_list()
        
        # Initialisation
        self._init_colors()
        self._init_fonts()
        self._init_cursor()
        self._init_sound(sound_manager)
        self._init_background()
        self._init_panel()
        self._init_buttons()
        
        self.clock = pygame.time.Clock()
        
    # =====================================
    # INITIALISATION
    # =====================================
    
    def _init_colors(self):
        """Initialise les couleurs"""
        self.BLANC = (255, 255, 255)
        self.GRIS_FONCE = (40, 40, 55)
        self.GRIS_MOYEN = (90, 90, 110)
        self.JAUNE = (255, 215, 0)
        self.ROUGE = (220, 50, 50)
        self.NOIR = (0, 0, 0)
        
    def _init_fonts(self):
        """Initialise les polices"""
        self.police_titre = pygame.font.Font("assets/fonts/SpaceNova.otf", 80)
        self.police_sous_titre = pygame.font.Font("assets/fonts/SpaceNova.otf", 30)
        self.police_bouton = pygame.font.Font("assets/fonts/SpaceNova.otf", 24)
        
    def _init_cursor(self):
        """Initialise le curseur personnalisé"""
        self.cursor = pygame.image.load('assets/img/menu/cursor.png')
        self.cursor = pygame.transform.scale(self.cursor, (40, 40))
        pygame.mouse.set_visible(False)
        
    def _init_sound(self, sound_manager):
        """Initialise le gestionnaire de sons"""
        if sound_manager is None:
            self.sm = SoundManager()
            self.sm.load_sfx("son_hover", "assets/sounds/menu/buttons/button_hover.mp3")
            self.sm.load_sfx("son_click", "assets/sounds/menu/buttons/button_pressed.mp3")
        else:
            self.sm = sound_manager
            
    def _init_background(self):
        """Initialise le fond animé"""
        screen_ratio = (self.largeur_ecran * 100 / 600) / 100
        self.stars, self.planet_manager, self.vaisseau_fond = create_space_background(
            num_stars=100,
            screen_ratio=screen_ratio
        )
        
    def _init_panel(self):
        """Initialise le panneau central"""
        self.panneau_largeur = 600
        self.panneau_hauteur = 300
        self.panneau_x = (self.largeur_ecran - self.panneau_largeur) // 2
        self.panneau_y = (self.hauteur_ecran - self.panneau_hauteur) // 2 - 50
        
    def _init_buttons(self):
        """Initialise les boutons"""
        image_base = pygame.image.load("assets/img/menu/bouton_menu.png").convert_alpha()
        
        # Configuration des boutons
        button_configs = [
            ("RETOUR AU MENU", "menu", self._action_menu),
            ("QUITTER", "quitter", self._action_quitter)
        ]
        
        # Création des boutons
        self.buttons = []
        button_images = []
        
        for text, action_id, action_func in button_configs:
            text_surf = self.police_bouton.render(text, True, self.BLANC)
            image = pygame.transform.scale(
                image_base,
                (text_surf.get_width() + 150, text_surf.get_height() + 80)
            )
            button_images.append((image, text_surf, action_id, action_func))
            
        # Positionnement horizontal
        espacement = 80
        y_boutons = self.hauteur_ecran - 150
        total_width = sum(img.get_width() for img, _, _, _ in button_images)
        total_width += espacement * (len(button_images) - 1)
        x = (self.largeur_ecran - total_width) // 2
        
        for image, text_surf, action_id, action_func in button_images:
            rect = pygame.Rect(x, y_boutons, image.get_width(), image.get_height())
            button = EndButton(rect, action_id, text_surf, image, action_func)
            self.buttons.append(button)
            x += image.get_width() + espacement
            
    # =====================================
    # ACTIONS DES BOUTONS
    # =====================================
    
    def _action_menu(self):
        """Retour au menu principal : défini le choix et quitte la boucle du menu"""
        self.running = False
        self.choix = "menu_principal"
        
    def _action_quitter(self):
        """Quitter le jeu : défini le choix et quitte la boucle du menu"""
        self.running = False
        self.choix = "quitter"
        
    # =====================================
    # GESTION DES ÉVÉNEMENTS
    # =====================================
    
    def _handle_events(self):
        """Gère les événements"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._action_quitter()
                
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self._handle_click(event.pos)
                
    def _handle_click(self, mouse_pos):
        """Gère les clics de souris"""
        for button in self.buttons:
            if button.is_clicked(mouse_pos):
                self.sm.play_sfx("son_click")
                if button.action:
                    button.action()
                    
    # =====================================
    # MISE À JOUR
    # =====================================
    
    def _update(self):
        """Met à jour la logique du menu"""
        mouse_pos = pygame.mouse.get_pos()
        
        for button in self.buttons:
            if button.update(mouse_pos):
                self.sm.play_sfx("son_hover")
                
    # =====================================
    # RENDU
    # =====================================
    
    def _draw_background(self):
        """Dessine le fond animé"""
        self.ecran.fill(self.NOIR)
        
        # Étoiles
        self.stars.update()
        self.stars.draw(self.ecran)
        
        # Planètes et animations
        self.planet_manager.update_and_draw()
        Animator.update_all()
        PlanetAnimator.update_all()
        ShipAnimator.update_all()
        
    def _draw_panel(self):
        """Dessine le panneau central semi-transparent"""
        panneau_surf = pygame.Surface(
            (self.panneau_largeur, self.panneau_hauteur),
            pygame.SRCALPHA
        )
        pygame.draw.rect(
            panneau_surf,
            (40, 40, 55, 200),
            (0, 0, self.panneau_largeur, self.panneau_hauteur),
            border_radius=20
        )
        pygame.draw.rect(
            panneau_surf,
            self.GRIS_MOYEN,
            (0, 0, self.panneau_largeur, self.panneau_hauteur),
            3,
            border_radius=20
        )
        self.ecran.blit(panneau_surf, (self.panneau_x, self.panneau_y))
        
    def _draw_title(self):
        """Dessine le titre (VICTOIRE ou DÉFAITE)"""
        if self.victoire:
            titre_texte = "VICTOIRE"
            couleur_titre = self.JAUNE
        else:
            titre_texte = "DEFAITE"
            couleur_titre = self.ROUGE
            
        titre_surf = self.police_titre.render(titre_texte, True, couleur_titre)
        rect = titre_surf.get_rect(
            center=(
                self.largeur_ecran // 2,
                self.panneau_y + self.panneau_hauteur // 2 - 30
            )
        )
        self.ecran.blit(titre_surf, rect)
        
    def _draw_subtitle(self):
        """Dessine le nom du joueur"""
        player_name = self.player.name if self.player is not None else ""
        sous_titre = self.police_sous_titre.render(player_name, True, self.BLANC)
        rect = sous_titre.get_rect(
            center=(
                self.largeur_ecran // 2,
                self.panneau_y + self.panneau_hauteur // 2 + 50
            )
        )
        self.ecran.blit(sous_titre, rect)
        
    def _draw_buttons(self):
        """Dessine les boutons"""
        for button in self.buttons:
            button.draw(self.ecran)
            
    def _draw_cursor(self):
        """Dessine le curseur"""
        mouse_pos = pygame.mouse.get_pos()
        self.ecran.blit(self.cursor, mouse_pos)
        
    def _render(self):
        """Effectue le rendu complet"""
        self._draw_background()
        self._draw_panel()
        self._draw_title()
        self._draw_subtitle()
        self._draw_buttons()
        self._draw_cursor()
        
        pygame.display.flip()
        
    # =====================================
    # BOUCLE PRINCIPALE
    # =====================================
    
    def run(self):
        """Lance la boucle principale du menu et retourne l'action choisie."""
        while self.running:
            self._handle_events()
            self._update()
            self._render()
            self.clock.tick(60)
            
        return self.choix


# =====================================
# FONCTION PRINCIPALE
# =====================================

def main(ecran, player, victoire=True, sound_manager=None):
    """
    Lance le menu de fin de partie. Gère l'action de quitter localement.
    Retourne l'action choisie ("menu_principal" ou None) au module appelant.
    """
    menu = MenuFin(ecran, player, victoire, sound_manager)
    action = menu.run()
    
    if action == "quitter":
        pygame.quit()
        sys.exit()
        
    return action