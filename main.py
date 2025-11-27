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
# Développé par :                                               #
# - nonov1012                                                   #
# - DAVID Gabriel                                               #
# - brian62100                                                  #
# - NOEL Clément                                                #
# - Tom Vanhove                                                 #
# - CAVEL Ugo                                                   #
#################################################################
# Copyright (c) 2025                                            #
# Tous droits réservés. Merci de ne pas reproduire              #
# ou modifier le code sans autorisation.                        #
#################################################################


# Import lib
from pickle import NONE
import pygame
import time

# Import classes
from classes.FloatingText import FloatingText
from classes.HUD.HUD import HUD

import menu.menuPause
import menu.menuFin
from menu.modifShips import SHIP_STATS
from classes.Turn import Turn
from classes.Map import Map
from classes.Start_Animation.StarField import StarField
from classes.Point import Type, Point
from classes.Discord import DiscordRP
from classes.Animator import Animator
from classes.PlanetAnimator import PlanetAnimator
from classes.ShipAnimator import ShipAnimator
from classes.Shop import Shop
from classes.Player import Player
from classes.MotherShip import MotherShip
from classes.ProjectileAnimator import ProjectileAnimator
from classes.Economie import Economie
from classes.Ship import Transport, Foreuse, Petit, Moyen, Lourd
from classes.GlobalVar.ScreenVar import ScreenVar
from classes.GlobalVar.GridVar import GridVar

from blazyck import *

from IA.petit.ia_utils import *
from IA.IA_Lourd import IA_Lourd
from IA.MotherShipAI import MotherShipIA
from IA.foreuse import jouer_tour_foreuse
from IA.IATransport import IATransport

def set_prevision_for_ship(ship, case, direction):
    largeur, hauteur = ship.donner_dimensions(direction)
    ship.prevision.pixel_w = largeur * GridVar.cell_size
    ship.prevision.pixel_h = hauteur * GridVar.cell_size
    ship.prevision.x = case[1] * GridVar.cell_size + GridVar.offset_x
    ship.prevision.y = case[0] * GridVar.cell_size

    if direction == "haut":
        ship.prevision.target_angle = 0
    elif direction == "droite":
        ship.prevision.target_angle = -90
    elif direction == "gauche":
        ship.prevision.target_angle = 90
    elif direction == "bas":
        ship.prevision.target_angle = 180

def draw_glowing_rect(ecran, x, y, color, thickness=2):
    """Dessine un carré façon 'hologramme' avec glow futuriste, sans croix."""
    r, g, b = color
    size = GridVar.cell_size
    rect = pygame.Rect(x, y, size, size)

    # contours superposés pour un effet lumineux
    for i in range(3):
        alpha = 80 - i * 25
        glow_surf = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.rect(glow_surf, (r, g, b, alpha),
                         glow_surf.get_rect(), thickness + i*2, border_radius=3)
        ecran.blit(glow_surf, (x, y))

