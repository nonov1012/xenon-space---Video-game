import pygame

def main(ecran):
    """Menu Parametres avec sliders et checkbox"""

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
    # Parametres
    # -------------------------------
    parametres = {
        "General": {"valeur": 50, "min": 0, "max": 100},
        "Musique": {"valeur": 50, "min": 0, "max": 100},
        "Son": {"valeur": 50, "min": 0, "max": 100},
    }

    checkbox = {"label": "Case visible", "checked": False}
    checkbox_rect = None

    # -------------------------------
    # Curseur personnalisé
    # -------------------------------
    curseur_img = pygame.image.load('assets/img/menu/cursor.png')
    curseur_img = pygame.transform.scale(curseur_img, (40, 40))
    pygame.mouse.set_visible(False)

    # -------------------------------
    # Fond
    # -------------------------------
    largeur_ecran, hauteur_ecran = ecran.get_size()
    image_fond = pygame.image.load("assets/img/menu/fond_start.jpg").convert()
    image_fond = pygame.transform.scale(image_fond, (largeur_ecran, hauteur_ecran))

    # -------------------------------
    # Boutons (JOUER / RESET / RETOUR)
    # -------------------------------
    image_bouton_base = pygame.image.load("assets/img/menu/bouton_menu.png").convert_alpha()
    def creer_image_bouton(largeur, hauteur):
        return pygame.transform.scale(image_bouton_base, (largeur, hauteur))

    texte_jouer = police_bouton.render("JOUER", True, BLANC)
    texte_reset = police_bouton.render("RESET", True, BLANC)
    texte_retour = police_bouton.render("RETOUR MENU", True, BLANC)

    image_jouer = creer_image_bouton(texte_jouer.get_width() + 100, texte_jouer.get_height() + 100)
    image_reset = creer_image_bouton(texte_reset.get_width() + 120, texte_reset.get_height() + 100)
    image_retour = creer_image_bouton(texte_retour.get_width() + 200, texte_retour.get_height() + 100)

    espacement_boutons = 80
    y_premiere_ligne = hauteur_ecran - 210  # remonté de 30px
    y_deuxieme_ligne = hauteur_ecran - 120  # remonté de 30px
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
    # Panneau
    # -------------------------------
    panneau_largeur = 650
    panneau_hauteur = 450
    panneau_x = (largeur_ecran - panneau_largeur) // 2
    panneau_y = 150

    # -------------------------------
    # Boucle principale
    # -------------------------------
    slider_actif = None
    horloge = pygame.time.Clock()
    en_cours = True

    while en_cours:
        souris = pygame.mouse.get_pos()
        clic = pygame.mouse.get_pressed()[0]

        # Fond
        ecran.blit(image_fond, (0, 0))

        # Titre
        titre_surface = police_titre.render("Parametres", True, BLANC)
        rect_titre = titre_surface.get_rect(center=(largeur_ecran // 2, 60))
        ecran.blit(titre_surface, rect_titre.topleft)

        # Panneau
        pygame.draw.rect(ecran, GRIS_FONCE, (panneau_x, panneau_y, panneau_largeur, panneau_hauteur), border_radius=15)
        pygame.draw.rect(ecran, GRIS_MOYEN, (panneau_x, panneau_y, panneau_largeur, panneau_hauteur), 2, border_radius=15)

        # Sliders
        slider_largeur = 400
        slider_hauteur = 15
        slider_x = panneau_x + (panneau_largeur - slider_largeur) // 2
        decalage_y = 70

        for idx, (nom, val) in enumerate(parametres.items()):
            y_courant = panneau_y + decalage_y + idx * 100

            # Texte et valeur
            texte_param = police_param.render(nom, True, BLANC)
            rect_param = texte_param.get_rect(center=(largeur_ecran // 2, y_courant - 25))
            ecran.blit(texte_param, rect_param)

            texte_valeur = police_param.render(str(val["valeur"]), True, BLEU_ACCENT)
            rect_valeur = texte_valeur.get_rect(center=(largeur_ecran // 2, y_courant))
            ecran.blit(texte_valeur, rect_valeur)

            # Slider
            rect_slider = pygame.Rect(slider_x, y_courant + 30, slider_largeur, slider_hauteur)
            pygame.draw.rect(ecran, GRIS_MOYEN, rect_slider, border_radius=8)

            rel_pos = (val["valeur"] - val["min"]) / (val["max"] - val["min"])
            largeur_prog = int(rel_pos * slider_largeur)
            if largeur_prog > 0:
                pygame.draw.rect(ecran, VERT, (slider_x, y_courant + 30, largeur_prog, slider_hauteur), border_radius=8)

            curseur_x = int(slider_x + rel_pos * slider_largeur)
            rect_curseur = pygame.Rect(curseur_x - 12, y_courant + 22, 24, slider_hauteur + 16)
            pygame.draw.ellipse(ecran, VERT_FONCE, rect_curseur)
            pygame.draw.ellipse(ecran, VERT, (curseur_x - 10, y_courant + 24, 20, slider_hauteur + 12))

        # Checkbox
        checkbox_y = panneau_y + decalage_y + len(parametres) * 100
        checkbox_rect = pygame.Rect(panneau_x + 50, checkbox_y, 30, 30)
        pygame.draw.rect(ecran, GRIS_MOYEN, checkbox_rect, border_radius=5)
        if checkbox["checked"]:
            pygame.draw.rect(ecran, VERT, checkbox_rect.inflate(-6, -6), border_radius=3)
        texte_checkbox = police_param.render(checkbox["label"], True, BLANC)
        ecran.blit(texte_checkbox, (checkbox_rect.right + 10, checkbox_rect.y + 2))

        # Boutons principaux
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

        # Evenements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                en_cours = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Slider actif
                for idx, (nom, val) in enumerate(parametres.items()):
                    y_courant = panneau_y + decalage_y + idx * 100
                    curseur_x = slider_x + int((val["valeur"] - val["min"]) / (val["max"] - val["min"]) * slider_largeur)
                    rect_curseur = pygame.Rect(curseur_x - 12, y_courant + 22, 24, slider_hauteur + 16)
                    if rect_curseur.collidepoint(event.pos):
                        slider_actif = nom
                # Checkbox
                if checkbox_rect.collidepoint(event.pos):
                    checkbox["checked"] = not checkbox["checked"]
                # Boutons
                for _, rect, label in boutons:
                    if rect.collidepoint(event.pos):
                        if label == "JOUER":
                            print("Sliders :", {k: v['valeur'] for k, v in parametres.items()})
                            print("Checkbox :", checkbox["checked"])
                        elif label == "RESET":
                            for val in parametres.values():
                                val["valeur"] = val["min"]
                            checkbox["checked"] = False
                        elif label == "RETOUR MENU":
                            en_cours = False
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                slider_actif = None

        # Glisser slider
        if slider_actif and clic:
            val = parametres[slider_actif]
            rel_x = max(0, min(slider_largeur, souris[0] - slider_x))
            val["valeur"] = int(val["min"] + (rel_x / slider_largeur) * (val["max"] - val["min"]))

        # Curseur
        ecran.blit(curseur_img, souris)

        pygame.display.flip()
        horloge.tick(60)
