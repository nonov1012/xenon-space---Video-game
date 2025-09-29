import pygame
from blazyck import *
from classes.Gif import *
import sys
from PIL import Image
import numpy as np
from classes.Animator import Animator
from classes.ProjectileAnimator import ProjectileAnimator

projectiles_data = {
    "bullet": (4, 16),
    "big bullet": (8, 16),
    "torpedo": (11, 32),
    "wave": (64, 64),
    "laser": (18, 38)
}

def main():
    pygame.init()
    screen = pygame.display.set_mode((400, 800))
    clock = pygame.time.Clock()
    pygame.display.set_caption("Test affichage Projectiles")

    # Créer un objet à tester
    ProjectileAnimator.set_screen(screen)
    P1 = ProjectileAnimator((1, 2), (0, 0), default_fps=10, speed=5, projectile_type="laser")
    P1.play("laser", True, frame_size=projectiles_data["laser"])
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
        screen.fill((0, 0, 0))
        # --- Update & draw ---
        P1.set_target(pygame.mouse.get_pos())
        ProjectileAnimator.update_all()
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