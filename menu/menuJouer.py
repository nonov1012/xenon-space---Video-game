import os
import random
from blazyck import *

from classes.GlobalVar.ScreenVar import ScreenVar
from classes.ShipAnimator import ShipAnimator
from classes.PlanetAnimator import PlanetAnimator
from classes.Animator import Animator
from classes.Start_Animation.main import create_space_background
from menu.modifShips import vaisseaux_sliders, limites_params, SHIP_STATS, noms_affichage, appliquer_modifications_sliders

def dessiner_slider(ecran, valeur, min_val, max_val, x, y, largeur, hauteur,
                    couleur_prog=(0, 200, 100), couleur_curseur=(0, 150, 80)):
    """Dessine un slider avec barre et curseur."""
    pygame.draw.rect(ecran, (90, 90, 110), (x, y, largeur, hauteur), border_radius=8)
    rel_pos = (valeur - min_val) / (max_val - min_val) if max_val > min_val else 0
    largeur_prog = int(rel_pos * largeur)
    if largeur_prog > 0:
        pygame.draw.rect(ecran, couleur_prog, (x, y, largeur_prog, hauteur), border_radius=8)
    curseur_x = x + int(rel_pos * largeur)
    pygame.draw.ellipse(ecran, couleur_curseur, (curseur_x - 8, y - 5, 16, hauteur + 10))

# Couleurs
class Couleur:
    BLANC = (255, 255, 255)
    GRIS_FONCE = (40, 40, 55)
    GRIS_MOYEN = (90, 90, 110)
    GRIS_CLAIR = (150, 150, 170)
    VERT = (0, 200, 100)
    VERT_FONCE = (0, 150, 80)
    BLEU_ACCENT = (70, 130, 255)

# Police
class Police:
    titre = pygame.font.Font("assets/fonts/SpaceNova.otf", 60)
    param = pygame.font.Font("assets/fonts/SpaceNova.otf", 24)
    bouton = pygame.font.Font("assets/fonts/SpaceNova.otf", 24)
    petite = pygame.font.Font("assets/fonts/SpaceNova.otf", 18)

