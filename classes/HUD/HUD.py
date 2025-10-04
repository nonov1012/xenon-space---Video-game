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
    left_bar: BarDisplay = None
    right_bar: BarDisplay = None
    turn_display: TurnDisplay = None

    @classmethod
    def init(cls, screen: pygame.Surface):
        """Initialise les éléments du HUD (à appeler une seule fois au démarrage)"""
        cls.left_bar = BarDisplay(Turn.players[0], left=True)
        cls.left_bar.highlight = True
        cls.right_bar = BarDisplay(Turn.players[1], left=False)
        cls.turn_display = TurnDisplay(screen)

    @classmethod
    def update(cls):
        cls.left_bar.update()
        cls.right_bar.update()
        cls.turn_display.update()

    @classmethod
    def change_turn(cls):
        """Inverse la mise en évidence des barres lors d'un changement de tour"""
        cls.left_bar.highlight = not cls.left_bar.highlight
        cls.right_bar.highlight = not cls.right_bar.highlight

    @classmethod
    def draw(cls):
        cls.left_bar.draw(cls.turn_display.screen)
        cls.right_bar.draw(cls.turn_display.screen)
        cls.turn_display.draw()

    @classmethod
    def update_and_draw(cls):
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
    P1.ships.append(MotherShip(pv_max=5000, attaque=11, port_attaque=10, port_deplacement=0, cout=0,
                      valeur_mort=0, taille=(4,5), tier=1, cordonner=Point(0,0), 
                      id=0, path="assets/img/ships/base", joueur = Turn.players[0].id))
    P2.ships.append(MotherShip(pv_max=5000, attaque=11, port_attaque=10, port_deplacement=0, cout=0,
                      valeur_mort=0, taille=(4,5), tier=1, cordonner=Point(0,0), 
                      id=1, path="assets/img/ships/base", joueur = Turn.players[1].id))
    
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