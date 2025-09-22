import pygame
import sys

# Initialisation
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Laser Continu avec Dissipation")
clock = pygame.time.Clock()

# Couleurs
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

player_pos = (WIDTH // 2, HEIGHT // 2)
laser_active = False

# Paramètres du laser
laser_width_max = 30
aura_width_max = 15
alpha_max = 255
dissipate_speed = 5  # vitesse de dissipation / apparition
laser_length = HEIGHT

# État actuel
laser_width = 0
aura_width = 0

running = True
while running:
    screen.fill(BLACK)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                laser_active = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                laser_active = False
    
    # Dessin du joueur
    pygame.draw.circle(screen, WHITE, player_pos, 20)
    
    # Gestion de l'extension/dissipation
    if laser_active:
        laser_width = min(laser_width + dissipate_speed, laser_width_max)
        aura_width = min(aura_width + dissipate_speed, aura_width_max)
    else:
        laser_width = max(laser_width - dissipate_speed, 0)
        aura_width = max(aura_width - dissipate_speed, 0)
    
    # Dessin du laser si visible
    if laser_width > 0 or aura_width > 0:
        temp_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        # cœur blanc
        pygame.draw.line(temp_surface, (255, 0, 0),
                         player_pos, (player_pos[0], player_pos[1] - laser_length), laser_width)
        # aura rouge
        pygame.draw.line(temp_surface, (255, 255, 255),
                         player_pos, (player_pos[0], player_pos[1] - laser_length), aura_width)
        screen.blit(temp_surface, (0, 0))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
