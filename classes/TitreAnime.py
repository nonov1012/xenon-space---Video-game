import pygame
import numpy as np

class TitreAnime:
    def __init__(self, texte, font, pos, couleur_haut, couleur_bas):
        self.font = font
        self.texte = texte
        self.pos = pos
        self.couleur_haut = couleur_haut
        self.couleur_bas = couleur_bas
        self.base = self.font.render(self.texte, True, (255,255,255))
        self.rect = self.base.get_rect(center=self.pos)
        self.offset = -100  # Position de départ (plus à gauche pour la diagonale)
        self.largeur_lumiere = 80  # Largeur de la bande lumineuse
        
    def gradient_text(self):
        width, height = self.base.get_size()
        gradient = pygame.Surface((width, height), pygame.SRCALPHA)
        for y in range(height):
            ratio = y / height
            r = int(self.couleur_haut[0]*(1-ratio) + self.couleur_bas[0]*ratio)
            g = int(self.couleur_haut[1]*(1-ratio) + self.couleur_bas[1]*ratio)
            b = int(self.couleur_haut[2]*(1-ratio) + self.couleur_bas[2]*ratio)
            pygame.draw.line(gradient, (r,g,b), (0,y), (width,y))
        gradient.blit(self.base, (0,0), special_flags=pygame.BLEND_RGBA_MULT)
        return gradient
    
    def draw(self, surface):
        texte_grad = self.gradient_text()
        width, height = texte_grad.get_size()
        
        # Masque alpha pour la lumière
        alpha_mask = pygame.surfarray.pixels_alpha(texte_grad).copy()
        
        # Overlay lumineux diagonal
        overlay = pygame.Surface(texte_grad.get_size(), pygame.SRCALPHA)
        overlay.fill((0,0,0,0))
        
        # Créer la bande diagonale
        # Points pour définir la diagonale (de haut-gauche vers bas-droite)
        points = []
        
        # Position x de la bande lumineuse (se déplace de gauche à droite)
        x_start = self.offset
        
        # Définir les 4 coins de la bande diagonale
        # Coin haut-gauche
        points.append((x_start, 0))
        # Coin haut-droite
        points.append((x_start + self.largeur_lumiere, 0))
        # Coin bas-droite (décalé vers la droite pour l'effet diagonal)
        points.append((x_start + self.largeur_lumiere + height * 0.5, height))
        # Coin bas-gauche (décalé vers la droite pour l'effet diagonal)
        points.append((x_start + height * 0.5, height))
        
        # Dessiner le polygone diagonal
        if len(points) >= 3:  # Vérifier qu'on a assez de points
            pygame.draw.polygon(overlay, (255,255,255,180), points)
        
        # Appliquer le masque alpha du texte pour limiter la lumière aux lettres
        alpha_overlay = pygame.surfarray.pixels_alpha(overlay)
        alpha_overlay[:] = (alpha_overlay * (alpha_mask / 255)).astype(np.uint8)
        del alpha_overlay
        
        # Ajouter l'overlay lumineux au texte dégradé
        texte_grad.blit(overlay, (0,0), special_flags=pygame.BLEND_RGBA_ADD)
        
        # Afficher sur l'écran
        surface.blit(texte_grad, self.rect)
        
        # Déplacer la lumière diagonale
        self.offset += 4  # Vitesse de déplacement
        
        # Réinitialiser quand la lumière sort complètement à droite
        if self.offset > width + height * 0.5:
            self.offset = -self.largeur_lumiere - height * 0.5