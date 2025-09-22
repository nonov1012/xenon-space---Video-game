import pygame
from blazyck import *
from classes.Gif import *
import sys
from PIL import Image
import numpy as np
from classes.PlanetAnimator import PlanetAnimator

def main():
    pygame.init()
    screen = pygame.display.set_mode((175, 175))
    clock = pygame.time.Clock()
    pygame.display.set_caption("Test affichage Planètes")

    # Créer un objet à tester
    PlanetAnimator.set_screen(screen)
    P1 = PlanetAnimator((5, 5), (0, 0), default_fps=10)
    P1.play("planet1", True)
    P1.update_and_draw()

    # --- Liste pour stocker les frames ---
    frames = []

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    animation = P1.current_anim
                    num = int(animation[6])
                    next_num = ((num) % MAX_PLANETES_ANIMATIONS) + 1
                    animation = animation[:6] + str(next_num) + animation[7:]
                    P1.play(animation, True)

        # --- Update & draw ---
        PlanetAnimator.update_all()
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()