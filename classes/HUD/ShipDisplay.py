import pygame
from blazyck import ICONES_PATH
from classes.GlobalVar.GridVar import GridVar
from classes.GlobalVar.ScreenVar import ScreenVar
from classes.MotherShip import MotherShip
from classes.Player import Player
from classes.Point import Point
from classes.Ship import Ship
from classes.Turn import Turn
from classes.Shop import Shop

class ShipDisplay:
    """Affichage compact futuriste d'un vaisseau sélectionné."""

    def __init__(self):
        self.ship : Ship = None
        self.shop : Shop = None
        self.width = 300
        self.height = 90
        self.alpha = 255

        pygame.font.init()
        self.font_name = pygame.font.SysFont("consolas", 18, bold=True)
        self.font_small = pygame.font.SysFont("consolas", 12)
        self.font_normal = pygame.font.SysFont("consolas", 13)

        self.icons = self._load_icons()

    def reset(self):
        """Cache l'affichage et réinitialise le vaisseau."""
        self.ship = None
        self.alpha = 0

    def _load_icons(self):
        def load(name):
            try:
                img = pygame.image.load(f"{ICONES_PATH}/{name}.png").convert_alpha()
                return pygame.transform.scale(img, (16, 16))
            except Exception as e:
                print(f"[WARN] Impossible de charger l'icône {name}.png : {e}")
                return None
        return {
            "hp": load("hp"),
            "attack": load("attack"),
            "range": load("range"),
            "move": load("move"),
        }

    def draw(self, surface, x=None, y=None):
        if not self.ship:
            return
        
        if isinstance(self.ship, MotherShip):
            # Quand le vaisseau à afficher est le vaisseau mère, on affiche le shop à la place
            player_id : int = Turn.get_player_with_id(self.ship.joueur)
            self.shop.draw()
            return
        
        scale = ScreenVar.scale
        screen_width = ScreenVar.screen.get_width()
        screen_height = ScreenVar.screen.get_height()
        
        # Position en bas à gauche dans la zone du HUD
        bar_height = min(GridVar.offset_y, 100)
        shop_y = screen_height - bar_height
        
        # Calculer la largeur et hauteur basées sur le scale
        self.width = int(280 * scale)
        self.height = int(85 * scale)
        
        # Position: en bas à gauche avec une marge
        margin = int(15 * scale)
        x = margin
        y = shop_y + (bar_height - self.height) // 2
        
        # Créer une surface sans fond ni bordure
        panel = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        
        # Charger et afficher l'image du vaisseau à gauche
        ship_img = self.ship.animator.static_image
        ship_size = int(70 * scale)

        # Redimensionner l'image
        ship_img_scaled = pygame.transform.scale(ship_img, (ship_size, ship_size))

        # Blitter l'image du vaisseau
        panel.blit(ship_img_scaled, (5, (self.height - ship_size) // 2))

        
        # Décalage pour le texte (après l'image)
        text_start_x = ship_size + int(15 * scale)
        current_y = int(8 * scale)
        
        # Nom du vaisseau avec effet de glow
        txt_name = self.font_name.render(self.ship.__class__.__name__, True, (255, 220, 120))
        # Petit glow derrière le nom
        glow_name = self.font_name.render(self.ship.__class__.__name__, True, (255, 180, 60, 100))
        panel.blit(glow_name, (text_start_x + 1, current_y + 1))
        panel.blit(txt_name, (text_start_x, current_y))
        current_y += int(22 * scale)
        
        # Barre de PV avec icône
        icon_hp = self.icons["hp"]
        if icon_hp:
            icon_hp_scaled = pygame.transform.scale(icon_hp, (int(16 * scale), int(16 * scale)))
            icon_hp_scaled.set_alpha(self.alpha)
            panel.blit(icon_hp_scaled, (text_start_x, current_y - int(2 * scale)))
        
        bar_x = text_start_x + int(22 * scale)
        bar_y = current_y
        bar_w = self.width - bar_x - int(10 * scale)
        bar_h = int(10 * scale)
        
        # Fond de la barre semi-transparent
        pygame.draw.rect(panel, (30, 35, 50, 120), (bar_x, bar_y, bar_w, bar_h), border_radius=int(5 * scale))
        
        # Barre de vie avec gradient
        hp_ratio = self.ship.pv_actuel / self.ship.pv_max if self.ship.pv_max else 0
        if hp_ratio > 0.6:
            color = (100, 255, 100)
        elif hp_ratio > 0.3:
            color = (255, 200, 50)
        else:
            color = (255, 80, 80)
        
        fill_w = int(bar_w * hp_ratio)
        if fill_w > 0:
            pygame.draw.rect(panel, color, (bar_x, bar_y, fill_w, bar_h), border_radius=int(5 * scale))
        
        # Bordure de la barre
        pygame.draw.rect(panel, (100, 150, 200, 180), (bar_x, bar_y, bar_w, bar_h), int(1 * scale), border_radius=int(5 * scale))
        
        # Texte HP centré dans la barre
        txt_hp = self.font_small.render(f"{self.ship.pv_actuel}/{self.ship.pv_max}", True, (255, 255, 255))
        hp_text_x = bar_x + bar_w // 2 - txt_hp.get_width() // 2
        hp_text_y = bar_y + bar_h // 2 - txt_hp.get_height() // 2
        panel.blit(txt_hp, (hp_text_x, hp_text_y))
        
        current_y += int(18 * scale)
        
        # Statistiques sur une ligne horizontale
        stat_y = current_y
        stat_spacing = int(60 * scale)
        
        # Attaque
        icon_attack = self.icons["attack"]
        if icon_attack:
            icon_scaled = pygame.transform.scale(icon_attack, (int(14 * scale), int(14 * scale)))
            icon_scaled.set_alpha(self.alpha)
            panel.blit(icon_scaled, (text_start_x, stat_y))
        txt_attack = self.font_normal.render(str(self.ship.attaque), True, (255, 200, 200))
        panel.blit(txt_attack, (text_start_x + int(18 * scale), stat_y))
        
        # Portée
        icon_range = self.icons["range"]
        if icon_range:
            icon_scaled = pygame.transform.scale(icon_range, (int(14 * scale), int(14 * scale)))
            icon_scaled.set_alpha(self.alpha)
            panel.blit(icon_scaled, (text_start_x + stat_spacing, stat_y))
        txt_range = self.font_normal.render(f"{self.ship.port_attaque}/{self.ship.port_attaque_max}", True, (200, 220, 255))
        panel.blit(txt_range, (text_start_x + stat_spacing + int(18 * scale), stat_y))
        
        # Déplacement
        icon_move = self.icons["move"]
        if icon_move:
            icon_scaled = pygame.transform.scale(icon_move, (int(14 * scale), int(14 * scale)))
            icon_scaled.set_alpha(self.alpha)
            panel.blit(icon_scaled, (text_start_x + stat_spacing * 2, stat_y))
        txt_move = self.font_normal.render(f"{self.ship.port_deplacement}/{self.ship.port_deplacement_max}", True, (200, 255, 200))
        panel.blit(txt_move, (text_start_x + stat_spacing * 2 + int(18 * scale), stat_y))
        
        surface.blit(panel, (x, y))


# --- Test ---
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    ScreenVar(screen)
    GridVar()
    clock = pygame.time.Clock()
    running = True

    # Exemple de vaisseau fictif
    ship = MotherShip(taille=(4,5), tier=1, cordonner=Point(0,0), 
                      id=0, path="assets/img/ships/base", joueur=Player("Alice"))

    hud_ship = ShipDisplay()
    hud_ship.ship = ship

    while running:
        dt = clock.tick(60) / 1000.0
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False

        screen.fill((10, 10, 20))
        
        # Simuler le fond du HUD
        screen_width, screen_height = screen.get_size()
        bar_height = 100
        shop_y = screen_height - bar_height
        shop_bg = pygame.Surface((screen_width, bar_height), pygame.SRCALPHA)
        for i in range(bar_height):
            alpha = int(200 - (i / bar_height) * 50)
            color = (20 + i // 5, 25 + i // 5, 35 + i // 5, alpha)
            pygame.draw.line(shop_bg, color, (0, i), (screen_width, i))
        screen.blit(shop_bg, (0, shop_y))
        
        hud_ship.draw(screen)

        pygame.display.flip()

    pygame.quit()