import pygame
import threading
import time
from blazyck import *
from classes.Animator import Animator
from classes.ResourceManager import ResourceManager
import os

class LoadingScreen:
    def __init__(self):
        pygame.init()
        info = pygame.display.Info()
        self.screen_width = info.current_w
        self.screen_height = info.current_h
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.FULLSCREEN)
        pygame.display.set_caption("Chargement - Xenon Space")
        
        Animator.set_screen(self.screen)
        
        self.clock = pygame.time.Clock()
        self.running = True
        self.loading_progress = 0
        self.loading_complete = False
        
        # Créer l'animation de chargement
        self.setup_loading_animation()
        
        # Gestionnaire de ressources
        self.resource_manager = ResourceManager()
        
    def setup_loading_animation(self):
        """Configure l'animation de chargement"""
        # Position centrale
        center_x = self.screen_width // 2
        center_y = self.screen_height // 2
        
        # L'animation sera centrée, disons 200x200 pixels
        self.loading_animator = Animator(
            IMG_PATH,
            (200 // TAILLE_CASE, 200 // TAILLE_CASE),  # dimensions en cases
            ((center_x - 100) // TAILLE_CASE, (center_y - 150) // TAILLE_CASE),  # position
            default_fps=30
        )
        
        # Charger et jouer l'animation
        try:
            self.loading_animator.load_animation("loading", "loading.gif")
            self.loading_animator.play("loading")
        except Exception as e:
            print(f"[LoadingScreen] Erreur chargement animation : {e}")
    
    def update_progress(self, value):
        """Callback pour mettre à jour la progression"""
        self.loading_progress = value
    
    def load_resources_thread(self):
        """Thread pour charger les ressources sans bloquer l'animation"""
        try:
            # Charger les planètes (70% du temps)
            self.resource_manager.load_planetes(
                lambda p: self.update_progress(p * 0.7)
            )
            
            # Charger les astéroïdes (30% du temps)
            self.resource_manager.load_asteroides(
                lambda p: self.update_progress(0.7 + p * 0.3)
            )
            
            # Petit délai pour voir la fin
            time.sleep(0.5)
            self.loading_progress = 1.0
            time.sleep(0.5)
            
            self.loading_complete = True
        except Exception as e:
            print(f"[LoadingScreen] Erreur dans le thread : {e}")
            self.loading_complete = True
    
    def draw_progress_bar(self):
        """Dessine la barre de progression"""
        bar_width = 600
        bar_height = 30
        bar_x = (self.screen_width - bar_width) // 2
        bar_y = self.screen_height // 2 + 50
        
        # Fond de la barre
        pygame.draw.rect(self.screen, (60, 60, 80), 
                        (bar_x, bar_y, bar_width, bar_height),
                        border_radius=15)
        
        # Barre de progression
        if self.loading_progress > 0:
            progress_width = int(bar_width * self.loading_progress)
            pygame.draw.rect(self.screen, (0, 200, 100),
                           (bar_x, bar_y, progress_width, bar_height),
                           border_radius=15)
        
        # Bordure
        pygame.draw.rect(self.screen, (100, 150, 200),
                        (bar_x, bar_y, bar_width, bar_height),
                        2, border_radius=15)
        
        # Texte de pourcentage
        font = pygame.font.Font("assets/fonts/SpaceNova.otf", 24)
        percent_text = f"{int(self.loading_progress * 100)}%"
        text_surf = font.render(percent_text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=(bar_x + bar_width // 2, bar_y + bar_height // 2))
        self.screen.blit(text_surf, text_rect)
        
        # Texte "Chargement..."
        loading_text = font.render("Chargement des ressources...", True, (200, 200, 200))
        loading_rect = loading_text.get_rect(center=(self.screen_width // 2, bar_y + bar_height + 30))
        self.screen.blit(loading_text, loading_rect)
    
    def run(self):
        """Lance l'écran de chargement"""
        # Démarrer le thread de chargement
        loading_thread = threading.Thread(target=self.load_resources_thread, daemon=True)
        loading_thread.start()
        
        while self.running and not self.loading_complete:
            # Gestion des événements
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                        return False
            
            # Affichage
            self.screen.fill((10, 10, 20))
            
            # Animation de chargement
            Animator.update_all()
            
            # Barre de progression
            self.draw_progress_bar()
            
            pygame.display.flip()
            self.clock.tick(60)
        
        return True

def main():
    """Point d'entrée principal avec écran de chargement"""
    # Lancer l'écran de chargement
    loader = LoadingScreen()
    success = loader.run()
    
    if success:
        # Importer le menu principal APRÈS le chargement
        Animator.clear_list()
        import menu.menuPrincipal
        # Le menu principal se lance automatiquement à l'import
    else:
        pygame.quit()

if __name__ == "__main__":
    main()