def handle_events(running, selection_ship, selection_cargo, interface_transport_active,
                  afficher_grille, map_obj, ships, shop, ecran, position_souris, case_souris,
                  next_uid, images, paths):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # --- Touches clavier ---
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = menu.menuPause.main_pause(ecran)
                continue
            elif event.key == pygame.K_LCTRL:
                afficher_grille = not afficher_grille
            elif event.key == pygame.K_LSHIFT:
                afficher_zones = True
            elif event.key == pygame.K_r and selection_ship:
                selection_ship.rotation_aperçu_si_possible(case_souris, map_obj.grille)
            elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                end_choice = end_turn_logic(ecran, map_obj)
                if end_choice == 0:
                    continue
                elif end_choice == 1:
                    running = False
                elif end_choice == 2:
                    running = 2
                            
        elif event.type == pygame.VIDEORESIZE:
            ScreenVar.update_scale()
            GridVar.update_grid()

        # --- Clic gauche ---
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            shop_clicked = False
            # Gérer les clics via la fonction du shop
            joueur_actuel = Turn.players[0]
            mothership_actuel = joueur_actuel.getMotherShip()
            type_action = shop.handle_click(event.pos, mothership_actuel)

            is_skipping = HUD.handle_click(event.pos)
            if is_skipping:
                end_choice = end_turn_logic(ecran, map_obj)
                if end_choice == 0:
                    continue
                elif end_choice == 1:
                    running = False
                elif end_choice == 2:
                    running = 2

            if type_action:

                # Si le joueur a acheté un vaisseau
                if type_action in ["Petit", "Moyen", "Lourd", "Foreuse", "Transport"]:
                    
                    tailles = {
                        "Petit": (2, 2),
                        "Moyen": (2, 2),
                        "Lourd": (3, 3),
                        "Foreuse": (2, 2),
                        "Transport": (3, 4)
                    }
                    position = trouver_position_libre_base(map_obj, joueur_actuel.id, tailles[type_action])

                    if position:
                        nouveau_vaisseau = creer_vaisseau_achete(
                            type_action, position, next_uid[0],
                            joueur_actuel.id, images, paths
                        )
                        
                        if nouveau_vaisseau:
                            next_uid[0] += 1
                            joueur_actuel.ships.append(nouveau_vaisseau)
                            ships.append(nouveau_vaisseau)
                            nouveau_vaisseau.occuper_plateau(map_obj.grille, Type.VAISSEAU)
                            HUD.ship_display.ship = nouveau_vaisseau
                            selection_ship = nouveau_vaisseau
                    else:
                        # Si aucune position libre, on rembourse
                        prix_vaisseaux = {
                            "Petit": 250,
                            "Moyen": 1000,
                            "Lourd": 4000,
                            "Foreuse": 700,
                            "Transport": 2000
                        }
                        
                        prix = prix_vaisseaux.get(type_action, 0)
                        if prix > 0:
                            joueur_actuel.economie.ajouter(prix)

                # Si c’est une amélioration de base
                elif type_action == "base_upgrade":
                    mothership_actuel = joueur_actuel.getMotherShip()
                    mothership_actuel.upgrade()



            # Si on n'a pas cliqué sur le shop
            elif not shop_clicked:
                if selection_ship and not interface_transport_active:
                    # Vérifier si on a cliqué sur une case de déplacement possible ou d'attaque
                    positions_deplacement = selection_ship.positions_possibles_adjacentes(map_obj.grille, direction=selection_ship.aperçu_direction)
                    positions_attaque = selection_ship.positions_possibles_attaque(map_obj.grille, direction=selection_ship.aperçu_direction)

                    # 🟦 Si on clique sur une case valide (déplacement ou attaque)
                    if case_souris in positions_deplacement or case_souris in positions_attaque:
                        success = selection_ship.deplacement(case_souris, map_obj.grille, ships)
                        if success:
                            selection_ship, selection_cargo = None, None
                            HUD.ship_display.ship = Turn.players[0].getMotherShip()

                    # 🟥 Si on clique sur le vaisseau sélectionné → on le désélectionne
                    elif (case_souris[0] == selection_ship.cordonner.x and
                          case_souris[1] == selection_ship.cordonner.y):
                        selection_ship, selection_cargo = None, None
                        HUD.ship_display.ship = Turn.players[0].getMotherShip()

                    # ⚪ Sinon → clic en dehors de toute zone utile → désélection
                    else:
                        selection_ship, selection_cargo = None, None
                        HUD.ship_display.ship = Turn.players[0].getMotherShip()

                else:
                    # Tentative de sélection d'un nouveau vaisseau
                    for ship in ships[:]:
                        largeur, hauteur = ship.donner_dimensions(ship.direction)
                        if (ship.cordonner.x <= case_souris[0] < ship.cordonner.x + hauteur and
                            ship.cordonner.y <= case_souris[1] < ship.cordonner.y + largeur):
                            if ship.joueur == Turn.players[0].id:
                                selection_ship = ship
                                HUD.ship_display.ship = selection_ship
                                selection_ship.aperçu_direction = ship.direction
                                selection_ship.aperçu_cordonner._x = ship.cordonner.x
                                selection_ship.aperçu_cordonner._y = ship.cordonner.y
                            break
                    else:
                        # Aucun vaisseau cliqué → désélection
                        selection_ship, selection_cargo = None, None
                        HUD.ship_display.ship = Turn.players[0].getMotherShip()

        # --- Clic droit ---
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3 and selection_ship:
            if isinstance(selection_ship, Transport):
                clicked_on_mini = False
                for i, ship in enumerate(selection_ship.cargaison):
                    if ship is None:
                        continue
                    rect = pygame.Rect(selection_ship.cordonner.y * GridVar.cell_size + GridVar.offset_x + i*22,
                                       selection_ship.cordonner.x * GridVar.cell_size - 22, 20, 20)
                    if rect.collidepoint(position_souris):
                        selection_cargo = ship
                        interface_transport_active = True
                        clicked_on_mini = True
                        break

                if not clicked_on_mini and interface_transport_active and selection_cargo:
                    positions_valides = selection_ship.positions_debarquement(selection_cargo, map_obj.grille)
                    if case_souris in positions_valides:
                        index = selection_ship.cargaison.index(selection_cargo)
                        success = selection_ship.retirer_cargo(index, case_souris[0], case_souris[1],
                                                               map_obj.grille, ships)
                        if success:
                            selection_cargo, interface_transport_active = None, False
            else:
                for target in ships:
                    if target == selection_ship:
                        continue
                    largeur, hauteur = target.donner_dimensions(target.direction)
                    if (target.cordonner.x <= case_souris[0] < target.cordonner.x + hauteur and
                        target.cordonner.y <= case_souris[1] < target.cordonner.y + largeur):
                        if isinstance(target, Transport):
                            success = target.ajouter_cargo(selection_ship, map_obj.grille)
                            if success:
                                selection_ship.liberer_position(map_obj.grille)
                                ships.remove(selection_ship)
                                selection_ship, selection_cargo, interface_transport_active = None, None, False
                        break

    return running, selection_ship, selection_cargo, interface_transport_active, afficher_grille, next_uid

