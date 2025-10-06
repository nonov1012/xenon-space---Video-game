import os
import random
from blazyck import *


from classes.ShipAnimator import ShipAnimator
from classes.PlanetAnimator import PlanetAnimator
from classes.Animator import Animator
from classes.Start_Animation.main import create_space_background
from menu.modifShips import vaisseaux_sliders, limites_params, SHIP_STATS, noms_affichage

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
    police_petite = pygame.font.Font("assets/fonts/SpaceNova.otf", 18)

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
    tier_actif = 1  # Pour MotherShip
    slider_vaisseau_actif = None
    
    # État du dropdown
    dropdown_ouvert = False
    dropdown_scroll = 0  # Scroll du dropdown
    max_items_dropdown = 2  # Nombre max d'items visibles
    
    # État du scroll
    scroll_offset = 0
    max_scroll = 0

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
    img_rect = None
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
        # Onglet Vaisseaux AMÉLIORÉ
        # -------------------------------
        # Définir les rects en dehors pour éviter les erreurs
        dropdown_x = panneau_x + 10
        dropdown_y = panneau_y + 10
        dropdown_largeur = 200
        dropdown_hauteur = 35
        rect_dropdown = pygame.Rect(dropdown_x, dropdown_y, dropdown_largeur, dropdown_hauteur)
        
        liste_rects = []
        tier_rects = []
        param_rects = []
        params_zone_x = panneau_x + 10
        params_zone_y = panneau_y + 120
        
        if onglet_actif == "Vaisseaux":
            # --- DROPDOWN pour sélectionner le vaisseau ---
            pygame.draw.rect(ecran, GRIS_MOYEN, rect_dropdown, border_radius=5)
            pygame.draw.rect(ecran, BLANC, rect_dropdown, 2, border_radius=5)
            
            # Texte du vaisseau sélectionné
            texte_dropdown = police_petite.render(vaisseau_actif, True, BLANC)
            ecran.blit(texte_dropdown, (dropdown_x + 10, dropdown_y + 8))
            
            # Flèche dropdown
            fleche = "▼" if not dropdown_ouvert else "▲"
            texte_fleche = police_petite.render(fleche, True, BLANC)
            ecran.blit(texte_fleche, (dropdown_x + dropdown_largeur - 30, dropdown_y + 8))
            
            # Liste déroulante si ouverte
            liste_rects = []
            if dropdown_ouvert:
                # Calculer les items visibles avec scroll
                total_items = len(types_vaisseaux)
                max_dropdown_scroll = max(0, total_items - max_items_dropdown)
                dropdown_scroll = max(0, min(dropdown_scroll, max_dropdown_scroll))
                
                items_visibles = types_vaisseaux[dropdown_scroll:dropdown_scroll + max_items_dropdown]
                
                for i, ship in enumerate(items_visibles):
                    rect_item = pygame.Rect(dropdown_x, dropdown_y + dropdown_hauteur + i * 30, dropdown_largeur, 30)
                    liste_rects.append((rect_item, ship))
                    
                    couleur = BLEU_ACCENT if ship == vaisseau_actif else GRIS_FONCE
                    pygame.draw.rect(ecran, couleur, rect_item)
                    pygame.draw.rect(ecran, GRIS_CLAIR, rect_item, 1)
                    
                    texte_item = police_petite.render(ship, True, BLANC)
                    ecran.blit(texte_item, (rect_item.x + 10, rect_item.y + 5))
                
                # Indicateur de scroll si nécessaire
                if total_items > max_items_dropdown:
                    scroll_indicator_x = dropdown_x + dropdown_largeur - 15
                    scroll_indicator_y = dropdown_y + dropdown_hauteur + 5
                    scroll_indicator_h = max_items_dropdown * 30 - 10
                    
                    # Barre de scroll
                    pygame.draw.rect(ecran, GRIS_MOYEN, 
                                   (scroll_indicator_x, scroll_indicator_y, 8, scroll_indicator_h), 
                                   border_radius=4)
                    
                    # Curseur de scroll
                    scroll_ratio = dropdown_scroll / max_dropdown_scroll if max_dropdown_scroll > 0 else 0
                    cursor_h = 20
                    cursor_y = scroll_indicator_y + int(scroll_ratio * (scroll_indicator_h - cursor_h))
                    pygame.draw.rect(ecran, BLEU_ACCENT, 
                                   (scroll_indicator_x, cursor_y, 8, cursor_h), 
                                   border_radius=4)
            
            # --- ICÔNE du vaisseau ---
            icone_x = dropdown_x + dropdown_largeur + 20
            icone_y = panneau_y + 10
            icone_taille = 80
            
            pygame.draw.rect(ecran, BLANC, (icone_x, icone_y, icone_taille, icone_taille), 2, border_radius=5)
            img_vaisseau = icones_vaisseaux[vaisseau_actif]
            img_rect = img_vaisseau.get_rect(center=(icone_x + icone_taille//2, icone_y + icone_taille//2))
            ecran.blit(img_vaisseau, img_rect.topleft)
            
            # --- SÉLECTEUR DE TIER (si MotherShip) - À CÔTÉ de l'icône ---
            tier_rects = []
            if vaisseau_actif == "MotherShip":
                # Positionner les tiers à droite de l'icône
                tier_x_start = icone_x + icone_taille + 20
                tier_y_start = icone_y + 25
                
                texte_tier_label = police_petite.render("Tier:", True, BLANC)
                ecran.blit(texte_tier_label, (tier_x_start, tier_y_start))
                
                # Disposition horizontale des tiers
                for i, tier in enumerate([1, 2, 3, 4]):
                    tier_rect = pygame.Rect(tier_x_start + 60 + i * 40, tier_y_start, 35, 30)
                    tier_rects.append((tier_rect, tier))
                    
                    couleur = BLEU_ACCENT if tier == tier_actif else GRIS_MOYEN
                    pygame.draw.rect(ecran, couleur, tier_rect, border_radius=5)
                    
                    texte_tier = police_petite.render(str(tier), True, BLANC)
                    ecran.blit(texte_tier, texte_tier.get_rect(center=tier_rect.center))
            
            # --- ZONE SCROLLABLE pour les paramètres ---
            params_zone_x = panneau_x + 10
            params_zone_y = panneau_y + 120
            params_zone_largeur = panneau_largeur - 20
            params_zone_hauteur = panneau_hauteur - 130
            
            # Surface pour le contenu scrollable
            surf_scroll = pygame.Surface((params_zone_largeur, params_zone_hauteur))
            surf_scroll.fill(GRIS_FONCE)
            
            # Récupérer les paramètres du vaisseau actuel
            if vaisseau_actif == "MotherShip":
                params_vaisseau = vaisseaux_sliders[vaisseau_actif][tier_actif]
            else:
                params_vaisseau = vaisseaux_sliders[vaisseau_actif]
            
            # Déterminer les paramètres qui utilisent des boutons vs sliders
            params_avec_boutons = ["taille_largeur", "taille_hauteur", "nb_vaisseaux", "port_attaque", "port_deplacement"]
            
            y_offset = 10 - scroll_offset
            param_rects = []  # Pour stocker les zones cliquables
            
            displayed_idx = 0  # Compteur pour les paramètres affichés uniquement
            for idx, (param, valeur) in enumerate(params_vaisseau.items()):
                if param in ["peut_miner", "peut_transporter", "taille"]:
                    continue  # Skip les booléens et taille (tuple)
                
                y_pos = y_offset + displayed_idx * 85  # Utiliser displayed_idx au lieu de idx
                displayed_idx += 1  # Incrémenter seulement pour les params affichés
                
                # Si en dehors de la zone visible, skip le dessin mais calculer la hauteur totale
                if y_pos < -85 or y_pos > params_zone_hauteur:
                    continue
                
                # Nom du paramètre avec affichage lisible
                nom_affiche = noms_affichage.get(param, param)
                texte_nom = police_petite.render(nom_affiche, True, BLANC)
                surf_scroll.blit(texte_nom, (10, y_pos))
                
                # Valeur
                texte_val = police_petite.render(str(valeur), True, BLEU_ACCENT)
                surf_scroll.blit(texte_val, (10, y_pos + 22))
                
                min_val = limites_params[param]["min"]
                max_val = limites_params[param]["max"]
                
                # Choix entre boutons +/- ou slider
                if param in params_avec_boutons:
                    # BOUTONS +/-
                    btn_moins_rect = pygame.Rect(200, y_pos + 15, 30, 30)
                    btn_plus_rect = pygame.Rect(340, y_pos + 15, 30, 30)
                    
                    pygame.draw.rect(surf_scroll, GRIS_MOYEN, btn_moins_rect, border_radius=5)
                    pygame.draw.rect(surf_scroll, GRIS_MOYEN, btn_plus_rect, border_radius=5)
                    
                    texte_moins = police_param.render("-", True, BLANC)
                    texte_plus = police_param.render("+", True, BLANC)
                    surf_scroll.blit(texte_moins, texte_moins.get_rect(center=btn_moins_rect.center))
                    surf_scroll.blit(texte_plus, texte_plus.get_rect(center=btn_plus_rect.center))
                    
                    # Valeur au centre
                    texte_val_centre = police_param.render(str(valeur), True, VERT)
                    val_rect = texte_val_centre.get_rect(center=(285, y_pos + 30))
                    surf_scroll.blit(texte_val_centre, val_rect)
                    
                    # Stocker les rects pour la détection de clic (ajuster avec offset de la zone)
                    param_rects.append((btn_moins_rect, param, "moins", y_offset))
                    param_rects.append((btn_plus_rect, param, "plus", y_offset))
                    
                else:
                    # SLIDER
                    slider_x_local = 200
                    slider_largeur_local = 250
                    slider_hauteur_local = 15
                    
                    # Dessiner le slider sur la surface
                    pygame.draw.rect(surf_scroll, GRIS_MOYEN, 
                                   (slider_x_local, y_pos + 25, slider_largeur_local, slider_hauteur_local), 
                                   border_radius=8)
                    
                    rel_pos = (valeur - min_val) / (max_val - min_val) if max_val > min_val else 0
                    largeur_prog = int(rel_pos * slider_largeur_local)
                    if largeur_prog > 0:
                        pygame.draw.rect(surf_scroll, VERT, 
                                       (slider_x_local, y_pos + 25, largeur_prog, slider_hauteur_local), 
                                       border_radius=8)
                    
                    curseur_x_local = int(slider_x_local + rel_pos * slider_largeur_local)
                    pygame.draw.ellipse(surf_scroll, VERT_FONCE, 
                                      (curseur_x_local - 8, y_pos + 20, 16, slider_hauteur_local + 10))
                    
                    # Stocker le rect pour la détection
                    slider_rect = pygame.Rect(slider_x_local, y_pos + 20, slider_largeur_local, 30)
                    param_rects.append((slider_rect, param, "slider", y_offset))
            
            # Calculer max_scroll avec le nombre réel de paramètres affichés
            nb_params_affiches = len([p for p in params_vaisseau.keys() if p not in ["peut_miner", "peut_transporter", "taille"]])
            hauteur_contenu = nb_params_affiches * 85
            max_scroll = max(0, hauteur_contenu - params_zone_hauteur + 20)
            
            # Clipper et afficher la surface
            ecran.set_clip(pygame.Rect(params_zone_x, params_zone_y, params_zone_largeur, params_zone_hauteur))
            ecran.blit(surf_scroll, (params_zone_x, params_zone_y))
            ecran.set_clip(None)
            
            # Bordure de la zone
            pygame.draw.rect(ecran, GRIS_CLAIR, 
                           (params_zone_x, params_zone_y, params_zone_largeur, params_zone_hauteur), 2)

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
                
            # MOLETTE pour scroll
            if event.type == pygame.MOUSEWHEEL:
                if onglet_actif == "Vaisseaux":
                    # Si dropdown ouvert, scroll le dropdown
                    if dropdown_ouvert:
                        dropdown_scroll -= event.y
                        max_dropdown_scroll = max(0, len(types_vaisseaux) - max_items_dropdown)
                        dropdown_scroll = max(0, min(dropdown_scroll, max_dropdown_scroll))
                    else:
                        # Sinon scroll la zone de paramètres
                        scroll_offset -= event.y * 20
                        scroll_offset = max(0, min(scroll_offset, max_scroll))
                
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Boutons bas
                for _, rect, label in boutons:
                    if rect.collidepoint(event.pos):
                        if label == "JOUER":
                            print("JOUER avec parametres:", {k: v["valeur"] for k, v in parametres.items()},
                                  "Random:", random_active)
                            print("Vaisseau :", vaisseau_actif)
                            if vaisseau_actif == "MotherShip":
                                print("Tier:", tier_actif, vaisseaux_sliders[vaisseau_actif][tier_actif])
                            else:
                                print(vaisseaux_sliders[vaisseau_actif])
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
                        if random_active:
                            for k in parametres:
                                parametres[k]["valeur"] = random.randint(parametres[k]["min"], parametres[k]["max"])
                
                # Onglets
                for i, nom in enumerate(onglets):
                    rect_onglet = pygame.Rect(panneau_x + i * (panneau_largeur // len(onglets)), panneau_y - 50,
                                              panneau_largeur // len(onglets), 40)
                    if rect_onglet.collidepoint(event.pos):
                        onglet_actif = nom
                        scroll_offset = 0  # Reset scroll
                        dropdown_scroll = 0  # Reset scroll dropdown
                        dropdown_ouvert = False  # Fermer dropdown
                
                # --- VAISSEAUX: Gestion des clics ---
                if onglet_actif == "Vaisseaux":
                    # Clic sur dropdown
                    if rect_dropdown.collidepoint(event.pos):
                        dropdown_ouvert = not dropdown_ouvert
                    
                    # Clic sur liste déroulante
                    elif dropdown_ouvert:
                        for rect_item, ship in liste_rects:
                            if rect_item.collidepoint(event.pos):
                                vaisseau_actif = ship
                                tier_actif = 1  # Reset tier
                                scroll_offset = 0
                                dropdown_scroll = 0  # Reset scroll dropdown
                                dropdown_ouvert = False
                                break
                    
                    # Clic sur tier (MotherShip)
                    if vaisseau_actif == "MotherShip":
                        for tier_rect, tier in tier_rects:
                            if tier_rect.collidepoint(event.pos):
                                tier_actif = tier
                                scroll_offset = 0
                                break
                    
                    # Clic sur boutons +/- ou sliders
                    for rect_param, param, action, y_off in param_rects:
                        # Ajuster la position du rect avec l'offset de la zone scrollable
                        rect_ajuste = rect_param.copy()
                        rect_ajuste.x += params_zone_x
                        rect_ajuste.y += params_zone_y
                        
                        if rect_ajuste.collidepoint(event.pos):
                            if vaisseau_actif == "MotherShip":
                                params = vaisseaux_sliders[vaisseau_actif][tier_actif]
                            else:
                                params = vaisseaux_sliders[vaisseau_actif]
                            
                            min_val = limites_params[param]["min"]
                            max_val = limites_params[param]["max"]
                            
                            if action == "moins":
                                params[param] = max(min_val, params[param] - 1)
                            elif action == "plus":
                                params[param] = min(max_val, params[param] + 1)
                            elif action == "slider":
                                slider_vaisseau_actif = param
                                # Appliquer immédiatement
                                rel_x = max(0, min(rect_param.width, event.pos[0] - rect_ajuste.x))
                                nouveau_val = int(min_val + (rel_x / rect_param.width) * (max_val - min_val))
                                params[param] = nouveau_val
                            break
                    
                    # Fermer dropdown si clic ailleurs
                    if dropdown_ouvert and not rect_dropdown.collidepoint(event.pos):
                        clic_sur_liste = False
                        for rect_item, _ in liste_rects:
                            if rect_item.collidepoint(event.pos):
                                clic_sur_liste = True
                                break
                        if not clic_sur_liste:
                            dropdown_ouvert = False
                            dropdown_scroll = 0  # Reset scroll

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                slider_vaisseau_actif = None
        
        # Glisser slider Vaisseaux
        if slider_vaisseau_actif and clic and onglet_actif == "Vaisseaux":
            for rect_param, param, action, y_off in param_rects:
                if param == slider_vaisseau_actif and action == "slider":
                    rect_ajuste = rect_param.copy()
                    rect_ajuste.x += params_zone_x
                    rect_ajuste.y += params_zone_y
                    
                    if vaisseau_actif == "MotherShip":
                        params = vaisseaux_sliders[vaisseau_actif][tier_actif]
                    else:
                        params = vaisseaux_sliders[vaisseau_actif]
                    
                    min_val = limites_params[param]["min"]
                    max_val = limites_params[param]["max"]
                    rel_x = max(0, min(rect_param.width, souris[0] - rect_ajuste.x))
                    nouveau_val = int(min_val + (rel_x / rect_param.width) * (max_val - min_val))
                    params[param] = nouveau_val
                    break

        # Curseur
        ecran.blit(curseur_img, souris)

        pygame.display.flip()
        horloge.tick(60)
    
    if lancer_partie == True:
        ShipAnimator.clear_list()
        PlanetAnimator.clear_list()
        from main import start_game
        start_game(ecran, parametres, random_active)
