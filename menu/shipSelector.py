# ShipSelector.py
import pygame
from menu.modifShips import vaisseaux_sliders

class ShipSelector:
    def __init__(self, ecran, police):
        self.ecran = ecran
        self.police = police
        self.types_vaisseaux = list(vaisseaux_sliders.keys())
        self.actif = self.types_vaisseaux[0]
        self.icones = self.load_icons()
        self.slider_actif = None
        self.largeur_slider = 300
        self.hauteur_slider = 15

    def load_icons(self):
        icones = {}
        for ship in self.types_vaisseaux:
            path = f"assets/img/ships/{ship.lower()}.png"
            img = pygame.image.load(path).convert_alpha()
            icones[ship] = pygame.transform.scale(img, (80, 80))
        return icones

    def draw(self, souris, clic):
        # Icône en haut à gauche
        self.ecran.blit(self.icones[self.actif], (50, 50))

        # Sliders pour le vaisseau actif
        x_start = 150
        y_start = 60
        decalage_y = 0

        for param, valeur in vaisseaux_sliders[self.actif].items():
            # Texte du paramètre
            texte_param = self.police.render(f"{param}: {valeur}", True, (255, 255, 255))
            self.ecran.blit(texte_param, (x_start, y_start + decalage_y))

            # Slider
            rect_slider = pygame.Rect(x_start, y_start + 25 + decalage_y, self.largeur_slider, self.hauteur_slider)
            pygame.draw.rect(self.ecran, (100, 100, 100), rect_slider, border_radius=8)

            # Barre de progression
            min_val, max_val = 0, valeur * 2  # exemple si tu veux limiter
            rel_pos = (valeur - min_val) / (max_val - min_val) if max_val > min_val else 1
            rect_prog = pygame.Rect(x_start, y_start + 25 + decalage_y, int(rel_pos * self.largeur_slider), self.hauteur_slider)
            pygame.draw.rect(self.ecran, (0, 200, 100), rect_prog, border_radius=8)

            # Curseur
            curseur_x = int(x_start + rel_pos * self.largeur_slider)
            rect_curseur = pygame.Rect(curseur_x - 8, y_start + 20 + decalage_y, 16, self.hauteur_slider + 10)
            pygame.draw.ellipse(self.ecran, (0, 150, 80), rect_curseur)

            # Slider actif
            if clic and rect_curseur.collidepoint(souris):
                self.slider_actif = param

            if self.slider_actif and clic:
                rel_x = max(0, min(self.largeur_slider, souris[0] - x_start))
                vaisseaux_sliders[self.actif][self.slider_actif] = int(min_val + (rel_x / self.largeur_slider) * (max_val - min_val))

            decalage_y += 60

        if not clic:
            self.slider_actif = None

    def handle_click(self, pos):
        icone_rect = pygame.Rect(50, 50, 80, 80)
        if icone_rect.collidepoint(pos):
            index = (self.types_vaisseaux.index(self.actif) + 1) % len(self.types_vaisseaux)
            self.actif = self.types_vaisseaux[index]
