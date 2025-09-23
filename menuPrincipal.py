import pygame
import sys
import menuJouer
import menuParam
from classes.TitreAnime import TitreAnime
from classes.Sounds import SoundManager
from classes.Start_Animation.StarField import StarField
from classes.Start_Animation.PlanetManager import PlanetManager
from classes.MotherShip import MotherShip
from classes.Point import Point
from blazyck import *
from classes.Achievements import AchievementManager 

# -------------------------------
# Créer le fond spatial (étoiles + planètes + vaisseau)
# -------------------------------
def create_space_background(screen: pygame.Surface, planete_path: str, num_stars=100, screen_ratio=1.0):
    screen_width, screen_height = screen.get_size()

    stars = StarField(
        screen_width,
        screen_height,
        num_stars=int(num_stars * screen_ratio),
        min_radius=1,
        max_radius=3,
        min_distance=15,
        size_distribution="small-biased",
        move_amplitude=3
    )

    planet_manager = PlanetManager(
        screen,
        planete_path,
        speed_range=(1, 2 * screen_ratio),
        planet_size_range=(1, int(5 * screen_ratio)),
        prob_increment=1
    )

    center_x = screen_width // 2
    center_y = screen_height // 2
    vaisseau_w = 4 * TAILLE_CASE * screen_ratio
    vaisseau_h = 5 * TAILLE_CASE * screen_ratio
    x = int(center_x - vaisseau_w / 2)
    y = int(center_y - vaisseau_h / 2)

    B1 = MotherShip(
        screen,
        Point(x, y),
        tier=1,
        show_health=False,
        largeur=4 * screen_ratio,
        hauteur=5 * screen_ratio
    )
    B1.animator.set_angle(90)
    B1.animator.play("base")
    B1.animator.play("engine")

    return stars, planet_manager, B1

# -------------------------------
# Initialisation Pygame
# -------------------------------
pygame.init()
screen_info = pygame.display.Info()
screen_width, screen_height = screen_info.current_w, screen_info.current_h
ecran = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
clock = pygame.time.Clock()
screen_ratio = (screen_width * 100 / 600) / 100

# Curseur personnalisé
new_cursor = pygame.image.load('assets/img/menu/cursor.png')
new_cursor = pygame.transform.scale(new_cursor, (40, 40))
pygame.mouse.set_visible(False)

# Sons
sm = SoundManager()
sm.play_music("assets/sounds/musics/music_ingame.mp3")
sm.load_sfx("son_hover", "assets/sounds/menu/buttons/button_hover.mp3")
sm.load_sfx("son_click", "assets/sounds/menu/buttons/button_pressed.mp3")

# Icône
icone = pygame.image.load("assets/img/menu/logo.png")
pygame.display.set_icon(icone)

# -------------------------------
# Fond animé avec planètes et vaisseau
# -------------------------------
stars, planet_manager, B1 = create_space_background(ecran, PLANETES_PATH, num_stars=100, screen_ratio=screen_ratio)

# -------------------------------
# Titre centré
# -------------------------------
police_titre = pygame.font.Font("assets/fonts/SpaceNova.otf", 100)
titre_position = (screen_width // 2, 200)
titre = TitreAnime("XENON-SPACE", police_titre, titre_position,
                   couleur_haut=(255,255,0), couleur_bas=(255,0,255))

# -------------------------------
# Boutons décalés à gauche
# -------------------------------
blanc = (255,255,255)
police = pygame.font.Font("assets/fonts/SpaceNova.otf", 25)
image_bouton = pygame.image.load("assets/img/menu/bouton_menu.png").convert_alpha()
image_bouton = pygame.transform.scale(image_bouton, (500,150))
largeur_bouton, hauteur_bouton = image_bouton.get_size()

decalage_boutons = -500  # boutons à gauche
x_bouton = screen_width // 2 - largeur_bouton // 2 + decalage_boutons
y_bouton = screen_height // 2

texte_jouer = police.render("Jouer", True, blanc)
texte_param = police.render("Parametre", True, blanc)
texte_succes = police.render("Succes", True, blanc)
texte_quitter = police.render("Quitter", True, blanc)
texte_credit = police.render("Credit", True, blanc)

bouton_jouer   = pygame.Rect(x_bouton, y_bouton - 200, largeur_bouton, hauteur_bouton)
bouton_param   = pygame.Rect(x_bouton, y_bouton - 100, largeur_bouton, hauteur_bouton)
bouton_succes  = pygame.Rect(x_bouton, y_bouton , largeur_bouton, hauteur_bouton)
bouton_quitter = pygame.Rect(x_bouton, y_bouton + 100, largeur_bouton, hauteur_bouton)

# Bouton crédit reste à sa position originale
bouton_credit  = pygame.Rect(screen_width - largeur_bouton - 30,
                             screen_height - hauteur_bouton - 30,
                             largeur_bouton, hauteur_bouton)

zoom_states = {}
zoom_speed = 0.08
hover_states = {}

# -------------------------------
# Boucle principale
# -------------------------------
en_cours = True
while en_cours:
    souris = pygame.mouse.get_pos()

    # --- Fond + planètes + vaisseau ---
    ecran.fill((0,0,0))
    stars.update()
    stars.draw(ecran)
    planet_manager.update_and_draw()
    B1.animator.update_and_draw()

    # --- Titre ---
    titre.draw(ecran)

    # --- Boutons ---
    boutons = [
        (bouton_jouer, texte_jouer),
        (bouton_param, texte_param),
        (bouton_succes, texte_succes),
        (bouton_quitter, texte_quitter),
        (bouton_credit, texte_credit)
    ]

    for i, (bouton, texte) in enumerate(boutons):
        if i not in zoom_states:
            zoom_states[i] = 1.0
        if i not in hover_states:
            hover_states[i] = False

        zone_survol = bouton.inflate(0, -100)
        est_survol = zone_survol.collidepoint(souris)
        if est_survol and not hover_states[i]:
            sm.play_sfx("son_hover")
        hover_states[i] = est_survol

        zoom_cible = 1.1 if est_survol else 1.0
        zoom_states[i] += (zoom_cible - zoom_states[i]) * zoom_speed

        bouton_zoom = pygame.transform.scale(
            image_bouton,
            (int(largeur_bouton * zoom_states[i]), int(hauteur_bouton * zoom_states[i]))
        )
        rect_zoom = bouton_zoom.get_rect(center=bouton.center)
        ecran.blit(bouton_zoom, rect_zoom.topleft)
        rect_texte = texte.get_rect(center=rect_zoom.center)
        ecran.blit(texte, rect_texte.topleft)

    # --- Curseur ---
    ecran.blit(new_cursor, souris)
    pygame.display.flip()
    clock.tick(30)

    # --- Événements ---
    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            en_cours = False
        elif evenement.type == pygame.MOUSEBUTTONDOWN:
            if bouton_jouer.collidepoint(evenement.pos):
                sm.play_sfx("son_click")
                menuJouer.main(ecran)
            elif bouton_param.collidepoint(evenement.pos):
                sm.play_sfx("son_click")
                menuParam.main(ecran)
            elif bouton_quitter.collidepoint(evenement.pos):
                sm.play_sfx("son_click")
                pygame.quit()
                sys.exit()
