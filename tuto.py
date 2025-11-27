"""
#################################################################
#  __   __ __                      _____                        #
#  \ \ / //_/                     / ____|                       #
#   \ V / ___ _ __   ___  _ __   | (___  _ __   __ _  ___ ___   #
#    > < / _ \ '_ \ / _ \| '_ \   \___ \| '_ \ / _` |/ __/ _ \  #
#   / . \  __/ | | | (_) | | | |  ____) | |_) | (_| | (_|  __/  #
#  /_/ \_\___|_| |_|\___/|_| |_| |_____/| .__/ \__,_|\___\___|  #
#                                       | |                     #
#                                       |_|                     #
#################################################################
# Système de tutoriel interactif pour Xenon Space
#################################################################
"""

import pygame
from enum import Enum, auto


class TutorialStep(Enum):
    """Énumération des différentes étapes du tutoriel"""
    WELCOME = auto()
    OBJECTIF = auto()
    GRILLE = auto()
    MOTHERSHIP = auto()
    VAISSEAUX = auto()
    DEPLACEMENT = auto()
    ATTAQUE = auto()
    ECONOMIE = auto()
    SHOP = auto()
    RESSOURCES = auto()
    FIN_TOUR = auto()
    VICTOIRE = auto()
    FIN = auto()


class TutorialContent:
    """Contenu textuel et visuel pour chaque étape du tutoriel"""
    
    # Chemins des images pour chaque étape
    IMAGES = {
        TutorialStep.WELCOME: "assets/img/menu/logo.png",
        TutorialStep.OBJECTIF: "assets/img/ships/base/base_tier_1.png",
        TutorialStep.GRILLE: None,  # Pas d'image spécifique
        TutorialStep.MOTHERSHIP: "assets/img/ships/base/base_tier_3.png",
        TutorialStep.VAISSEAUX: None,  # Affichage spécial avec multiples images
        TutorialStep.DEPLACEMENT: "assets/img/ships/petit/base.png",
        TutorialStep.ATTAQUE: "assets/img/ships/moyen/base.png",
        TutorialStep.ECONOMIE: "assets/img/ships/foreuse/base.png",
        TutorialStep.SHOP: None,  # Pas d'image
        TutorialStep.RESSOURCES: "assets/img/ships/foreuse/base.png",
        TutorialStep.FIN_TOUR: None,
        TutorialStep.VICTOIRE: "assets/img/ships/base/base_tier_3.png",
        TutorialStep.FIN: "assets/img/menu/logo.png"
    }
    
    # Tailles spécifiques pour certaines étapes (en pixels)
    IMAGE_SIZES = {
        TutorialStep.WELCOME: 250,
        TutorialStep.OBJECTIF: 250,
        TutorialStep.MOTHERSHIP: 250,
        TutorialStep.DEPLACEMENT: 150,  # 25% plus petit
        TutorialStep.ATTAQUE: 150,
        TutorialStep.ECONOMIE: 150,
        TutorialStep.RESSOURCES: 150,
        TutorialStep.VICTOIRE: 250,
        TutorialStep.FIN: 250
    }
    
    # Images spécifiques pour les vaisseaux (affichage multiple)
    SHIP_IMAGES = {
        "petit": "assets/img/ships/petit/base.png",
        "moyen": "assets/img/ships/moyen/base.png",
        "lourd": "assets/img/ships/lourd/base.png",
        "foreuse": "assets/img/ships/foreuse/base.png",
        "transport": "assets/img/ships/transport/base.png"
    }
    
    STEPS = {
        TutorialStep.WELCOME: {
            "titre": "Bienvenue dans Xenon Space !",
            "texte": [
                "Xenon Space est un jeu de stratégie au tour par tour dans l'espace.",
                "",
                "Vous allez apprendre à :",
                "• Gérer votre flotte de vaisseaux",
                "• Collecter des ressources",
                "• Attaquer vos ennemis",
                "• Développer votre base spatiale",
                "",
                "Appuyez sur [ENTRÉE] pour commencer"
            ],
            "couleur": (100, 200, 255)
        },
        
        TutorialStep.OBJECTIF: {
            "titre": "Objectif du jeu",
            "texte": [
                "OBJECTIF PRINCIPAL :",
                "Détruire le MotherShip (base spatiale) ennemi !",
                "",
                "Pour y parvenir :",
                "• Construisez une flotte puissante",
                "• Collectez des ressources (BITCOINS)",
                "• Améliorez votre base",
                "• Détruisez tous les vaisseaux ennemis",
                "",
                "[ENTRÉE] pour continuer"
            ],
            "couleur": (255, 215, 0)
        },
        
        TutorialStep.GRILLE: {
            "titre": "La grille de jeu",
            "texte": [
                "Le jeu se déroule sur une grille spatiale.",
                "",
                "ÉLÉMENTS DE LA CARTE :",
                "• Planètes : donnent des ressources",
                "• Astéroïdes (gris) : peuvent être minés",
                "• Vaisseaux (colorés) : vos unités",
                "• Bases (grandes structures) : MotherShips",
                "",
                "CONTRÔLES :",
                "• [CTRL] : Afficher/masquer la grille",
                "• [SHIFT] : Afficher les zones d'influence",
                "",
                "[ENTRÉE] pour continuer"
            ],
            "couleur": (150, 150, 200)
        },
        
        TutorialStep.MOTHERSHIP: {
            "titre": "Le MotherShip",
            "texte": [
                "Votre MotherShip est votre base principale.",
                "",
                "CARACTÉRISTIQUES :",
                "• Structure : 5x4 cases",
                "• Points de vie élevés",
                "• Peut être amélioré (3 niveaux)",
                "• Produit des ressources chaque tour",
                "",
                "⚠️ SI VOTRE MOTHERSHIP EST DÉTRUIT, VOUS PERDEZ !",
                "",
                "Protégez-le à tout prix !",
                "",
                "[ENTRÉE] pour continuer"
            ],
            "couleur": (200, 100, 255)
        },
        
        TutorialStep.VAISSEAUX: {
            "titre": "Types de vaisseaux",
            "texte": [
                "PETIT VAISSEAU (2x2) :",
                "• Rapide et peu coûteux",
                "• Bon pour l'exploration",
                "",
                "VAISSEAU MOYEN (2x2) :",
                "• Équilibré en attaque et défense",
                "",
                "VAISSEAU LOURD (3x3) :",
                "• Puissant mais lent et coûteux",
                "",
                "FOREUSE (2x2) :",
                "• Spécialisé dans le minage d'astéroïdes",
                "",
                "TRANSPORTEUR (3x4) :",
                "• Peut transporter d'autres vaisseaux",
                "",
                "[ENTRÉE] pour continuer"
            ],
            "couleur": (100, 255, 150)
        },
        
        TutorialStep.DEPLACEMENT: {
            "titre": "Déplacement",
            "texte": [
                "COMMENT DÉPLACER UN VAISSEAU :",
                "",
                "1. Cliquez sur un de vos vaisseaux",
                "2. Les cases CYAN montrent où vous pouvez aller",
                "3. Appuyez sur [R] pour faire pivoter le vaisseau",
                "4. Cliquez sur une case cyan pour vous déplacer",
                "",
                "NOTE :",
                "• Chaque vaisseau ne peut bouger qu'UNE FOIS par tour",
                "• La rotation ne compte pas comme un mouvement",
                "• Les cases ROUGES sont les zones d'attaque",
                "",
                "[ENTRÉE] pour continuer"
            ],
            "couleur": (80, 200, 255)
        },
        
        TutorialStep.ATTAQUE: {
            "titre": "Combat",
            "texte": [
                "ATTAQUER UN ENNEMI :",
                "",
                "1. Sélectionnez un vaisseau",
                "2. Les cases ROUGES montrent votre portée d'attaque",
                "3. Cliquez sur une case rouge contenant un ennemi",
                "4. Votre vaisseau attaquera automatiquement",
                "",
                "POINTS IMPORTANTS :",
                "• Chaque vaisseau a des PV (points de vie)",
                "• Les dégâts dépendent du type de vaisseau",
                "• Un vaisseau détruit disparaît de la carte",
                "• Attaquer consomme votre action du tour",
                "",
                "[ENTRÉE] pour continuer"
            ],
            "couleur": (255, 80, 80)
        },
        
        TutorialStep.ECONOMIE: {
            "titre": "Économie",
            "texte": [
                "LES BITCOINS sont la monnaie du jeu.",
                "",
                "GAGNER DES BITCOINS :",
                "• Foreuses près des planètes : +50 BITCOINS/tour",
                "• Foreuses près des astéroïdes : +30 BITCOINS/tour",
                "• Revenus de base : +10 BITCOINS/tour",
                "",
                "DÉPENSER DES BITCOINS :",
                "• Acheter de nouveaux vaisseaux",
                "• Améliorer votre MotherShip",
                "",
                "💡 Astuce : Construisez des foreuses rapidement !",
                "",
                "[ENTRÉE] pour continuer"
            ],
            "couleur": (255, 215, 0)
        },
        
        TutorialStep.SHOP: {
            "titre": "Le Shop",
            "texte": [
                "Le shop apparaît sur le côté de l'écran.",
                "",
                "VOUS POUVEZ ACHETER :",
                "• Petit vaisseau : peu cher",
                "• Moyen vaisseau : prix moyen",
                "• Grand vaisseau : cher mais puissant",
                "• Foreuse : pour les ressources",
                "• Transporteur : pour déplacer des vaisseaux",
                "",
                "AMÉLIORATION DE BASE :",
                "• Cliquez sur 'Améliorer la base'",
                "• Augmente les PV et capacités du MotherShip",
                "",
                "[ENTRÉE] pour continuer"
            ],
            "couleur": (150, 255, 150)
        },
        
        TutorialStep.RESSOURCES: {
            "titre": "Minage et Ressources",
            "texte": [
                "PLANÈTES :",
                "• Placez une foreuse à côté",
                "• Génère +50 BITCOINS/tour",
                "",
                "ASTÉROÏDES (gris) :",
                "• Placez une foreuse à côté",
                "• Génère +30 BITCOINS/tour",
                "• Les foreuses peuvent les détruire",
                "",
                "TRANSPORTEURS :",
                "• Clic droit pour charger un petit vaisseau",
                "• Clic droit pour décharger (cases jaunes)",
                "• Utile pour déplacer rapidement des unités",
                "",
                "[ENTRÉE] pour continuer"
            ],
            "couleur": (255, 180, 80)
        },
        
        TutorialStep.FIN_TOUR: {
            "titre": "Fin de tour",
            "texte": [
                "TERMINER VOTRE TOUR :",
                "",
                "• Appuyez sur [ENTRÉE] ou cliquez sur le bouton",
                "• Vos ressources sont collectées",
                "• Les vaisseaux récupèrent leur action",
                "• C'est au tour de l'adversaire",
                "",
                "INTERFACE :",
                "• HUD en bas : infos sur le vaisseau sélectionné",
                "• Shop à droite : achats disponibles",
                "• Solde de BITCOINS affiché en haut",
                "",
                "PAUSE :",
                "• [ÉCHAP] pour mettre en pause",
                "",
                "[ENTRÉE] pour continuer"
            ],
            "couleur": (200, 200, 100)
        },
        
        TutorialStep.VICTOIRE: {
            "titre": "Conditions de victoire",
            "texte": [
                "VOUS GAGNEZ SI :",
                "Le MotherShip ennemi est détruit !",
                "",
                "VOUS PERDEZ SI :",
                "Votre MotherShip est détruit !",
                "",
                "STRATÉGIES GAGNANTES :",
                "• Développez votre économie rapidement",
                "• Équilibrez attaque et défense",
                "• Protégez votre MotherShip",
                "• Améliorez votre base dès que possible",
                "• Utilisez les transporteurs tactiquement",
                "",
                "[ENTRÉE] pour continuer"
            ],
            "couleur": (255, 215, 0)
        },
        
        TutorialStep.FIN: {
            "titre": "Prêt à jouer !",
            "texte": [
                "Vous connaissez maintenant les bases de Xenon Space !",
                "",
                "RÉCAPITULATIF DES TOUCHES :",
                "• Clic gauche : Sélectionner/Déplacer",
                "• Clic droit : Transporter (si transporteur)",
                "• [R] : Rotation du vaisseau",
                "• [ENTRÉE] : Fin de tour",
                "• [ÉCHAP] : Pause",
                "• [CTRL] : Afficher grille",
                "• [SHIFT] : Afficher zones",
                "",
                "Bonne chance, Commandant ! 🚀",
                "",
                "[ENTRÉE] pour commencer à jouer"
            ],
            "couleur": (100, 255, 100)
        }
    }


