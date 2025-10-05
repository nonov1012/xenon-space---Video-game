import pygame
import os
import threading
import time
from classes.Gif import Gif

class LoadingScreen:
    def __init__(self, screen):
        """
        Initialise l'écran de chargement
        
        Args:
            screen: La surface d'affichage pygame
        """
        self.screen = screen
        self.screen_width, self.screen_height = screen.get_size()
        
        # Couleurs
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GREEN = (0, 255, 0)
        self.GRAY = (128, 128, 128)
        self.BLUE = (70, 130, 255)
        
        # Police pour le texte
        try:
            self.font = pygame.font.Font("assets/fonts/SpaceNova.otf", 36)
            self.small_font = pygame.font.Font("assets/fonts/SpaceNova.otf", 24)
            self.title_font = pygame.font.Font("assets/fonts/SpaceNova.otf", 60)
        except:
            self.font = pygame.font.Font(None, 36)
            self.small_font = pygame.font.Font(None, 24)
            self.title_font = pygame.font.Font(None, 60)
        
        # GIF de chargement
        try:
            self.loading_gif = Gif("assets/Loading.gif")
        except:
            self.loading_gif = None
            print("Impossible de charger le GIF de chargement")
        
        # Barre de progression
        self.progress = 0
        self.max_progress = 100
        self.bar_width = 600
        self.bar_height = 30
        self.bar_x = (self.screen_width - self.bar_width) // 2
        self.bar_y = self.screen_height - 200
        
        # Variables de chargement
        self.loading_complete = False
        self.loading_thread = None
        self.current_task = "Initialisation..."
        self.planet_images = {}
        
        # Curseur personnalisé
        try:
            self.cursor_img = pygame.image.load('assets/img/menu/cursor.png')
            self.cursor_img = pygame.transform.scale(self.cursor_img, (40, 40))
            pygame.mouse.set_visible(False)
        except:
            pygame.mouse.set_visible(True)
            self.cursor_img = None
        
        # Animation du titre
        self.title_alpha = 255
        self.title_direction = -2
    
    def load_planet_images(self):
        """
        Charge toutes les images des planètes
        Cette méthode s'exécute dans un thread séparé
        """
        planet_folder = "assets/img/planets/"
        
        # Liste des fichiers de planètes à charger
        planet_files = []
        
        # Scanner le dossier des planètes
        try:
            if os.path.exists(planet_folder):
                for filename in os.listdir(planet_folder):
                    if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                        planet_files.append(filename)
        except Exception as e:
            print(f"Erreur lors de la lecture du dossier planètes: {e}")
        
        total_files = len(planet_files)
        
        if total_files == 0:
            # Si aucune planète trouvée, créer quelques images factices pour la démo
            self.current_task = "Aucune planète trouvée, chargement des ressources..."
            for i in range(10):
                self.current_task = f"Chargement des ressources... {i+1}/10"
                self.progress = int((i + 1) / 10 * 100)
                time.sleep(0.2)
            
            self.current_task = "Chargement terminé!"
            self.loading_complete = True
            return
        
        # Charger chaque image de planète
        for i, filename in enumerate(planet_files):
            try:
                self.current_task = f"Chargement de {filename}..."
                
                # Charger l'image
                image_path = os.path.join(planet_folder, filename)
                planet_image = pygame.image.load(image_path).convert_alpha()
                
                # Stocker l'image dans le dictionnaire
                planet_name = os.path.splitext(filename)[0]
                self.planet_images[planet_name] = planet_image
                
                # Mettre à jour la progression
                self.progress = int((i + 1) / total_files * 100)
                
                # Petit délai pour voir la progression
                time.sleep(0.1)
                
            except Exception as e:
                print(f"Erreur lors du chargement de {filename}: {e}")
                continue
        
        # Chargement terminé
        self.current_task = "Chargement terminé!"
        self.loading_complete = True
        time.sleep(1)  # Pause avant de continuer
    
    def start_loading(self):
        """
        Démarre le chargement dans un thread séparé
        """
        if self.loading_thread is None or not self.loading_thread.is_alive():
            self.loading_thread = threading.Thread(target=self.load_planet_images)
            self.loading_thread.daemon = True
            self.loading_thread.start()
    
    def draw_progress_bar(self):
        """
        Dessine la barre de progression
        """
        # Fond de la barre avec bordure arrondie
        pygame.draw.rect(self.screen, self.GRAY, 
                        (self.bar_x - 2, self.bar_y - 2, self.bar_width + 4, self.bar_height + 4),
                        border_radius=15)
        
        pygame.draw.rect(self.screen, self.BLACK, 
                        (self.bar_x, self.bar_y, self.bar_width, self.bar_height),
                        border_radius=12)
        
        # Progression
        if self.progress > 0:
            progress_width = int((self.progress / self.max_progress) * (self.bar_width - 4))
            if progress_width > 0:
                pygame.draw.rect(self.screen, self.GREEN,
                               (self.bar_x + 2, self.bar_y + 2, progress_width, self.bar_height - 4),
                               border_radius=10)
        
        # Texte de pourcentage
        percent_text = f"{self.progress}%"
        text_surface = self.font.render(percent_text, True, self.WHITE)
        text_rect = text_surface.get_rect(center=(self.screen_width // 2, self.bar_y + self.bar_height + 50))
        self.screen.blit(text_surface, text_rect)
    
    def update_title_animation(self):
        """
        Met à jour l'animation du titre
        """
        self.title_alpha += self.title_direction
        if self.title_alpha <= 180:
            self.title_direction = 2
        elif self.title_alpha >= 255:
            self.title_direction = -2
    
    def draw(self):
        """
        Dessine l'écran de chargement
        """
        # Fond noir avec effet d'étoiles (points blancs aléatoires)
        self.screen.fill(self.BLACK)
        
        # Quelques étoiles décoratives
        import random
        for _ in range(50):
            x = random.randint(0, self.screen_width)
            y = random.randint(0, self.screen_height)
            brightness = random.randint(100, 255)
            pygame.draw.circle(self.screen, (brightness, brightness, brightness), (x, y), 1)
        
        # GIF de chargement (centré)
        if self.loading_gif:
            try:
                if hasattr(self.loading_gif, 'get_current_frame'):
                    gif_frame = self.loading_gif.get_current_frame()
                    if gif_frame:
                        gif_rect = gif_frame.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - 50))
                        self.screen.blit(gif_frame, gif_rect)
            except:
                # Si le GIF ne fonctionne pas, dessiner un cercle qui tourne
                center = (self.screen_width // 2, self.screen_height // 2 - 50)
                angle = (pygame.time.get_ticks() / 10) % 360
                radius = 40
                for i in range(8):
                    angle_rad = (angle + i * 45) * 3.14159 / 180
                    x = center[0] + radius * pygame.math.cos(angle_rad)
                    y = center[1] + radius * pygame.math.sin(angle_rad)
                    alpha = 255 - (i * 30)
                    color = (0, alpha, 0) if alpha > 0 else (0, 0, 0)
                    pygame.draw.circle(self.screen, color, (int(x), int(y)), 8)
        
        # Titre animé
        self.update_title_animation()
        title_surface = self.title_font.render("XENON-SPACE", True, self.WHITE)
        title_surface.set_alpha(self.title_alpha)
        title_rect = title_surface.get_rect(center=(self.screen_width // 2, 120))
        self.screen.blit(title_surface, title_rect)
        
        # Sous-titre de chargement
        loading_text = self.small_font.render("Chargement en cours...", True, self.BLUE)
        loading_rect = loading_text.get_rect(center=(self.screen_width // 2, 170))
        self.screen.blit(loading_text, loading_rect)
        
        # Tâche actuelle
        task_text = self.small_font.render(self.current_task, True, self.WHITE)
        task_rect = task_text.get_rect(center=(self.screen_width // 2, self.bar_y - 50))
        self.screen.blit(task_text, task_rect)
        
        # Barre de progression
        self.draw_progress_bar()
        
        # Instructions
        instruction_text = self.small_font.render("Appuyez sur ECHAP pour quitter", True, (150, 150, 150))
        instruction_rect = instruction_text.get_rect(center=(self.screen_width // 2, self.screen_height - 50))
        self.screen.blit(instruction_text, instruction_rect)
        
        # Curseur personnalisé
        if self.cursor_img:
            mouse_pos = pygame.mouse.get_pos()
            self.screen.blit(self.cursor_img, mouse_pos)
    
    def update(self):
        """
        Met à jour l'écran de chargement
        """
        # Mettre à jour le GIF si disponible
        if self.loading_gif and hasattr(self.loading_gif, 'update'):
            try:
                self.loading_gif.update()
            except:
                pass
    
    def is_complete(self):
        """
        Retourne True si le chargement est terminé
        """
        return self.loading_complete
    
    def get_loaded_images(self):
        """
        Retourne le dictionnaire des images chargées
        """
        return self.planet_images
    
    def run(self):
        """
        Exécute l'écran de chargement jusqu'à ce qu'il soit terminé
        
        Returns:
            dict: Dictionnaire des images chargées
        """
        clock = pygame.time.Clock()
        self.start_loading()
        
        running = True
        while running and not self.is_complete():
            # Gérer les événements
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
            
            # Mettre à jour et dessiner
            self.update()
            self.draw()
            
            pygame.display.flip()
            clock.tick(60)
        
        # Attendre que le thread de chargement se termine
        if self.loading_thread and self.loading_thread.is_alive():
            self.loading_thread.join()
        
        return self.get_loaded_images()


# Exemple d'utilisation
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((1200, 800))
    pygame.display.set_caption("Xenon-Space - Chargement")
    
    # Créer et exécuter l'écran de chargement
    loading_screen = LoadingScreen(screen)
    loaded_images = loading_screen.run()
    
    print(f"Images chargées: {list(loaded_images.keys())}")
    
    pygame.quit()