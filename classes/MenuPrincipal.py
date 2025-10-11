"""
MenuPrincipal.py
Menu principal du jeu - Version restructurée
"""
import pygame
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from classes.PlanetAnimator import PlanetAnimator
from classes.ShipAnimator import ShipAnimator
from classes.TitreAnime import TitreAnime
from classes.Animator import Animator
from classes.Start_Animation.main import create_space_background
import menu.menuJouer as menuJouer
import menu.menuParam as menuParam
import menu.menuSucces as menuSucces
import menu.menuPause as menuPause


class MenuButton:
    """Représente un bouton de menu avec animation"""
    
    def __init__(self, rect, text, font, image):
        self.rect = rect
        self.text = font.render(text, True, (255, 255, 255))
        self.image = image
        self.zoom = 1.0
        self.is_hovered = False
        
    def update(self, mouse_pos):
        """Met à jour l'animation du bouton"""
        hover_zone = self.rect.inflate(0, -100)
        was_hovered = self.is_hovered
        self.is_hovered = hover_zone.collidepoint(mouse_pos)
        
        zoom_target = 1.1 if self.is_hovered else 1.0
        self.zoom += (zoom_target - self.zoom) * 0.08
        
        return self.is_hovered and not was_hovered
        
    def draw(self, surface):
        """Dessine le bouton"""
        width = int(self.image.get_width() * self.zoom)
        height = int(self.image.get_height() * self.zoom)
        scaled = pygame.transform.scale(self.image, (width, height))
        rect = scaled.get_rect(center=self.rect.center)
        
        surface.blit(scaled, rect.topleft)
        text_rect = self.text.get_rect(center=rect.center)
        surface.blit(self.text, text_rect.topleft)
        
    def is_clicked(self, mouse_pos):
        """Vérifie si le bouton est cliqué"""
        return self.rect.collidepoint(mouse_pos)


