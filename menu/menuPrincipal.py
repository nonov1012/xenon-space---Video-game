import pygame
import sys
from titreAnime import TitreAnime 

pygame.init()

# fenêtre plein écran
ecran = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Xenon Space")

# icone
icone = pygame.image.load("Images/logo.png")
pygame.display.set_icon(icone)

# fond
fond = pygame.image.load("Images/fond.png").convert()
fond = pygame.transform.scale(fond, ecran.get_size())

# Création du titre animé
police_titre = pygame.font.Font("Fonts/SPINC.ttf", 100)
titre = TitreAnime("XENON-SPACE", police_titre, (ecran.get_width()//2, 200),
                   couleur_haut=(255,255,0), couleur_bas=(255,0,255))

# couleur et police pour le texte des boutons
blanc = (255, 255, 255)
police = pygame.font.Font("Fonts/SPINC.ttf", 25)

# taille des boutons
largeur_bouton = 160
hauteur_bouton = 50

# Centrer bouton au milieu de l'écran
x_bouton = ecran.get_width() // 2 - largeur_bouton // 2
y_bouton = ecran.get_height() // 2

# Créer les textes des boutons
texte_jouer = police.render("Jouer", True, blanc)
texte_param = police.render("Parametre", True, blanc)
texte_succes = police.render("Succes", True, blanc)
texte_quitter = police.render("Quitter", True, blanc)

# Définir les positions des boutons
bouton_jouer = pygame.Rect(x_bouton, y_bouton - 120, largeur_bouton, hauteur_bouton)
bouton_param = pygame.Rect(x_bouton, y_bouton - 50 , largeur_bouton, hauteur_bouton)
bouton_succes = pygame.Rect(x_bouton, y_bouton + 20, largeur_bouton, hauteur_bouton)
bouton_quitter = pygame.Rect(x_bouton, y_bouton + 90, largeur_bouton, hauteur_bouton)

# Charger l'image du bouton
image_bouton = pygame.image.load("Images/bouton_menu.png").convert_alpha()
image_bouton = pygame.transform.scale(image_bouton, (largeur_bouton + 50, hauteur_bouton + 50))

# -------------------------------
# Boucle principale
# -------------------------------
clock = pygame.time.Clock()
en_cours = True
while en_cours:
    ecran.blit(fond, (0, 0))

    # dessiner le titre animé
    titre.draw(ecran)

    souris = pygame.mouse.get_pos()

    # afficher chaque bouton avec image et effet survol
    for bouton in [bouton_jouer, bouton_param, bouton_succes, bouton_quitter]:
        if bouton.collidepoint(souris):

            # copie de l'image pour survol et effet léger
            bouton_survol = image_bouton.copy()
            bouton_survol.fill((50, 50, 50, 50), special_flags=pygame.BLEND_RGBA_ADD)
            ecran.blit(bouton_survol, bouton.topleft)
        else:
            ecran.blit(image_bouton, bouton.topleft)

    # afficher le texte au centre de chaque bouton
    ecran.blit(texte_jouer, texte_jouer.get_rect(center=bouton_jouer.center))
    ecran.blit(texte_param, texte_param.get_rect(center=bouton_param.center))
    ecran.blit(texte_succes, texte_succes.get_rect(center=bouton_succes.center))
    ecran.blit(texte_quitter, texte_quitter.get_rect(center=bouton_quitter.center))

    pygame.display.flip()
    clock.tick(60)

    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            en_cours = False
        if evenement.type == pygame.MOUSEBUTTONDOWN:
            if bouton_quitter.collidepoint(evenement.pos):
                pygame.quit()
                sys.exit()
