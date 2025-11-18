import pygame
from blazyck import *
from menu.modifShips import SHIP_STATS

class Shop:
    def __init__(self, player, font, screen):
        self.player = player
        self.font = font
        self.screen = screen
        self.base_level = 1  # Niveau de base actuel
        
        # Image de la base
        self.base_image = self.load_image("assets/img/ships/shop/base.png")
        
        # Liste des vaisseaux disponibles
        self.ships = self.build_ships(SHIP_STATS)

        mothership_stat = SHIP_STATS["MotherShip"]
        
        # Améliorations de base
        self.base_upgrades = self.build_base_upgrades(mothership_stat)
        self.render = True

    def build_ships(self, data):
        ships = []
        tier = 1
        for name, info in data.items():
            if name == "MotherShip":
                continue  # On gère la base à part

            # Détermination du tier selon puissance (simple heuristique)
            cout = info.get("cout", 0)
            if cout >= 4000:
                tier = 4
            elif cout >= 2000:
                tier = 3
            elif cout >= 1000:
                tier = 2
            else:
                tier = 1

            # Nom du fichier image basé sur le nom
            image = self.load_image(f"assets/img/ships/shop/{name.lower()}.png")

            ships.append({
                "name": name,
                "price": cout,
                "tier": tier,
                "image": image
            })
        return ships
    
    def build_base_upgrades(self, mothership_data):
        upgrades = []
        for lvl, info in mothership_data.items():
            if lvl == 1:
                continue  # niveau de départ
            upgrades.append({
                "level": lvl,
                "price": info["cout"]
            })
        return upgrades
    
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
        if self.render:
            # --- SCALING ---
            icon_size_base = int(ICON_SIZE * SCALE)
            padding = int(CASE_PADDING * SCALE)
            margin = int(ICON_MARGIN * SCALE)
            bar_height = int(BAR_HEIGHT * SCALE)

            num_ships = len(self.ships)
            total_width = num_ships * (icon_size_base + 2 * padding) + (num_ships - 1) * margin
            start_x = (self.screen.get_width() - total_width) // 2
            y = self.screen.get_height() - bar_height + (bar_height - icon_size_base) // 2

            mouse_pos = pygame.mouse.get_pos()

            # === Vaisseaux ===
            for i, ship in enumerate(self.ships):
                x = start_x + i * (icon_size_base + 2 * padding + margin)

                case_rect = pygame.Rect(
                    x, y,
                    icon_size_base + 2 * padding,
                    icon_size_base + 2 * padding
                )

                hovered = case_rect.collidepoint(mouse_pos)

                # Ombre
                shadow_rect = case_rect.copy()
                shadow_rect.x += int(3 * SCALE)
                shadow_rect.y += int(3 * SCALE)
                pygame.draw.rect(self.screen, (20, 20, 20), shadow_rect, border_radius=int(8 * SCALE))

                color = (60, 60, 80) if not hovered else (90, 90, 120)
                pygame.draw.rect(self.screen, color, case_rect, border_radius=int(8 * SCALE))

                # Bordure
                border_width = int(2 * SCALE)
                pygame.draw.rect(
                    self.screen,
                    (100, 100, 140) if not hovered else (150, 200, 255),
                    case_rect,
                    border_radius=int(8 * SCALE),
                    width=border_width
                )

                # Icône + effet hover
                icon_size = icon_size_base + int(8 * SCALE) if hovered else icon_size_base
                icon_img = pygame.transform.scale(ship["image"], (icon_size, icon_size))

                icon_x = x + padding + (icon_size_base - icon_size) // 2
                icon_y = y + padding + (icon_size_base - icon_size) // 2

                # Glow
                if hovered:
                    glow_size = icon_size + int(8 * SCALE)
                    glow_surface = pygame.Surface((glow_size, glow_size), pygame.SRCALPHA)
                    pygame.draw.circle(
                        glow_surface,
                        (255, 255, 255, 30),
                        (glow_size // 2, glow_size // 2),
                        glow_size // 2
                    )
                    self.screen.blit(glow_surface, (icon_x - int(4 * SCALE), icon_y - int(4 * SCALE)))

                self.screen.blit(icon_img, (icon_x, icon_y))
                ship["rect"] = case_rect

                # Info hover
                if hovered:
                    info_w = int(250 * SCALE)
                    info_h = int(30 * SCALE)

                    info_bg = pygame.Surface((info_w, info_h), pygame.SRCALPHA)
                    pygame.draw.rect(info_bg, (0, 0, 0, 200), info_bg.get_rect(), border_radius=int(6 * SCALE))
                    pygame.draw.rect(info_bg, (255, 215, 0), info_bg.get_rect(), border_radius=int(6 * SCALE), width=int(2 * SCALE))

                    info_text = self.font.render(
                        f"{ship['name']} - {ship['price']} coins",
                        True,
                        (255, 255, 100)
                    )

                    text_rect = info_text.get_rect(center=(info_w // 2, info_h // 2))
                    info_bg.blit(info_text, text_rect)

                    bg_rect = info_bg.get_rect(center=(case_rect.centerx, case_rect.top - int(20 * SCALE)))
                    self.screen.blit(info_bg, bg_rect)

            # === Bloc base upgrade ===
            base_x = start_x + total_width + int(3 * margin)

            base_case = pygame.Rect(
                base_x, y,
                icon_size_base + 2 * padding,
                icon_size_base + 2 * padding
            )

            hovered = base_case.collidepoint(mouse_pos)

            # Bordure spéciale
            if self.base_level >= 4:
                gradient_colors = [(255, 215, 0), (255, 140, 0), (255, 69, 0)]
                for i, col in enumerate(gradient_colors):
                    offset = int(i * 2 * SCALE)
                    inner = base_case.inflate(-offset, -offset)
                    pygame.draw.rect(self.screen, col, inner, border_radius=int(8 * SCALE), width=int(2 * SCALE))
                color = (40, 40, 40)
            else:
                color = (30, 30, 50) if not hovered else (50, 50, 80)

            pygame.draw.rect(self.screen, color, base_case, border_radius=int(8 * SCALE))

            border_color = self.get_base_color_filter() if self.base_level < 4 else (255, 215, 0)
            if hovered:
                border_color = tuple(min(c + 50, 255) for c in border_color)

            pygame.draw.rect(self.screen, border_color, base_case, border_radius=int(8 * SCALE), width=int(3 * SCALE))

            # Icône base
            icon_size = icon_size_base + int(8 * SCALE) if hovered else icon_size_base
            base_icon = pygame.transform.scale(self.base_image, (icon_size, icon_size))

            icon_x = base_x + padding + (icon_size_base - icon_size) // 2
            icon_y = y + padding + (icon_size_base - icon_size) // 2

            # Glow
            if hovered:
                glow_size = icon_size + int(12 * SCALE)
                glow_surface = pygame.Surface((glow_size, glow_size), pygame.SRCALPHA)
                color_filter = self.get_base_color_filter()

                for i in range(3):
                    radius = (icon_size // 2) + int(6 * SCALE) - int(i * 2 * SCALE)
                    alpha = 30 - i * 10
                    pygame.draw.circle(
                        glow_surface,
                        (*color_filter, alpha),
                        (glow_size // 2, glow_size // 2),
                        radius
                    )

                self.screen.blit(
                    glow_surface,
                    (icon_x - int(6 * SCALE), icon_y - int(6 * SCALE))
                )

            self.screen.blit(base_icon, (icon_x, icon_y))

            # Étoiles
            star_r = int(4 * SCALE)
            for i, (sx, sy) in enumerate([
                (icon_x + icon_size * 0.2, icon_y + icon_size * 0.2),
                (icon_x + icon_size * 0.8, icon_y + icon_size * 0.2),
                (icon_x + icon_size * 0.2, icon_y + icon_size * 0.8),
                (icon_x + icon_size * 0.8, icon_y + icon_size * 0.8),
            ]):
                if i >= self.base_level:
                    break

                pygame.draw.circle(self.screen, (255, 255, 100), (int(sx), int(sy)), star_r)
                pygame.draw.circle(self.screen, (255, 255, 255), (int(sx), int(sy)), star_r // 2)

            self.base_rect = base_case

            # Info base hover
            if hovered:
                info_w = int(300 * SCALE)
                info_h = int(35 * SCALE)

                info_bg = pygame.Surface((info_w, info_h), pygame.SRCALPHA)
                pygame.draw.rect(info_bg, (0, 0, 0, 200), info_bg.get_rect(), border_radius=int(8 * SCALE))

                if self.base_level >= 4:
                    pygame.draw.rect(info_bg, (255, 215, 0), info_bg.get_rect(), border_radius=int(8 * SCALE), width=int(2 * SCALE))
                    info_text = self.font.render("BASE NIVEAU MAX", True, (255, 215, 0))
                else:
                    next_up = self.base_upgrades[self.base_level - 1]
                    pygame.draw.rect(info_bg, (100, 200, 255), info_bg.get_rect(), border_radius=int(8 * SCALE), width=int(2 * SCALE))
                    info_text = self.font.render(
                        f"Base Nv.{self.base_level} -> Nv.{next_up['level']} - {next_up['price']} coins",
                        True,
                        (150, 220, 255)
                    )

                text_rect = info_text.get_rect(center=(info_w // 2, info_h // 2))
                info_bg.blit(info_text, text_rect)

                bg_rect = info_bg.get_rect(center=(base_case.centerx, base_case.top - int(22 * SCALE)))
                self.screen.blit(info_bg, bg_rect)

    def handle_click(self, pos, mothership_actuel):
        """Gère les clics sur les boutons du shop et retourne le type de vaisseau acheté ou 'base_upgrade'"""
        if self.render:
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
    
if __name__ == "__main__":
    pygame.init()

    # Créer la fenêtre à la taille de l'écran
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)

    font = pygame.font.SysFont("Arial", int(20 * SCALE))   # police scalable
    shop = Shop(None, font, screen)
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                result = shop.handle_click(pos, None)
                if result:
                    print(f"Achat effectué: {result}")
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    shop.render = not shop.render

        screen.fill((0, 0, 0))
        shop.draw()
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
