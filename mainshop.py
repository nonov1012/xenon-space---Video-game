#POUR TESTER LA BOUTIQUE
import pygame
import sys
from classes.Shop import Shop
from classes.Player import Player

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Jeu avec boutique")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 30)

# Joueur
player = Player("TestPlayer", solde_initial=3000)

# Boutique
shop = Shop(player, font, screen)

# Boucle principale
running = True
while running:
    screen.fill((0, 0, 0))

    # Affichage solde du joueur
    coins_text = font.render(f"Coins: {player.economie.solde}", True, (255, 255, 0))
    screen.blit(coins_text, (10, 10))

    # Dessiner la boutique
    shop.draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            shop.handle_click(event.pos)

    pygame.display.flip()
    clock.tick(60)

# Affichage final des vaisseaux achetés
print(f"Vaisseaux achetés: {player.ships}")
print(f"Solde final: {player.economie.solde}")

pygame.quit()
sys.exit()
