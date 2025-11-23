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
from classes.GlobalVar.ScreenVar import ScreenVar

# -------------------------------
# Données des crédits
# -------------------------------
CREDITS_DATA = [
    {"nom": "NOEL CLEMENT", "role": "Lead Developer", "color": (100, 200, 255)},
    {"nom": "VOITURIER NOA", "role": "Game Designer", "color": (255, 100, 150)},
    {"nom": "DAVID GABRIEL", "role": "Graphics Artist", "color": (150, 255, 100)},
    {"nom": "CAVEL UGO", "role": "Sound Engineer", "color": (255, 200, 100)},
    {"nom": "DUPUIS BRIAN", "role": "Systems Architect", "color": (200, 100, 255)},
    {"nom": "VANHOVE TOM", "role": "Quality Assurance", "color": (100, 255, 200)},
    {"nom": "IUT du Littoral Cote d'Opale", "role": "Special Thanks", "color": (255, 255, 100)}
]

# -------------------------------
# Couleurs
# -------------------------------
class Couleur:
    BLANC = (255, 255, 255)
    GRIS_CLAIR = (200, 200, 200)
    BLEU_NEON = (0, 200, 255)
    CYAN = (100, 255, 255)
    NOIR = (0, 0, 0)

# -------------------------------
# Police
# -------------------------------
class Police:
    titre = pygame.font.Font("assets/fonts/SpaceNova.otf", 50)
    nom = pygame.font.Font("assets/fonts/SpaceNova.otf", 40)
    role = pygame.font.Font("assets/fonts/SpaceNova.otf", 24)
    info = pygame.font.Font("assets/fonts/SpaceNova.otf", 22)

# -------------------------------
# Classe Particule
# -------------------------------
class Particle:
    """Particule d'explosion pour effet visuel"""
    
    def __init__(self, x, y, color, vx, vy):
        self.x = x
        self.y = y
        self.color = color
        self.vx = vx
        self.vy = vy
        self.life = 60
        self.alpha = 255

    def update(self):
        """Met à jour la position et la vie de la particule"""
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.2  # Gravité
        self.life -= 1
        self.alpha = int((self.life / 60) * 255)

    def draw(self, surface):
        """Dessine la particule avec transparence"""
        if self.life > 0:
            # Créer une surface avec alpha pour la transparence
            s = pygame.Surface((6, 6), pygame.SRCALPHA)
            color_with_alpha = (*self.color[:3], self.alpha)
            pygame.draw.circle(s, color_with_alpha, (3, 3), 3)
            surface.blit(s, (int(self.x) - 3, int(self.y) - 3))

# -------------------------------
# Classe effet de lueur
# -------------------------------
class GlowEffect:
    """Effet de lueur pour les textes"""
    
    @staticmethod
    def draw_text_with_glow(surface, text, font, color, pos, glow_size=3):
        """Dessine un texte avec effet de lueur"""
        # Lueur (plusieurs couches avec transparence)
        for i in range(glow_size, 0, -1):
            alpha = int(100 / i)
            glow_surf = font.render(text, True, color)
            glow_surf.set_alpha(alpha)
            glow_rect = glow_surf.get_rect(center=pos)
            
            # Dessiner la lueur dans plusieurs directions
            for dx, dy in [(-i, 0), (i, 0), (0, -i), (0, i), (-i, -i), (i, i), (-i, i), (i, -i)]:
                surface.blit(glow_surf, (glow_rect.x + dx, glow_rect.y + dy))
        
        # Texte principal
        text_surf = font.render(text, True, color)
        text_rect = text_surf.get_rect(center=pos)
        surface.blit(text_surf, text_rect)
        
        return text_rect

