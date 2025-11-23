import pygame
from classes.Player import Player
from classes.Turn import Turn
from classes.GlobalVar.ScreenVar import ScreenVar
from classes.GlobalVar.GridVar import GridVar
from blazyck import *

class TurnDisplay:
    """
    Classe TurnDisplay qui permet d'afficher le panneau du tour avec bouton "Terminer Tour".

    Attributs:
    - screen: Surface de l'écran
    - width: Largeur du panneau
    - height: Hauteur du panneau
    - margin: Marge entre le panneau et le bord de l'écran
    - button_callback: Fonction appelée lors du clic sur le bouton

    Méthodes:
    - __init__: Initialisation de la classe
    - update: Mise à jour des éléments du panneau
    - draw: Dessin du panneau
    - handle_click: Gère les clics de souris
    """

    def __init__(self, on_end_turn_callback=None):
        """
        Initialisation de la classe TurnDisplay.

        :param on_end_turn_callback: Fonction à appeler lors du clic sur "Terminer Tour"
        """
        self.width = int(160 * ScreenVar.scale)
        self.height = int(60 * ScreenVar.scale)
        self.margin = int(30 * ScreenVar.scale)

        # Police futuriste
        self.font_title = pygame.font.SysFont("Orbitron", 20, bold=True)
        self.font_player = pygame.font.SysFont("Consolas", 18)
        self.font_button = pygame.font.SysFont("Orbitron", 16, bold=True)

        # Couleurs
        self.bg_color = (20, 25, 40, 180)
        self.border_color = (80, 210, 255)
        self.text_color = (255, 255, 255)
        self.warn_color = (255, 80, 80)
        self.button_color = (50, 150, 255, 200)
        self.button_hover_color = (80, 180, 255, 220)
        self.button_text_color = (255, 255, 255)

        # État du bouton
        self.button_rect = None
        self.button_hovered = False
        self.button_callback = on_end_turn_callback

        # Animation du bouton
        self.button_scale = 1.0
        self.target_scale = 1.0

    def update(self):
        """
        Met à jour les éléments du panneau du tour.
        """
        # Animation du bouton
        self.button_scale += (self.target_scale - self.button_scale) * 0.15
        
        # Vérifier le survol du bouton
        if self.button_rect:
            mouse_pos = pygame.mouse.get_pos()
            self.button_hovered = self.button_rect.collidepoint(mouse_pos)
            self.target_scale = 1.05 if self.button_hovered else 1.0

    def draw(self):
        """Dessine le panneau du tour avec transparence et bouton"""
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
        spacing = 8

        panel_width = max(title_surf.get_width(), player_surf.get_width(), (100 * ScreenVar.scale)) + padding_x * 2
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

        # --- Bouton "Terminer Tour" à droite ---
        self.update()
        self._draw_button(screen, x + panel_width + 15, y)

    def _draw_button(self, screen, x, y):
        """Dessine le bouton 'Terminer Tour' avec tooltip"""

        # --- Dimensions logiques du bouton ---
        button_width = 40
        button_height = 28

        # Animation scale
        scaled_width = int(button_width * self.button_scale)
        scaled_height = int(button_height * self.button_scale)

        # Position réelle
        button_x = x
        button_y = y

        # Zone cliquable
        self.button_rect = pygame.Rect(button_x, button_y, scaled_width, scaled_height)

        # Surface bouton en alpha
        button_surf = pygame.Surface((scaled_width, scaled_height), pygame.SRCALPHA)

        # --- UTILITAIRE clamp ---
        def clamp(v): 
            return max(0, min(255, int(v)))

        # Couleur selon hover
        if self.button_hovered:
            color = (
                clamp(self.button_color[0] + 40),
                clamp(self.button_color[1] + 40),
                clamp(self.button_color[2] + 40),
                230  # alpha ok car button_surf est en SRCALPHA
            )
        else:
            # Si self.button_color est RGB → on ajoute alpha
            if len(self.button_color) == 3:
                color = (*self.button_color, 200)
            else:
                color = self.button_color

        # --- DESSIN BOUTON ---
        pygame.draw.rect(
            button_surf, color,
            (0, 0, scaled_width, scaled_height),
            border_radius=6
        )

        # Bordure néon
        border_color = (120, 220, 255) if self.button_hovered else self.border_color
        pygame.draw.rect(
            button_surf, border_color,
            (0, 0, scaled_width, scaled_height),
            width=2, border_radius=6
        )

        # Glow si hover
        if self.button_hovered:
            glow = pygame.Surface((scaled_width + 12, scaled_height + 12), pygame.SRCALPHA)
            pygame.draw.rect(glow, (80, 180, 255, 100),
                            (0, 0, scaled_width + 12, scaled_height + 12),
                            border_radius=8)
            screen.blit(glow, (button_x - 6, button_y - 6))

        # Icône >>
        arrow_font = pygame.font.SysFont("Consolas", 18, bold=True)
        arrow_surf = arrow_font.render(">>", True, self.button_text_color)
        arrow_rect = arrow_surf.get_rect(center=(scaled_width // 2, scaled_height // 2))
        button_surf.blit(arrow_surf, arrow_rect)

        # Affiche le bouton
        screen.blit(button_surf, (button_x, button_y))

        # ------------------
        #   TOOLTIP
        # ------------------
        if self.button_hovered:
            tooltip_text = "PASSER SON TOUR"
            tooltip_font = pygame.font.SysFont("Orbitron", 14, bold=True)

            tip_surf = tooltip_font.render(tooltip_text, True, (255, 255, 255))
            padding = 8
            tip_w = tip_surf.get_width() + padding * 2
            tip_h = tip_surf.get_height() + padding * 2

            tip_x = button_x + scaled_width + 15
            tip_y = button_y + (scaled_height // 2) - (tip_h // 2)

            # Surface tooltip
            tip_box = pygame.Surface((tip_w, tip_h), pygame.SRCALPHA)

            pygame.draw.rect(tip_box, (20, 25, 40, 200),
                            (0, 0, tip_w, tip_h), border_radius=6)
            pygame.draw.rect(tip_box, (80, 210, 255),
                            (0, 0, tip_w, tip_h), width=2, border_radius=6)

            # Glow tooltip
            glow = pygame.Surface((tip_w + 10, tip_h + 10), pygame.SRCALPHA)
            pygame.draw.rect(glow, (80, 180, 255, 80),
                            (0, 0, tip_w + 10, tip_h + 10),
                            border_radius=8)
            screen.blit(glow, (tip_x - 5, tip_y - 5))

            tip_box.blit(tip_surf, (padding, padding))
            screen.blit(tip_box, (tip_x, tip_y))


    def handle_click(self, mouse_pos):
        """
        Gère les clics de souris sur le bouton.
        
        :param mouse_pos: Position de la souris (tuple x, y)
        :return: True si le bouton a été cliqué, False sinon
        """
        if self.button_rect and self.button_rect.collidepoint(mouse_pos):
            Turn.next()
            return True
        return False


# Fonction callback exemple
def on_end_turn():
    """Fonction appelée quand on clique sur 'Terminer Tour'"""
    Turn.next()


if __name__ == "__main__":

    pygame.init()
    screen = pygame.display.set_mode((1920, 1080), pygame.RESIZABLE)
    ScreenVar(screen)
    GridVar()
    clock = pygame.time.Clock()

    Turn.players = [Player("Alice"), Player("Bob")]
    
    # Créer le display avec le callback
    hud_turn = TurnDisplay(on_end_turn_callback=on_end_turn)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                Turn.next()  # passe au joueur suivant
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Gérer le clic sur le bouton
                print("Clic sur le bouton")
                print("Position du clic:", event.pos)

                hud_turn.handle_click(event.pos)
            elif event.type == pygame.VIDEORESIZE:
                ScreenVar.update_scale()
                GridVar.update_grid()

        screen.fill((10, 10, 20))
        hud_turn.update(pygame.mouse.get_pos())
        hud_turn.draw()
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()