import pygame
from classes.HUD.BarDisplay import BarDisplay
from classes.HUD.TurnDisplay import TurnDisplay
from classes.MotherShip import MotherShip
from classes.Player import Player
from classes.Point import Point
from classes.Turn import Turn
from classes.HUD.ShipDisplay import ShipDisplay
from classes.Shop import Shop
from blazyck import *

class HUD:
    left_bar: BarDisplay = None
    right_bar: BarDisplay = None
    turn_display: TurnDisplay = None
    ship_display: ShipDisplay = None
    screen: pygame.Surface = None

    @classmethod
    def init(cls, screen: pygame.Surface):
        cls.left_bar = BarDisplay(Turn.players[0], left=True)
        cls.left_bar.highlight = True
        cls.right_bar = BarDisplay(Turn.players[1], left=False)
        cls.turn_display = TurnDisplay(screen)
        cls.ship_display = ShipDisplay()
        cls.screen = screen
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
        cls.left_bar.draw(cls.turn_display.screen)
        cls.right_bar.draw(cls.turn_display.screen)
        cls.turn_display.draw()

        # --- Dessiner le vaisseau si défini ---
        if cls.ship_display.ship:
            x = 0 if cls.ship_display_left else SCREEN_WIDTH - cls.ship_display.width
            y = cls.screen.get_height() - cls.ship_display.height
            cls.ship_display.shop = Turn.get_shop_with_id(cls.ship_display.ship.joueur)
            cls.ship_display.draw(cls.turn_display.screen, x, y)

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
        info = pygame.display.Info()
        SCREEN_WIDTH = info.current_w
        SCREEN_HEIGHT = info.current_h
        BASE_W = 1920
        BASE_H = 1080
        SCALE_X = SCREEN_WIDTH / BASE_W
        SCALE_Y = SCREEN_HEIGHT / BASE_H
        SCALE = min(SCALE_X, SCALE_Y)

        if cls.render_bottom_background:
            shop_width = SCREEN_WIDTH
            bar_height = int(BAR_HEIGHT * SCALE)
            shop_y = SCREEN_HEIGHT - bar_height

            # Fond du shop avec dégradé
            shop_bg = pygame.Surface((shop_width, bar_height), pygame.SRCALPHA)
            for i in range(bar_height):
                alpha = int(200 - (i / bar_height) * 50)
                color = (20 + i // 5, 25 + i // 5, 35 + i // 5, alpha)
                pygame.draw.line(shop_bg, color, (0, i), (shop_width, i))
            cls.screen.blit(shop_bg, (0, shop_y))

            # Bordure supérieure du shop
            pygame.draw.line(cls.screen, (100, 150, 200), (0, shop_y), (shop_width, shop_y), int(3 * SCALE))
            pygame.draw.line(cls.screen, (150, 200, 255), (0, shop_y + int(1 * SCALE)), (shop_width, shop_y + int(1 * SCALE)), int(1 * SCALE))

            # Coins décoratifs
            corner_size = int(20 * SCALE)
            line_width = int(4 * SCALE)

            # Coin supérieur gauche
            pygame.draw.line(cls.screen, (150, 200, 255), (0, shop_y), (corner_size, shop_y), line_width)
            pygame.draw.line(cls.screen, (150, 200, 255), (0, shop_y), (0, shop_y + corner_size), line_width)

            # Coin supérieur droit
            # horizontal
            pygame.draw.line(cls.screen, (150, 200, 255),
                            (shop_width - corner_size, shop_y),
                            (shop_width - 1, shop_y),
                            line_width)
            # vertical
            pygame.draw.line(cls.screen, (150, 200, 255),
                            (shop_width - 1, shop_y),
                            (shop_width - 1, shop_y + corner_size),
                            line_width)

            # Motifs décoratifs
            radius = int(3 * SCALE)
            for i in range(3):
                offset = int((30 + i * 40) * SCALE)
                pygame.draw.circle(cls.screen, (100, 150, 200, 100), (offset, shop_y + bar_height // 2), radius)
                pygame.draw.circle(cls.screen, (100, 150, 200, 100), (shop_width - offset, shop_y + bar_height // 2), radius)


if __name__ == "__main__":
    import pygame
    from blazyck import *
    from classes.HUD.HUD import HUD
    from classes.Player import Player
    from classes.Point import Point
    from classes.Turn import Turn
    from classes.MotherShip import MotherShip

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
    clock = pygame.time.Clock()

    # --- Initialisation des joueurs ---
    P1 = Player("Alice")
    P2 = Player("Bob")
    Turn.players = [P1, P2]
    Turn.shops = [Shop(P1, screen=screen), Shop(P2, screen=screen)]

    # Créer des MotherShip fictives
    P1.ships.append(MotherShip(taille=(4,5), tier=1, cordonner=Point(0,0), 
                      id=0, path="assets/img/ships/base", joueur = Turn.players[0].id))
    P2.ships.append(MotherShip(taille=(4,5), tier=1, cordonner=Point(0,0), 
                      id=1, path="assets/img/ships/base", joueur = Turn.players[1].id))

    # Initialisation du HUD
    HUD.init(screen)

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

        screen.fill((10, 10, 20))
        HUD.update_and_draw()
        pygame.display.flip()

    pygame.quit()