# -------------------------------
# Menu Crédits
# -------------------------------
class MenuCredits:
    """Menu des crédits avec effets futuristes"""
    
    def __init__(self):
        self.en_cours = False
        self.particles = []
        self.credit_y = 0
        self.vitesse_defilement = 1.5
        self.vitesse_acceleree = 5
        self.espace_enfonce = False
        
        # Effet de scanline
        self.scanline_offset = 0
        
    def update(self):
        """Initialise ou met à jour le menu"""
        self.screen = ScreenVar.screen
        self.screen_width, self.screen_height = self.screen.get_size()
        
        # Position initiale des crédits
        self.credit_y = self.screen_height
        
        # Bouton retour (optionnel, en bas à gauche)
        self.rect_retour = pygame.Rect(20, self.screen_height - 80, 180, 60)
        
    def creer_explosion(self, text_surf, rect, color):
        """Crée une explosion de particules à partir d'un texte"""
        w, h = text_surf.get_size()
        step = 8  # Échantillonnage des pixels
        
        for i in range(0, w, step):
            for j in range(0, h, step):
                try:
                    pixel_color = text_surf.get_at((i, j))
                    if len(pixel_color) >= 4 and pixel_color[3] > 0:  # Pixel visible
                        # Variation de couleur pour effet
                        r = min(255, pixel_color[0] + random.randint(-30, 30))
                        g = min(255, pixel_color[1] + random.randint(-30, 30))
                        b = min(255, pixel_color[2] + random.randint(-30, 30))
                        
                        vx = random.uniform(-4, 4)
                        vy = random.uniform(-6, -1)
                        self.particles.append(
                            Particle(rect.x + i, rect.y + j, (r, g, b), vx, vy)
                        )
                except:
                    pass
    
    def draw_scanlines(self):
        """Dessine des lignes de scan pour effet CRT"""
        for y in range(0, self.screen_height, 4):
            scanline_y = (y + self.scanline_offset) % self.screen_height
            pygame.draw.line(self.screen, (0, 0, 0, 30), 
                           (0, scanline_y), (self.screen_width, scanline_y), 1)
        self.scanline_offset = (self.scanline_offset + 1) % 4
    
    def draw_grid_background(self):
        """Dessine une grille en perspective pour effet rétro-futuriste"""
        grid_color = (0, 100, 150, 50)
        spacing = 50
        
        # Lignes horizontales qui s'éloignent
        for i in range(10):
            y = self.screen_height // 2 + i * spacing
            if y < self.screen_height:
                width = int(self.screen_width * (1 - i * 0.05))
                x_start = (self.screen_width - width) // 2
                pygame.draw.line(self.screen, grid_color, 
                               (x_start, y), (x_start + width, y), 1)
    
    def draw_titre(self):
        """Dessine le titre avec effet néon"""
        titre_y = 80
        GlowEffect.draw_text_with_glow(
            self.screen, 
            "XENON SPACE - CREDITS", 
            Police.titre, 
            Couleur.BLEU_NEON, 
            (self.screen_width // 2, titre_y),
            glow_size=5
        )
        
        # Ligne décorative sous le titre
        line_y = titre_y + 40
        line_width = 400
        line_x = (self.screen_width - line_width) // 2
        pygame.draw.line(self.screen, Couleur.CYAN, 
                        (line_x, line_y), (line_x + line_width, line_y), 2)
    
    def draw_credits(self):
        """Dessine les crédits qui défilent"""
        y_offset = self.credit_y
        espacement = 100
        
        for idx, credit_data in enumerate(CREDITS_DATA):
            # Position verticale de ce crédit
            credit_center_y = y_offset + idx * espacement
            
            # Ne dessiner que si visible
            if -100 < credit_center_y < self.screen_height + 100:
                # Nom avec effet de lueur
                nom_rect = GlowEffect.draw_text_with_glow(
                    self.screen,
                    credit_data["nom"],
                    Police.nom,
                    credit_data["color"],
                    (self.screen_width // 2, credit_center_y),
                    glow_size=3
                )
                
                # Rôle en dessous avec couleur atténuée
                role_color = tuple(int(c * 0.7) for c in credit_data["color"])
                role_surf = Police.role.render(credit_data["role"], True, role_color)
                role_rect = role_surf.get_rect(center=(self.screen_width // 2, credit_center_y + 35))
                self.screen.blit(role_surf, role_rect)
                
                # Ligne décorative
                line_width = 300
                line_x = (self.screen_width - line_width) // 2
                pygame.draw.line(self.screen, credit_data["color"],
                               (line_x, credit_center_y + 55),
                               (line_x + line_width, credit_center_y + 55), 1)
        
        # Retourner la position du dernier crédit
        return y_offset + len(CREDITS_DATA) * espacement
    
    def draw_particles(self):
        """Met à jour et dessine les particules"""
        for p in self.particles[:]:
            p.update()
            p.draw(self.screen)
            if p.life <= 0:
                self.particles.remove(p)
    
    def draw_info(self):
        """Dessine les informations de contrôle"""
        info_texts = [
            "SPACE : Accelerer",
            "ESC : Quitter",
            "CLIC : Explosion"
        ]
        
        y_start = self.screen_height - 100
        for i, text in enumerate(info_texts):
            info_surf = Police.info.render(text, True, Couleur.GRIS_CLAIR)
            info_rect = info_surf.get_rect(bottomright=(self.screen_width - 30, y_start + i * 25))
            self.screen.blit(info_surf, info_rect)
    
    def draw(self):
        """Dessine tout le menu"""
        self.souris = pygame.mouse.get_pos()
        
        # Grille de fond (optionnel)
        # self.draw_grid_background()
        
        # Scanlines
        self.draw_scanlines()
        
        # Titre
        self.draw_titre()
        
        # Crédits défilants
        dernier_credit_y = self.draw_credits()
        
        # Vérifier si les crédits sont terminés
        if dernier_credit_y < -100:
            self.en_cours = False
        
        # Particules
        self.draw_particles()
        
        # Informations
        self.draw_info()
    
    def handle_events(self, event):
        """Gère les événements"""
        if event.type == pygame.QUIT:
            self.en_cours = False
            
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.en_cours = False
            elif event.key == pygame.K_SPACE:
                self.espace_enfonce = True
                
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                self.espace_enfonce = False
                
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Clic sur un crédit pour explosion
            y_offset = self.credit_y
            espacement = 100
            
            for idx, credit_data in enumerate(CREDITS_DATA):
                credit_center_y = y_offset + idx * espacement
                
                # Créer un rect approximatif pour le texte
                text_surf = Police.nom.render(credit_data["nom"], True, credit_data["color"])
                rect = text_surf.get_rect(center=(self.screen_width // 2, credit_center_y))
                
                if rect.collidepoint(event.pos):
                    self.creer_explosion(text_surf, rect, credit_data["color"])
                    break
    
    def update_scroll(self):
        """Met à jour le défilement des crédits"""
        vitesse = self.vitesse_acceleree if self.espace_enfonce else self.vitesse_defilement
        self.credit_y -= vitesse


# -------------------------------
# Fonction principale
# -------------------------------
def main(ecran):
    """
    Lance le menu des crédits
    
    Args:
        ecran: Surface Pygame
    """
    # Création du fond spatial animé
    stars, planet_manager, vaisseau_fond = create_space_background()
    
    # Création de l'instance du menu
    menu = MenuCredits()
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
        
        # Mise à jour du défilement
        menu.update_scroll()
        
        # Dessin du menu
        menu.draw()
        
        pygame.display.flip()
        horloge.tick(30)  # 30 FPS pour cohérence avec le menu principal
    
    # PAS de nettoyage pour garder les animations du menu principal
    # ShipAnimator.clear_list()
    # PlanetAnimator.clear_list()


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    main(screen)
    pygame.quit()
    sys.exit()