import pygame

class Vaisseau:
    def __init__(self, x, y, orientation="vertical"):
        self.x = x
        self.y = y
        self.orientation = orientation
        self.chemin = []
        self.selectionne = False  # pour savoir si le vaisseau est sélectionné

    @property
    def largeur(self):
        """Retourne la largeur du vaisseau selon son orientation."""
        return 2 if self.orientation == "vertical" else 3

    @property
    def hauteur(self):
        """Retourne la hauteur du vaisseau selon son orientation."""
        return 3 if self.orientation == "vertical" else 2

    def dessiner(self, surface):
        """Dessine le vaisseau sur l'écran, avec l'ancre en orange."""
        rect = pygame.Rect(self.x*40, self.y*40,
                           self.largeur*40, self.hauteur*40)
        pygame.draw.rect(surface, (0,0,255), rect)
        rect_ancre = pygame.Rect(self.x*40, self.y*40, 40, 40)
        pygame.draw.rect(surface, (255,150,0), rect_ancre)

    def pivoter(self, gestion_deplacement):
        """
        Pivote le vaisseau entre vertical et horizontal.
        La rotation ne se fait que si elle ne rentre pas en collision.
        """
        orientation_sauvee = self.orientation
        self.orientation = "horizontal" if self.orientation == "vertical" else "vertical"
                # Vérifie collision avec obstacles
        if not gestion_deplacement.peut_aller(self.x, self.y):
            self.orientation = orientation_sauvee  # revient en arrière si impossible
        
    def mettre_a_jour_position(self, nx, ny):
        """Met à jour la position du vaisseau."""
        self.x = nx
        self.y = ny
