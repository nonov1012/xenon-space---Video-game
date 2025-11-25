import pygame
from classes.HUD.BarDisplay import BarDisplay
from classes.HUD.TurnDisplay import TurnDisplay
from classes.MotherShip import MotherShip
from classes.Player import Player
from classes.Point import Point
from classes.Turn import Turn
from classes.HUD.ShipDisplay import ShipDisplay
from classes.Shop import Shop
from classes.GlobalVar.ScreenVar import ScreenVar
from classes.GlobalVar.GridVar import GridVar
from blazyck import *


class HUD:
    left_bar: BarDisplay = None
    right_bar: BarDisplay = None
    turn_display: TurnDisplay = None
    ship_display: ShipDisplay = None
    
    # Boutons toggle
    show_grid_button = None
    show_colors_button = None
    show_grid = False
    show_colors = False
    
    # Tooltip
    tooltip_text = None
    tooltip_pos = None

    @classmethod
    def init(cls):
        cls.left_bar = BarDisplay(Turn.players[0], left=True)
        cls.left_bar.highlight = True   
        cls.right_bar = BarDisplay(Turn.players[1], left=False)
        cls.turn_display = TurnDisplay()
        cls.ship_display = ShipDisplay()
        cls.render_bottom_background = True
        
        # Initialiser les boutons toggle
        cls.init_toggle_buttons()

    @classmethod
    def init_toggle_buttons(cls):
        """Initialise les boutons de toggle pour la grille et les couleurs."""
        screen_width = ScreenVar.screen.get_width()
        screen_height = ScreenVar.screen.get_height()
        scale = ScreenVar.scale
        
        button_size = int(45 * scale)
        margin = int(15 * scale)
        bottom_offset = int(15 * scale)
        right_offset = int(15 * scale)
        
        # Position en bas à droite
        x_pos_2 = screen_width - button_size - right_offset
        x_pos_1 = x_pos_2 - button_size - margin
        y_pos = screen_height - button_size - bottom_offset
        
        cls.show_grid_button = {
            'rect': pygame.Rect(x_pos_1, y_pos, button_size, button_size),
            'active': cls.show_grid,
            'tooltip': 'Afficher/Masquer la grille',
            'icon': 'grid'
        }
        
        cls.show_colors_button = {
            'rect': pygame.Rect(x_pos_2, y_pos, button_size, button_size),
            'active': cls.show_colors,
            'tooltip': 'Afficher/Masquer les couleurs',
            'icon': 'colors'
        }

    @classmethod
    def update(cls):
        cls.left_bar.update()
        cls.right_bar.update()
        
        # Mettre à jour la position des boutons si l'écran a été redimensionné
        if cls.show_grid_button:
            screen_width = ScreenVar.screen.get_width()
            screen_height = ScreenVar.screen.get_height()
            scale = ScreenVar.scale
            
            button_size = int(45 * scale)
            margin = int(15 * scale)
            bottom_offset = int(15 * scale)
            right_offset = int(15 * scale)
            
            # Position en bas à droite
            x_pos_2 = screen_width - button_size - right_offset
            x_pos_1 = x_pos_2 - button_size - margin
            y_pos = screen_height - button_size - bottom_offset
            
            cls.show_grid_button['rect'] = pygame.Rect(x_pos_1, y_pos, button_size, button_size)
            cls.show_colors_button['rect'] = pygame.Rect(x_pos_2, y_pos, button_size, button_size)
            
            # Mettre à jour l'état actif
            cls.show_grid_button['active'] = cls.show_grid
            cls.show_colors_button['active'] = cls.show_colors

    @classmethod
    def change_turn(cls):
        cls.left_bar.highlight = not cls.left_bar.highlight
        cls.right_bar.highlight = not cls.right_bar.highlight

    @classmethod
    def draw(cls):
        cls.draw_bottom_background()
        cls.left_bar.draw(ScreenVar.screen)
        cls.right_bar.draw(ScreenVar.screen)
        cls.turn_display.draw()
        
        # Dessiner les boutons toggle
        cls.draw_toggle_buttons()
        
        # Dessiner le tooltip si présent
        if cls.tooltip_text and cls.tooltip_pos:
            cls.draw_tooltip()

        # --- Dessiner le vaisseau si défini ---
        if cls.ship_display.ship:
            x = 0 if cls.ship_display else ScreenVar.screen.get_width() - cls.ship_display.width
            y = ScreenVar.screen.get_height() - cls.ship_display.height
            cls.ship_display.shop = Turn.get_shop_with_id(cls.ship_display.ship.joueur)
            cls.ship_display.draw(ScreenVar.screen, x, y)

    @classmethod
    def draw_toggle_buttons(cls):
        """Dessine les boutons toggle avec un style futuriste."""
        screen = ScreenVar.screen
        scale = ScreenVar.scale
        mouse_pos = pygame.mouse.get_pos()
        
        for button in [cls.show_grid_button, cls.show_colors_button]:
            if not button:
                continue
                
            rect = button['rect']
            active = button['active']
            is_hover = rect.collidepoint(mouse_pos)
            
            # Couleurs selon l'état
            if active:
                bg_color = (50, 150, 255, 200)
                border_color = (100, 200, 255)
                glow_color = (100, 200, 255, 100)
            else:
                bg_color = (30, 35, 45, 180)
                border_color = (80, 100, 130)
                glow_color = (80, 100, 130, 50)
            
            # Effet hover
            if is_hover:
                border_color = tuple(min(c + 50, 255) for c in border_color[:3])
                cls.tooltip_text = button['tooltip']
                cls.tooltip_pos = mouse_pos
            
            # Fond avec effet de glow si actif
            if active:
                glow_rect = rect.inflate(int(8 * scale), int(8 * scale))
                glow_surf = pygame.Surface((glow_rect.width, glow_rect.height), pygame.SRCALPHA)
                pygame.draw.rect(glow_surf, glow_color, glow_surf.get_rect(), border_radius=int(8 * scale))
                screen.blit(glow_surf, glow_rect.topleft)
            
            # Fond du bouton
            button_surf = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
            pygame.draw.rect(button_surf, bg_color, button_surf.get_rect(), border_radius=int(6 * scale))
            screen.blit(button_surf, rect.topleft)
            
            # Bordure
            pygame.draw.rect(screen, border_color, rect, int(2 * scale), border_radius=int(6 * scale))
            
            # Dessiner l'icône
            cls.draw_button_icon(screen, rect, button['icon'], active, scale)

    @classmethod
    def draw_button_icon(cls, screen, rect, icon_type, active, scale):
        """Dessine l'icône du bouton."""
        center_x, center_y = rect.center
        icon_color = (255, 255, 255) if active else (150, 160, 180)
        line_width = int(2 * scale)
        
        if icon_type == 'grid':
            # Icône grille 3x3
            size = int(20 * scale)
            offset = size // 3
            start_x = center_x - size // 2
            start_y = center_y - size // 2
            
            # Lignes verticales
            for i in range(4):
                x = start_x + i * offset
                pygame.draw.line(screen, icon_color, (x, start_y), (x, start_y + size), line_width)
            
            # Lignes horizontales
            for i in range(4):
                y = start_y + i * offset
                pygame.draw.line(screen, icon_color, (start_x, y), (start_x + size, y), line_width)
        
        elif icon_type == 'colors':
            # Icône palette de couleurs
            size = int(18 * scale)
            colors = [(255, 80, 80), (80, 255, 80), (80, 80, 255), (255, 255, 80)]
            
            for i, color in enumerate(colors):
                angle = i * 90
                rad = 3.14159 * angle / 180
                offset_x = int(size * 0.35 * (1 if i % 2 == 0 else -1) * (1 if i < 2 else -1))
                offset_y = int(size * 0.35 * (1 if i < 2 else -1) * (1 if i % 2 == 0 else -1))
                
                circle_color = color if active else tuple(c // 2 for c in color)
                pygame.draw.circle(screen, circle_color, 
                                 (center_x + offset_x // 2, center_y + offset_y // 2), 
                                 int(5 * scale))

    @classmethod
    def draw_tooltip(cls):
        """Dessine l'infobulle au survol."""
        if not cls.tooltip_text:
            return
            
        screen = ScreenVar.screen
        scale = ScreenVar.scale
        font = pygame.font.Font(None, int(20 * scale))
        
        # Créer le texte
        text_surf = font.render(cls.tooltip_text, True, (255, 255, 255))
        padding = int(8 * scale)
        
        # Position du tooltip (au-dessus du curseur)
        tooltip_width = text_surf.get_width() + padding * 2
        tooltip_height = text_surf.get_height() + padding * 2
        tooltip_x = cls.tooltip_pos[0] - tooltip_width // 2
        tooltip_y = cls.tooltip_pos[1] - tooltip_height - int(10 * scale)
        
        # S'assurer que le tooltip reste dans l'écran
        tooltip_x = max(5, min(tooltip_x, screen.get_width() - tooltip_width - 5))
        tooltip_y = max(5, tooltip_y)
        
        # Fond du tooltip
        tooltip_rect = pygame.Rect(tooltip_x, tooltip_y, tooltip_width, tooltip_height)
        tooltip_surf = pygame.Surface((tooltip_width, tooltip_height), pygame.SRCALPHA)
        pygame.draw.rect(tooltip_surf, (20, 25, 35, 230), tooltip_surf.get_rect(), border_radius=int(4 * scale))
        screen.blit(tooltip_surf, (tooltip_x, tooltip_y))
        
        # Bordure
        pygame.draw.rect(screen, (100, 150, 200), tooltip_rect, int(2 * scale), border_radius=int(4 * scale))
        
        # Texte
        screen.blit(text_surf, (tooltip_x + padding, tooltip_y + padding))
        
        # Réinitialiser le tooltip pour le prochain frame
        cls.tooltip_text = None
        cls.tooltip_pos = None

    @classmethod
    def handle_click(cls, pos):
        """Gère les clics sur les boutons toggle."""
        if cls.show_grid_button and cls.show_grid_button['rect'].collidepoint(pos):
            cls.show_grid = not cls.show_grid
            cls.show_grid_button['active'] = cls.show_grid
            return False
            
        if cls.show_colors_button and cls.show_colors_button['rect'].collidepoint(pos):
            cls.show_colors = not cls.show_colors
            cls.show_colors_button['active'] = cls.show_colors
            return False
            
        # Passer le clic au turn_display
        return cls.turn_display.handle_click(pos)

    @classmethod
    def update_and_draw(cls):
        cls.update()
        cls.draw()

    @classmethod
    def show_ship(cls, ship, left_side=True):
        """
        Affiche un vaisseau dans le HUD.

        :param ship: dictionnaire ou objet représentant le vaisseau
        :param left_side: True pour afficher en bas à gauche, False pour en bas à droite
        """
        cls.ship_display.ship = ship
        cls.ship_display_left = left_side

    @classmethod
    def hide_ship(cls):
        """Cache le vaisseau affiché."""
        cls.ship_display.set_ship(None)

    @classmethod
    def draw_bottom_background(cls):
        if cls.render_bottom_background:
            screen = ScreenVar.screen

            screen_width, screen_height = screen.get_size()
            # Recalcule SCALE basé sur les dimensions actuelles
            scale = ScreenVar.scale
            
            bar_height = min(GridVar.offset_y, 100)
            shop_y = screen_height - bar_height

            # Fond du shop avec dégradé
            shop_bg = pygame.Surface((screen_width, bar_height), pygame.SRCALPHA)
            for i in range(bar_height):
                alpha = int(200 - (i / bar_height) * 50)
                color = (20 + i // 5, 25 + i // 5, 35 + i // 5, alpha)
                pygame.draw.line(shop_bg, color, (0, i), (screen_width, i))
            screen.blit(shop_bg, (0, shop_y))

            # Bordure supérieure du shop
            pygame.draw.line(screen, (100, 150, 200), (0, shop_y), (screen_width, shop_y), int(3 * scale))
            pygame.draw.line(screen, (150, 200, 255), (0, shop_y + int(1 * scale)), (screen_width, shop_y + int(1 * scale)), int(1 * scale))

            # Coins décoratifs
            corner_size = int(20 * scale)
            line_width = int(4 * scale)

            # Coin supérieur gauche
            pygame.draw.line(screen, (150, 200, 255), (0, shop_y), (corner_size, shop_y), line_width)
            pygame.draw.line(screen, (150, 200, 255), (0, shop_y), (0, shop_y + corner_size), line_width)

            # Coin supérieur droit
            pygame.draw.line(screen, (150, 200, 255),
                            (screen_width - corner_size, shop_y),
                            (screen_width - 1, shop_y),
                            line_width)
            pygame.draw.line(screen, (150, 200, 255),
                            (screen_width - 1, shop_y),
                            (screen_width - 1, shop_y + corner_size),
                            line_width)

            # Motifs décoratifs
            radius = int(3 * scale)
            for i in range(3):
                offset = int((30 + i * 40) * scale)
                pygame.draw.circle(screen, (100, 150, 200, 100), (offset, shop_y + bar_height // 2), radius)
                pygame.draw.circle(screen, (100, 150, 200, 100), (screen_width - offset, shop_y + bar_height // 2), radius)


if __name__ == "__main__":
    import pygame
    from blazyck import *
    from classes.HUD.HUD import HUD
    from classes.Player import Player
    from classes.Point import Point
    from classes.Turn import Turn
    from classes.MotherShip import MotherShip

    pygame.init()
    ScreenVar(pygame.display.set_mode((400, 800), pygame.RESIZABLE))
    GridVar()
    clock = pygame.time.Clock()

    # --- Initialisation des joueurs ---
    P1 = Player("Alice")
    P2 = Player("Bob")
    Turn.players = [P1, P2]
    Turn.shops = [Shop(P1), Shop(P2)]

    # Créer des MotherShip fictives
    P1.ships.append(MotherShip(taille=(4,5), tier=1, cordonner=Point(0,0), 
                      id=0, path="assets/img/ships/base", joueur = Turn.players[0].id))
    P2.ships.append(MotherShip(taille=(4,5), tier=1, cordonner=Point(0,0), 
                      id=1, path="assets/img/ships/base", joueur = Turn.players[1].id))

    # Initialisation du HUD
    HUD.init()

    # Affichage initial en bas à gauche
    HUD.show_ship(Turn.players[0].ships[0], left_side=True)
    show_ship = True
    left_side = True

    running = True
    while running:

        dt = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_h:
                    show_ship = not show_ship
                    if show_ship:
                        HUD.show_ship(Turn.players[0].ships[0], left_side=left_side)
                    else:
                        HUD.hide_ship()
                elif event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    # changer de côté
                    Turn.next()
                    HUD.change_turn()
                    left_side = not left_side
                    if show_ship:
                        HUD.show_ship(Turn.players[0].ships[0], left_side=left_side)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                HUD.handle_click(event.pos)
            elif event.type == pygame.VIDEORESIZE:
                ScreenVar.update_scale()
                GridVar.update_grid()

        ScreenVar.screen.fill((10, 10, 20))
        HUD.update_and_draw()
        
        # Afficher l'état des toggles pour le debug
        font = pygame.font.Font(None, 24)
        debug_text = f"Grille: {HUD.show_grid} | Couleurs: {HUD.show_colors}"
        text_surf = font.render(debug_text, True, (255, 255, 255))
        ScreenVar.screen.blit(text_surf, (10, ScreenVar.screen.get_height() - 30))
        
        pygame.display.flip()

    pygame.quit()