class TutorialButton:
    """Bouton interactif pour naviguer dans le tutoriel"""
    
    def __init__(self, x, y, width, height, text, color=(100, 150, 255)):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = tuple(min(c + 30, 255) for c in color)
        self.is_hovered = False
        
    def draw(self, screen, font):
        """Dessine le bouton avec effet de survol"""
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(screen, color, self.rect, border_radius=10)
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2, border_radius=10)
        
        text_surface = font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
    
    def update(self, mouse_pos):
        """Met à jour l'état de survol"""
        self.is_hovered = self.rect.collidepoint(mouse_pos)


class TutorialManager:
    """Gestionnaire principal du système de tutoriel"""
    
    def __init__(self, screen, stars=None, planet_manager=None):
        self.screen = screen
        self.stars = stars
        self.planet_manager = planet_manager
        self.current_step = TutorialStep.WELCOME
        self.font_title = pygame.font.Font(None, 48)
        self.font_text = pygame.font.Font(None, 28)
        self.font_button = pygame.font.Font(None, 32)
        
        # Charger les images
        self.images = {}
        for step, path in TutorialContent.IMAGES.items():
            if path:
                try:
                    img = pygame.image.load(path).convert_alpha()
                    # Récupérer la taille spécifique ou utiliser la taille par défaut
                    max_size = TutorialContent.IMAGE_SIZES.get(step, 250)
                    ratio = min(max_size / img.get_width(), max_size / img.get_height())
                    new_size = (int(img.get_width() * ratio), int(img.get_height() * ratio))
                    self.images[step] = pygame.transform.smoothscale(img, new_size)
                except Exception as e:
                    print(f"Erreur chargement image {path}: {e}")
                    self.images[step] = None
            else:
                self.images[step] = None
        
        # Charger les petites images de vaisseaux
        self.ship_images = {}
        for ship_type, path in TutorialContent.SHIP_IMAGES.items():
            try:
                img = pygame.image.load(path).convert_alpha()
                # Petite taille pour les icônes
                icon_size = 50
                ratio = min(icon_size / img.get_width(), icon_size / img.get_height())
                new_size = (int(img.get_width() * ratio), int(img.get_height() * ratio))
                self.ship_images[ship_type] = pygame.transform.smoothscale(img, new_size)
            except Exception as e:
                print(f"Erreur chargement image vaisseau {path}: {e}")
                self.ship_images[ship_type] = None
        
        # Création des boutons
        screen_width = screen.get_width()
        screen_height = screen.get_height()
        button_width = 150
        button_height = 50
        
        self.button_next = TutorialButton(
            screen_width - button_width - 50,
            screen_height - button_height - 30,
            button_width,
            button_height,
            "Suivant",
            (100, 200, 100)
        )
        
        self.button_prev = TutorialButton(
            50,
            screen_height - button_height - 30,
            button_width,
            button_height,
            "Précédent",
            (200, 100, 100)
        )
        
        self.button_skip = TutorialButton(
            screen_width // 2 - button_width // 2,
            screen_height - button_height - 30,
            button_width,
            button_height,
            "Passer",
            (150, 150, 150)
        )
    
    def draw_background(self):
        """Dessine un fond spatial animé"""
        if self.stars and self.planet_manager:
            # Utiliser le fond du menu principal
            self.screen.fill((0, 0, 0))
            self.stars.update()
            self.stars.draw(self.screen)
            self.planet_manager.update_and_draw()
        else:
            # Fond par défaut si pas de StarField fourni
            self.screen.fill((10, 10, 30))
            
            # Étoiles statiques
            for i in range(100):
                x = (i * 137) % self.screen.get_width()
                y = (i * 239) % self.screen.get_height()
                size = (i % 3) + 1
                brightness = 150 + (i % 100)
                pygame.draw.circle(self.screen, (brightness, brightness, brightness), (x, y), size)
    
    def draw_content_box(self, content):
        """Dessine la boîte de contenu du tutoriel"""
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()
        
        # Boîte semi-transparente
        box_width = screen_width - 200
        box_height = screen_height - 200
        box_x = 100
        box_y = 80
        
        # Fond de la boîte avec transparence
        box_surface = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
        pygame.draw.rect(box_surface, (20, 20, 50, 230), box_surface.get_rect(), border_radius=20)
        pygame.draw.rect(box_surface, content["couleur"], box_surface.get_rect(), 3, border_radius=20)
        self.screen.blit(box_surface, (box_x, box_y))
        
        # Titre
        title_surface = self.font_title.render(content["titre"], True, content["couleur"])
        title_rect = title_surface.get_rect(centerx=screen_width // 2, y=box_y + 30)
        self.screen.blit(title_surface, title_rect)
        
        # Image associée à l'étape (si disponible et pas page vaisseaux)
        image = self.images.get(self.current_step)
        image_offset = 0
        
        # Affichage spécial pour la page des vaisseaux
        if self.current_step == TutorialStep.VAISSEAUX:
            y_offset = box_y + 100
            
            # Définir les types de vaisseaux avec leurs images
            ships_info = [
                ("petit", "PETIT VAISSEAU (2x2) :", ["• Rapide et peu coûteux", "• Bon pour l'exploration"]),
                ("moyen", "VAISSEAU MOYEN (2x2) :", ["• Équilibré en attaque et défense"]),
                ("lourd", "VAISSEAU LOURD (3x3) :", ["• Puissant mais lent et coûteux"]),
                ("foreuse", "FOREUSE (2x2) :", ["• Spécialisé dans le minage d'astéroïdes"]),
                ("transport", "TRANSPORTEUR (3x4) :", ["• Peut transporter d'autres vaisseaux"])
            ]
            
            for ship_type, title, details in ships_info:
                ship_img = self.ship_images.get(ship_type)
                
                # Position de départ pour cette section
                section_x = box_x + 150
                
                # Dessiner l'image du vaisseau (petite icône à gauche)
                if ship_img:
                    img_rect = ship_img.get_rect(x=section_x, centery=y_offset + 20)
                    
                    # Cadre autour de l'icône
                    glow_rect = pygame.Rect(img_rect.x - 5, img_rect.y - 5, 
                                           img_rect.width + 10, img_rect.height + 10)
                    pygame.draw.rect(self.screen, content["couleur"], glow_rect, 2, border_radius=5)
                    
                    self.screen.blit(ship_img, img_rect)
                
                # Dessiner le titre du vaisseau à droite de l'image
                title_x = section_x + 70
                title_surface = self.font_text.render(title, True, content["couleur"])
                title_rect = title_surface.get_rect(x=title_x, y=y_offset)
                self.screen.blit(title_surface, title_rect)
                
                # Dessiner les détails en dessous
                detail_y = y_offset + 30
                for detail in details:
                    detail_surface = self.font_text.render(detail, True, (200, 200, 255))
                    detail_rect = detail_surface.get_rect(x=title_x, y=detail_y)
                    self.screen.blit(detail_surface, detail_rect)
                    detail_y += 25
                
                y_offset += 90  # Espacement entre les vaisseaux
            
            # Message de fin
            y_offset += 20
            end_text = self.font_text.render("[ENTRÉE] pour continuer", True, (220, 220, 220))
            end_rect = end_text.get_rect(centerx=screen_width // 2, y=y_offset)
            self.screen.blit(end_text, end_rect)
            
        else:
            # Affichage normal pour les autres pages
            if image:
                # Créer un cadre avec glow pour l'image
                img_rect = image.get_rect(centerx=screen_width // 2, y=box_y + 90)
                
                # Effet de glow autour de l'image
                glow_surface = pygame.Surface((img_rect.width + 20, img_rect.height + 20), pygame.SRCALPHA)
                glow_rect = glow_surface.get_rect(center=img_rect.center)
                
                for i in range(3):
                    alpha = 60 - i * 20
                    pygame.draw.rect(glow_surface, (*content["couleur"], alpha), 
                                   glow_surface.get_rect(), 3 + i * 2, border_radius=10)
                
                self.screen.blit(glow_surface, glow_rect)
                self.screen.blit(image, img_rect)
                
                # Cadre autour de l'image
                pygame.draw.rect(self.screen, content["couleur"], img_rect.inflate(10, 10), 2, border_radius=5)
                
                image_offset = img_rect.height + 30
            
            # Texte (ajusté selon la présence d'image)
            y_offset = box_y + 90 + image_offset
            for line in content["texte"]:
                if line.startswith("•"):
                    # Puces avec couleur
                    text_surface = self.font_text.render(line, True, (200, 200, 255))
                elif line == "":
                    y_offset += 10
                    continue
                elif ":" in line and not line.startswith(" "):
                    # Titres de section en gras/couleur
                    text_surface = self.font_text.render(line, True, content["couleur"])
                else:
                    text_surface = self.font_text.render(line, True, (220, 220, 220))
                
                text_rect = text_surface.get_rect(centerx=screen_width // 2, y=y_offset)
                self.screen.blit(text_surface, text_rect)
                y_offset += 35
    
    def next_step(self):
        """Passe à l'étape suivante"""
        steps = list(TutorialStep)
        current_index = steps.index(self.current_step)
        if current_index < len(steps) - 1:
            self.current_step = steps[current_index + 1]
            return True
        return False
    
    def prev_step(self):
        """Retourne à l'étape précédente"""
        steps = list(TutorialStep)
        current_index = steps.index(self.current_step)
        if current_index > 0:
            self.current_step = steps[current_index - 1]
    
    def run(self):
        """Boucle principale du tutoriel"""
        clock = pygame.time.Clock()
        running = True
        
        while running:
            mouse_pos = pygame.mouse.get_pos()
            
            # Gestion des événements
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                        if not self.next_step():
                            return True  # Fin du tutoriel
                    elif event.key == pygame.K_ESCAPE:
                        return False  # Quitter le tutoriel
                    elif event.key == pygame.K_LEFT:
                        self.prev_step()
                    elif event.key == pygame.K_RIGHT:
                        if not self.next_step():
                            return True
                
                # Gestion des clics sur les boutons (dans les événements)
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.button_next.rect.collidepoint(mouse_pos):
                        if not self.next_step():
                            return True
                    elif self.button_prev.rect.collidepoint(mouse_pos):
                        self.prev_step()
                    elif self.button_skip.rect.collidepoint(mouse_pos):
                        return True
            
            # Mise à jour des boutons (uniquement pour le survol)
            self.button_next.update(mouse_pos)
            self.button_prev.update(mouse_pos)
            self.button_skip.update(mouse_pos)
            
            # Dessin
            self.draw_background()
            content = TutorialContent.STEPS[self.current_step]
            self.draw_content_box(content)
            
            # Dessin des boutons
            if self.current_step != TutorialStep.WELCOME:
                self.button_prev.draw(self.screen, self.font_button)
            
            if self.current_step != TutorialStep.FIN:
                self.button_next.draw(self.screen, self.font_button)
            else:
                # Bouton "Commencer" au lieu de "Suivant"
                self.button_next.text = "Commencer !"
                self.button_next.color = (100, 255, 100)
                self.button_next.draw(self.screen, self.font_button)
            
            self.button_skip.draw(self.screen, self.font_button)
            
            # Indicateur de progression
            steps = list(TutorialStep)
            current_index = steps.index(self.current_step) + 1
            total_steps = len(steps)
            progress_text = f"Étape {current_index}/{total_steps}"
            progress_surface = self.font_text.render(progress_text, True, (150, 150, 150))
            self.screen.blit(progress_surface, (self.screen.get_width() // 2 - 70, 30))
            
            pygame.display.flip()
            clock.tick(60)
        
        return False


def lancer_tutoriel(screen, stars=None, planet_manager=None):
    """
    Fonction principale pour lancer le tutoriel
    
    Args:
        screen: L'écran Pygame
        stars: (optionnel) StarField du menu pour garder le fond animé
        planet_manager: (optionnel) PlanetManager du menu pour garder les planètes
    
    Returns:
        bool: True si le tutoriel est terminé, False si quitté
    """
    tutorial = TutorialManager(screen, stars, planet_manager)
    return tutorial.run()


# Test du tutoriel si exécuté directement
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("Xenon Space - Tutoriel")
    
    resultat = lancer_tutoriel(screen)
    
    if resultat:
        print("Tutoriel terminé ! Le joueur est prêt.")
    else:
        print("Tutoriel quitté.")
    
    pygame.quit()