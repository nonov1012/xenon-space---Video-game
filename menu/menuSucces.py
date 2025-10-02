import pygame

def main(ecran):
    """Menu Succes avec titre et descriptions"""

    # -------------------------------
    # Couleurs et polices
    # -------------------------------
    BLANC = (255, 255, 255)
    GRIS_FONCE = (40, 40, 55)
    GRIS_MOYEN = (90, 90, 110)
    GRIS_CLAIR = (150, 150, 170)
    OR = (255, 200, 0)
    BLEU_ACCENT = (70, 130, 255)

    police_titre = pygame.font.Font("assets/fonts/SpaceNova.otf", 60)
    police_succes = pygame.font.Font("assets/fonts/SpaceNova.otf", 24)  # réduit légèrement
    police_desc = pygame.font.Font("assets/fonts/SpaceNova.otf", 16)    # description plus petite
    police_bouton = pygame.font.Font("assets/fonts/SpaceNova.otf", 24)

    # -------------------------------
    # Fond et curseur
    # -------------------------------
    largeur_ecran, hauteur_ecran = ecran.get_size()
    image_fond = pygame.image.load("assets/img/menu/fond_start.jpg").convert()
    image_fond = pygame.transform.scale(image_fond, (largeur_ecran, hauteur_ecran))

    curseur_img = pygame.image.load('assets/img/menu/cursor.png')
    curseur_img = pygame.transform.scale(curseur_img, (40, 40))
    pygame.mouse.set_visible(False)

    # -------------------------------
    # Bouton Retour
    # -------------------------------
    image_bouton_base = pygame.image.load("assets/img/menu/bouton_menu.png").convert_alpha()
    def creer_image_bouton(largeur, hauteur):
        return pygame.transform.scale(image_bouton_base, (largeur, hauteur))

    texte_retour = police_bouton.render("RETOUR", True, BLANC)
    image_retour = creer_image_bouton(texte_retour.get_width() + 150, texte_retour.get_height() + 80)
    rect_retour = pygame.Rect((largeur_ecran - image_retour.get_width()) // 2,
                              hauteur_ecran - 120,
                              image_retour.get_width(),
                              image_retour.get_height())
    zoom_etat_retour = 1.0
    vitesse_zoom = 0.08

    # -------------------------------
    # Liste des succès
    # -------------------------------
    succes_liste = [
        {"titre": "Premier vol", "description": "Vous avez lance votre vaisseau pour la premiere fois."},
        {"titre": "Maitre des étoiles", "description": "Vous avez collecte toutes les planetes."},
        {"titre": "Champion galactique", "description": "Vous avez termine toutes les missions."},
    ]

    # -------------------------------
    # Panneau des succès
    # -------------------------------
    panneau_largeur = 700
    panneau_hauteur = 500  # agrandi
    panneau_x = (largeur_ecran - panneau_largeur) // 2
    panneau_y = 150

    horloge = pygame.time.Clock()
    en_cours = True

    while en_cours:
        souris = pygame.mouse.get_pos()
        clic = pygame.mouse.get_pressed()[0]

        # Fond
        ecran.blit(image_fond, (0, 0))

        # Titre
        titre_surface = police_titre.render("SUCCES", True, OR)
        rect_titre = titre_surface.get_rect(center=(largeur_ecran // 2, 60))
        ecran.blit(titre_surface, rect_titre.topleft)

        # Panneau
        pygame.draw.rect(ecran, GRIS_FONCE, (panneau_x, panneau_y, panneau_largeur, panneau_hauteur), border_radius=15)
        pygame.draw.rect(ecran, GRIS_MOYEN, (panneau_x, panneau_y, panneau_largeur, panneau_hauteur), 3, border_radius=15)

        # Affichage des succès
        decalage_y = 30
        for idx, s in enumerate(succes_liste):
            y_courant = panneau_y + decalage_y + idx * 130  # espacement plus grand
            # Encadré du succès
            rect_succes = pygame.Rect(panneau_x + 20, y_courant, panneau_largeur - 40, 110)  # encadré plus grand
            pygame.draw.rect(ecran, GRIS_MOYEN, rect_succes, border_radius=10)
            pygame.draw.rect(ecran, BLEU_ACCENT, rect_succes, 2, border_radius=10)

            # Titre du succès
            titre_surf = police_succes.render(s["titre"], True, OR)
            ecran.blit(titre_surf, (rect_succes.x + 15, rect_succes.y + 10))

            # Description
            desc_surf = police_desc.render(s["description"], True, BLANC)
            ecran.blit(desc_surf, (rect_succes.x + 15, rect_succes.y + 50))

        # Bouton Retour
        est_hover = rect_retour.collidepoint(souris)
        cible_zoom = 1.1 if est_hover else 1.0
        zoom_etat_retour += (cible_zoom - zoom_etat_retour) * vitesse_zoom
        image_zoom = pygame.transform.scale(image_retour, (int(image_retour.get_width() * zoom_etat_retour),
                                                           int(image_retour.get_height() * zoom_etat_retour)))
        rect_zoom = image_zoom.get_rect(center=rect_retour.center)
        ecran.blit(image_zoom, rect_zoom.topleft)
        rect_texte = texte_retour.get_rect(center=rect_zoom.center)
        ecran.blit(texte_retour, rect_texte.topleft)

        # Curseur
        ecran.blit(curseur_img, souris)

        pygame.display.flip()
        horloge.tick(60)

        # Evenements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                en_cours = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if rect_retour.collidepoint(event.pos):
                    en_cours = False
