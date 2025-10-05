import pygame
from blazyck import OFFSET_X, SCREEN_WIDTH, SCREEN_HEIGHT
import math

class BarDisplay:
    def __init__(self, player, left=True):
        self.player = player
        self.left = left
        self.width = OFFSET_X // 2
        self.height = SCREEN_HEIGHT // 2
        self.margin = 30

        # Vérifie si le joueur a une MotherShip
        mother_ship = self.player.getMotherShip()
        if mother_ship is not None:
            self.health_max = mother_ship.pv_actuel
            self.health = mother_ship.pv_actuel
        else:
            self.health_max = 0
            self.health = 0
            print(f"[DEBUG] {self.player.name} n'a pas de MotherShip !")

        self.money = self.player.economie.solde

        pygame.font.init()
        self.font_small = pygame.font.SysFont("consolas", 16)
        self.font_medium = pygame.font.SysFont("consolas", 20)

        self.highlight = False
        self._time = 0  # temps interne pour animation

    def set_money(self, amount):
        self.money = amount

    def set_health(self, value):
        self.health = max(0, min(self.health_max, value))

    def update(self, dt=0):
        self.set_money(self.player.economie.solde)
        mother_ship = self.player.getMotherShip()
        health = mother_ship.pv_actuel if mother_ship else 0
        self.set_health(health)
        self._time += dt

    def draw(self, surface):
        x = self.margin if self.left else SCREEN_WIDTH - self.width - self.margin
        y = SCREEN_HEIGHT // 2 - self.height // 2

        # --- Glow animé ---
        if self.highlight:
            pulse = 3 + 2 * math.sin(self._time * 4)  # pulse 2 à 5 px
            alpha = 100 + 50 * math.sin(self._time * 6)
            glow_color = (255, 255, 255, int(alpha)+50)
            for i in range(3):
                rect_w = self.width + int(pulse) + i*2
                rect_h = self.height + int(pulse) + i*2
                glow_surf = pygame.Surface((rect_w, rect_h), pygame.SRCALPHA)
                pygame.draw.rect(glow_surf, glow_color, (0,0,rect_w,rect_h), width=2, border_radius=4)
                surface.blit(glow_surf, (x - rect_w//2 + self.width//2, y - rect_h//2 + self.height//2))

        # --- Cadre principal ---
        pygame.draw.rect(surface, (20, 25, 40), (x, y, self.width, self.height))
        pygame.draw.rect(surface, (80, 210, 255), (x, y, self.width, self.height), 2)

        # --- Barre de vie ---
        ratio = self.health / self.health_max if self.health_max > 0 else 0
        life_height = int(self.height * ratio)
        life_y = y + (self.height - life_height)
        inner_rect = pygame.Rect(x + 4, life_y + 4, self.width - 8, life_height - 8)
        pygame.draw.rect(surface, (255, 80, 80), inner_rect)

        # --- Texte monnaie ---
        sym = self.font_medium.render("₿", True, (255, 200, 0))
        txt_money = self.font_medium.render(str(self.money), True, (255, 255, 255))
        space = 6
        total_width = sym.get_width() + space + txt_money.get_width()
        start_x = x + self.width // 2 - total_width // 2
        y_text = y - 30
        surface.blit(sym, (start_x, y_text))
        surface.blit(txt_money, (start_x + sym.get_width() + space, y_text))

        # --- Texte PV ---
        txt_hp = self.font_small.render(f"{self.health}/{self.health_max}", True, (255, 255, 255))
        surface.blit(txt_hp, (x + self.width // 2 - txt_hp.get_width() // 2, y + self.height + 10))
