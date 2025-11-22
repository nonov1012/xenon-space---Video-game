import pygame
import json
import os
from classes.ShipAnimator import ShipAnimator
from classes.PlanetAnimator import PlanetAnimator
from classes.Animator import Animator
from classes.Start_Animation.main import create_space_background
from classes.GlobalVar.ScreenVar import ScreenVar

# -------------------------------
# Couleurs
# -------------------------------
class Couleur:
    BLANC = (255, 255, 255)
    GRIS_FONCE = (40, 40, 55)
    GRIS_MOYEN = (90, 90, 110)
    GRIS_CLAIR = (180, 180, 200)
    OR = (255, 200, 0)
    BLEU_ACCENT = (70, 130, 255)
    NOIR_TRANSPARENT = (0, 0, 0, 180)

# -------------------------------
# Police
# -------------------------------
class Police:
    titre = pygame.font.Font("assets/fonts/SpaceNova.otf", 60)
    succes = pygame.font.Font("assets/fonts/SpaceNova.otf", 22)
    desc = pygame.font.Font("assets/fonts/SpaceNova.otf", 16)
    bouton = pygame.font.Font("assets/fonts/SpaceNova.otf", 24)
    cadenas = pygame.font.Font("assets/fonts/SpaceNova.otf", 50)

# -------------------------------
# Menu Succès
# -------------------------------
class MenuSucces:

    def __init__(self):
        self.image_bouton_base = pygame.image.load("assets/img/menu/bouton_menu.png").convert_alpha()
        self.en_cours = False
        self.succes_liste = []
        self.succes_images = {}
        self.succes_rects = []
        self.succes_survole = None
        
        # Scroll
        self.scroll_offset = 0
        self.max_scroll = 0
        
        # Zoom bouton
        self.zoom_etat_retour = 1.0
        self.vitesse_zoom = 0.08

    def update(self):
        """Initialise ou met à jour le menu"""
        self.screen = ScreenVar.screen
        self.screen_width, self.screen_height = self.screen.get_size()
        
        # Curseur personnalisé
        self.curseur_img = pygame.image.load('assets/img/menu/cursor.png')
        self.curseur_img = pygame.transform.scale(self.curseur_img, (40, 40))
        pygame.mouse.set_visible(False)
        
        # Bouton Retour
        self.texte_retour = Police.bouton.render("RETOUR", True, Couleur.BLANC)
        self.image_retour = self.creer_image_bouton(self.texte_retour.get_width() + 150, 
                                                     self.texte_retour.get_height() + 80)
        self.rect_retour = pygame.Rect((self.screen_width - self.image_retour.get_width()) // 2,
                                       self.screen_height - 120,
                                       self.image_retour.get_width(),
                                       self.image_retour.get_height())
        
        # Configuration panneau
        self.panneau_largeur = 800
        self.panneau_hauteur = 500
        self.panneau_x = (self.screen_width - self.panneau_largeur) // 2
        self.panneau_y = 150
        
        # Grille
        self.colonnes = 3
        self.espacement = 30
        self.taille_case = 140
        self.marge_gauche = (self.panneau_largeur - (self.colonnes * self.taille_case + 
                                                      (self.colonnes - 1) * self.espacement)) // 2
        
        # Charger les succès
        self.charger_succes()
        self.calculer_positions()

    def creer_image_bouton(self, largeur, hauteur):
        """Crée une image de bouton aux dimensions spécifiées"""
        return pygame.transform.scale(self.image_bouton_base, (largeur, hauteur))

    def charger_succes(self):
        """Charge les succès depuis le fichier JSON"""
        chemin_json = os.path.join(os.path.dirname(__file__), "succes.json")
        
        try:
            with open(chemin_json, "r", encoding="utf-8") as f:
                self.succes_liste = json.load(f)
            print(f"Succès chargés depuis : {chemin_json}")
            print(f"Nombre de succès : {len(self.succes_liste)}")
            for s in self.succes_liste:
                print(f"  - {s['id']}: {s['titre']} (débloqué: {s['debloque']})")
        except FileNotFoundError:
            print(f"Fichier non trouvé : {chemin_json}")
            self.succes_liste = []
        except json.JSONDecodeError as e:
            print(f"Erreur de parsing JSON : {e}")
            self.succes_liste = []
        except Exception as e:
            print(f"Erreur lors du chargement : {e}")
            self.succes_liste = []
        
        # Charger les images
        for succes in self.succes_liste:
            chemin_img = succes.get("image", "")
            if os.path.exists(chemin_img):
                try:
                    img = pygame.image.load(chemin_img).convert_alpha()
                    self.succes_images[succes["id"]] = pygame.transform.scale(img, (120, 120))
                    print(f"✅ Image chargée : {chemin_img}")
                except Exception as e:
                    print(f"❌ Erreur chargement image {chemin_img} : {e}")
                    placeholder = pygame.Surface((120, 120))
                    placeholder.fill((100, 100, 100))
                    self.succes_images[succes["id"]] = placeholder
            else:
                placeholder = pygame.Surface((120, 120))
                placeholder.fill((100, 100, 100))
                self.succes_images[succes["id"]] = placeholder
                print(f"⚠️ Image non trouvée : {chemin_img} (utilisation placeholder)")

    def calculer_positions(self):
        """Calcule les positions des succès dans la grille"""
        self.succes_rects = []
        for idx, succes in enumerate(self.succes_liste):
            col = idx % self.colonnes
            ligne = idx // self.colonnes
            x = self.panneau_x + self.marge_gauche + col * (self.taille_case + self.espacement)
            y = self.panneau_y + 40 + ligne * (self.taille_case + self.espacement)
            self.succes_rects.append((pygame.Rect(x, y, self.taille_case, self.taille_case), succes))
        
        # Calcul du scroll max
        nb_lignes = (len(self.succes_liste) + self.colonnes - 1) // self.colonnes
        hauteur_contenu = nb_lignes * (self.taille_case + self.espacement) + 40
        self.max_scroll = max(0, hauteur_contenu - self.panneau_hauteur + 60)

    def draw_titre(self):
        """Dessine le titre"""
        titre_surface = Police.titre.render("SUCCES", True, Couleur.OR)
        rect_titre = titre_surface.get_rect(center=(self.screen_width // 2, 60))
        self.screen.blit(titre_surface, rect_titre.topleft)

    def draw_panneau(self):
        """Dessine le panneau principal"""
        pygame.draw.rect(self.screen, Couleur.GRIS_FONCE, 
                        (self.panneau_x, self.panneau_y, self.panneau_largeur, self.panneau_hauteur), 
                        border_radius=15)
        pygame.draw.rect(self.screen, Couleur.GRIS_MOYEN, 
                        (self.panneau_x, self.panneau_y, self.panneau_largeur, self.panneau_hauteur), 
                        3, border_radius=15)

    def draw_grille_succes(self):
        """Dessine la grille des succès avec scroll"""
        zone_scroll = pygame.Rect(self.panneau_x, self.panneau_y, self.panneau_largeur, self.panneau_hauteur)
        self.screen.set_clip(zone_scroll)
        
        self.succes_survole = None
        
        for rect_succes, succes in self.succes_rects:
            # Appliquer le scroll
            rect_affiche = rect_succes.copy()
            rect_affiche.y -= self.scroll_offset
            
            # Ne dessiner que si visible
            if rect_affiche.bottom < self.panneau_y or rect_affiche.top > self.panneau_y + self.panneau_hauteur:
                continue
            
            # Vérifier le survol
            est_survole = rect_affiche.collidepoint(self.souris)
            if est_survole:
                self.succes_survole = succes
            
            # Couleur selon état
            if succes["debloque"]:
                couleur_fond = Couleur.BLEU_ACCENT
                couleur_bordure = Couleur.OR
            else:
                couleur_fond = Couleur.GRIS_MOYEN
                couleur_bordure = Couleur.GRIS_CLAIR
            
            # Effet de survol
            if est_survole:
                rect_hover = rect_affiche.inflate(10, 10)
                pygame.draw.rect(self.screen, Couleur.OR, rect_hover, border_radius=10)
            
            # Fond du succès
            pygame.draw.rect(self.screen, couleur_fond, rect_affiche, border_radius=10)
            pygame.draw.rect(self.screen, couleur_bordure, rect_affiche, 3, border_radius=10)
            
            # Image du succès
            img = self.succes_images[succes["id"]]
            img_rect = img.get_rect(center=rect_affiche.center)
            self.screen.blit(img, img_rect)
            
            # Si non débloqué, assombrir
            if not succes["debloque"]:
                overlay = pygame.Surface((self.taille_case, self.taille_case), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 150))
                self.screen.blit(overlay, rect_affiche.topleft)
                
                # Cadenas
                texte_cadenas = Police.cadenas.render("🔒", True, Couleur.BLANC)
                rect_cadenas = texte_cadenas.get_rect(center=rect_affiche.center)
                self.screen.blit(texte_cadenas, rect_cadenas)
        
        self.screen.set_clip(None)

    def draw_tooltip(self):
        """Dessine le tooltip au survol d'un succès"""
        if not self.succes_survole:
            return
        
        tooltip_largeur = 350
        tooltip_hauteur = 100
        tooltip_x = min(self.souris[0] + 20, self.screen_width - tooltip_largeur - 10)
        tooltip_y = min(self.souris[1] + 20, self.screen_height - tooltip_hauteur - 10)
        
        # Fond du tooltip
        tooltip_surf = pygame.Surface((tooltip_largeur, tooltip_hauteur), pygame.SRCALPHA)
        pygame.draw.rect(tooltip_surf, Couleur.NOIR_TRANSPARENT, (0, 0, tooltip_largeur, tooltip_hauteur), 
                        border_radius=10)
        pygame.draw.rect(tooltip_surf, Couleur.OR, (0, 0, tooltip_largeur, tooltip_hauteur), 2, border_radius=10)
        self.screen.blit(tooltip_surf, (tooltip_x, tooltip_y))
        
        # Titre du succès
        titre_surf = Police.succes.render(self.succes_survole["titre"], True, Couleur.OR)
        self.screen.blit(titre_surf, (tooltip_x + 15, tooltip_y + 15))
        
        # Description (multi-lignes)
        desc = self.succes_survole["description"]
        mots = desc.split()
        lignes = []
        ligne_actuelle = ""
        
        for mot in mots:
            test_ligne = ligne_actuelle + mot + " "
            if Police.desc.size(test_ligne)[0] < tooltip_largeur - 30:
                ligne_actuelle = test_ligne
            else:
                if ligne_actuelle:
                    lignes.append(ligne_actuelle)
                ligne_actuelle = mot + " "
        if ligne_actuelle:
            lignes.append(ligne_actuelle)
        
        for i, ligne in enumerate(lignes[:2]):  # Max 2 lignes
            desc_surf = Police.desc.render(ligne.strip(), True, Couleur.GRIS_CLAIR)
            self.screen.blit(desc_surf, (tooltip_x + 15, tooltip_y + 50 + i * 20))

    def draw_bouton_retour(self):
        """Dessine le bouton retour avec effet de zoom"""
        est_hover = self.rect_retour.collidepoint(self.souris)
        cible_zoom = 1.1 if est_hover else 1.0
        self.zoom_etat_retour += (cible_zoom - self.zoom_etat_retour) * self.vitesse_zoom
        
        image_zoom = pygame.transform.scale(self.image_retour, 
                                           (int(self.image_retour.get_width() * self.zoom_etat_retour),
                                            int(self.image_retour.get_height() * self.zoom_etat_retour)))
        rect_zoom = image_zoom.get_rect(center=self.rect_retour.center)
        self.screen.blit(image_zoom, rect_zoom.topleft)
        
        rect_texte = self.texte_retour.get_rect(center=rect_zoom.center)
        self.screen.blit(self.texte_retour, rect_texte.topleft)

    def draw(self):
        """Dessine tout le menu"""
        self.souris = pygame.mouse.get_pos()
        
        self.draw_titre()
        self.draw_panneau()
        self.draw_grille_succes()
        self.draw_tooltip()
        self.draw_bouton_retour()
        
        # Curseur
        self.screen.blit(self.curseur_img, self.souris)

    def handle_events(self, event):
        """Gère les événements"""
        if event.type == pygame.QUIT:
            self.en_cours = False
        
        # Scroll avec la molette
        elif event.type == pygame.MOUSEWHEEL:
            self.scroll_offset -= event.y * 30
            self.scroll_offset = max(0, min(self.scroll_offset, self.max_scroll))
        
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect_retour.collidepoint(event.pos):
                self.en_cours = False


# -------------------------------
# Fonction main pour compatibilité
# -------------------------------
def main(ecran):
    """Menu Succès avec fond animé et grille d'images"""
    
    # Création du fond spatial animé
    stars, planet_manager, vaisseau_fond = create_space_background()
    
    # Création de l'instance du menu
    menu = MenuSucces()
    menu.update()
    menu.en_cours = True
    
    horloge = pygame.time.Clock()

    while menu.en_cours:
        # Fond animé
        ecran.fill((0, 0, 0))
        stars.update()
        stars.draw(ecran)
        planet_manager.update_and_draw()
        Animator.update_all()
        PlanetAnimator.update_all()
        ShipAnimator.update_all()
        
        # Gestion des événements
        for event in pygame.event.get():
            menu.handle_events(event)
        
        # Dessin du menu
        menu.draw()
        
        pygame.display.flip()
        horloge.tick(60)
    
    # Nettoyage
    ShipAnimator.clear_list()
    PlanetAnimator.clear_list()