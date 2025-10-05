import pygame
from classes.HUD.BarDisplay import BarDisplay
from classes.HUD.TurnDisplay import TurnDisplay
from classes.MotherShip import MotherShip
from classes.Player import Player
from classes.Point import Point
from classes.Turn import Turn
from classes.HUD.ShipDisplay import ShipDisplay  # <-- nouveau
from blazyck import *

class HUD:
    left_bar: BarDisplay = None
    right_bar: BarDisplay = None
    turn_display: TurnDisplay = None
    ship_display: ShipDisplay = None  # <-- ajout

    @classmethod
    def init(cls, screen: pygame.Surface):
        cls.left_bar = BarDisplay(Turn.players[0], left=True)
        cls.left_bar.highlight = True
        cls.right_bar = BarDisplay(Turn.players[1], left=False)
        cls.turn_display = TurnDisplay(screen)
        cls.ship_display = ShipDisplay()  # initialisation

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
        cls.left_bar.draw(cls.turn_display.screen)
        cls.right_bar.draw(cls.turn_display.screen)
        cls.turn_display.draw()

        # --- Dessiner le vaisseau si défini ---
        if cls.ship_display.ship:
            x = 10 if cls.ship_display_left else SCREEN_WIDTH - cls.ship_display.width - 10
            y = 0
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
        cls.ship_display.set_ship(ship)
        cls.ship_display_left = left_side  # position

    @classmethod
    def hide_ship(cls):
        """Cache le vaisseau affiché."""
        cls.ship_display.set_ship(None)

if __name__ == "__main__":
    import pygame
    from blazyck import SCREEN_WIDTH, SCREEN_HEIGHT, OFFSET_X
    from classes.HUD.HUD import HUD
    from classes.Player import Player
    from classes.Point import Point
    from classes.Turn import Turn
    from classes.MotherShip import MotherShip

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    # --- Initialisation des joueurs ---
    P1 = Player("Alice")
    P2 = Player("Bob")
    Turn.players = [P1, P2]

    # Créer des MotherShip fictives
    P1.ships.append(MotherShip(taille=(4,5), tier=1, cordonner=Point(0,0), 
                      id=0, path="assets/img/ships/base", joueur = Turn.players[0].id))
    P2.ships.append(MotherShip(taille=(4,5), tier=1, cordonner=Point(0,0), 
                      id=1, path="assets/img/ships/base", joueur = Turn.players[1].id))

    # Initialisation du HUD
    HUD.init(screen)

    # Exemple de vaisseau fictif pour ShipDisplay
    ship_example = {
        "name": "Chasseur",
        "pv_actuel": 40,
        "pv_max": 100,
        "attaque": 15,
        "port_attaque": 3,
        "port_attaque_max": 5,
        "port_deplacement": 2,
        "port_deplacement_max": 4
    }

    # Affichage initial en bas à gauche
    HUD.show_ship(ship_example, left_side=True)
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
                        HUD.show_ship(ship_example, left_side=left_side)
                    else:
                        HUD.hide_ship()
                elif event.key == pygame.K_SPACE:
                    # changer de côté
                    left_side = not left_side
                    if show_ship:
                        HUD.show_ship(ship_example, left_side=left_side)

        screen.fill((10, 10, 20))
        HUD.update_and_draw()
        pygame.display.flip()

    pygame.quit()