def draw_game(ecran, stars, map_obj, colors, ships, selection_ship, selection_cargo,
              interface_transport_active, case_souris, font, player, shop, position_souris,
              afficher_grille, dt, ia_tour_termine=False):
    ecran.fill((0, 0, 0, 0))
    stars.update()
    stars.draw(ecran)

    keys = pygame.key.get_pressed()
    afficher_zones = keys[pygame.K_LSHIFT]

    map_obj.generer_grille(ecran, HUD.show_colors, HUD.show_grid, colors)

    for (ax, ay), img in map_obj.asteroide_img_map.items():
        ecran.blit(img, (ax * GridVar.cell_size + GridVar.offset_x, ay * GridVar.cell_size))

    if selection_ship and isinstance(selection_ship, Transport):
        selection_ship.afficher_cargaison(ecran)

    # --- Preview déplacement / débarquement ---
    if selection_ship:
        if interface_transport_active and selection_cargo:
            # Cases possibles pour débarquer (jaune holographique)
            positions_possibles = selection_ship.positions_debarquement(selection_cargo, map_obj.grille)
            for ligne, colonne in positions_possibles:
                draw_glowing_rect(ecran,
                                colonne * GridVar.cell_size + GridVar.offset_x,
                                ligne * GridVar.cell_size,
                                (255, 255, 120))

            if case_souris in positions_possibles:
                selection_cargo.prevision.alpha = 120
                set_prevision_for_ship(selection_cargo, case_souris, selection_cargo.direction)
                selection_cargo.prevision.update_and_draw()
            else:
                selection_cargo.prevision.alpha = 0
        else:
            # Cases possibles pour déplacement (cyan futuriste)
            positions_possibles = selection_ship.positions_possibles_adjacentes(
                map_obj.grille, direction=selection_ship.aperçu_direction
            )
            for ligne, colonne in positions_possibles:
                draw_glowing_rect(ecran,
                                colonne * GridVar.cell_size + GridVar.offset_x,
                                ligne * GridVar.cell_size,
                                (80, 200, 255))

            if case_souris in positions_possibles:
                selection_ship.prevision.alpha = 120
                set_prevision_for_ship(selection_ship, case_souris, selection_ship.aperçu_direction)
                selection_ship.prevision.update_and_draw()
            else:
                selection_ship.prevision.alpha = 0

    # --- Preview attaque / minage ---
    if selection_ship and not interface_transport_active:
        positions_attaque = selection_ship.positions_possibles_attaque(
            map_obj.grille, direction=selection_ship.aperçu_direction
        )
        for ligne, colonne in positions_attaque:
            draw_glowing_rect(ecran,
                            colonne * GridVar.cell_size + GridVar.offset_x,
                            ligne * GridVar.cell_size,
                            (255, 80, 80))

            # Si astéroïde minable → orange
            if (0 <= ligne < len(map_obj.grille) and 0 <= colonne < len(map_obj.grille[0]) and
                map_obj.grille[ligne][colonne].type == Type.ASTEROIDE and selection_ship.peut_miner):
                draw_glowing_rect(ecran,
                                colonne * GridVar.cell_size + GridVar.offset_x,
                                ligne * GridVar.cell_size,
                                (255, 180, 80))
                
    if ia_tour_termine:
        # Message principal
        message = font.render("L'IA a terminé son tour", True, (100, 255, 100))
        rect_msg = message.get_rect(center=(ecran.get_width() // 2, ecran.get_height() // 2 - 30))
        
        # Message instruction
        instruction = font.render("Appuyez sur ENTRÉE pour continuer", True, (255, 255, 255))
        rect_inst = instruction.get_rect(center=(ecran.get_width() // 2, ecran.get_height() // 2 + 10))
        
        # Fond semi-transparent
        overlay = pygame.Surface((ecran.get_width(), ecran.get_height()), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        ecran.blit(overlay, (0, 0))
        
        # Afficher les messages
        ecran.blit(message, rect_msg)
        ecran.blit(instruction, rect_inst)



    # (--- preview mouvement/attaque ---)

    Animator.update_all()
    PlanetAnimator.update_all()
    ShipAnimator.update_all()
    ProjectileAnimator.update_all()
    FloatingText.update_and_draw_all(ecran, dt)
    HUD.update_and_draw()

    if selection_ship:
        info_text = f"{selection_ship.__class__.__name__} - PV: {selection_ship.pv_actuel}/{selection_ship.pv_max}"
        ecran.blit(font.render(info_text, True, (255, 255, 255)), (10, 40))

    pygame.display.flip()
    
def trouver_position_libre_base(map_obj, joueur_id, taille_vaisseau):
    """
    Trouve une position libre près de la base du joueur pour spawner un vaisseau.
    joueur_id: 1 pour joueur 1 (base en haut à gauche), 2 pour joueur 2 (base en bas à droite)
    """
    grille = map_obj.grille
    
    # Définir la zone de recherche selon le joueur
    if joueur_id == 0:
        # Base en haut à gauche (0,0 à 5,4)
        start_y, end_y = 0, 7  # Chercher dans une zone plus large autour de la base
        start_x, end_x = 0, 7
    else:  # joueur_id == 2
        # Base en bas à droite
        start_y = max(0, GridVar.nb_cells_y - 7)
        end_y = GridVar.nb_cells_y
        start_x = max(0, GridVar.nb_cells_x - 7)
        end_x = GridVar.nb_cells_x
    
    largeur, hauteur = taille_vaisseau
    
    # Chercher une position libre dans la zone
    for y in range(start_y, min(end_y, GridVar.nb_cells_y - hauteur + 1)):
        for x in range(start_x, min(end_x, GridVar.nb_cells_x - largeur + 1)):
            # Vérifier si toutes les cases sont libres
            position_valide = True
            for dy in range(hauteur):
                for dx in range(largeur):
                    if y + dy >= GridVar.nb_cells_y or x + dx >= GridVar.nb_cells_x:
                        position_valide = False
                        break
                    case = grille[y + dy][x + dx]
                    if case.type not in [Type.VIDE, Type.ATMOSPHERE]:
                        position_valide = False
                        break
                if not position_valide:
                    break
            
            if position_valide:
                return Point(y, x)
    
    # Si aucune position trouvée dans la zone préférée, chercher ailleurs
    for y in range(GridVar.nb_cells_y - hauteur + 1):
        for x in range(GridVar.nb_cells_x - largeur + 1):
            position_valide = True
            for dy in range(hauteur):
                for dx in range(largeur):
                    case = grille[y + dy][x + dx]
                    if case.type not in [Type.VIDE, Type.ATMOSPHERE]:
                        position_valide = False
                        break
                if not position_valide:
                    break
            
            if position_valide:
                return Point(y, x)
    
    return None  # Aucune position trouvée


def creer_vaisseau_achete(type_vaisseau, position, next_uid, joueur_id, images, paths):
    """
    Crée une instance du vaisseau acheté selon son type.
    """
    
    # Type simplifié selon le vaisseau
    type_key = type_vaisseau.lower()
    if type_vaisseau == "lourd":
        type_key = "lourd"
    elif type_vaisseau == "transport":
        type_key = "transport"
    
    
    # Cas spécial : Petit n'a pas besoin de path/image
    if type_vaisseau == "Petit":
        vaisseau = Petit(
            cordonner=position,
            id=next_uid,
            joueur=joueur_id
        )
        return vaisseau
    
    # Mapping des types vers les classes
    classes_vaisseaux = {
        "Moyen": Moyen,
        "Lourd": Lourd,
        "Foreuse": Foreuse,
        "Transport": Transport
    }
    
    classe = classes_vaisseaux.get(type_vaisseau)
    
    if classe is None:
        return None
    
    path = paths.get(type_key, paths['petit'])
    image = images.get(type_key, images['petit'])
    
    try:
        vaisseau = classe(
            cordonner=position,
            id=next_uid,
            path=path,
            image=image,
            joueur=joueur_id
        )
        return vaisseau
    except Exception as e:
        import traceback
        traceback.print_exc()
        return None

def end_turn_logic(ecran, map_obj):
    """
    Contient toute la logique de fin de tour (gain, changement de joueur, 
    vérification de victoire). Peut être appelée par le joueur ou l'IA.
    """
    current_player = Turn.players[0]
    
    # Logique de gain de fin de tour
    for ship in current_player.ships:
        ship.reset_porters()
        if isinstance(ship, Foreuse):
            if ship.est_a_cote_planete(map_obj.grille): # Note: map_obj devra être accessible
                ship.gain += PLANETES_REWARD
            if ship.est_autour_asteroide(map_obj.grille):
                ship.gain += ASTEROIDES_REWARD
    current_player.gain()

    # Passer au joueur suivant
    Turn.next()
    HUD.change_turn()

    # Vérification de la condition de victoire
    for player in Turn.players:
        mother_ships = [s for s in player.ships if isinstance(s, MotherShip) and not s.est_mort()]
        if not mother_ships:
            gagnant = [p for p in Turn.players if p != player][0]
            return menu.menuFin.main(ecran, gagnant, victoire=True)
    
    return 0 # Le jeu continue

def draw_ia_tour_termine_message(ecran):
    """Affiche un message stylisé 'Tour terminé' en haut à droite"""
    screen_width = ecran.get_width()
    
    # Créer les fonts
    font_titre = pygame.font.Font(None, 36)
    font_instruction = pygame.font.Font(None, 24)
    
    # Texte principal
    message = font_titre.render("Tour terminé", True, (100, 255, 100))
    instruction = font_instruction.render("Appuyez sur ENTRÉE", True, (200, 200, 200))
    
    # Position en haut à droite
    padding = 20
    box_width = max(message.get_width(), instruction.get_width()) + 40
    box_height = message.get_height() + instruction.get_height() + 30
    box_x = screen_width - box_width - padding
    box_y = padding
    
    # Fond semi-transparent avec bordure
    background = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
    pygame.draw.rect(background, (0, 0, 0, 180), background.get_rect(), border_radius=10)
    pygame.draw.rect(background, (100, 255, 100, 255), background.get_rect(), 3, border_radius=10)
    
    ecran.blit(background, (box_x, box_y))
    
    # Afficher les textes
    msg_rect = message.get_rect(center=(box_x + box_width // 2, box_y + 25))
    inst_rect = instruction.get_rect(center=(box_x + box_width // 2, box_y + 55))
    
    ecran.blit(message, msg_rect)
    ecran.blit(instruction, inst_rect)

def start_game(parametres, random_active, joueurs):

    # Initialisations rapides
    clock = pygame.time.Clock()
    screen = ScreenVar.screen
    ScreenVar.update_scale()
    GridVar.update_grid()
    font = pygame.font.Font(None, 30)
    

    # Générer la map
    screen_width, screen_height = screen.get_size()
    num_stars=100
    screen_ratio=1.0
    stars = StarField(
        screen_width,
        screen_height,
        num_stars=int(num_stars * screen_ratio),
        min_radius=1,
        max_radius=3,
        move_amplitude=0
    )


    map_obj = Map()
    map_obj.generer_planet(parametres["Nombre de planètes"]["valeur"])
    map_obj.generer_asteroides(parametres["Nombre d'astéroïdes"]["valeur"])
    
    # couleurs pour l'affichage des zones
    colors = {
        Type.VIDE: (0, 0, 0, 0),
        Type.PLANETE: (255, 215, 0, 128),
        Type.ATMOSPHERE: (0, 200, 255, 128),
        Type.ASTEROIDE: (255, 215, 0, 128),
        Type.BASE: (100, 100, 125, 128),
        Type.VAISSEAU: (255, 0, 0, 128),
    }
    
    # Status discord
    discord = DiscordRP(RPC_ID)
    discord.connect()

    # ===== Player =====
    Turn.players = [Player(joueurs["Joueur 1"]["nom"], id=0, is_ia = joueurs["Joueur 1"]["est_ia"]), Player(joueurs["Joueur 2"]["nom"], id=1, is_ia = joueurs["Joueur 2"]["est_ia"])]
    Turn.shops=[Shop(Turn.players[0]), Shop(Turn.players[1])]

    # ===== Images et chemins pour les vaisseaux =====
    # Dictionnaires pour stocker les images et chemins
    
    img_Lourd = pygame.image.load("assets/img/ships/lourd/base.png").convert_alpha()
    img_moyen = pygame.image.load("assets/img/ships/moyen/base.png").convert_alpha()
    img_petit = pygame.image.load("assets/img/ships/petit/base.png").convert_alpha()
    img_foreuse = pygame.image.load("assets/img/ships/foreuse/base.png").convert_alpha()
    img_transport = pygame.image.load("assets/img/ships/transport/base.png").convert_alpha()

    # --- Chemins vers les dossiers ---
    img_lourd_dir = "assets/img/ships/lourd"
    img_moyen_dir = "assets/img/ships/moyen"
    img_petit_dir = "assets/img/ships/petit"
    img_foreuse_dir = "assets/img/ships/foreuse"
    img_transport_dir = "assets/img/ships/transport"
    img_base_dir = "assets/img/ships/base"
    
    images = {
        'lourd': img_Lourd,
        'moyen': img_moyen,
        'petit': img_petit,
        'foreuse': img_foreuse,
        'transport': img_transport
    }
    
    paths = {
        'lourd': img_lourd_dir,
        'moyen': img_moyen_dir,
        'petit': img_petit_dir,
        'foreuse': img_foreuse_dir,
        'transport': img_transport_dir,
        'base': img_base_dir
    }

    # --- Création vaisseaux ---
    next_uid = [1]

    # MotherShip du joueur 1
    smm1 = MotherShipIA(
        tier=4,
        cordonner=Point(0, 0),
        id=next_uid[0],
        path=img_base_dir,
        joueur=Turn.players[0].id
    )
    next_uid[0] += 1
    Turn.players[0].ships.append(smm1)

    # Petit vaisseau joueur 1
    sp1 = Petit(
        cordonner=Point(5, 1),
        id=next_uid[0],
        joueur=Turn.players[0].id
    )
    next_uid[0] += 1
    Turn.players[0].ships.append(sp1)

    # Foreuse joueur 1
    sf1 = Foreuse(
        cordonner=Point(1, 5),
        id=next_uid[0],
        path=img_foreuse_dir,
        image=img_foreuse,
        joueur=Turn.players[0].id
    )
    next_uid[0] += 1
    Turn.players[0].ships.append(sf1)


    # MotherShip du joueur 2
    smm2 = MotherShipIA(
        tier=4,
        cordonner=Point(25, 46),
        id=next_uid[0],
        path=img_base_dir,
        joueur=Turn.players[1].id
    )
    next_uid[0] += 1
    Turn.players[1].ships.append(smm2)

        # Petit vaisseau joueur 2
    sp2 = Petit(
        cordonner=Point(24, 45),
        id=next_uid[0],
        joueur=Turn.players[1].id
    )
    next_uid[0] += 1
    Turn.players[1].ships.append(sp2)


    # Foreuse joueur 2
    sf2 = Foreuse(
        cordonner=Point(24, 38),
        id=next_uid[0],
        path=img_foreuse_dir,
        image=img_foreuse,
        joueur=Turn.players[1].id
    )
    next_uid[0] += 1
    Turn.players[1].ships.append(sf2)

    

    # --- Placer vaisseaux sur la grille ---
    for s in Turn.get_players_ships():
        s.occuper_plateau(map_obj.grille, Type.VAISSEAU)

    # --- initialisation du HUD ---
    HUD.init()
    HUD.ship_display.ship = Turn.players[0].getMotherShip()

    # --- Variables de sélection et contrôle ---
    selection_ship = None
    selection_cargo = None
    interface_transport_active = False
    afficher_grille = False
    running = True
    ships_passed = False

    pygame.time.wait(500) # Petite pause pour que le joueur voie le message "Prêt

    # =================================================================
    # ✨ NOUVELLE BOUCLE DE JEU PRINCIPALE AVEC GESTION DE L'IA ✨
    # =================================================================
    dernier_temps_ia = 0
    delai_ia_ms = 250  # 250 ms entre chaque action IA

    # ---------------------
    # BOUCLE PRINCIPALE
    # ---------------------
    # Au début de start_game, ajoutez cette variable
    ia_tour_termine = False  # Indique si l'IA a fini son tour et attend confirmation

    # Dans la boucle principale
    while running:
        discord.update("En jeu")
        position_souris = pygame.mouse.get_pos()
        case_souris = ((position_souris[1]) // GridVar.cell_size, 
                       (position_souris[0] - GridVar.offset_x) // GridVar.cell_size)

        joueur_actuel = Turn.players[0]
        shop = Turn.shops[0]

        # ---------------------
        # TOUR DE L'IA
        # ---------------------
        if joueur_actuel.is_ia:
            # ✨ Si l'IA a fini, attendre que le joueur appuie sur Entrée
            if ia_tour_termine:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            menu.menuPause.main_pause(screen)
                        elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                            ia_tour_termine = False
                            end_choice = end_turn_logic(screen, map_obj)
                            if end_choice == 0:
                                continue
                            elif end_choice == 1:
                                running = False
                            elif end_choice == 2:
                                running = 2
                    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        ia_tour_termine = False
                        # Gérer les clics via la fonction du shop
                        joueur_actuel = Turn.players[0]
                        mothership_actuel = joueur_actuel.getMotherShip()
                        is_skipping = HUD.handle_click(event.pos)
                        if is_skipping:
                            end_choice = end_turn_logic(screen, map_obj)
                            if end_choice == 0:
                                continue
                            elif end_choice == 1:
                                running = False
                            elif end_choice == 2:
                                running = 2
                        
            # Sinon, l'IA continue de jouer
            else:
                # Gérer seulement QUIT et ESC pendant que l'IA joue
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        menu.menuPause.main_pause(screen)
                
                maintenant = pygame.time.get_ticks()
                if maintenant - dernier_temps_ia >= delai_ia_ms:
                    dernier_temps_ia = maintenant

                    tous_les_vaisseaux = Turn.get_players_ships()
                    ships_passed = True

                    for ship_ia in joueur_actuel.ships[:]:
                        transport_ia_instance = None

                        if ship_ia.animator.target == (ship_ia.animator.x, ship_ia.animator.y) or ship_ia.animator.current_anim != "weapon":
                            if isinstance(ship_ia, IA_Lourd):
                                ship_ia.jouer_tour_ia(map_obj.grille, tous_les_vaisseaux, Turn.players[1].ships)
                            elif isinstance(ship_ia, Petit):
                                ships_passed = ia_petit_play(ship_ia, map_obj, tous_les_vaisseaux)
                            elif isinstance(ship_ia, Moyen):
                                ships_passed = ia_petit_play(ship_ia, map_obj, tous_les_vaisseaux)
                            elif isinstance(ship_ia, Foreuse):
                                jouer_tour_foreuse(ship_ia, map_obj.grille, tous_les_vaisseaux)
                            elif isinstance(ship_ia, Transport):
                                transport_ia_instance.jouer_tour(map_obj.grille, joueur_actuel.ships)
                            elif isinstance(ship_ia, MotherShipIA):
                                if not ship_ia.est_mort():
                                    ship_ia.jouer_tour(map_obj.grille, tous_les_vaisseaux, joueur_actuel, shop, map_obj, next_uid, images, paths)
                        else:
                            ships_passed = False

                    # ✨ Si tous les vaisseaux ont fini, marquer le tour comme terminé
                    if ships_passed:
                        ia_tour_termine = True

        # ---------------------
        # TOUR DU JOUEUR HUMAIN
        # ---------------------
        else:
            ia_tour_termine = False  # Réinitialiser au cas où
            running, selection_ship, selection_cargo, interface_transport_active, afficher_grille, next_uid = \
                handle_events(running, selection_ship, selection_cargo, interface_transport_active,
                              afficher_grille, map_obj, Turn.get_players_ships(), shop, screen, position_souris, case_souris,
                              next_uid, images, paths)
        if running == 2:
            return 2
        
        # ---------------------
        # DESSIN (pour le joueur humain, l'IA dessine pendant son tour)
        # ---------------------
        dt = clock.tick(60) / 1000.0
        draw_game(screen, stars, map_obj, colors, Turn.get_players_ships(), selection_ship, selection_cargo,
                  interface_transport_active, case_souris, font, joueur_actuel, shop, position_souris,
                  afficher_grille, dt)
