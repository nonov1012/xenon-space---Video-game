import os
import random
from blazyck import *

from main import start_game
from classes.ShipAnimator import ShipAnimator
from classes.PlanetAnimator import PlanetAnimator
from classes.Animator import Animator
from classes.Start_Animation.main import create_space_background
from menu.modifShips import vaisseaux_sliders, limites_params, vaisseaux

def dessiner_slider(ecran, valeur, min_val, max_val, x, y, largeur, hauteur,
                    couleur_prog=(0, 200, 100), couleur_curseur=(0, 150, 80)):
    """Dessine un slider avec barre et curseur."""
    # Fond du slider
    pygame.draw.rect(ecran, (90, 90, 110), (x, y, largeur, hauteur), border_radius=8)
    # Barre de progression
    rel_pos = (valeur - min_val) / (max_val - min_val) if max_val > min_val else 0
    largeur_prog = int(rel_pos * largeur)
    if largeur_prog > 0:
        pygame.draw.rect(ecran, couleur_prog, (x, y, largeur_prog, hauteur), border_radius=8)
    # Curseur
    curseur_x = x + int(rel_pos * largeur)
    pygame.draw.ellipse(ecran, couleur_curseur, (curseur_x - 8, y - 5, 16, hauteur + 10))


def draw(ecran):
    """Interface de personnalisation avec onglets Classique/Avance/Vaisseaux"""

    # -------------------------------
    # Couleurs et polices
    # -------------------------------
    BLANC = (255, 255, 255)
    GRIS_FONCE = (40, 40, 55)
    GRIS_MOYEN = (90, 90, 110)
    GRIS_CLAIR = (150, 150, 170)
    VERT = (0, 200, 100)
    VERT_FONCE = (0, 150, 80)
    BLEU_ACCENT = (70, 130, 255)

    police_titre = pygame.font.Font("assets/fonts/SpaceNova.otf", 60)
    police_param = pygame.font.Font("assets/fonts/SpaceNova.otf", 24)
    police_bouton = pygame.font.Font("assets/fonts/SpaceNova.otf", 24)

    # -------------------------------
    # Parametres avec sliders
    # -------------------------------
    parametres = {
        "Nombre de planetes": {"valeur": 3, "min": 1, "max": 10},
        "Nombre d'asteroides": {"valeur": 5, "min": 1, "max": 20},
        "Niveau base depart": {"valeur": 1, "min": 1, "max": 5},
        "Argent depart": {"valeur": 1000, "min": 500, "max": 5000},
    }

    random_active = False

    # -------------------------------
    # Vaisseaux
    # -------------------------------
    types_vaisseaux = list(vaisseaux_sliders.keys())
    vaisseau_actif = types_vaisseaux[0]
    slider_vaisseau_actif = None

    icones_vaisseaux = {}
    for ship in types_vaisseaux:
        path = os.path.join(IMG_PATH, "ships", ship, "base.png")
        if os.path.exists(path):
            img = pygame.image.load(path).convert_alpha()
        else:
            print(f"⚠️ Fichier non trouvé : {path}")
            img = pygame.Surface((80, 80))
            img.fill((255, 0, 0))
        icones_vaisseaux[ship] = pygame.transform.scale(img, (80, 80))

    # -------------------------------
    # Curseur personnalise
    # -------------------------------
    curseur_img = pygame.image.load('assets/img/menu/cursor.png')
    curseur_img = pygame.transform.scale(curseur_img, (40, 40))
    pygame.mouse.set_visible(False)

    # -------------------------------
    # Image de fond (même animation que menu principal)
    # -------------------------------
    largeur_ecran, hauteur_ecran = ecran.get_size()
    screen_ratio = (largeur_ecran * 100 / 600) / 100
    
    # Création du fond spatial animé avec étoiles et planètes
    stars, planet_manager, vaisseau_fond = create_space_background(
        num_stars=100, 
        screen_ratio=screen_ratio
    )

    # -------------------------------
    # Image de base pour les boutons
    # -------------------------------
    image_bouton_base = pygame.image.load("assets/img/menu/bouton_menu.png").convert_alpha()

    def creer_image_bouton(largeur, hauteur):
        return pygame.transform.scale(image_bouton_base, (largeur, hauteur))

    # -------------------------------
    # Boutons principaux
    # -------------------------------
    texte_jouer = police_bouton.render("JOUER", True, BLANC)
    texte_reset = police_bouton.render("RESET", True, BLANC)
    texte_retour = police_bouton.render("RETOUR MENU", True, BLANC)

    image_jouer = creer_image_bouton(texte_jouer.get_width() + 100, texte_jouer.get_height() + 100)
    image_reset = creer_image_bouton(texte_reset.get_width() + 120, texte_reset.get_height() + 100)
    image_retour = creer_image_bouton(texte_retour.get_width() + 200, texte_retour.get_height() + 100)

    # Position bas
    espacement_boutons = 80
    y_premiere_ligne = hauteur_ecran - 210
    y_deuxieme_ligne = hauteur_ecran - 120

    total_largeur_premiere = image_jouer.get_width() + image_reset.get_width() + espacement_boutons
    x_depart_premiere = (largeur_ecran - total_largeur_premiere) // 2

    rect_jouer = pygame.Rect(x_depart_premiere, y_premiere_ligne,
                             image_jouer.get_width(), image_jouer.get_height())
    rect_reset = pygame.Rect(rect_jouer.right + espacement_boutons, y_premiere_ligne,
                             image_reset.get_width(), image_reset.get_height())
    rect_retour = pygame.Rect((largeur_ecran - image_retour.get_width()) // 2, y_deuxieme_ligne,
                              image_retour.get_width(), image_retour.get_height())

    boutons = [
        (image_jouer, rect_jouer, "JOUER"),
        (image_reset, rect_reset, "RESET"),
        (image_retour, rect_retour, "RETOUR MENU")
    ]
    zoom_etats = {label: 1.0 for _, _, label in boutons}
    vitesse_zoom = 0.08

    # -------------------------------
    # Panneau + Onglets
    # -------------------------------
    panneau_largeur = 650
    panneau_hauteur = 500
    panneau_x = (largeur_ecran - panneau_largeur) // 2
    panneau_y = 205

    onglets = ["Classique", "Avance", "Vaisseaux"]
    onglet_actif = "Classique"

    # -------------------------------
    # Boucle principale
    # -------------------------------
    slider_actif = None
    img_rect = None  # Initialisation pour éviter l'erreur
    horloge = pygame.time.Clock()
    en_cours = True
    lancer_partie = False

    while en_cours:
        souris = pygame.mouse.get_pos()
        clic = pygame.mouse.get_pressed()[0]

        # Fond animé (comme menu principal)
        ecran.fill((0, 0, 0))
        stars.update()
        stars.draw(ecran)
        planet_manager.update_and_draw()
        Animator.update_all()
        PlanetAnimator.update_all()
        ShipAnimator.update_all()

        # Titre
        titre_surface = police_titre.render("Personnalisation", True, BLANC)
        rect_titre = titre_surface.get_rect(center=(largeur_ecran // 2, 60))
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
        # Onglet Classique / Avancé
        # -------------------------------
        if onglet_actif in ["Classique", "Avance"]:
            # Parametres affiches selon onglet
            liste_affichee = []
            if onglet_actif == "Classique":
                liste_affichee = ["Nombre de planetes", "Nombre d'asteroides"]
            elif onglet_actif == "Avance":
                liste_affichee = list(parametres.keys())

            # Sliders
            slider_largeur = 400
            slider_hauteur = 15
            slider_x = panneau_x + (panneau_largeur - slider_largeur) // 2
            decalage_y = 60
            for nom in liste_affichee:
                val = parametres[nom]
                y_courant = panneau_y + decalage_y

                texte_param = police_param.render(nom, True, BLANC)
                rect_param = texte_param.get_rect(center=(largeur_ecran // 2, y_courant - 25))
                ecran.blit(texte_param, rect_param)

                texte_valeur = police_param.render(str(val["valeur"]), True, BLEU_ACCENT)
                rect_valeur = texte_valeur.get_rect(center=(largeur_ecran // 2, y_courant))
                ecran.blit(texte_valeur, rect_valeur)

                rect_slider = pygame.Rect(slider_x, y_courant + 30, slider_largeur, slider_hauteur)
                pygame.draw.rect(ecran, GRIS_MOYEN, rect_slider, border_radius=8)

                rel_pos = (val["valeur"] - val["min"]) / (val["max"] - val["min"])
                largeur_prog = int(rel_pos * slider_largeur)
                if largeur_prog > 0:
                    rect_prog = pygame.Rect(slider_x, y_courant + 30, largeur_prog, slider_hauteur)
                    pygame.draw.rect(ecran, VERT, rect_prog, border_radius=8)

                curseur_x = int(slider_x + rel_pos * slider_largeur)
                rect_curseur = pygame.Rect(curseur_x - 12, y_courant + 22, 24, slider_hauteur + 16)
                pygame.draw.ellipse(ecran, VERT_FONCE, rect_curseur)
                pygame.draw.ellipse(ecran, VERT, (curseur_x - 10, y_courant + 24, 20, slider_hauteur + 12))

                if clic and rect_curseur.collidepoint(souris):
                    slider_actif = nom

                decalage_y += 100

            if slider_actif and clic:
                val = parametres[slider_actif]
                rel_x = max(0, min(slider_largeur, souris[0] - slider_x))
                val["valeur"] = int(val["min"] + (rel_x / slider_largeur) * (val["max"] - val["min"]))
            if not clic:
                slider_actif = None

            # Bouton Random
            rect_random = pygame.Rect(panneau_x + panneau_largeur - 230, panneau_y + panneau_hauteur - 50, 200, 40)
            pygame.draw.rect(ecran, VERT if random_active else GRIS_CLAIR, rect_random, border_radius=10)
            txt_random = police_param.render("RANDOM " + ("ON" if random_active else "OFF"), True, BLANC)
            ecran.blit(txt_random, txt_random.get_rect(center=rect_random.center))

        # -------------------------------
        # Onglet Vaisseaux
        # -------------------------------
        if onglet_actif == "Vaisseaux":
            # Cadre du vaisseau actif
            cadre_x, cadre_y, cadre_taille = panneau_x + 10, panneau_y + 10, 90
            pygame.draw.rect(ecran, BLANC, (cadre_x, cadre_y, cadre_taille, cadre_taille), 2, border_radius=5)
            img_vaisseau = icones_vaisseaux[vaisseau_actif]
            img_rect = img_vaisseau.get_rect(center=(cadre_x + cadre_taille//2, cadre_y + cadre_taille//2))
            ecran.blit(img_vaisseau, img_rect.topleft)

            # Nom du vaisseau
            texte_nom = police_param.render(vaisseau_actif, True, BLEU_ACCENT)
            ecran.blit(texte_nom, (cadre_x + cadre_taille + 10, cadre_y + 10))

            slider_largeur_v = 300
            slider_hauteur_v = 15
            slider_x_v = panneau_x + 150
            decalage_y_v = 60

            for idx, (param, valeur) in enumerate(vaisseaux_sliders[vaisseau_actif].items()):
                y = panneau_y + decalage_y_v + idx * 60
                
                # Utilise limites_params pour min/max
                min_val = limites_params[param]["min"]
                max_val = limites_params[param]["max"]
                
                # Dessine le slider
                dessiner_slider(ecran, valeur, min_val, max_val, slider_x_v, y + 25, slider_largeur_v, slider_hauteur_v)
                
                # Affiche le nom et la valeur
                texte_param = police_param.render(f"{param}: {valeur}", True, BLANC)
                ecran.blit(texte_param, (slider_x_v, y))

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

            texte_surf = police_bouton.render(label, True, BLANC)
            rect_texte = texte_surf.get_rect(center=rect_zoom.center)
            ecran.blit(texte_surf, rect_texte)

        # -------------------------------
        # Evenements
        # -------------------------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                en_cours = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Boutons bas
                for _, rect, label in boutons:
                    if rect.collidepoint(event.pos):
                        if label == "JOUER":
                            print("JOUER avec parametres:", {k: v["valeur"] for k, v in parametres.items()},
                                  "Random:", random_active)
                            print("Vaisseau :", vaisseau_actif, vaisseaux_sliders[vaisseau_actif])
                            en_cours = False
                            lancer_partie = True
                        elif label == "RESET":
                            for k in parametres:
                                parametres[k]["valeur"] = parametres[k]["min"]
                        elif label == "RETOUR MENU":
                            en_cours = False
                
                # Bouton Random (uniquement pour Classique/Avancé)
                if onglet_actif in ["Classique", "Avance"]:
                    rect_random = pygame.Rect(panneau_x + panneau_largeur - 230, panneau_y + panneau_hauteur - 50, 200, 40)
                    if rect_random.collidepoint(event.pos):
                        random_active = not random_active
                        # Si Random activé, randomize les valeurs
                        if random_active:
                            for k in parametres:
                                parametres[k]["valeur"] = random.randint(parametres[k]["min"], parametres[k]["max"])
                
                # Onglets
                for i, nom in enumerate(onglets):
                    rect_onglet = pygame.Rect(panneau_x + i * (panneau_largeur // len(onglets)), panneau_y - 50,
                                              panneau_largeur // len(onglets), 40)
                    if rect_onglet.collidepoint(event.pos):
                        onglet_actif = nom

                # Slider Vaisseaux - clic sur toute la barre
                if onglet_actif == "Vaisseaux":
                    slider_largeur_v = 300
                    slider_x_v = panneau_x + 150
                    decalage_y_v = 60
                    
                    for idx, param in enumerate(vaisseaux_sliders[vaisseau_actif].keys()):
                        y = panneau_y + decalage_y_v + idx * 60
                        # Zone cliquable = toute la barre du slider
                        rect_slider_zone = pygame.Rect(slider_x_v, y + 20, slider_largeur_v, 30)
                        if rect_slider_zone.collidepoint(event.pos):
                            slider_vaisseau_actif = param
                            # Applique immédiatement la nouvelle valeur avec limites_params
                            min_val = limites_params[param]["min"]
                            max_val = limites_params[param]["max"]
                            rel_x = max(0, min(slider_largeur_v, event.pos[0] - slider_x_v))
                            nouveau_val = int(min_val + (rel_x / slider_largeur_v) * (max_val - min_val))
                            vaisseaux_sliders[vaisseau_actif][param] = nouveau_val

                    # Changer vaisseau actif (clic sur l'image)
                    if img_rect and img_rect.collidepoint(event.pos):
                        index = (types_vaisseaux.index(vaisseau_actif) + 1) % len(types_vaisseaux)
                        vaisseau_actif = types_vaisseaux[index]

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                slider_vaisseau_actif = None
    
        # Glisser slider Vaisseaux
        if slider_vaisseau_actif and clic and onglet_actif == "Vaisseaux":
            slider_largeur_v = 300
            slider_x_v = panneau_x + 150
            # Utilise limites_params pour les limites
            min_val = limites_params[slider_vaisseau_actif]["min"]
            max_val = limites_params[slider_vaisseau_actif]["max"]
            rel_x = max(0, min(slider_largeur_v, souris[0] - slider_x_v))
            nouveau_val = int(min_val + (rel_x / slider_largeur_v) * (max_val - min_val))
            vaisseaux_sliders[vaisseau_actif][slider_vaisseau_actif] = nouveau_val

        # Curseur
        ecran.blit(curseur_img, souris)

        pygame.display.flip()
        horloge.tick(60)
    
    if lancer_partie == True:
        ShipAnimator.clear_list()
        PlanetAnimator.clear_list()
        start_game(ecran, parametres, random_active)