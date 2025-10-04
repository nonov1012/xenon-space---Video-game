import pygame
from classes.Player import Player
from classes.Turn import Turn
from blazyck import *

class TurnDisplay:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.width = 160
        self.height = 60
        self.margin = 30

        # Police futuriste
        self.font_title = pygame.font.SysFont("Orbitron", 20, bold=True)
        self.font_player = pygame.font.SysFont("Consolas", 18)

        # Couleurs
        self.bg_color = (20, 25, 40)
        self.border_color = (80, 210, 255)
        self.text_color = (255, 255, 255)
        self.warn_color = (255, 80, 80)

    def update(self):
        # Rien de dynamique pour l’instant
        pass

    def draw(self):
        """Dessine le panneau du tour"""
        x = self.screen.get_width() // 2 - self.width // 2
        y = self.margin

        # --- Fond principal ---
        pygame.draw.rect(self.screen, self.bg_color, (x, y, self.width, self.height), border_radius=8)
        pygame.draw.rect(self.screen, self.border_color, (x, y, self.width, self.height), width=2, border_radius=8)

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
