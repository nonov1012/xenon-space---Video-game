import pygame
import sys
import os
import json
from blazyck import *
import copy
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from classes.Animator import Animator
from classes.PlanetAnimator import PlanetAnimator
from classes.Start_Animation.main import create_space_background

# Fichier de sauvegarde
SAVE_FILE = "save_parametre.json"

# Paramètres par défaut
DEFAULT_SETTINGS = {
    "touches": {
        "rotation_vaisseau": pygame.K_r,
        "terminer_tour": pygame.K_RETURN,
        "afficher_grille": pygame.K_LCTRL,
        "afficher_zones": pygame.K_LSHIFT,
        "menu_pause": pygame.K_ESCAPE
    },
    "audio": {
        "volume_general": 50,
        "volume_musique": 50,
        "volume_sons": 50
    }
}

def charger_parametres():
    """Charge les paramètres depuis le fichier de sauvegarde"""
    try:
        with open(SAVE_FILE, 'r') as f:
            return json.load(f)
    except:
        return DEFAULT_SETTINGS.copy()

def sauvegarder_parametres(settings):
    """Sauvegarde les paramètres dans un fichier"""
    with open(SAVE_FILE, 'w') as f:
        json.dump(settings, f, indent=4)

def get_key_name(key_code):
    """Retourne le nom d'une touche"""
    return pygame.key.name(key_code).upper()

def dessiner_slider(ecran, valeur, min_val, max_val, x, y, largeur, hauteur,
                    couleur_prog=(0, 200, 100), couleur_curseur=(0, 150, 80)):
    """Dessine un slider avec barre et curseur."""
    pygame.draw.rect(ecran, (90, 90, 110), (x, y, largeur, hauteur), border_radius=8)
    rel_pos = (valeur - min_val) / (max_val - min_val) if max_val > min_val else 1
    largeur_prog = int(rel_pos * largeur)
    if largeur_prog > 0:
        pygame.draw.rect(ecran, couleur_prog, (x, y, largeur_prog, hauteur), border_radius=8)
    curseur_x = x + int(rel_pos * largeur)
    pygame.draw.ellipse(ecran, couleur_curseur, (curseur_x - 8, y - 5, 16, hauteur + 10))


