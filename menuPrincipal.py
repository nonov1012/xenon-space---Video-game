import pygame
import sys
from classes.TitreAnime import TitreAnime 



pygame.init()

# -------------------------------
# Fenêtre et son
# -------------------------------
ecran = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Xenon Space")

new_cursor = pygame.image.load('assets/img/menu/cursor.png')
new_cursor = pygame.transform.scale(new_cursor,(40,40))

pygame.mouse.set_visible(False)

pygame.mixer.init()
musique_menu = pygame.mixer.music.load('assets/sounds/musics/music_ingame.mp3')
pygame.mixer.music.play(loops=-1)
pygame.mixer.music.set_volume(0.2)


son_hover = pygame.mixer.Sound("assets/sounds/menu/buttons/button_hover.mp3")
son_click = pygame.mixer.Sound("assets/sounds/menu/buttons/button_pressed.mp3")
son_hover.set_volume(0.3)
son_click.set_volume(1)

# -------------------------------
# Icône et fond
# -------------------------------
icone = pygame.image.load("assets/img/menu/logo.png")
pygame.display.set_icon(icone)

fond = pygame.image.load("assets/img/menu/fond.png").convert()
fond = pygame.transform.scale(fond, ecran.get_size())

# -------------------------------
# Titre animé
# -------------------------------
police_titre = pygame.font.Font("assets/fonts/SpaceNova.otf", 100)
titre = TitreAnime("XENON-SPACE", police_titre, (ecran.get_width()//2, 200),
                   couleur_haut=(255,255,0), couleur_bas=(255,0,255))

# -------------------------------
# Couleur, police et boutons
# -------------------------------
blanc = (255, 255, 255)
police = pygame.font.Font("assets/fonts/SpaceNova.otf", 25)

image_bouton = pygame.image.load("assets/img/menu/bouton_menu.png").convert_alpha()
image_bouton = pygame.transform.scale(image_bouton, (500, 150))  
largeur_bouton, hauteur_bouton = image_bouton.get_size()

x_bouton = ecran.get_width() // 2 - largeur_bouton // 2
y_bouton = ecran.get_height() // 2

texte_jouer = police.render("Jouer", True, blanc)
texte_param = police.render("Parametre", True, blanc)
texte_succes = police.render("Succes", True, blanc)
texte_quitter = police.render("Quitter", True, blanc)
texte_credit = police.render("Credit", True, blanc)

bouton_jouer   = pygame.Rect(x_bouton, y_bouton - 200, largeur_bouton, hauteur_bouton)
bouton_param   = pygame.Rect(x_bouton, y_bouton - 100, largeur_bouton, hauteur_bouton)
bouton_succes  = pygame.Rect(x_bouton, y_bouton , largeur_bouton, hauteur_bouton)
bouton_quitter = pygame.Rect(x_bouton, y_bouton + 100, largeur_bouton, hauteur_bouton)
bouton_credit  = pygame.Rect(ecran.get_width() - largeur_bouton - 30,
                             ecran.get_height() - hauteur_bouton - 30,
                             largeur_bouton, hauteur_bouton)

# -------------------------------
# Variables animation et hover
# -------------------------------
zoom_states = {}
zoom_speed = 0.08
hover_states = {}

# -------------------------------
# Boucle principale
# -------------------------------
en_cours = True
while en_cours:
    ecran.blit(fond, (0, 0))
    titre.draw(ecran)

    souris = pygame.mouse.get_pos()

    boutons = [
        (bouton_jouer, texte_jouer),
        (bouton_param, texte_param),
        (bouton_succes, texte_succes),
        (bouton_quitter, texte_quitter),
        (bouton_credit, texte_credit)
    ]

    for i, (bouton, texte) in enumerate(boutons):

        # Initialiser zoom et hover si nécessaire
        if i not in zoom_states:
            zoom_states[i] = 1.0
        if i not in hover_states:
            hover_states[i] = False

        # Zone de survol réduite
        zone_survol = bouton.inflate(0, -100)
        est_survol = zone_survol.collidepoint(souris)

        # Jouer le son hover uniquement à l’entrée
        if est_survol and not hover_states[i]:
            son_hover.play()
        hover_states[i] = est_survol

        # Calcul du zoom progressif
        zoom_cible = 1.1 if est_survol else 1.0
        zoom_states[i] += (zoom_cible - zoom_states[i]) * zoom_speed

        # Appliquer le zoom
        bouton_zoom = pygame.transform.scale(
            image_bouton,
            (int(largeur_bouton * zoom_states[i]), int(hauteur_bouton * zoom_states[i]))
        )
        rect_zoom = bouton_zoom.get_rect(center=bouton.center)
        ecran.blit(bouton_zoom, rect_zoom.topleft)

        # Texte centré sur le bouton zoomé
        rect_texte = texte.get_rect(center=rect_zoom.center)
        ecran.blit(texte, rect_texte.topleft)

    ecran.blit(new_cursor,souris)
    pygame.display.flip()

    # -------------------------------
    # Événements
    # -------------------------------
    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            en_cours = False

        if evenement.type == pygame.MOUSEBUTTONDOWN:
            for bouton_check, _ in boutons:
                if bouton_check.collidepoint(evenement.pos):
                    son_click.play()
            if bouton_quitter.collidepoint(evenement.pos):
                pygame.quit()
                sys.exit()
