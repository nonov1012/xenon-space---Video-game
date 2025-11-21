from pickle import TRUE
import pygame
import sys
from classes.PlanetAnimator import PlanetAnimator
from classes.ShipAnimator import ShipAnimator
import menu.menuJouer
import menu.menuParam
import menu.menuSucces
import menu.credit

from classes.TitreAnime import TitreAnime
from classes.Sounds import SoundManager
from classes.Start_Animation.StarField import StarField
from classes.Start_Animation.PlanetManager import PlanetManager
from classes.MotherShip import MotherShip
from classes.Point import Point
from blazyck import *
from classes.Achievements import AchievementManager
from classes.Animator import Animator
from classes.Start_Animation.main import create_space_background
from classes.GlobalVar.ScreenVar import ScreenVar
from classes.GlobalVar.GridVar import GridVar
from menu.menuJouer import MenuPlay

# -------------------------------
# Initialisation Pygame
# -------------------------------
pygame.init()
screen_info = pygame.display.Info()
screen_width, screen_height = screen_info.current_w, screen_info.current_h
ScreenVar(pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE))
GridVar()

ScreenVar.update_scale()
GridVar.update_grid()

screen = ScreenVar.screen
pygame.display.set_caption("Xénon Space")
clock = pygame.time.Clock()

# Curseur personnalise
new_cursor = pygame.image.load('assets/img/menu/cursor.png')
new_cursor = pygame.transform.scale(new_cursor, (48, 48))
pygame.mouse.set_visible(False)

# Sons
sm = SoundManager()
sm.play_music("assets/sounds/musics/music_ingame.mp3")
sm.load_sfx("son_hover", "assets/sounds/menu/buttons/button_hover.mp3")
sm.load_sfx("son_click", "assets/sounds/menu/buttons/button_pressed.mp3")

# Icone
icone = pygame.image.load("assets/img/menu/logo.png")
pygame.display.set_icon(icone)

# -------------------------------
# Fond anime avec planetes et vaisseau
# -------------------------------
stars, planet_manager, B1 = create_space_background()

# -------------------------------
# Titre centre
# -------------------------------
police_titre = pygame.font.Font("assets/fonts/SpaceNova.otf", 100)
titre_position = (screen.get_width() // 2, 200)
titre = TitreAnime("XENON-SPACE", police_titre, titre_position,
                couleur_haut=(255,255,0), couleur_bas=(255,0,255))

# -------------------------------
# Boutons decales a gauche
# -------------------------------
blanc = (255,255,255)
police = pygame.font.Font("assets/fonts/SpaceNova.otf", 25)
image_bouton = pygame.image.load("assets/img/menu/bouton_menu.png").convert_alpha()
image_bouton = pygame.transform.scale(image_bouton, (500,150))
largeur_bouton, hauteur_bouton = image_bouton.get_size()

decalage_boutons = -500
x_bouton = screen_width // 2 - largeur_bouton // 2 + decalage_boutons
y_bouton = screen_height // 2

texte_jouer = police.render("Jouer", True, blanc)
texte_param = police.render("Parametres", True, blanc)
texte_succes = police.render("Succes", True, blanc)
texte_quitter = police.render("Quitter", True, blanc)
texte_credit = police.render("Credits", True, blanc)

bouton_jouer   = pygame.Rect(x_bouton, y_bouton - hauteur_bouton / 1.25 - 20, largeur_bouton, hauteur_bouton)
bouton_param   = pygame.Rect(x_bouton, y_bouton - (hauteur_bouton / 4) - 10, largeur_bouton, hauteur_bouton)
bouton_succes  = pygame.Rect(x_bouton, y_bouton + (hauteur_bouton / 4) + 10, largeur_bouton, hauteur_bouton)
bouton_quitter = pygame.Rect(x_bouton, y_bouton + hauteur_bouton / 1.25 + 20, largeur_bouton, hauteur_bouton)
bouton_credit  = pygame.Rect(screen_width - largeur_bouton - 30,
                            screen_height - hauteur_bouton - 30,
                            largeur_bouton, hauteur_bouton)

zoom_states = {}
zoom_speed = 0.08
hover_states = {}

def draw_main_menu():
    """Dessine le menu principal"""
    titre.draw(screen)

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
        screen.blit(bouton_zoom, rect_zoom.topleft)
        rect_texte = texte.get_rect(center=rect_zoom.center)
        screen.blit(texte, rect_texte.topleft)

# -------------------------------
# Boucle principale
# -------------------------------
en_cours = True
main_menu = True  # État du menu principal
succes_menu = False
play_menu = False
param_menu = False
credits_menu = False

# Créer l'instance du menu play
menu_play = MenuPlay()

while en_cours:
    clock.tick(30)
    screen.fill((0, 0, 0))
        
    try:
        souris = pygame.mouse.get_pos()
    except pygame.error:
        souris = (0, 0)

    # --- Fond + planetes + vaisseau ---
    stars.update()
    stars.draw(screen)
    planet_manager.update_and_draw()
    Animator.update_all()
    PlanetAnimator.update_all()
    ShipAnimator.update_all()

    # --- Affichage selon l'état ---
    if main_menu:
        draw_main_menu()
    elif play_menu:
        # Mettre à jour le menu play à chaque frame
        menu_play.draw()
        # Gérer les événements du menu play
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                en_cours = False
            else:
                menu_play.handle_events(event)
        
        # Mettre à jour le slider pendant le drag
        menu_play.update_slider_vaisseau()
        
        # Vérifier si on doit retourner au menu principal
        if not menu_play.en_cours:
            play_menu = False
            main_menu = True
            
            # Si on lance la partie
            if menu_play.lancer_partie:
                from menu.modifShips import appliquer_modifications_sliders
                appliquer_modifications_sliders()
                ShipAnimator.clear_list()
                PlanetAnimator.clear_list()
                from main import start_game
                start_game(screen, menu_play.parametres, menu_play.random_active)
                # Réinitialiser après le jeu
                menu_play.lancer_partie = False
                menu_play = MenuPlay()  # Recréer une nouvelle instance
                menu_play.update()
        
        # Curseur et affichage
        screen.blit(new_cursor, souris)
        pygame.display.flip()
        continue  # Sauter le reste de la boucle
    
    elif succes_menu:
        menu.menuSucces.main(screen)
    elif param_menu:
        menu.menuParam.main(screen)
    elif credits_menu:
        menu.credit.main(screen)

    # --- Curseur ---
    screen.blit(new_cursor, souris)
    pygame.display.flip()

    # --- Evenements du menu principal uniquement ---
    if main_menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                en_cours = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if bouton_jouer.collidepoint(event.pos):
                    sm.play_sfx("son_click")
                    main_menu = False
                    play_menu = True
                    # Réinitialiser et mettre à jour le menu play
                    menu_play = MenuPlay()
                    menu_play.update()
                    menu_play.en_cours = True
                elif bouton_param.collidepoint(event.pos):
                    sm.play_sfx("son_click")
                    main_menu = False
                    param_menu = True
                elif bouton_succes.collidepoint(event.pos):
                    sm.play_sfx("son_click")
                    main_menu = False
                    succes_menu = True
                elif bouton_credit.collidepoint(event.pos):
                    sm.play_sfx("son_click")
                    main_menu = False
                    credits_menu = True
                elif bouton_quitter.collidepoint(event.pos):
                    sm.play_sfx("son_click")
                    pygame.quit()
                    sys.exit()
            elif event.type == pygame.VIDEORESIZE:
                ScreenVar.update_scale()
                GridVar.update_grid()

pygame.quit()
sys.exit()