class MenuPrincipal:
    """Menu principal du jeu"""
    
    def __init__(self, ecran, screen_width, screen_height, screen_ratio, cursor, 
                 button_image, title_font, button_font, sound_manager):
        """
        Initialise le menu principal
        
        Args:
            ecran: Surface d'affichage Pygame
            screen_width: Largeur de l'écran
            screen_height: Hauteur de l'écran
            screen_ratio: Ratio de l'écran
            cursor: Image du curseur
            button_image: Image des boutons
            title_font: Police du titre
            button_font: Police des boutons
            sound_manager: Gestionnaire de sons
        """
        # Ressources du jeu
        self.ecran = ecran
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen_ratio = screen_ratio
        self.cursor = cursor
        self.button_image = button_image
        self.title_font = title_font
        self.button_font = button_font
        self.sm = sound_manager
        
        # Horloge
        self.clock = pygame.time.Clock()
        
        # État
        self.running = True
        
        # Initialisation des composants
        self._setup_background()
        self._setup_title()
        self._setup_buttons()
        
    def _setup_background(self):
        """Configure le fond spatial animé"""
        self.stars, self.planet_manager, self.B1 = create_space_background(
            num_stars=100,
            screen_ratio=self.screen_ratio
        )
        
    def _setup_title(self):
        """Configure le titre animé"""
        title_pos = (self.screen_width // 2, 200)
        self.titre = TitreAnime(
            "XENON-SPACE",
            self.title_font,
            title_pos,
            couleur_haut=(255, 255, 0),
            couleur_bas=(255, 0, 255)
        )
        
    def _setup_buttons(self):
        """Configure tous les boutons du menu"""
        button_width, button_height = self.button_image.get_size()
        
        # Position des boutons (décalés à gauche)
        x_offset = -500
        x_pos = self.screen_width // 2 - button_width // 2 + x_offset
        y_center = self.screen_height // 2
        
        # Création des boutons principaux
        self.btn_jouer = MenuButton(
            pygame.Rect(x_pos, y_center - 200, button_width, button_height),
            "Jouer", self.button_font, self.button_image
        )
        self.btn_param = MenuButton(
            pygame.Rect(x_pos, y_center - 100, button_width, button_height),
            "Parametres", self.button_font, self.button_image
        )
        self.btn_succes = MenuButton(
            pygame.Rect(x_pos, y_center, button_width, button_height),
            "Succes", self.button_font, self.button_image
        )
        self.btn_quitter = MenuButton(
            pygame.Rect(x_pos, y_center + 100, button_width, button_height),
            "Quitter", self.button_font, self.button_image
        )
        
        # Bouton crédits (en bas à droite)
        self.btn_credit = MenuButton(
            pygame.Rect(
                self.screen_width - button_width - 30,
                self.screen_height - button_height - 30,
                button_width, button_height
            ),
            "Credits", self.button_font, self.button_image
        )
        
        # Liste de tous les boutons
        self.buttons = [
            self.btn_jouer,
            self.btn_param,
            self.btn_succes,
            self.btn_quitter,
            self.btn_credit
        ]
        
    # =====================================
    # GESTION DES ÉVÉNEMENTS
    # =====================================
    
    def _handle_events(self):
        """Gère tous les événements Pygame"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
            elif event.type == pygame.KEYDOWN:
                self._handle_keypress(event.key)
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._handle_click(event.pos)
                
    def _handle_keypress(self, key):
        """Gère les touches du clavier"""
        if key == pygame.K_ESCAPE:
            menuPause.main_pause(self.ecran, self.sm)
            
    def _handle_click(self, mouse_pos):
        """Gère les clics de souris"""
        if self.btn_jouer.is_clicked(mouse_pos):
            self.sm.play_sfx("son_click")
            menuJouer.draw(self.ecran)
            
        elif self.btn_param.is_clicked(mouse_pos):
            self.sm.play_sfx("son_click")
            menuParam.main(self.ecran)
            
        elif self.btn_succes.is_clicked(mouse_pos):
            self.sm.play_sfx("son_click")
            menuSucces.main(self.ecran)
            
        elif self.btn_quitter.is_clicked(mouse_pos):
            self.sm.play_sfx("son_click")
            pygame.quit()
            sys.exit()
            
        elif self.btn_credit.is_clicked(mouse_pos):
            self.sm.play_sfx("son_click")
            # TODO: Implémenter menu crédits
            pass
            
    # =====================================
    # MISE À JOUR
    # =====================================
    
    def _update(self):
        """Met à jour la logique du menu"""
        mouse_pos = pygame.mouse.get_pos()
        
        # Mise à jour des boutons et gestion des sons de survol
        for button in self.buttons:
            if button.update(mouse_pos):
                self.sm.play_sfx("son_hover")
                
    # =====================================
    # RENDU
    # =====================================
    
    def _draw_background(self):
        """Dessine le fond animé"""
        self.ecran.fill((0, 0, 0))
        
        # Étoiles
        self.stars.update()
        self.stars.draw(self.ecran)
        
        # Planètes et animations
        self.planet_manager.update_and_draw()
        Animator.update_all()
        PlanetAnimator.update_all()
        ShipAnimator.update_all()
        
    def _draw_ui(self):
        """Dessine l'interface utilisateur"""
        # Titre
        self.titre.draw(self.ecran)
        
        # Boutons
        for button in self.buttons:
            button.draw(self.ecran)
            
        # Curseur
        mouse_pos = pygame.mouse.get_pos()
        self.ecran.blit(self.cursor, mouse_pos)
        
    def _render(self):
        """Effectue le rendu complet"""
        self._draw_background()
        self._draw_ui()
        pygame.display.flip()
        
    # =====================================
    # BOUCLE PRINCIPALE
    # =====================================
    
    def run(self):
        """Lance la boucle principale du menu"""
        while self.running:
            self._handle_events()
            self._update()
            self._render()
            self.clock.tick(30)


# =====================================
# FONCTION PRINCIPALE
# =====================================

# =====================================
# FONCTION PRINCIPALE
# =====================================

def main(ecran=None, screen_width=None, screen_height=None, screen_ratio=None, 
         cursor=None, button_image=None, title_font=None, button_font=None, 
         sound_manager=None):
    """
    Lance le menu principal
    
    Args:
        Tous les paramètres sont optionnels. Si non fournis, ils seront initialisés ici.
    """
    # Si appelé sans paramètres (depuis menuFin par exemple), initialiser
    if ecran is None:
        import pygame
        from classes.Sounds import SoundManager
        
        pygame.init()
        screen_info = pygame.display.Info()
        screen_width = screen_info.current_w
        screen_height = screen_info.current_h
        ecran = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
        screen_ratio = (screen_width * 100 / 600) / 100
        
        # Initialiser Animator
        Animator.set_screen(ecran)
        
        # Icône
        icone = pygame.image.load("assets/img/menu/logo.png")
        pygame.display.set_icon(icone)
        
        # Curseur
        cursor = pygame.image.load('assets/img/menu/cursor.png')
        cursor = pygame.transform.scale(cursor, (40, 40))
        pygame.mouse.set_visible(False)
        
        # Boutons
        button_image = pygame.image.load("assets/img/menu/bouton_menu.png").convert_alpha()
        button_image = pygame.transform.scale(button_image, (500, 150))
        
        # Polices
        title_font = pygame.font.Font("assets/fonts/SpaceNova.otf", 100)
        button_font = pygame.font.Font("assets/fonts/SpaceNova.otf", 25)
        
        # Son
        sound_manager = SoundManager()
        sound_manager.play_music("assets/sounds/musics/music_ingame.mp3")
        sound_manager.load_sfx("son_hover", "assets/sounds/menu/buttons/button_hover.mp3")
        sound_manager.load_sfx("son_click", "assets/sounds/menu/buttons/button_pressed.mp3")


        ecran.fill((0, 0, 0)) 
        pygame.display.flip()

    
    menu = MenuPrincipal(
        ecran, screen_width, screen_height, screen_ratio,
        cursor, button_image, title_font, button_font, sound_manager
    )
    menu.run()
    Animator.update_all()


if __name__ == "__main__":
    main()