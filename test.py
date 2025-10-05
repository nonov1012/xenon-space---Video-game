import pygame
from classes.Player import Player
from classes.Animator import Animator
import menu.menuFin

pygame.init()
ecran = pygame.display.set_mode((1200, 800))
pygame.display.set_caption("Test Menu Fin Partie")

# IMPORTANT : Initialiser l'écran pour Animator
Animator.screen = ecran

player = Player(name="Clement")

print("Test VICTOIRE")
choix = menu.menuFin.main(ecran, player, victoire=True)
print(f"Choix: {choix}")

pygame.quit()