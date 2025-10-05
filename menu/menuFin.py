import pygame
from classes.ShipAnimator import ShipAnimator
from classes.PlanetAnimator import PlanetAnimator
from classes.Animator import Animator
from classes.Start_Animation.main import create_space_background
from classes.Sounds import SoundManager

def main(ecran, player, victoire=True, sound_manager=None):
    """Menu Fin de Partie avec fond animé
    
    Args:
        ecran: Surface pygame
        player: Instance de Player avec les stats de la partie
        victoire: True si victoire, False si défaite
        sound_manager: Instance de SoundManager (optionnel)
    
    Returns:
        str: "menu" pour retour au menu, "quitter" pour fermer le jeu
    """
    ShipAnimator.clear_list()
    PlanetAnimator.clear_list()
    # -------------------------------
    # Couleurs et polices
    # -------------------------------
    BLANC = (255, 255, 255)
    GRIS_FONCE = (40, 40, 55)
    GRIS_MOYEN = (90, 90, 110)
    JAUNE = (255, 215, 0)
    ROUGE = (220, 50, 50)

    police_titre = pygame.font.Font("assets/fonts/SpaceNova.otf", 80)
    police_sous_titre = pygame.font.Font("assets/fonts/SpaceNova.otf", 30)
    police_bouton = pygame.font.Font("assets/fonts/SpaceNova.otf", 24)

    # -------------------------------
    # Fond animé
    # -------------------------------
    largeur_ecran, hauteur_ecran = ecran.get_size()
    screen_ratio = (largeur_ecran * 100 / 600) / 100
    
    stars, planet_manager, vaisseau_fond = create_space_background(
        num_stars=100, 
        screen_ratio=screen_ratio
    )

    # -------------------------------
    # Sons
    # -------------------------------
    sm = sound_manager
    if sm is None:
        sm = SoundManager()
        sm.load_sfx("son_hover", "assets/sounds/menu/buttons/button_hover.mp3")
        sm.load_sfx("son_click", "assets/sounds/menu/buttons/button_pressed.mp3")

    # -------------------------------
    # Sons
    # -------------------------------
    sm = sound_manager
    if sm is None:
        # Créer un SoundManager si non fourni
        sm = SoundManager()
        sm.load_sfx("son_hover", "assets/sounds/menu/buttons/button_hover.mp3")
        sm.load_sfx("son_click", "assets/sounds/menu/buttons/button_pressed.mp3")

    # -------------------------------
    # Curseur
    # -------------------------------
    curseur_img = pygame.image.load('assets/img/menu/cursor.png')
    curseur_img = pygame.transform.scale(curseur_img, (40, 40))
    pygame.mouse.set_visible(False)

    # -------------------------------
    # Boutons
    # -------------------------------
    image_bouton_base = pygame.image.load("assets/img/menu/bouton_menu.png").convert_alpha()
    
    def creer_image_bouton(largeur, hauteur):
        return pygame.transform.scale(image_bouton_base, (largeur, hauteur))

    texte_retour_menu = police_bouton.render("RETOUR AU MENU", True, BLANC)
    texte_quitter = police_bouton.render("QUITTER", True, BLANC)

    image_retour_menu = creer_image_bouton(texte_retour_menu.get_width() + 150, 
                                           texte_retour_menu.get_height() + 80)
    image_quitter = creer_image_bouton(texte_quitter.get_width() + 150, 
                                       texte_quitter.get_height() + 80)

    # Positionnement des boutons (côte à côte en bas)
    espacement = 80
    y_boutons = hauteur_ecran - 150
    total_largeur = image_retour_menu.get_width() + image_quitter.get_width() + espacement
    x_depart = (largeur_ecran - total_largeur) // 2

    rect_retour_menu = pygame.Rect(x_depart, y_boutons, 
                                   image_retour_menu.get_width(), 
                                   image_retour_menu.get_height())
    rect_quitter = pygame.Rect(rect_retour_menu.right + espacement, y_boutons,
                               image_quitter.get_width(), 
                               image_quitter.get_height())

    boutons = [
        (image_retour_menu, rect_retour_menu, "menu", texte_retour_menu),
        (image_quitter, rect_quitter, "quitter", texte_quitter)
    ]

    zoom_etats = {"menu": 1.0, "quitter": 1.0}
    vitesse_zoom = 0.08
    hover_states = {"menu": False, "quitter": False}
    hover_states = {"menu": False, "quitter": False}

    # -------------------------------
    # Panneau central
    # -------------------------------
    panneau_largeur = 600
    panneau_hauteur = 300
    panneau_x = (largeur_ecran - panneau_largeur) // 2
    panneau_y = (hauteur_ecran - panneau_hauteur) // 2 - 50

    # -------------------------------
    # Boucle principale
    # -------------------------------
    horloge = pygame.time.Clock()
    en_cours = True
    choix = None

    while en_cours:
        souris = pygame.mouse.get_pos()

        # Fond animé
        ecran.fill((0, 0, 0))
        stars.update()
        stars.draw(ecran)
        planet_manager.update_and_draw()
        Animator.update_all()
        PlanetAnimator.update_all()
        ShipAnimator.update_all()

        # Panneau semi-transparent
        panneau_surf = pygame.Surface((panneau_largeur, panneau_hauteur), pygame.SRCALPHA)
        pygame.draw.rect(panneau_surf, (40, 40, 55, 200), 
                        (0, 0, panneau_largeur, panneau_hauteur), 
                        border_radius=20)
        pygame.draw.rect(panneau_surf, GRIS_MOYEN, 
                        (0, 0, panneau_largeur, panneau_hauteur), 
                        3, border_radius=20)
        ecran.blit(panneau_surf, (panneau_x, panneau_y))

        # Titre Victoire ou Défaite
        if victoire:
            titre_texte = "VICTOIRE"
            couleur_titre = JAUNE
        else:
            titre_texte = "DEFAITE"
            couleur_titre = ROUGE

        titre_surface = police_titre.render(titre_texte, True, couleur_titre)
        rect_titre = titre_surface.get_rect(center=(largeur_ecran // 2, 
                                                     panneau_y + panneau_hauteur // 2 - 30))
        ecran.blit(titre_surface, rect_titre.topleft)

        # Nom du joueur en dessous
        player_name = player.name if player is not None else ""
        sous_titre = police_sous_titre.render(player_name, True, BLANC)

        rect_sous_titre = sous_titre.get_rect(center=(largeur_ecran // 2, 
                                                       panneau_y + panneau_hauteur // 2 + 50))
        ecran.blit(sous_titre, rect_sous_titre.topleft)

        # Boutons avec effet de zoom
        for image, rect, action, texte in boutons:
            est_hover = rect.collidepoint(souris)
            
            # Son au survol
            if est_hover and not hover_states[action]:
                sm.play_sfx("son_hover")
            hover_states[action] = est_hover
            
            cible_zoom = 1.1 if est_hover else 1.0
            zoom_etats[action] += (cible_zoom - zoom_etats[action]) * vitesse_zoom

            largeur_zoom = int(image.get_width() * zoom_etats[action])
            hauteur_zoom = int(image.get_height() * zoom_etats[action])
            image_zoom = pygame.transform.scale(image, (largeur_zoom, hauteur_zoom))
            rect_zoom = image_zoom.get_rect(center=rect.center)

            ecran.blit(image_zoom, rect_zoom.topleft)
            
            rect_texte = texte.get_rect(center=rect_zoom.center)
            ecran.blit(texte, rect_texte.topleft)

        # Curseur
        ecran.blit(curseur_img, souris)

        pygame.display.flip()
        horloge.tick(60)

        # Événements
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for _, rect, action, _ in boutons:
                    if rect.collidepoint(event.pos):
                        import menu.menuPrincipal
                        en_cours = False
                        
                        choix = action


    
    return choix if choix else "menu"