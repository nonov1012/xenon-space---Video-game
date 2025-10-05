import pygame
from blazyck import OFFSET_X, SCREEN_WIDTH, SCREEN_HEIGHT
from classes.Player import Player
from classes.Point import Point
from classes.Turn import Turn
from classes.MotherShip import MotherShip

import math
import pygame

class BarDisplay:
    """
    Classe pour afficher la barre d'état d'un joueur.

    La barre d'état contient les informations suivantes :
    - Argent du joueur
    - Points de vie du vaisseau mère du joueur
    - Etat de la barre d'affichage (animé)
    """

    def __init__(self, player, left=True):
        """
        Constructeur de la classe BarDisplay.

        :param player: Le joueur lié à la barre d'affichage
        :param left: True si la barre doit être affichée à gauche de l'écran, False sinon
        """
        self.player = player
        self.left = left
        self.width = OFFSET_X // 2
        self.height = SCREEN_HEIGHT // 2
        self.margin = 30
        self.health_max = self.player.getMotherShip().pv_actuel
        self.health = self.player.getMotherShip().pv_actuel
        self.money = self.player.economie.solde

        pygame.font.init()
        self.font_small = pygame.font.SysFont("consolas", 16)
        self.font_medium = pygame.font.SysFont("consolas", 20)

        self.highlight = False
        self._time = 0  # temps interne pour animation

    def set_money(self, amount):
        """
        Met à jour l'argent du joueur.

        :param amount: Montant d'argent à mettre à jour
        """
        self.money = amount

    def set_health(self, value):
        """
        Met à jour les points de vie du vaisseau mère du joueur.

        :param value: Valeur à mettre à jour (entre 0 et health_max)
        """
        self.health = max(0, min(self.health_max, value))

    def update(self, dt=0):
        """
        Met à jour l'affichage de la barre d'état du joueur.

        :param dt: Temps écoulé depuis la dernière mise à jour (en secondes)
        """
        self.set_money(self.player.economie.solde)
        self.set_health(self.player.getMotherShip().pv_actuel if self.player.getMotherShip() else 0)
        # Incrémente le temps interne pour l'animation
        self._time += dt

    def draw(self, surface):
        """
        Dessine la barre d'affichage du joueur sur la surface passée en paramètre.

        :param surface: La surface sur laquelle dessiner la barre d'affichage
        """
        x = self.margin if self.left else SCREEN_WIDTH - self.width - self.margin
        y = SCREEN_HEIGHT // 2 - self.height // 2

        # --- Glow animé ---
        if self.highlight:
            pulse = 3 + 2 * math.sin(self._time * 4)  # pulse 2 à 5 px
            alpha = 100 + 50 * math.sin(self._time * 6)
            glow_color = (255, 255, 255, int(alpha)+50)
            for i in range(3):
                # Calcul des dimensions du glow
                rect_w = self.width + int(pulse) + i*2
                rect_h = self.height + int(pulse) + i*2
                glow_surf = pygame.Surface((rect_w, rect_h), pygame.SRCALPHA)
                # Dessin du glow
                pygame.draw.rect(glow_surf, glow_color, (0,0,rect_w,rect_h), width=2, border_radius=4)
                # Placement du glow sur la surface
                surface.blit(glow_surf, (x - rect_w//2 + self.width//2, y - rect_h//2 + self.height//2))

        # --- Cadre principal ---
        pygame.draw.rect(surface, (20, 25, 40), (x, y, self.width, self.height))
        pygame.draw.rect(surface, (80, 210, 255), (x, y, self.width, self.height), 2)

        # --- Barre de vie ---
        ratio = self.health / self.health_max
        life_height = int(self.height * ratio)
        life_y = y + (self.height - life_height)
        inner_rect = pygame.Rect(x + 4, life_y + 4, self.width - 8, life_height - 8)
        # Dessin de la barre de vie
        pygame.draw.rect(surface, (255, 80, 80), inner_rect)

        # --- Texte monnaie ---
        sym = self.font_medium.render("₿", True, (255, 200, 0))
        txt_money = self.font_medium.render(str(self.money), True, (255, 255, 255))
        space = 6
        total_width = sym.get_width() + space + txt_money.get_width()
        start_x = x + self.width // 2 - total_width // 2
        y_text = y - 30
        # Placement du texte sur la surface
        surface.blit(sym, (start_x, y_text))
        surface.blit(txt_money, (start_x + sym.get_width() + space, y_text))

        # --- Texte PV ---
        txt_hp = self.font_small.render(f"{self.health}/{self.health_max}", True, (255, 255, 255))
        # Placement du texte sur la surface
        surface.blit(txt_hp, (x + self.width // 2 - txt_hp.get_width() // 2, y + self.height + 10))

# --- Exemple d’utilisation ---
def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    running = True

    P1 = Player("Alice")
    P2 = Player("Bob")
    Turn.players = [P1, P2]
    P1.ships.append(MotherShip(pv_max=5000, attaque=11, port_attaque=10, port_deplacement=0, cout=0,
                      taille=(4,5), tier=1, cordonner=Point(0,0), 
                      id=0, path="assets/img/ships/base", joueur = Turn.players[0].id))
    P2.ships.append(MotherShip(pv_max=5000, attaque=11, port_attaque=10, port_deplacement=0, cout=0,
                      taille=(4,5), tier=1, cordonner=Point(0,0), 
                      id=1, path="assets/img/ships/base", joueur = Turn.players[1].id))

    hud_left = BarDisplay(left=True, player=Turn.players[0])
    hud_right = BarDisplay(left=False, player=Turn.players[1])
    hud_right.set_money(128)
    hud_right.set_health(620)

    while running:
        dt = clock.tick(60) / 1000.0
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False

        hud_left.update()
        hud_right.update()

        # affichage
        screen.fill((10, 10, 15))
        hud_left.draw(screen)
        hud_right.draw(screen)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