def main(ecran, animation=True):
    """Menu Paramètres avec configuration des touches et sauvegarde
    
    Args:
        ecran: Surface Pygame principale
        animation: bool - True = fond complet (étoiles + planètes + vaisseau)
                         False = seulement étoiles
    """

    # Charger les paramètres
    settings = charger_parametres()

    # -------------------------------
    # Couleurs et polices
    # -------------------------------
    BLANC = (255, 255, 255)
    GRIS_FONCE = (40, 40, 55)
    GRIS_MOYEN = (90, 90, 110)
    GRIS_CLAIR = (150, 150, 170)
    VERT = (0, 200, 100)
    BLEU_ACCENT = (70, 130, 255)
    ORANGE = (255, 165, 0)
    NOIR = (0, 0, 0)

    police_titre = pygame.font.Font("assets/fonts/SpaceNova.otf", 60)
    police_param = pygame.font.Font("assets/fonts/SpaceNova.otf", 22)
    police_bouton = pygame.font.Font("assets/fonts/SpaceNova.otf", 28)

    # -------------------------------
    # Curseur personnalisé
    # -------------------------------
    curseur_img = pygame.image.load('assets/img/menu/cursor.png')
    curseur_img = pygame.transform.scale(curseur_img, (40, 40))
    pygame.mouse.set_visible(False)

    # -------------------------------
    # Fond animé (sans vaisseau)
    # -------------------------------
    largeur_ecran, hauteur_ecran = ecran.get_size()
    screen_ratio = (largeur_ecran * 100 / 600) / 100
    stars, planet_manager, _ = create_space_background(
        num_stars=100, screen_ratio=screen_ratio
    )
    # Le vaisseau n'est pas utilisé, on l'ignore avec _

    # -------------------------------
    # Boutons - Taille augmentée
    # -------------------------------
    image_bouton_base = pygame.image.load("assets/img/menu/bouton_menu.png").convert_alpha()
    def creer_image_bouton(largeur, hauteur):
        return pygame.transform.scale(image_bouton_base, (largeur, hauteur))

    texte_sauv = police_bouton.render("SAUVEGARDER", True, BLANC)
    texte_reset = police_bouton.render("RESET", True, BLANC)
    texte_retour = police_bouton.render("RETOUR", True, BLANC)

    image_sauv = creer_image_bouton(texte_sauv.get_width() + 160, texte_sauv.get_height() + 130)
    image_reset = creer_image_bouton(texte_reset.get_width() + 160, texte_reset.get_height() + 130)
    image_retour = creer_image_bouton(texte_retour.get_width() + 160, texte_retour.get_height() + 130)

    espacement = 50
    y_boutons = hauteur_ecran - 170
    total_largeur = image_sauv.get_width() + image_reset.get_width() + image_retour.get_width() + espacement * 2
    x_depart = (largeur_ecran - total_largeur) // 2

    rect_sauv = pygame.Rect(x_depart, y_boutons, image_sauv.get_width(), image_sauv.get_height())
    rect_reset = pygame.Rect(rect_sauv.right + espacement, y_boutons, image_reset.get_width(), image_reset.get_height())
    rect_retour = pygame.Rect(rect_reset.right + espacement, y_boutons, image_retour.get_width(), image_retour.get_height())

    boutons = [
        (image_sauv, rect_sauv, "SAUVEGARDER"),
        (image_reset, rect_reset, "RESET"),
        (image_retour, rect_retour, "RETOUR")
    ]
    zoom_etats = {label: 1.0 for _, _, label in boutons}
    vitesse_zoom = 0.08

    # -------------------------------
    # Panneau + Onglets
    # -------------------------------
    panneau_largeur, panneau_hauteur = 800, 500
    panneau_x, panneau_y = (largeur_ecran - panneau_largeur) // 2, 120

    onglets = ["Touches", "Audio"]
    onglet_actif = "Touches"

    # État de capture de touche
    capture_touche = None

    # -------------------------------
    # Boucle principale
    # -------------------------------
    slider_actif = None
    horloge = pygame.time.Clock()
    en_cours = True

    while en_cours:
        souris = pygame.mouse.get_pos()
        clic = pygame.mouse.get_pressed()[0]

        # -------------------------------
        # Fond selon le paramètre animation
        # -------------------------------
        ecran.fill(NOIR)

        # Toujours afficher les étoiles
        stars.update()
        stars.draw(ecran)

        # Afficher planètes seulement si animation=True
        if animation:
            planet_manager.update_and_draw()
            PlanetAnimator.update_all()
        else:
            # Clear quand on ne montre pas l'animation pour éviter de laisser le vaisseau
            Animator.clear_list()
            PlanetAnimator.clear_list()

        # Titre
        titre_surface = police_titre.render("Parametres", True, BLANC)
        rect_titre = titre_surface.get_rect(center=(largeur_ecran // 2, 50))
        ecran.blit(titre_surface, rect_titre.topleft)

        # Panneau
        pygame.draw.rect(ecran, GRIS_FONCE, (panneau_x, panneau_y, panneau_largeur, panneau_hauteur), border_radius=15)
        pygame.draw.rect(ecran, GRIS_MOYEN, (panneau_x, panneau_y, panneau_largeur, panneau_hauteur), 2, border_radius=15)

        # Onglets
        onglet_largeur = panneau_largeur // len(onglets)
        for i, nom in enumerate(onglets):
            rect_onglet = pygame.Rect(panneau_x + i * onglet_largeur, panneau_y - 50, onglet_largeur, 40)
            couleur = BLEU_ACCENT if nom == onglet_actif else GRIS_CLAIR
            pygame.draw.rect(ecran, couleur, rect_onglet, border_radius=8)
            texte = police_param.render(nom, True, BLANC if nom == onglet_actif else GRIS_FONCE)
            rect_txt = texte.get_rect(center=rect_onglet.center)
            ecran.blit(texte, rect_txt)

        # -------------------------------
        # Onglet Touches
        # -------------------------------
        if onglet_actif == "Touches":
            y_offset = panneau_y + 40
            espacement_ligne = 70

            touches_config = [
                ("Rotation vaisseau", "rotation_vaisseau"),
                ("Terminer tour", "terminer_tour"),
                ("Afficher grille", "afficher_grille"),
                ("Afficher zones", "afficher_zones"),
                ("Menu pause", "menu_pause")
            ]

            for i, (label, key_id) in enumerate(touches_config):
                y = y_offset + i * espacement_ligne
                
                # Label
                texte_label = police_param.render(label + ":", True, BLANC)
                ecran.blit(texte_label, (panneau_x + 40, y))

                # Bouton de touche
                bouton_w, bouton_h = 150, 40
                bouton_x = panneau_x + panneau_largeur - bouton_w - 40
                rect_bouton = pygame.Rect(bouton_x, y - 5, bouton_w, bouton_h)
                
                # Couleur selon l'état
                if capture_touche == key_id:
                    couleur_bouton = ORANGE
                    texte_touche = "Appuyez..."
                else:
                    couleur_bouton = GRIS_MOYEN
                    texte_touche = get_key_name(settings["touches"][key_id])
                
                pygame.draw.rect(ecran, couleur_bouton, rect_bouton, border_radius=8)
                texte_surf = police_param.render(texte_touche, True, BLANC)
                texte_rect = texte_surf.get_rect(center=rect_bouton.center)
                ecran.blit(texte_surf, texte_rect)

        # -------------------------------
        # Onglet Audio
        # -------------------------------
        elif onglet_actif == "Audio":
            slider_largeur = 400
            slider_hauteur = 15
            slider_x = panneau_x + (panneau_largeur - slider_largeur) // 2
            y_offset = 80

            audio_params = [
                ("Volume general", "volume_general"),
                ("Volume musique", "volume_musique"),
                ("Volume sons", "volume_sons")
            ]

            for idx, (label, param_id) in enumerate(audio_params):
                y = panneau_y + y_offset + idx * 100
                
                # Label
                texte_param = police_param.render(label, True, BLANC)
                ecran.blit(texte_param, (slider_x, y - 25))
                
                # Valeur
                valeur = settings["audio"][param_id]
                texte_valeur = police_param.render(f"{valeur}%", True, BLEU_ACCENT)
                ecran.blit(texte_valeur, (slider_x + slider_largeur + 20, y - 25))
                
                # Slider
                dessiner_slider(ecran, valeur, 0, 100, slider_x, y + 10, slider_largeur, slider_hauteur)

        # -------------------------------
        # Boutons principaux
        # -------------------------------
        for image, rect, label in boutons:
            est_hover = rect.collidepoint(souris)
            cible_zoom = 1.1 if est_hover else 1.0
            zoom_etats[label] += (cible_zoom - zoom_etats[label]) * vitesse_zoom
            
            largeur_zoom = int(image.get_width() * zoom_etats[label])
            hauteur_zoom = int(image.get_height() * zoom_etats[label])
            image_zoom = pygame.transform.scale(image, (largeur_zoom, hauteur_zoom))
            rect_zoom = image_zoom.get_rect(center=rect.center)
            
            ecran.blit(image_zoom, rect_zoom.topleft)
            rect_texte = police_bouton.render(label, True, BLANC).get_rect(center=rect_zoom.center)
            ecran.blit(police_bouton.render(label, True, BLANC), rect_texte)

        # -------------------------------
        # Evenements
        # -------------------------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                en_cours = False
            
            elif event.type == pygame.KEYDOWN:
                # Si on est en mode capture de touche
                if capture_touche:
                    settings["touches"][capture_touche] = event.key
                    capture_touche = None
            
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Onglets
                for i, nom in enumerate(onglets):
                    onglet_largeur = panneau_largeur // len(onglets)
                    rect_onglet = pygame.Rect(panneau_x + i * onglet_largeur, panneau_y - 50, onglet_largeur, 40)
                    if rect_onglet.collidepoint(event.pos):
                        onglet_actif = nom
                        capture_touche = None

                # Clic sur boutons de touches
                if onglet_actif == "Touches":
                    touches_config = [
                        ("Rotation vaisseau", "rotation_vaisseau"),
                        ("Terminer tour", "terminer_tour"),
                        ("Afficher grille", "afficher_grille"),
                        ("Afficher zones", "afficher_zones"),
                        ("Menu pause", "menu_pause")
                    ]
                    y_offset = panneau_y + 40
                    espacement_ligne = 70
                    
                    for i, (label, key_id) in enumerate(touches_config):
                        y = y_offset + i * espacement_ligne
                        bouton_x = panneau_x + panneau_largeur - 150 - 40
                        rect_bouton = pygame.Rect(bouton_x, y - 5, 150, 40)
                        if rect_bouton.collidepoint(event.pos):
                            capture_touche = key_id

                # Clic sur sliders audio
                elif onglet_actif == "Audio":
                    slider_largeur = 400
                    slider_x = panneau_x + (panneau_largeur - slider_largeur) // 2
                    y_offset = 80
                    
                    audio_params = [
                        ("Volume general", "volume_general"),
                        ("Volume musique", "volume_musique"),
                        ("Volume sons", "volume_sons")
                    ]
                    
                    for idx, (label, param_id) in enumerate(audio_params):
                        y = panneau_y + y_offset + idx * 100
                        rect_slider = pygame.Rect(slider_x, y + 10, slider_largeur, 15)
                        if rect_slider.collidepoint(event.pos):
                            slider_actif = param_id

                # Boutons
                for _, rect, label in boutons:
                    if rect.collidepoint(event.pos):
                        if label == "SAUVEGARDER":
                            sauvegarder_parametres(settings)
                            print("Parametres sauvegardes dans", SAVE_FILE)
                        elif label == "RESET":
                            settings = copy.deepcopy(DEFAULT_SETTINGS)
                            capture_touche = None
                            print("Paramètres réinitialisés")
                        elif label == "RETOUR":
                            en_cours = False

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                slider_actif = None

        if slider_actif and clic and onglet_actif == "Audio":
            slider_largeur = 400
            slider_x = panneau_x + (panneau_largeur - slider_largeur) // 2
            rel_x = max(0, min(slider_largeur, souris[0] - slider_x))
            settings["audio"][slider_actif] = int((rel_x / slider_largeur) * 100)

        # Curseur
        ecran.blit(curseur_img, souris)

        pygame.display.flip()
        horloge.tick(60)
