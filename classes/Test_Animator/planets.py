import pygame
from blazyck import *
from classes.Gif import *
import sys
from PIL import Image
import numpy as np
from classes.Animator import Animator

def main():
    pygame.init()
    screen = pygame.display.set_mode((175, 175))
    clock = pygame.time.Clock()
    pygame.display.set_caption("Test affichage Planètes")

    # Créer un objet à tester
    P1 = Animator(screen, PLANETES_PATH, (5, 5), (0, 0), default_fps=15)
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
        P1.erase()
        P1.update_and_draw()
        pygame.display.flip()
        clock.tick(60)

        # --- Capturer la frame pour GIF ---
        frame_array = pygame.surfarray.array3d(screen)
        frame_array = np.transpose(frame_array, (1, 0, 2))
        frame_image = Image.fromarray(frame_array)
        frames.append(frame_image)

    # --- Sauvegarder le GIF ---
    if frames and False == True:
        frames[0].save("capture.gif", save_all=True, append_images=frames[1:], duration=1000//60, loop=0)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()