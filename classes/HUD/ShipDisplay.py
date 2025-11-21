import pygame
from blazyck import ICONES_PATH
from classes.GlobalVar.GridVar import GridVar
from classes.MotherShip import MotherShip
from classes.Player import Player
from classes.Point import Point
from classes.Ship import Ship
from classes.Turn import Turn
from classes.Shop import Shop

class ShipDisplay:
    """Affichage compact futuriste d’un vaisseau sélectionné."""

    def __init__(self):
        self.ship : Ship = None
        self.shop : Shop = None
        self.width = GridVar.offset_x
        self.height = 140
        self.alpha = 255

        pygame.font.init()
        self.font_name = pygame.font.SysFont("consolas", 16, bold=True)
        self.font_small = pygame.font.SysFont("consolas", 14)
        self.font_normal = pygame.font.SysFont("consolas", 14)

        self.icons = self._load_icons()

    def reset(self):
        """Cache l'affichage et réinitialise le vaisseau."""
        self.ship = None
        self.alpha = 0

    def _load_icons(self):
        def load(name):
            try:
                img = pygame.image.load(f"{ICONES_PATH}/{name}.png").convert_alpha()
                return pygame.transform.scale(img, (18, 18))
            except Exception as e:
                print(f"[WARN] Impossible de charger l'icône {name}.png : {e}")
                return None
        return {
            "hp": load("hp"),
            "attack": load("attack"),
            "range": load("range"),
            "move": load("move"),
        }

    def draw(self, surface, x, y):
        if not self.ship:
            return
        if isinstance(self.ship, MotherShip):
            # Quand le vaisseau à afficher est le vaisseau mère, on affiche le shop à la place
            from classes.Shop import Shop
            player_id : int = Turn.get_player_with_id(self.ship.joueur)
            self.shop.draw()
            return
        panel = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.rect(panel, (15, 20, 35, 200), (0, 0, self.width, self.height))
        pygame.draw.rect(panel, (80, 210, 255, 255), (0, 0, self.width, self.height), 2)

        current_y = 5
        # Nom
        txt_name = self.font_name.render(self.ship.__class__.__name__, True, (255, 200, 100))
        panel.blit(txt_name, (10, current_y))
        current_y += 28

        # PV avec icône
        icon_hp = self.icons["hp"]
        if icon_hp:
            icon_hp.set_alpha(self.alpha)
            panel.blit(icon_hp, (10, current_y))
        bar_x, bar_y, bar_w, bar_h = 35, current_y + 2, self.width - 50, 12
        pygame.draw.rect(panel, (40, 40, 60), (bar_x, bar_y, bar_w, bar_h))
        hp_ratio = self.ship.pv_actuel / self.ship.pv_max if self.ship.pv_max else 0
        color = (100, 255, 100) if hp_ratio > 0.6 else (255, 200, 50) if hp_ratio > 0.3 else (255, 80, 80)
        pygame.draw.rect(panel, color, (bar_x, bar_y, int(bar_w * hp_ratio), bar_h))
        pygame.draw.rect(panel, (80, 210, 255), (bar_x, bar_y, bar_w, bar_h), 1)
        txt_hp = self.font_small.render(f"{self.ship.pv_actuel}/{self.ship.pv_max}", True, (255, 255, 255))
        panel.blit(txt_hp, (bar_x + bar_w // 2 - txt_hp.get_width() // 2, bar_y + bar_h + 2))
        current_y += 28

        # Attaque
        icon_attack = self.icons["attack"]
        if icon_attack:
            icon_attack.set_alpha(self.alpha)
            panel.blit(icon_attack, (10, current_y))
        txt_attack = self.font_normal.render(str(self.ship.attaque), True, (255, 255, 255))
        panel.blit(txt_attack, (35, current_y + 1))
        current_y += 26

        # Portée
        icon_range = self.icons["range"]
        if icon_range:
            icon_range.set_alpha(self.alpha)
            panel.blit(icon_range, (10, current_y))
        txt_range = self.font_normal.render(f"{self.ship.port_attaque}/{self.ship.port_attaque_max}", True, (255, 255, 255))
        panel.blit(txt_range, (35, current_y + 1))
        current_y += 26

        # Déplacement
        icon_move = self.icons["move"]
        if icon_move:
            icon_move.set_alpha(self.alpha)
            panel.blit(icon_move, (10, current_y))
        txt_move = self.font_normal.render(f"{self.ship.port_deplacement}/{self.ship.port_deplacement_max}", True, (255, 255, 255))
        panel.blit(txt_move, (35, current_y + 1))

        surface.blit(panel, (x, y))


# --- Test ---
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    running = True

    # Exemple de vaisseau fictif
    ship = MotherShip(taille=(4,5), tier=1, cordonner=Point(0,0), 
                      id=0, path="assets/img/ships/base", joueur = Player("Alice"))

    hud_ship = ShipDisplay()
    hud_ship.set_ship(ship)

    while running:
        dt = clock.tick(60) / 1000.0
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False

        screen.fill((10, 10, 20))
        hud_ship.draw(screen, 10, 10)

        pygame.display.flip()

    pygame.quit()