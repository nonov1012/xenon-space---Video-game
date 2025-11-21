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

    @classmethod
    def init(cls):
        cls.left_bar = BarDisplay(Turn.players[0], left=True)
        cls.left_bar.highlight = True   
        cls.right_bar = BarDisplay(Turn.players[1], left=False)
        cls.turn_display = TurnDisplay()
        cls.ship_display = ShipDisplay()
        cls.render_bottom_background = True

    @classmethod
    def update(cls):
        cls.left_bar.update()
        cls.right_bar.update()
        cls.turn_display.update()

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

        # --- Dessiner le vaisseau si défini ---
        if cls.ship_display.ship:
            x = 0 if cls.ship_display_left else ScreenVar.screen.get_width() - cls.ship_display.width
            y = ScreenVar.screen.get_height() - cls.ship_display.height
            cls.ship_display.shop = Turn.get_shop_with_id(cls.ship_display.ship.joueur)
            cls.ship_display.draw(ScreenVar.screen, x, y)

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
            print(shop_y)

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
            elif event.type == pygame.VIDEORESIZE:
                ScreenVar.update_scale()
                GridVar.update_grid()

        ScreenVar.screen.fill((10, 10, 20))
        HUD.update_and_draw()
        pygame.display.flip()

    pygame.quit()