# Menu play
class MenuPlay:

    def __init__(self):
        self.image_bouton_base = pygame.image.load("assets/img/menu/bouton_menu.png").convert_alpha()
        
        # Parametres avec sliders
        self.parametres = {
            "Nombre de planètes": {"valeur": 3, "min": 1, "max": 10},
            "Nombre d'astéroïdes": {"valeur": 5, "min": 1, "max": 20},
            "Niveau de départ de la base": {"valeur": 1, "min": 1, "max": 5},
            "Argent de départ": {"valeur": 1000, "min": 500, "max": 5000},
        }

        self.random_active = False
        self.slider_actif = None
        self.img_rect = None
        self.lancer_partie = False
        self.en_cours = False
        
        # Variables pour dropdown et scroll
        self.dropdown_ouvert = False
        self.dropdown_scroll = 0
        self.max_items_dropdown = 5
        self.scroll_offset = 0
        self.max_scroll = 0
        self.slider_vaisseau_actif = None

    def update(self):
        self.screen = ScreenVar.screen
        self.screen_width, self.screen_height = self.screen.get_size()
        self.scale = ScreenVar.scale
        
        # Curseur personnalise
        self.curseur_img = pygame.image.load('assets/img/menu/cursor.png')
        self.curseur_img = pygame.transform.scale(self.curseur_img, (40, 40))
        pygame.mouse.set_visible(False)
        
        self.update_base_game_param()
        self.update_ship_param()

    def update_base_game_param(self):
        # Boutons principaux
        self.texte_jouer = Police.bouton.render("JOUER", True, Couleur.BLANC)
        self.texte_reset = Police.bouton.render("RESET", True, Couleur.BLANC)
        self.texte_retour = Police.bouton.render("RETOUR MENU", True, Couleur.BLANC)

        self.image_jouer = self.creer_image_bouton(self.texte_jouer.get_width() + 100, self.texte_jouer.get_height() + 100)
        self.image_reset = self.creer_image_bouton(self.texte_reset.get_width() + 120, self.texte_reset.get_height() + 100)
        self.image_retour = self.creer_image_bouton(self.texte_retour.get_width() + 200, self.texte_retour.get_height() + 100)

        # Position bas
        self.espacement_boutons = 80
        self.y_premiere_ligne = self.screen_height - 210
        self.y_deuxieme_ligne = self.screen_height - 120

        self.total_largeur_premiere = self.image_jouer.get_width() + self.image_reset.get_width() + self.espacement_boutons
        self.x_depart_premiere = (self.screen_width - self.total_largeur_premiere) // 2

        self.rect_jouer = pygame.Rect(self.x_depart_premiere, self.y_premiere_ligne,
                                self.image_jouer.get_width(), self.image_jouer.get_height())
        self.rect_reset = pygame.Rect(self.rect_jouer.right + self.espacement_boutons, self.y_premiere_ligne,
                                self.image_reset.get_width(), self.image_reset.get_height())
        self.rect_retour = pygame.Rect((self.screen_width - self.image_retour.get_width()) // 2, self.y_deuxieme_ligne,
                                self.image_retour.get_width(), self.image_retour.get_height())

        self.boutons = [
            (self.image_jouer, self.rect_jouer, "JOUER"),
            (self.image_reset, self.rect_reset, "RESET"),
            (self.image_retour, self.rect_retour, "RETOUR MENU")
        ]
        self.zoom_etats = {label: 1.0 for _, _, label in self.boutons}
        self.vitesse_zoom = 0.08

        # Panneau + Onglets
        self.panneau_largeur = 650
        self.panneau_hauteur = 500
        self.panneau_x = (self.screen_width - self.panneau_largeur) // 2
        self.panneau_y = 205

        self.onglets = ["Classique", "Avance", "Vaisseaux"]
        self.onglet_actif = "Classique"

    def update_ship_param(self):
        self.types_vaisseaux = list(vaisseaux_sliders.keys())
        self.vaisseau_actif = self.types_vaisseaux[0]
        self.tier_actif = 1

        self.icones_vaisseaux = {}
        for ship in self.types_vaisseaux:
            ship_name = "base" if ship == "MotherShip" else ship
            path = os.path.join(IMG_PATH, "ships", ship_name, "base.png")
            if os.path.exists(path):
                img = pygame.image.load(path).convert_alpha()
            else:
                print(f"⚠️ Fichier non trouvé : {path}")
                img = pygame.Surface((80, 80))
                img.fill((255, 0, 0))
            self.icones_vaisseaux[ship] = pygame.transform.scale(img, (80, 80))

    def creer_image_bouton(self, largeur, hauteur):
        return pygame.transform.scale(self.image_bouton_base, (largeur, hauteur))

    def draw_base_game_param(self):
        # Titre
        titre_surface = Police.titre.render("Personnalisation", True, Couleur.BLANC)
        rect_titre = titre_surface.get_rect(center=(self.screen_width // 2, 60))
        self.screen.blit(titre_surface, rect_titre.topleft)

        # Panneau
        pygame.draw.rect(self.screen, Couleur.GRIS_FONCE, (self.panneau_x, self.panneau_y, self.panneau_largeur, self.panneau_hauteur), border_radius=15)
        pygame.draw.rect(self.screen, Couleur.GRIS_MOYEN, (self.panneau_x, self.panneau_y, self.panneau_largeur, self.panneau_hauteur), 2, border_radius=15)

        # Onglets
        self.onglet_largeur = self.panneau_largeur // len(self.onglets)
        for i, nom in enumerate(self.onglets):
            rect_onglet = pygame.Rect(self.panneau_x + i * self.onglet_largeur, self.panneau_y - 50, self.onglet_largeur, 40)
            couleur = Couleur.BLEU_ACCENT if nom == self.onglet_actif else Couleur.GRIS_CLAIR
            pygame.draw.rect(self.screen, couleur, rect_onglet, border_radius=8)
            texte = Police.param.render(nom, True, Couleur.BLANC if nom == self.onglet_actif else Couleur.GRIS_FONCE)
            rect_txt = texte.get_rect(center=rect_onglet.center)
            self.screen.blit(texte, rect_txt)

    def draw_avanced_game_param(self):
        if self.onglet_actif in ["Classique", "Avance"]:
            liste_affichee = []
            if self.onglet_actif == "Classique":
                liste_affichee = ["Nombre de planètes", "Nombre d'astéroïdes"]
            elif self.onglet_actif == "Avance":
                liste_affichee = list(self.parametres.keys())

            slider_largeur = 400
            slider_hauteur = 15
            slider_x = self.panneau_x + (self.panneau_largeur - slider_largeur) // 2
            decalage_y = 60
            
            for nom in liste_affichee:
                val = self.parametres[nom]
                y_courant = self.panneau_y + decalage_y

                texte_param = Police.param.render(nom, True, Couleur.BLANC)
                rect_param = texte_param.get_rect(center=(self.screen_width // 2, y_courant - 25))
                self.screen.blit(texte_param, rect_param)

                texte_valeur = Police.param.render(str(val["valeur"]), True, Couleur.BLEU_ACCENT)
                rect_valeur = texte_valeur.get_rect(center=(self.screen_width // 2, y_courant))
                self.screen.blit(texte_valeur, rect_valeur)

                rect_slider = pygame.Rect(slider_x, y_courant + 30, slider_largeur, slider_hauteur)
                pygame.draw.rect(self.screen, Couleur.GRIS_MOYEN, rect_slider, border_radius=8)

                rel_pos = (val["valeur"] - val["min"]) / (val["max"] - val["min"])
                largeur_prog = int(rel_pos * slider_largeur)
                if largeur_prog > 0:
                    rect_prog = pygame.Rect(slider_x, y_courant + 30, largeur_prog, slider_hauteur)
                    pygame.draw.rect(self.screen, Couleur.VERT, rect_prog, border_radius=8)

                curseur_x = int(slider_x + rel_pos * slider_largeur)
                rect_curseur = pygame.Rect(curseur_x - 12, y_courant + 22, 24, slider_hauteur + 16)
                pygame.draw.ellipse(self.screen, Couleur.VERT_FONCE, rect_curseur)
                pygame.draw.ellipse(self.screen, Couleur.VERT, (curseur_x - 10, y_courant + 24, 20, slider_hauteur + 12))

                if self.clic and rect_curseur.collidepoint(self.souris):
                    self.slider_actif = nom

                decalage_y += 100

            if self.slider_actif and self.clic:
                val = self.parametres[self.slider_actif]
                rel_x = max(0, min(slider_largeur, self.souris[0] - slider_x))
                val["valeur"] = int(val["min"] + (rel_x / slider_largeur) * (val["max"] - val["min"]))
            if not self.clic:
                self.slider_actif = None

            # Bouton Random
            rect_random = pygame.Rect(self.panneau_x + self.panneau_largeur - 230, self.panneau_y + self.panneau_hauteur - 50, 200, 40)
            pygame.draw.rect(self.screen, Couleur.VERT if self.random_active else Couleur.GRIS_CLAIR, rect_random, border_radius=10)
            txt_random = Police.param.render("RANDOM " + ("ON" if self.random_active else "OFF"), True, Couleur.BLANC)
            self.screen.blit(txt_random, txt_random.get_rect(center=rect_random.center))

    def draw_ship_param(self):
        self.dropdown_x = self.panneau_x + 10
        self.dropdown_y = self.panneau_y + 10
        self.dropdown_largeur = 200
        self.dropdown_hauteur = 35
        self.rect_dropdown = pygame.Rect(self.dropdown_x, self.dropdown_y, self.dropdown_largeur, self.dropdown_hauteur)
        
        self.liste_rects = []
        self.tier_rects = []
        self.param_rects = []
        self.params_zone_x = self.panneau_x + 10
        self.params_zone_y = self.panneau_y + 120
        
        if self.onglet_actif == "Vaisseaux":
            # Dropdown
            pygame.draw.rect(self.screen, Couleur.GRIS_MOYEN, self.rect_dropdown, border_radius=5)
            pygame.draw.rect(self.screen, Couleur.BLANC, self.rect_dropdown, 2, border_radius=5)
            
            texte_dropdown = Police.petite.render(self.vaisseau_actif, True, Couleur.BLANC)
            self.screen.blit(texte_dropdown, (self.dropdown_x + 10, self.dropdown_y + 8))
            
            fleche = "▼" if not self.dropdown_ouvert else "▲"
            texte_fleche = Police.petite.render(fleche, True, Couleur.BLANC)
            self.screen.blit(texte_fleche, (self.dropdown_x + self.dropdown_largeur - 30, self.dropdown_y + 8))
            
            # Liste déroulante
            if self.dropdown_ouvert:
                total_items = len(self.types_vaisseaux)
                max_dropdown_scroll = max(0, total_items - self.max_items_dropdown)
                self.dropdown_scroll = max(0, min(self.dropdown_scroll, max_dropdown_scroll))
                
                items_visibles = self.types_vaisseaux[self.dropdown_scroll:self.dropdown_scroll + self.max_items_dropdown]
                
                for i, ship in enumerate(items_visibles):
                    rect_item = pygame.Rect(self.dropdown_x, self.dropdown_y + self.dropdown_hauteur + i * 30, self.dropdown_largeur, 30)
                    self.liste_rects.append((rect_item, ship))
                    
                    couleur = Couleur.BLEU_ACCENT if ship == self.vaisseau_actif else Couleur.GRIS_FONCE
                    pygame.draw.rect(self.screen, couleur, rect_item)
                    pygame.draw.rect(self.screen, Couleur.GRIS_CLAIR, rect_item, 1)
                    
                    texte_item = Police.petite.render(ship, True, Couleur.BLANC)
                    self.screen.blit(texte_item, (rect_item.x + 10, rect_item.y + 5))
            
            # Icône vaisseau
            icone_x = self.dropdown_x + self.dropdown_largeur + 20
            icone_y = self.panneau_y + 10
            icone_taille = 80
            
            pygame.draw.rect(self.screen, Couleur.BLANC, (icone_x, icone_y, icone_taille, icone_taille), 2, border_radius=5)
            self.img_vaisseau = self.icones_vaisseaux[self.vaisseau_actif]
            self.img_rect = self.img_vaisseau.get_rect(center=(icone_x + icone_taille//2, icone_y + icone_taille//2))
            self.screen.blit(self.img_vaisseau, self.img_rect.topleft)
            
            # Sélecteur de tier (MotherShip)
            if self.vaisseau_actif == "MotherShip":
                tier_x_start = icone_x + icone_taille + 20
                tier_y_start = icone_y + 25
                
                texte_tier_label = Police.petite.render("Tier:", True, Couleur.BLANC)
                self.screen.blit(texte_tier_label, (tier_x_start, tier_y_start))
                
                for i, tier in enumerate([1, 2, 3, 4]):
                    tier_rect = pygame.Rect(tier_x_start + 60 + i * 40, tier_y_start, 35, 30)
                    self.tier_rects.append((tier_rect, tier))
                    
                    couleur = Couleur.BLEU_ACCENT if tier == self.tier_actif else Couleur.GRIS_MOYEN
                    pygame.draw.rect(self.screen, couleur, tier_rect, border_radius=5)
                    
                    texte_tier = Police.petite.render(str(tier), True, Couleur.BLANC)
                    self.screen.blit(texte_tier, texte_tier.get_rect(center=tier_rect.center))
            
            # Zone scrollable paramètres
            params_zone_largeur = self.panneau_largeur - 20
            params_zone_hauteur = self.panneau_hauteur - 130
            
            surf_scroll = pygame.Surface((params_zone_largeur, params_zone_hauteur))
            surf_scroll.fill(Couleur.GRIS_FONCE)
            
            # Paramètres du vaisseau
            if self.vaisseau_actif == "MotherShip":
                params_vaisseau = vaisseaux_sliders[self.vaisseau_actif][self.tier_actif]
            else:
                params_vaisseau = vaisseaux_sliders[self.vaisseau_actif]
            
            params_avec_boutons = ["taille_largeur", "taille_hauteur", "nb_vaisseaux", "port_attaque", "port_deplacement"]
            
            y_offset = 10 - self.scroll_offset
            displayed_idx = 0
            
            for param, valeur in params_vaisseau.items():
                if param in ["peut_miner", "peut_transporter", "taille"]:
                    continue
                if self.vaisseau_actif == "Foreuse" and param in ["port_attaque", "port_deplacement"]:
                    continue
                    
                y_pos = y_offset + displayed_idx * 85
                displayed_idx += 1
                
                if y_pos < -85 or y_pos > params_zone_hauteur:
                    continue
                
                nom_affiche = noms_affichage.get(param, param)
                texte_nom = Police.petite.render(nom_affiche, True, Couleur.BLANC)
                surf_scroll.blit(texte_nom, (10, y_pos))
                
                texte_val = Police.petite.render(str(valeur), True, Couleur.BLEU_ACCENT)
                surf_scroll.blit(texte_val, (10, y_pos + 22))
                
                min_val = limites_params[param]["min"]
                max_val = limites_params[param]["max"]
                
                if param in params_avec_boutons:
                    # Boutons +/-
                    btn_moins_rect = pygame.Rect(200, y_pos + 15, 30, 30)
                    btn_plus_rect = pygame.Rect(340, y_pos + 15, 30, 30)
                    
                    pygame.draw.rect(surf_scroll, Couleur.GRIS_MOYEN, btn_moins_rect, border_radius=5)
                    pygame.draw.rect(surf_scroll, Couleur.GRIS_MOYEN, btn_plus_rect, border_radius=5)
                    
                    texte_moins = Police.param.render("-", True, Couleur.BLANC)
                    texte_plus = Police.param.render("+", True, Couleur.BLANC)
                    surf_scroll.blit(texte_moins, texte_moins.get_rect(center=btn_moins_rect.center))
                    surf_scroll.blit(texte_plus, texte_plus.get_rect(center=btn_plus_rect.center))
                    
                    texte_val_centre = Police.param.render(str(valeur), True, Couleur.VERT)
                    val_rect = texte_val_centre.get_rect(center=(285, y_pos + 30))
                    surf_scroll.blit(texte_val_centre, val_rect)
                    
                    self.param_rects.append((btn_moins_rect, param, "moins", y_offset))
                    self.param_rects.append((btn_plus_rect, param, "plus", y_offset))
                else:
                    # Slider
                    slider_x_local = 200
                    slider_largeur_local = 250
                    slider_hauteur_local = 15
                    
                    pygame.draw.rect(surf_scroll, Couleur.GRIS_MOYEN, 
                                   (slider_x_local, y_pos + 25, slider_largeur_local, slider_hauteur_local), 
                                   border_radius=8)
                    
                    rel_pos = (valeur - min_val) / (max_val - min_val) if max_val > min_val else 0
                    largeur_prog = int(rel_pos * slider_largeur_local)
                    if largeur_prog > 0:
                        pygame.draw.rect(surf_scroll, Couleur.VERT, 
                                       (slider_x_local, y_pos + 25, largeur_prog, slider_hauteur_local), 
                                       border_radius=8)
                    
                    curseur_x_local = int(slider_x_local + rel_pos * slider_largeur_local)
                    pygame.draw.ellipse(surf_scroll, Couleur.VERT_FONCE, 
                                      (curseur_x_local - 8, y_pos + 20, 16, slider_hauteur_local + 10))
                    
                    slider_rect = pygame.Rect(slider_x_local, y_pos + 20, slider_largeur_local, 30)
                    self.param_rects.append((slider_rect, param, "slider", y_offset))
            
            # Calcul max_scroll
            nb_params_affiches = len([p for p in params_vaisseau.keys() if p not in ["peut_miner", "peut_transporter", "taille"]])
            if self.vaisseau_actif == "Foreuse":
                nb_params_affiches -= 2  # Soustraire port_attaque et port_deplacement
            hauteur_contenu = nb_params_affiches * 85
            self.max_scroll = max(0, hauteur_contenu - params_zone_hauteur + 20)
            
            # Affichage surface
            self.screen.set_clip(pygame.Rect(self.params_zone_x, self.params_zone_y, params_zone_largeur, params_zone_hauteur))
            self.screen.blit(surf_scroll, (self.params_zone_x, self.params_zone_y))
            self.screen.set_clip(None)
            
            pygame.draw.rect(self.screen, Couleur.GRIS_CLAIR, 
                           (self.params_zone_x, self.params_zone_y, params_zone_largeur, params_zone_hauteur), 2)

    def draw(self):
        self.souris = pygame.mouse.get_pos()
        self.clic = pygame.mouse.get_pressed()[0]

        self.draw_base_game_param()
        self.draw_avanced_game_param()
        self.draw_ship_param()

        # Boutons principaux
        for image, rect, label in self.boutons:
            est_hover = rect.collidepoint(self.souris)
            cible_zoom = 1.1 if est_hover else 1.0
            self.zoom_etats[label] += (cible_zoom - self.zoom_etats[label]) * self.vitesse_zoom

            largeur_zoom = int(image.get_width() * self.zoom_etats[label])
            hauteur_zoom = int(image.get_height() * self.zoom_etats[label])
            image_zoom = pygame.transform.scale(image, (largeur_zoom, hauteur_zoom))
            rect_zoom = image_zoom.get_rect(center=rect.center)

            self.screen.blit(image_zoom, rect_zoom.topleft)

            texte_surf = Police.bouton.render(label, True, Couleur.BLANC)
            rect_texte = texte_surf.get_rect(center=rect_zoom.center)
            self.screen.blit(texte_surf, rect_texte)

        # Curseur
        self.screen.blit(self.curseur_img, self.souris)

    def handle_events(self, event):
        """Gère les événements de manière centralisée"""
        if event.type == pygame.QUIT:
            self.en_cours = False
            
        # MOLETTE pour scroll
        elif event.type == pygame.MOUSEWHEEL:
            if self.onglet_actif == "Vaisseaux":
                if self.dropdown_ouvert:
                    self.dropdown_scroll -= event.y
                    max_dropdown_scroll = max(0, len(self.types_vaisseaux) - self.max_items_dropdown)
                    self.dropdown_scroll = max(0, min(self.dropdown_scroll, max_dropdown_scroll))
                else:
                    self.scroll_offset -= event.y * 20
                    self.scroll_offset = max(0, min(self.scroll_offset, self.max_scroll))
            
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Boutons bas
            for _, rect, label in self.boutons:
                if rect.collidepoint(event.pos):
                    if label == "JOUER":
                        print("JOUER avec parametres:", {k: v["valeur"] for k, v in self.parametres.items()},
                              "Random:", self.random_active)
                        print("Vaisseau :", self.vaisseau_actif)
                        if self.vaisseau_actif == "MotherShip":
                            print("Tier:", self.tier_actif, vaisseaux_sliders[self.vaisseau_actif][self.tier_actif])
                        else:
                            print(vaisseaux_sliders[self.vaisseau_actif])
                        self.en_cours = False
                        self.lancer_partie = True
                    elif label == "RESET":
                        for k in self.parametres:
                            self.parametres[k]["valeur"] = self.parametres[k]["min"]
                    elif label == "RETOUR MENU":
                        self.en_cours = False
            
            # Bouton Random
            if self.onglet_actif in ["Classique", "Avance"]:
                rect_random = pygame.Rect(self.panneau_x + self.panneau_largeur - 230, 
                                         self.panneau_y + self.panneau_hauteur - 50, 200, 40)
                if rect_random.collidepoint(event.pos):
                    self.random_active = not self.random_active
                    if self.random_active:
                        for k in self.parametres:
                            self.parametres[k]["valeur"] = random.randint(self.parametres[k]["min"], self.parametres[k]["max"])
            
            # Onglets
            for i, nom in enumerate(self.onglets):
                rect_onglet = pygame.Rect(self.panneau_x + i * (self.panneau_largeur // len(self.onglets)), 
                                         self.panneau_y - 50,
                                         self.panneau_largeur // len(self.onglets), 40)
                if rect_onglet.collidepoint(event.pos):
                    self.onglet_actif = nom
                    self.scroll_offset = 0
                    self.dropdown_scroll = 0
                    self.dropdown_ouvert = False
            
            # Gestion Vaisseaux
            if self.onglet_actif == "Vaisseaux":
                # Clic sur dropdown
                if self.rect_dropdown.collidepoint(event.pos):
                    self.dropdown_ouvert = not self.dropdown_ouvert
                
                # Clic sur liste déroulante
                elif self.dropdown_ouvert:
                    for rect_item, ship in self.liste_rects:
                        if rect_item.collidepoint(event.pos):
                            self.vaisseau_actif = ship
                            self.tier_actif = 1
                            self.scroll_offset = 0
                            self.dropdown_scroll = 0
                            self.dropdown_ouvert = False
                            break
                
                # Clic sur tier (MotherShip)
                if self.vaisseau_actif == "MotherShip":
                    for tier_rect, tier in self.tier_rects:
                        if tier_rect.collidepoint(event.pos):
                            self.tier_actif = tier
                            self.scroll_offset = 0
                            break
                
                # Clic sur boutons +/- ou sliders
                for rect_param, param, action, y_off in self.param_rects:
                    rect_ajuste = rect_param.copy()
                    rect_ajuste.x += self.params_zone_x
                    rect_ajuste.y += self.params_zone_y
                    
                    if rect_ajuste.collidepoint(event.pos):
                        if self.vaisseau_actif == "MotherShip":
                            params = vaisseaux_sliders[self.vaisseau_actif][self.tier_actif]
                        else:
                            params = vaisseaux_sliders[self.vaisseau_actif]
                        
                        min_val = limites_params[param]["min"]
                        max_val = limites_params[param]["max"]
                        
                        if action == "moins":
                            params[param] = max(min_val, params[param] - 1)
                        elif action == "plus":
                            params[param] = min(max_val, params[param] + 1)
                        elif action == "slider":
                            self.slider_vaisseau_actif = param
                            rel_x = max(0, min(rect_param.width, event.pos[0] - rect_ajuste.x))
                            nouveau_val = int(min_val + (rel_x / rect_param.width) * (max_val - min_val))
                            params[param] = nouveau_val
                        break
                
                # Fermer dropdown si clic ailleurs
                if self.dropdown_ouvert and not self.rect_dropdown.collidepoint(event.pos):
                    clic_sur_liste = False
                    for rect_item, _ in self.liste_rects:
                        if rect_item.collidepoint(event.pos):
                            clic_sur_liste = True
                            break
                    if not clic_sur_liste:
                        self.dropdown_ouvert = False
                        self.dropdown_scroll = 0

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.slider_vaisseau_actif = None
    
    def update_slider_vaisseau(self):
        """Met à jour le slider de vaisseau pendant le drag"""
        if self.slider_vaisseau_actif and self.clic and self.onglet_actif == "Vaisseaux":
            for rect_param, param, action, y_off in self.param_rects:
                if param == self.slider_vaisseau_actif and action == "slider":
                    rect_ajuste = rect_param.copy()
                    rect_ajuste.x += self.params_zone_x
                    rect_ajuste.y += self.params_zone_y
                    
                    if self.vaisseau_actif == "MotherShip":
                        params = vaisseaux_sliders[self.vaisseau_actif][self.tier_actif]
                    else:
                        params = vaisseaux_sliders[self.vaisseau_actif]
                    
                    min_val = limites_params[param]["min"]
                    max_val = limites_params[param]["max"]
                    rel_x = max(0, min(rect_param.width, self.souris[0] - rect_ajuste.x))
                    nouveau_val = int(min_val + (rel_x / rect_param.width) * (max_val - min_val))
                    params[param] = nouveau_val
                    break


def draw(ecran):
    """Interface de personnalisation avec onglets Classique/Avance/Vaisseaux"""
    
    largeur_ecran, hauteur_ecran = ecran.get_size()
    screen_ratio = (largeur_ecran * 100 / 600) / 100
    
    # Création du fond spatial animé
    stars, planet_manager, vaisseau_fond = create_space_background()
    
    # Création de l'instance du menu
    menu = MenuPlay()
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
        
        # Mise à jour du slider pendant le drag
        menu.update_slider_vaisseau()
        
        # Dessin du menu
        menu.draw()

        pygame.display.flip()
        horloge.tick(60)
    
    if menu.lancer_partie:
        appliquer_modifications_sliders()
        ShipAnimator.clear_list()
        PlanetAnimator.clear_list()
        from main import start_game
        start_game(ecran, menu.parametres, menu.random_active)