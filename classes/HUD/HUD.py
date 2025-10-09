import pygame
from classes.HUD.BarDisplay import BarDisplay
from classes.HUD.TurnDisplay import TurnDisplay
from classes.MotherShip import MotherShip
from classes.Player import Player
from classes.Point import Point
from classes.Turn import Turn
from blazyck import *

class HUD:
    # --- Attributs de classe ---
    """
    Les attributs de classe suivants contiennent les éléments du HUD :
    - La barre de gauche qui affiche le joueur 0
    - La barre de droite qui affiche le joueur 1
    - L'affichage du tour actuel
    """
    left_bar: BarDisplay = None
    right_bar: BarDisplay = None
    turn_display: TurnDisplay = None

    @classmethod
    def init(cls, screen: pygame.Surface):
        """
        Initialise les éléments du HUD (à appeler une seule fois au démarrage).

        Les éléments initialisés sont :
        - La barre de gauche qui affiche le joueur 0
        - La barre de droite qui affiche le joueur 1
        - L'affichage du tour actuel
        """
        cls.left_bar = BarDisplay(Turn.players[0], left=True)
        cls.left_bar.highlight = True  # La barre de gauche est mise en évidence
        cls.right_bar = BarDisplay(Turn.players[1], left=False)
        cls.turn_display = TurnDisplay(screen)

    @classmethod
    def update(cls):
        """
        Mettre à jour les éléments du HUD.

        Appelle les méthodes update() des barres et de l'affichage du tour actuel.
        """
        # Mettre à jour les barres de gauche et de droite
        cls.left_bar.update()
        cls.right_bar.update()
        # Mettre à jour l'affichage du tour actuel
        cls.turn_display.update()

    @classmethod
    def change_turn(cls):
        """
        Inverse la mise en évidence des barres lors d'un changement de tour.

        Les barres de gauche et de droite sont mises en évidence à tour de rôle.
        """
        # Inverse la mise en évidence des barres
        cls.left_bar.highlight = not cls.right_bar.highlight
        cls.right_bar.highlight = not cls.left_bar.highlight

    @classmethod
    def draw(cls):
        """
        Dessine les éléments du HUD.

        Dessine les barres de gauche et de droite, ainsi que l'affichage du tour actuel.
        """
        cls.left_bar.draw(cls.turn_display.screen)
        cls.right_bar.draw(cls.turn_display.screen)
        cls.turn_display.draw()

    @classmethod
    def update_and_draw(cls):
        """
        Mettre à jour et dessine les éléments du HUD.

        Appelle les méthodes update() et draw() pour mettre à jour et dessiner
        les éléments du HUD.

        La méthode update() met à jour l'argent et les points de vie du vaisseau mère du joueur,
        tandis que la méthode draw() dessine les éléments du HUD sur l'écran.
        """
        cls.update()
        cls.draw()


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.NOFRAME)
    clock = pygame.time.Clock()

    # Initialisation des joueurs
    P1 = Player("Alice")
    P2 = Player("Bob")
    Turn.players = [P1, P2]
    
    # Création simplifiée des MotherShip
    P1.ships.append(MotherShip(
        tier=1,
        cordonner=Point(0, 0),
        id=0,
        path="assets/img/ships/base",
        joueur=Turn.players[0].id
    ))
    
    P2.ships.append(MotherShip(
        tier=1,
        cordonner=Point(0, 0),
        id=1,
        path="assets/img/ships/base",
        joueur=Turn.players[1].id
    ))
    
    # Initialisation du HUD
    HUD.init(screen)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                Turn.next()  # passe au joueur suivant
                HUD.change_turn()

        P1.economie.ajouter(10)
        P2.getMotherShip().pv_actuel -= 10

        screen.fill((10, 10, 20))
        HUD.update()
        HUD.draw()
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()