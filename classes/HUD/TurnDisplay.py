import pygame
from classes.Player import Player
from classes.Turn import Turn
from classes.GlobalVar.ScreenVar import ScreenVar
from classes.GlobalVar.GridVar import GridVar
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

    def __init__(self):
        """
        Initialisation de la classe TurnDisplay.

        :param screen: Surface de l'écran
        """
        self.width = int(160 * ScreenVar.scale)
        self.height = int(60 * ScreenVar.scale)
        self.margin = int(30 * ScreenVar.scale)

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
        """Dessine le panneau du tour avec transparence"""

        screen = ScreenVar.screen
        y = self.margin

        # --- Texte du tour ---
        turn_text = f"{Turn.sentence} {Turn.get_nb_turns()}"
        title_surf = self.font_title.render(turn_text, True, self.text_color)

        # --- Joueur courant ---
        if Turn.players:
            current_player = Turn.players[0].name
            player_surf = self.font_player.render(current_player, True, self.border_color)
        else:
            player_surf = self.font_player.render("Aucun joueur", True, self.warn_color)

        # --- Calcul dynamique de la taille du panneau ---
        padding_x = 20
        padding_y = 10
        spacing = 8  # espace entre les deux lignes

        panel_width = max(title_surf.get_width(), player_surf.get_width()) + padding_x * 2
        panel_height = title_surf.get_height() + player_surf.get_height() + padding_y * 2 + spacing

        # Position horizontale centrée
        x = (screen.get_width() - panel_width) // 2

        # --- Surface transparente ---
        panel_surf = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        pygame.draw.rect(panel_surf, self.bg_color,
                        (0, 0, panel_width, panel_height),
                        border_radius=8)
        pygame.draw.rect(panel_surf, self.border_color,
                        (0, 0, panel_width, panel_height),
                        width=2, border_radius=8)

        # --- Placement du texte ---
        title_rect = title_surf.get_rect(center=(panel_width // 2, padding_y + title_surf.get_height() // 2))
        player_rect = player_surf.get_rect(center=(panel_width // 2,
                                                title_rect.bottom + spacing + player_surf.get_height() // 2))

        panel_surf.blit(title_surf, title_rect)
        panel_surf.blit(player_surf, player_rect)

        # --- Blit sur l'écran ---
        screen.blit(panel_surf, (x, y))


if __name__ == "__main__":

    pygame.init()
    screen = pygame.display.set_mode((1920, 1080), pygame.RESIZABLE)
    ScreenVar(screen)
    GridVar()
    clock = pygame.time.Clock()

    Turn.players = [Player("Alice"), Player("Bob")]
    hud_turn = TurnDisplay()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                Turn.next()  # passe au joueur suivant
            elif event.type == pygame.VIDEORESIZE:
                ScreenVar.update_scale()
                GridVar.update_grid()

        screen.fill((10, 10, 20))
        hud_turn.update()
        hud_turn.draw()
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
