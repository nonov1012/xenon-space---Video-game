import pygame
from blazyck import *
from classes.HUD import HUD

class Shop:
    def __init__(self, player, font, screen):
        self.player = player  # Player doit maintenant avoir un attribut self.economie
        self.font = font
        self.screen = screen
        self.base_level = 1  # Niveau de base actuel
        
        # Image de la base
        self.base_image = self.load_image("assets/img/ships/shop/base.png")
        
        # Liste des vaisseaux disponibles
        self.ships = [
            {"name": "Petit", "price": 325, "tier": 1, "image": self.load_image("assets/img/ships/shop/petit.png")},
            {"name": "Moyen", "price": 650, "tier": 3, "image": self.load_image("assets/img/ships/shop/moyen.png")},
            {"name": "Grand", "price": 1050, "tier": 4, "image": self.load_image("assets/img/ships/shop/grand.png")},
            {"name": "Foreuse", "price": 400, "tier": 1, "image": self.load_image("assets/img/ships/shop/foreuse.png")},
            {"name": "Transporteur", "price": 500, "tier": 2, "image": self.load_image("assets/img/ships/shop/transporteur.png")}
        ]

        
        # Améliorations de base
        self.base_upgrades = [
            {"level": 2, "price": 1000},
            {"level": 3, "price": 2000},
            {"level": 4, "price": 6000}
        ]
    
    def load_image(self, path, size=(ICON_SIZE, ICON_SIZE)):
        try:
            img = pygame.image.load(path).convert_alpha()
            return pygame.transform.scale(img, size)
        except pygame.error:
            placeholder = pygame.Surface(size, pygame.SRCALPHA)
            placeholder.fill((150, 150, 150))
            return placeholder
    
    def buy_ship(self, ship, mothership_actuel):
        """Achète un vaisseau et retourne son nom si l'achat réussit"""
        if mothership_actuel.tier >= ship["tier"] :
            if self.player.economie.retirer(ship["price"]):
                return ship["name"]
            else:
                return None


    def upgrade_base(self):
        """Améliore la base si possible"""
        if self.base_level != 4:
            # Trouve le prix de l'amélioration suivante
            next_upgrade = self.base_upgrades[self.base_level - 1]
            
            if self.player.economie.retirer(next_upgrade["price"]):
                self.base_level = next_upgrade["level"]
                return True
            else:
                return False
        else:
            return False
    
    def get_base_color_filter(self):
        """Retourne la couleur de bordure selon le niveau de base"""
        if self.base_level == 1:
            return (80, 150, 200)  # Bleu
        elif self.base_level == 2:
            return (150, 100, 200)  # Violet
        elif self.base_level == 3:
            return (200, 150, 50)  # Or
        else:  # Niveau 4
            return (50, 200, 150)  # Turquoise
    
    def draw(self):
        # Dessiner le cadre du shop
        shop_y = self.screen.get_height() - BAR_HEIGHT
        shop_width = self.screen.get_width()
        
        # Fond du shop avec dégradé
        shop_bg = pygame.Surface((shop_width, BAR_HEIGHT), pygame.SRCALPHA)
        for i in range(BAR_HEIGHT):
            alpha = int(200 - (i / BAR_HEIGHT) * 50)
            color = (20 + i // 5, 25 + i // 5, 35 + i // 5, alpha)
            pygame.draw.line(shop_bg, color, (0, i), (shop_width, i))
        self.screen.blit(shop_bg, (0, shop_y))
        
        # Bordure supérieure du shop
        pygame.draw.line(self.screen, (100, 150, 200), (0, shop_y), (shop_width, shop_y), 3)
        pygame.draw.line(self.screen, (150, 200, 255), (0, shop_y + 1), (shop_width, shop_y + 1), 1)
        
        # Coins décoratifs
        corner_size = 20
        # Coin supérieur gauche
        pygame.draw.line(self.screen, (150, 200, 255), (0, shop_y), (corner_size, shop_y), 4)
        pygame.draw.line(self.screen, (150, 200, 255), (0, shop_y), (0, shop_y + corner_size), 4)
        
        # Coin supérieur droit
        pygame.draw.line(self.screen, (150, 200, 255), (shop_width - corner_size, shop_y), (shop_width, shop_y), 4)
        pygame.draw.line(self.screen, (150, 200, 255), (shop_width, shop_y), (shop_width, shop_y + corner_size), 4)
        
        # Motifs décoratifs sur les côtés
        for i in range(3):
            offset = 30 + i * 40
            pygame.draw.circle(self.screen, (100, 150, 200, 100), (offset, shop_y + BAR_HEIGHT // 2), 3)
            pygame.draw.circle(self.screen, (100, 150, 200, 100), (shop_width - offset, shop_y + BAR_HEIGHT // 2), 3)
        
        num_ships = len(self.ships)
        total_width = num_ships * (ICON_SIZE + 2 * CASE_PADDING) + (num_ships - 1) * ICON_MARGIN
        start_x = (self.screen.get_width() - total_width) // 2
        y = self.screen.get_height() - BAR_HEIGHT + (BAR_HEIGHT - ICON_SIZE) // 2
        
        mouse_pos = pygame.mouse.get_pos()
        
        # Dessiner les vaisseaux
        for i, ship in enumerate(self.ships):
            x = start_x + i * (ICON_SIZE + 2 * CASE_PADDING + ICON_MARGIN)
            case_rect = pygame.Rect(x, y, ICON_SIZE + 2 * CASE_PADDING, ICON_SIZE + 2 * CASE_PADDING)
            
            hovered = case_rect.collidepoint(mouse_pos)
            
            # Fond avec effet de profondeur
            shadow_rect = case_rect.copy()
            shadow_rect.x += 3
            shadow_rect.y += 3
            pygame.draw.rect(self.screen, (20, 20, 20), shadow_rect, border_radius=8)
            
            color = (60, 60, 80) if not hovered else (90, 90, 120)
            pygame.draw.rect(self.screen, color, case_rect, border_radius=8)
            
            # Bordure avec effet hover
            border_color = (100, 100, 140) if not hovered else (150, 200, 255)
            pygame.draw.rect(self.screen, border_color, case_rect, border_radius=8, width=2)
            
            # Dessin de l'icône avec glow effect au survol
            icon_size = ICON_SIZE + 8 if hovered else ICON_SIZE
            icon_img = pygame.transform.scale(ship["image"], (icon_size, icon_size))
            icon_x = x + CASE_PADDING + (ICON_SIZE - icon_size) // 2
            icon_y = y + CASE_PADDING + (ICON_SIZE - icon_size) // 2
            
            # Effet de lueur au survol
            if hovered:
                glow_surface = pygame.Surface((icon_size + 8, icon_size + 8), pygame.SRCALPHA)
                pygame.draw.circle(glow_surface, (255, 255, 255, 30), 
                                 (icon_size // 2 + 4, icon_size // 2 + 4), icon_size // 2 + 4)
                self.screen.blit(glow_surface, (icon_x - 4, icon_y - 4))
            
            self.screen.blit(icon_img, (icon_x, icon_y))
            
            ship["rect"] = case_rect
            
            # Info survol avec fond stylisé
            if hovered:
                info_bg = pygame.Surface((250, 30), pygame.SRCALPHA)
                pygame.draw.rect(info_bg, (0, 0, 0, 200), info_bg.get_rect(), border_radius=6)
                pygame.draw.rect(info_bg, (255, 215, 0), info_bg.get_rect(), border_radius=6, width=2)
                
                info_text = self.font.render(f"{ship['name']} - {ship['price']} coins", True, (255, 255, 100))
                text_rect = info_text.get_rect(center=(125, 15))
                info_bg.blit(info_text, text_rect)
                
                bg_rect = info_bg.get_rect(center=(case_rect.centerx, case_rect.top - 20))
                self.screen.blit(info_bg, bg_rect)
        
        # Dessiner l'amélioration de base à droite, décalée
        base_x = start_x + total_width + ICON_MARGIN * 3
        case_rect = pygame.Rect(base_x, y, ICON_SIZE + 2 * CASE_PADDING, ICON_SIZE + 2 * CASE_PADDING)
        hovered = case_rect.collidepoint(mouse_pos)
        
        # Bordure avec effet de brillance
        if self.base_level >= 4:
            # Effet arc-en-ciel pour niveau max
            gradient_colors = [(255, 215, 0), (255, 140, 0), (255, 69, 0)]
            for i, col in enumerate(gradient_colors):
                offset = i * 2
                inner_rect = case_rect.inflate(-offset, -offset)
                pygame.draw.rect(self.screen, col, inner_rect, border_radius=8, width=2)
            color = (40, 40, 40)
        else:
            color = (30, 30, 50) if not hovered else (50, 50, 80)
        
        # Fond avec dégradé simulé
        pygame.draw.rect(self.screen, color, case_rect, border_radius=8)
        
        # Bordure lumineuse
        border_color = self.get_base_color_filter() if self.base_level < 4 else (255, 215, 0)
        if hovered:
            border_color = tuple(min(c + 50, 255) for c in border_color)
        pygame.draw.rect(self.screen, border_color, case_rect, border_radius=8, width=3)
        
        # Dessin de l'icône de base
        icon_size = ICON_SIZE + 8 if hovered else ICON_SIZE
        
        # Redimensionner l'image de base
        base_icon = pygame.transform.scale(self.base_image, (icon_size, icon_size))
        
        # Effet de lueur au survol
        if hovered:
            glow_surface = pygame.Surface((icon_size + 12, icon_size + 12), pygame.SRCALPHA)
            color_filter = self.get_base_color_filter()
            for i in range(3):
                radius = (icon_size // 2) + 6 - i * 2
                alpha = 30 - i * 10
                pygame.draw.circle(glow_surface, (*color_filter, alpha), 
                                 (icon_size // 2 + 6, icon_size // 2 + 6), radius)
            self.screen.blit(glow_surface, (base_x + CASE_PADDING - 6 + (ICON_SIZE - icon_size) // 2, 
                                           y + CASE_PADDING - 6 + (ICON_SIZE - icon_size) // 2))
        
        icon_x = base_x + CASE_PADDING + (ICON_SIZE - icon_size) // 2
        icon_y = y + CASE_PADDING + (ICON_SIZE - icon_size) // 2
        self.screen.blit(base_icon, (icon_x, icon_y))
        
        # Ajouter des étoiles/points selon le niveau par-dessus l'image
        star_color = (255, 255, 100) if self.base_level < 4 else (255, 215, 0)
        star_positions = [
            (icon_x + icon_size * 0.2, icon_y + icon_size * 0.2),
            (icon_x + icon_size * 0.8, icon_y + icon_size * 0.2),
            (icon_x + icon_size * 0.2, icon_y + icon_size * 0.8),
            (icon_x + icon_size * 0.8, icon_y + icon_size * 0.8)
        ]
        
        for i in range(min(self.base_level, 4)):
            star_x, star_y = star_positions[i]
            pygame.draw.circle(self.screen, star_color, (int(star_x), int(star_y)), 4)
            pygame.draw.circle(self.screen, (255, 255, 255), (int(star_x), int(star_y)), 2)
        
        self.base_rect = case_rect
        
        # Info survol
        if hovered:
            info_bg = pygame.Surface((300, 35), pygame.SRCALPHA)
            pygame.draw.rect(info_bg, (0, 0, 0, 200), info_bg.get_rect(), border_radius=8)
            
            if self.base_level >= 4:
                pygame.draw.rect(info_bg, (255, 215, 0), info_bg.get_rect(), border_radius=8, width=2)
                info_text = self.font.render("BASE NIVEAU MAX", True, (255, 215, 0))
            else:
                next_upgrade = self.base_upgrades[self.base_level - 1]
                pygame.draw.rect(info_bg, (100, 200, 255), info_bg.get_rect(), border_radius=8, width=2)
                info_text = self.font.render(f"Base Nv.{self.base_level} -> Nv.{next_upgrade['level']} - {next_upgrade['price']} coins", 
                                            True, (150, 220, 255))
            
            text_rect = info_text.get_rect(center=(150, 17))
            info_bg.blit(info_text, text_rect)
            bg_rect = info_bg.get_rect(center=(case_rect.centerx, case_rect.top - 22))
            self.screen.blit(info_bg, bg_rect)
    
    def handle_click(self, pos, mothership_actuel):
        """Gère les clics sur les boutons du shop et retourne le type de vaisseau acheté ou 'base_upgrade'"""
        # Vérifier clic sur amélioration de base
        if hasattr(self, 'base_rect') and self.base_rect.collidepoint(pos):
            if self.upgrade_base():
                return "base_upgrade"
            return None
        
        # Vérifier clic sur vaisseaux
        for ship in self.ships:
            if "rect" in ship and ship["rect"].collidepoint(pos):
                return self.buy_ship(ship, mothership_actuel)
        
        return None