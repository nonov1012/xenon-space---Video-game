import pygame

def main(screen):
    """Le 'mode jeu' s'exécute dans la même fenêtre que le menu principal"""

    # -------------------------------
    # Couleurs et polices
    # -------------------------------
    blanc = (255, 255, 255)
    gris = (150, 150, 150)
    vert = (0, 255, 0)
    font_titre = pygame.font.Font("assets/fonts/SpaceNova.otf", 60)
    police = pygame.font.Font("assets/fonts/SpaceNova.otf", 30)

    # -------------------------------
    # Paramètres avec sliders
    # -------------------------------
    params = {
        "Nombre de planètes": {"val": 3, "min": 1, "max": 10, "y": 150},
        "Nombre d'astéroïdes": {"val": 5, "min": 1, "max": 20, "y": 220}
    }

    # -------------------------------
    # Curseur personnalisé
    # -------------------------------
    new_cursor = pygame.image.load('assets/img/menu/cursor.png')
    new_cursor = pygame.transform.scale(new_cursor, (40, 40))
    pygame.mouse.set_visible(False)

    # -------------------------------
    # Image de bouton de base
    # -------------------------------
    base_image = pygame.image.load("assets/img/menu/bouton_menu.png").convert_alpha()

    window_width, window_height = screen.get_size()

    # -------------------------------
    # Padding pour bouton
    # -------------------------------
    padding_x = 70
    padding_y = 50
    espacement_boutons = 50  # espace entre JOUER et RÉINITIALISER

    # -------------------------------
    # Fonction pour créer image bouton adaptée au texte
    # -------------------------------
    def create_button_image(text_surface):
        largeur = text_surface.get_width() + padding_x * 2
        hauteur = text_surface.get_height() + padding_y * 2
        return pygame.transform.scale(base_image, (largeur, hauteur))

    # -------------------------------
    # Texte et boutons
    # -------------------------------
    texte_jouer_render = police.render("JOUER", True, blanc)
    image_jouer = create_button_image(texte_jouer_render)
    texte_reset_render = police.render("REINITIALISER", True, blanc)
    image_reset = create_button_image(texte_reset_render)
    texte_retour_render = police.render("RETOUR AU MENU PRINCIPAL", True, blanc)
    image_retour = create_button_image(texte_retour_render)

    # Position des boutons JOUER et RÉINITIALISER côte à côte, centrés
    total_width = image_jouer.get_width() + image_reset.get_width() + espacement_boutons
    x_start = window_width // 2 - total_width // 2
    y_boutons = window_height - 180

    bouton_jouer_rect = image_jouer.get_rect(topleft=(x_start, y_boutons))
    bouton_reset_rect = image_reset.get_rect(topleft=(x_start + image_jouer.get_width() + espacement_boutons, y_boutons))

    # Bouton RETOUR au menu en bas
    bouton_retour_rect = image_retour.get_rect(center=(window_width//2, window_height - 50))

    # -------------------------------
    # Boucle principale
    # -------------------------------
    dragging_slider = None
    clock = pygame.time.Clock()
    en_cours = True
    while en_cours:
        souris = pygame.mouse.get_pos()
        clic = pygame.mouse.get_pressed()[0]

        screen.fill((0,0,0))  # Fond noir

        # Titre
        texte_titre = font_titre.render("Personnalisation", True, blanc)
        rect_titre = texte_titre.get_rect(center=(window_width//2, 50))
        screen.blit(texte_titre, rect_titre.topleft)

        # Sliders
        for key, val in params.items():
            texte_param = police.render(f"{key}: {val['val']}", True, blanc)
            screen.blit(texte_param, (50, val["y"] - 30))

            slider_x = 50
            slider_y = val["y"]
            pygame.draw.rect(screen, gris, (slider_x, slider_y, 300, 10), border_radius=8)

            rel_pos = (val["val"] - val["min"]) / (val["max"] - val["min"])
            curseur_x = int(slider_x + rel_pos * 300)
            curseur_rect = pygame.Rect(curseur_x - 10, slider_y - 5, 20, 20)
            pygame.draw.rect(screen, vert, curseur_rect, border_radius=5)

            if clic and curseur_rect.collidepoint(souris):
                dragging_slider = key

        if dragging_slider and clic:
            val = params[dragging_slider]
            rel_x = max(0, min(300, souris[0] - 50))
            val["val"] = int(val["min"] + (rel_x / 300) * (val["max"] - val["min"]))
        if not clic:
            dragging_slider = None

        # Dessin des boutons avec image + texte
        for image, rect, texte in [(image_jouer, bouton_jouer_rect, texte_jouer_render),
                                   (image_reset, bouton_reset_rect, texte_reset_render),
                                   (image_retour, bouton_retour_rect, texte_retour_render)]:
            screen.blit(image, rect.topleft)
            texte_rect = texte.get_rect(center=rect.center)
            screen.blit(texte, texte_rect.topleft)

        # Événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                en_cours = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if bouton_jouer_rect.collidepoint(event.pos):
                    print("JOUER avec paramètres:", {k:v['val'] for k,v in params.items()})
                if bouton_reset_rect.collidepoint(event.pos):
                    for k in params:
                        params[k]["val"] = params[k]["min"]
                if bouton_retour_rect.collidepoint(event.pos):
                    en_cours = False

        # Curseur personnalisé
        screen.blit(new_cursor, souris)

        pygame.display.flip()
        clock.tick(60)
