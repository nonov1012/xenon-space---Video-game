import pygame
import json
import os
from classes.ShipAnimator import ShipAnimator
from classes.PlanetAnimator import PlanetAnimator
from classes.Animator import Animator
from classes.Start_Animation.main import create_space_background

def main(ecran):
    """Menu Succès avec fond animé et grille d'images"""

    # -------------------------------
    # Couleurs et polices
    # -------------------------------
    BLANC = (255, 255, 255)
    GRIS_FONCE = (40, 40, 55)
    GRIS_MOYEN = (90, 90, 110)
    GRIS_CLAIR = (180, 180, 200)
    OR = (255, 200, 0)
    BLEU_ACCENT = (70, 130, 255)
    NOIR_TRANSPARENT = (0, 0, 0, 180)

    police_titre = pygame.font.Font("assets/fonts/SpaceNova.otf", 60)
    police_succes = pygame.font.Font("assets/fonts/SpaceNova.otf", 22)
    police_desc = pygame.font.Font("assets/fonts/SpaceNova.otf", 16)
    police_bouton = pygame.font.Font("assets/fonts/SpaceNova.otf", 24)

    # -------------------------------
    # Fond animé (comme menu personnalisation)
    # -------------------------------
    largeur_ecran, hauteur_ecran = ecran.get_size()
    screen_ratio = (largeur_ecran * 100 / 600) / 100
    
    stars, planet_manager, vaisseau_fond = create_space_background(
        num_stars=100, 
        screen_ratio=screen_ratio
    )

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
    # Chargement des succès depuis JSON
    # -------------------------------
    succes_liste = []
    
    # Chemin relatif depuis le fichier menuSucces.py qui est dans menu/
    chemin_json = os.path.join(os.path.dirname(__file__), "succes.json")
    
    try:
        with open(chemin_json, "r", encoding="utf-8") as f:
            succes_liste = json.load(f)
        print(f"Succes charges depuis : {chemin_json}")
        print(f"Nombre de succes : {len(succes_liste)}")
        # Afficher les ID pour vérifier
        for s in succes_liste:
            print(f"  - {s['id']}: {s['titre']} (debloque: {s['debloque']})")
    except FileNotFoundError:
        print(f"Fichier non trouve : {chemin_json}")
        succes_liste = []
    except json.JSONDecodeError as e:
        print(f"Erreur de parsing JSON : {e}")
        succes_liste = []
    except Exception as e:
        print(f"Erreur lors du chargement : {e}")
        succes_liste = []

    # Chargement des images des succès
    succes_images = {}
    for succes in succes_liste:
        chemin_img = succes.get("image", "")
        if os.path.exists(chemin_img):
            try:
                img = pygame.image.load(chemin_img).convert_alpha()
                succes_images[succes["id"]] = pygame.transform.scale(img, (120, 120))
                print(f"✅ Image chargée : {chemin_img}")
            except Exception as e:
                print(f"❌ Erreur chargement image {chemin_img} : {e}")
                placeholder = pygame.Surface((120, 120))
                placeholder.fill((100, 100, 100))
                succes_images[succes["id"]] = placeholder
        else:
            # Image placeholder si fichier manquant
            placeholder = pygame.Surface((120, 120))
            placeholder.fill((100, 100, 100))
            succes_images[succes["id"]] = placeholder
            print(f"⚠️ Image non trouvée : {chemin_img} (utilisation placeholder)")

    # -------------------------------
    # Configuration de la grille
    # -------------------------------
    panneau_largeur = 800
    panneau_hauteur = 500
    panneau_x = (largeur_ecran - panneau_largeur) // 2
    panneau_y = 150

    # Grille : 3 colonnes
    colonnes = 3
    espacement = 30
    taille_case = 140
    marge_gauche = (panneau_largeur - (colonnes * taille_case + (colonnes - 1) * espacement)) // 2

    # Calcul des positions des succès
    succes_rects = []
    for idx, succes in enumerate(succes_liste):
        col = idx % colonnes
        ligne = idx // colonnes
        x = panneau_x + marge_gauche + col * (taille_case + espacement)
        y = panneau_y + 40 + ligne * (taille_case + espacement)
        succes_rects.append((pygame.Rect(x, y, taille_case, taille_case), succes))

    # Scroll
    scroll_offset = 0
    nb_lignes = (len(succes_liste) + colonnes - 1) // colonnes
    hauteur_contenu = nb_lignes * (taille_case + espacement) + 40
    max_scroll = max(0, hauteur_contenu - panneau_hauteur + 60)

    horloge = pygame.time.Clock()
    en_cours = True
    succes_survole = None

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

        # Titre
        titre_surface = police_titre.render("SUCCES", True, OR)
        rect_titre = titre_surface.get_rect(center=(largeur_ecran // 2, 60))
        ecran.blit(titre_surface, rect_titre.topleft)

        # Panneau
        pygame.draw.rect(ecran, GRIS_FONCE, (panneau_x, panneau_y, panneau_largeur, panneau_hauteur), border_radius=15)
        pygame.draw.rect(ecran, GRIS_MOYEN, (panneau_x, panneau_y, panneau_largeur, panneau_hauteur), 3, border_radius=15)

        # Zone clippée pour le scroll
        zone_scroll = pygame.Rect(panneau_x, panneau_y, panneau_largeur, panneau_hauteur)
        ecran.set_clip(zone_scroll)

        # Affichage de la grille de succès
        succes_survole = None
        for rect_succes, succes in succes_rects:
            # Appliquer le scroll
            rect_affiche = rect_succes.copy()
            rect_affiche.y -= scroll_offset

            # Ne dessiner que si visible
            if rect_affiche.bottom < panneau_y or rect_affiche.top > panneau_y + panneau_hauteur:
                continue

            # Vérifier le survol
            est_survole = rect_affiche.collidepoint(souris)
            if est_survole:
                succes_survole = succes

            # Couleur de fond selon état
            if succes["debloque"]:
                couleur_fond = BLEU_ACCENT
                couleur_bordure = OR
            else:
                couleur_fond = GRIS_MOYEN
                couleur_bordure = GRIS_CLAIR

            # Effet de survol
            if est_survole:
                rect_hover = rect_affiche.inflate(10, 10)
                pygame.draw.rect(ecran, OR, rect_hover, border_radius=10)

            # Fond du succès
            pygame.draw.rect(ecran, couleur_fond, rect_affiche, border_radius=10)
            pygame.draw.rect(ecran, couleur_bordure, rect_affiche, 3, border_radius=10)

            # Image du succès
            img = succes_images[succes["id"]]
            img_rect = img.get_rect(center=rect_affiche.center)
            ecran.blit(img, img_rect)

            # Si non débloqué, assombrir
            if not succes["debloque"]:
                overlay = pygame.Surface((taille_case, taille_case), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 150))
                ecran.blit(overlay, rect_affiche.topleft)

                # Cadenas
                police_cadenas = pygame.font.Font("assets/fonts/SpaceNova.otf", 50)
                texte_cadenas = police_cadenas.render("🔒", True, BLANC)
                rect_cadenas = texte_cadenas.get_rect(center=rect_affiche.center)
                ecran.blit(texte_cadenas, rect_cadenas)

        ecran.set_clip(None)

        # Tooltip au survol
        if succes_survole:
            # Créer une surface semi-transparente pour le tooltip
            tooltip_largeur = 350
            tooltip_hauteur = 100
            tooltip_x = min(souris[0] + 20, largeur_ecran - tooltip_largeur - 10)
            tooltip_y = min(souris[1] + 20, hauteur_ecran - tooltip_hauteur - 10)

            # Fond du tooltip
            tooltip_surf = pygame.Surface((tooltip_largeur, tooltip_hauteur), pygame.SRCALPHA)
            pygame.draw.rect(tooltip_surf, NOIR_TRANSPARENT, (0, 0, tooltip_largeur, tooltip_hauteur), border_radius=10)
            pygame.draw.rect(tooltip_surf, OR, (0, 0, tooltip_largeur, tooltip_hauteur), 2, border_radius=10)
            ecran.blit(tooltip_surf, (tooltip_x, tooltip_y))

            # Titre du succès
            titre_surf = police_succes.render(succes_survole["titre"], True, OR)
            ecran.blit(titre_surf, (tooltip_x + 15, tooltip_y + 15))

            # Description (multi-lignes si nécessaire)
            desc = succes_survole["description"]
            mots = desc.split()
            lignes = []
            ligne_actuelle = ""
            
            for mot in mots:
                test_ligne = ligne_actuelle + mot + " "
                if police_desc.size(test_ligne)[0] < tooltip_largeur - 30:
                    ligne_actuelle = test_ligne
                else:
                    if ligne_actuelle:
                        lignes.append(ligne_actuelle)
                    ligne_actuelle = mot + " "
            if ligne_actuelle:
                lignes.append(ligne_actuelle)

            for i, ligne in enumerate(lignes[:2]):  # Max 2 lignes
                desc_surf = police_desc.render(ligne.strip(), True, GRIS_CLAIR)
                ecran.blit(desc_surf, (tooltip_x + 15, tooltip_y + 50 + i * 20))

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

        pygame.display.flip()
        horloge.tick(60)

        # Événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                en_cours = False
            
            # Scroll avec la molette
            elif event.type == pygame.MOUSEWHEEL:
                scroll_offset -= event.y * 30
                scroll_offset = max(0, min(scroll_offset, max_scroll))
            
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if rect_retour.collidepoint(event.pos):
                    en_cours = False

    # Nettoyage
    ShipAnimator.clear_list()
    PlanetAnimator.clear_list()