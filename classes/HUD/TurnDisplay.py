import pygame
from classes.Player import Player
from classes.Turn import Turn
from blazyck import *

class TurnDisplay:
    """
    Classe TurnDisplay qui permet d'afficher le panneau du tour.

    Attributs:
    - screen: Surface de l'écran
    - width: Largeur du panneau
    - height: Hauteur du panneau
    - margin: Marge entre le panneau et le bord de l'écran

    Méthodes:
    - __init__: Initialisation de la classe
    - update: Mise à jour des éléments du panneau
    - draw: Dessin du panneau
    """

    def __init__(self, screen: pygame.Surface):
        """
        Initialisation de la classe TurnDisplay.

        :param screen: Surface de l'écran
        """
        self.screen = screen
        self.width = 160
        self.height = 60
        self.margin = 30

        # Police futuriste
        self.font_title = pygame.font.SysFont("Orbitron", 20, bold=True)
        self.font_player = pygame.font.SysFont("Consolas", 18)

        # Couleurs
        self.bg_color = (20, 25, 40, 180)      # 180 = alpha pour semi-transparence
        self.border_color = (80, 210, 255)
        self.text_color = (255, 255, 255)
        self.warn_color = (255, 80, 80)

    def update(self):
        """
        Met à jour les éléments du panneau du tour.

        Cette méthode est actuellement vide, mais elle sera utilisée à l'avenir pour mettre à jour les éléments du panneau.
        """
        pass

    def draw(self):
        """Dessine le panneau du tour avec transparence

        Ce panneau affiche le nombre du tour en cours ainsi que le nom du joueur courant.
        """
        x = self.screen.get_width() // 2 - self.width // 2
        y = self.margin

        # --- Surface transparente ---
        panel_surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.rect(panel_surf, self.bg_color, (0, 0, self.width, self.height), border_radius=8)
        pygame.draw.rect(panel_surf, self.border_color, (0, 0, self.width, self.height), width=2, border_radius=8)

        # --- Blit de la surface transparente sur l'écran ---
        self.screen.blit(panel_surf, (x, y))

        # --- Texte du tour ---
        turn_text = f"{Turn.sentence} {Turn.get_nb_turns()}"
        text_surface = self.font_title.render(turn_text, True, self.text_color)
        text_rect = text_surface.get_rect(center=(x + self.width // 2, y + 20))
        self.screen.blit(text_surface, text_rect)

        # --- Joueur courant ---
        if Turn.players:
            current_player = Turn.players[0].name
            player_surface = self.font_player.render(current_player, True, self.border_color)
        else:
            player_surface = self.font_player.render("Aucun joueur", True, self.warn_color)
        player_rect = player_surface.get_rect(center=(x + self.width // 2, y + 42))
        self.screen.blit(player_surface, player_rect)

if __name__ == "__main__":

    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()

    Turn.players = [Player("Alice"), Player("Bob")]
    hud_turn = TurnDisplay(screen)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                Turn.next()  # passe au joueur suivant

        screen.fill((10, 10, 20))
        hud_turn.update()
        hud_turn.draw()
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
