from pickle import TRUE
import pygame
import sys
from classes.PlanetAnimator import PlanetAnimator
from classes.ShipAnimator import ShipAnimator
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
from menu.menuSucces import MenuSucces
from menu.menuParam import MenuParametres
from menu.credit import MenuCredits
from tuto import lancer_tutoriel

# -------------------------------
# Initialisation Pygame
# -------------------------------
pygame.init()
screen_info = pygame.display.Info()
screen_width, screen_height = screen_info.current_w, screen_info.current_h
ScreenVar(pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE | pygame.FULLSCREEN))
GridVar()

ScreenVar.update_scale()
GridVar.update_grid()

screen = ScreenVar.screen
pygame.display.set_caption("Xénon Space")
clock = pygame.time.Clock()

# Curseur personnalise
cursor_image = pygame.image.load(os.path.join(MENU_PATH, "cursor.png")).convert_alpha()
CURSOR_SIZE = (48, 32)
cursor_image = pygame.transform.smoothscale(cursor_image, CURSOR_SIZE)
hotspot = (CURSOR_SIZE[0] // 2, CURSOR_SIZE[1] // 2)
custom_cursor = pygame.cursors.Cursor(hotspot, cursor_image)
pygame.mouse.set_cursor(custom_cursor)

# Sons
sm = SoundManager()
sm.play_music("assets/sounds/musics/music_ingame.mp3")
sm.load_sfx("son_hover", "assets/sounds/menu/buttons/button_hover.mp3")
sm.load_sfx("son_click", "assets/sounds/menu/buttons/button_pressed.mp3")
sm.load_sfx("shop_yes", "assets/sounds/others/Complete_02.ogg")
sm.load_sfx("shop_no", "assets/sounds/others/Denied_03.ogg")

# Charger et appliquer les paramètres au démarrage
import json
try:
    
    with open(get_resource_path("save_parametre.json"), 'r') as f:
        saved_settings = json.load(f)
        sm.set_master_volume(saved_settings["audio"]["volume_general"])
        sm.set_music_volume(saved_settings["audio"]["volume_musique"])
        sm.set_sfx_volume(saved_settings["audio"]["volume_sons"])
except:
    pass

# Icone
icone = pygame.image.load("assets/img/menu/logo.png")
pygame.display.set_icon(icone)

# -------------------------------
# Fond anime avec planetes et vaisseau
# -------------------------------
stars, planet_manager, B1 = create_space_background()
animator_main_ship = B1.animator

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
texte_tutoriel = police.render("Tutoriel", True, blanc)
texte_param = police.render("Parametres", True, blanc)
texte_succes = police.render("Succes", True, blanc)
texte_quitter = police.render("Quitter", True, blanc)
texte_credit = police.render("Credits", True, blanc)

# Ajustement des positions des boutons pour faire de la place au tutoriel
espacement = 5
bouton_jouer    = pygame.Rect(x_bouton, y_bouton - hauteur_bouton * 1.5 - espacement * 2, largeur_bouton, hauteur_bouton)
bouton_tutoriel = pygame.Rect(x_bouton, y_bouton - hauteur_bouton * 0.75 - espacement, largeur_bouton, hauteur_bouton)
bouton_param    = pygame.Rect(x_bouton, y_bouton, largeur_bouton, hauteur_bouton)
bouton_succes   = pygame.Rect(x_bouton, y_bouton + hauteur_bouton * 0.75 + espacement, largeur_bouton, hauteur_bouton)
bouton_quitter  = pygame.Rect(x_bouton, y_bouton + hauteur_bouton * 1.5 + espacement * 2, largeur_bouton, hauteur_bouton)
bouton_credit   = pygame.Rect(screen_width - largeur_bouton - 30,
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
        (bouton_tutoriel, texte_tutoriel),
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


def gerer_menu_generique(menu, flag_menu):
    """Gère un menu générique de manière unifiée"""
    global main_menu
    
    menu.draw()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False, False, False
        else:
            menu.handle_events(event)
    
    if isinstance(menu, MenuPlay):
        menu.update_slider_vaisseau()
    elif isinstance(menu, MenuParametres):
        menu.update_slider()
    
    if not menu.en_cours:
        if isinstance(menu, MenuPlay) and menu.lancer_partie:
            return False, False, True
        return False, True, False
    
    return True, False, False


# -------------------------------
# Boucle principale
# -------------------------------
en_cours = True
main_menu = True
play_menu = False
tutoriel_menu = False
succes_menu = False
param_menu = False
credits_menu = False

menu_play = None
menu_succes = None
menu_param = None
menu_credits = None

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
    animator_main_ship.update_and_draw()


    # --- Affichage selon l'état ---
    if main_menu:
        draw_main_menu()
        
    elif tutoriel_menu:
        resultat_tuto = lancer_tutoriel(screen, stars, planet_manager)
        tutoriel_menu = False
        main_menu = True
        
    elif play_menu and menu_play:
        continuer, retour_main, lancer = gerer_menu_generique(menu_play, "play_menu")
        
        if not continuer:
            play_menu = False
            if retour_main:
                main_menu = True
            elif lancer:
                from menu.modifShips import appliquer_modifications_sliders
                appliquer_modifications_sliders()
                ShipAnimator.clear_list()
                PlanetAnimator.clear_list()
                joueurs = menu_play.joueurs
                from main import start_game
                start_game(menu_play.parametres, menu_play.random_active, joueurs)
                main_menu = True
                menu_play = None
        
        pygame.display.flip()
        continue
    
    elif succes_menu and menu_succes:
        continuer, retour_main, _ = gerer_menu_generique(menu_succes, "succes_menu")
        
        if not continuer:
            succes_menu = False
            if retour_main:
                main_menu = True
                menu_succes = None
        
        pygame.display.flip()
        continue
    
    elif param_menu and menu_param:
        continuer, retour_main, _ = gerer_menu_generique(menu_param, "param_menu")
        
        if not continuer:
            param_menu = False
            if retour_main:
                main_menu = True
                menu_param = None
        
        pygame.display.flip()
        continue
    
    elif credits_menu:
        menu.credit.main(screen)
        credits_menu = False
        main_menu = True

    pygame.display.flip()

    # --- Événements du menu principal uniquement ---
    if main_menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                en_cours = False
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if bouton_jouer.collidepoint(event.pos):
                    sm.play_sfx("son_click")
                    main_menu = False
                    play_menu = True
                    menu_play = MenuPlay()
                    menu_play.update()
                    menu_play.en_cours = True
                
                elif bouton_tutoriel.collidepoint(event.pos):
                    sm.play_sfx("son_click")
                    main_menu = False
                    tutoriel_menu = True
                    
                elif bouton_param.collidepoint(event.pos):
                    sm.play_sfx("son_click")
                    main_menu = False
                    param_menu = True
                    menu_param = MenuParametres()
                    menu_param.sound_manager = sm
                    menu_param.update()
                    menu_param.en_cours = True
                    
                elif bouton_succes.collidepoint(event.pos):
                    sm.play_sfx("son_click")
                    main_menu = False
                    succes_menu = True
                    menu_succes = MenuSucces()
                    menu_succes.update()
                    menu_succes.en_cours = True
                    
                elif bouton_credit.collidepoint(event.pos):
                    sm.play_sfx("son_click")
                    main_menu = False
                    credits_menu = True
                    menu_credits = MenuCredits()
                    menu_credits.update()
                    menu_credits.en_cours = True
                    
                elif bouton_quitter.collidepoint(event.pos):
                    sm.play_sfx("son_click")
                    pygame.quit()
                    sys.exit()
                    
            elif event.type == pygame.VIDEORESIZE:
                ScreenVar.update_scale()
                GridVar.update_grid()

pygame.quit()
sys.exit()