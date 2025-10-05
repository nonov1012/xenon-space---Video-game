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
# - NOEL Clément
# - 
# -
#################################################################
# Copyright (c) 2025                                            #
# Tous droits réservés. Merci de ne pas reproduire              #
# ou modifier le code sans autorisation.                        #
#################################################################

# Import lib
from pickle import NONE
import pygame

# Import classes
from classes.FloatingText import FloatingText
from classes.HUD.HUD import HUD
import menu.menuPause
import menu.menuPrincipal
import menu.menuFin
from classes.Turn import Turn
from classes.Map import Map
from classes.Start_Animation.StarField import StarField
from classes.Point import Type, Point
from blazyck import *
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


def set_prevision_for_ship(ship, case, direction):
    largeur, hauteur = ship.donner_dimensions(direction)
    ship.prevision.pixel_w = largeur * TAILLE_CASE
    ship.prevision.pixel_h = hauteur * TAILLE_CASE
    ship.prevision.x = case[1] * TAILLE_CASE + OFFSET_X
    ship.prevision.y = case[0] * TAILLE_CASE

    if direction == "haut":
        ship.prevision.target_angle = 0
    elif direction == "droite":
        ship.prevision.target_angle = -90
    elif direction == "gauche":
        ship.prevision.target_angle = 90
    elif direction == "bas":
        ship.prevision.target_angle = 180

def draw_glowing_rect(ecran, x, y, color, size=TAILLE_CASE, thickness=2):
    """Dessine un carré façon 'hologramme' avec glow futuriste, sans croix."""
    r, g, b = color
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
                menu.menuPause.main_pause(ecran)
            elif event.key == pygame.K_LCTRL:
                afficher_grille = not afficher_grille
            elif event.key == pygame.K_LSHIFT:
                afficher_zones = True
            elif event.key == pygame.K_r and selection_ship:
                selection_ship.rotation_aperçu_si_possible(case_souris, map_obj.grille)
            elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                # Fin de tour
                for ship in Turn.players[0].ships:
                    ship.reset_porters()
                    if isinstance(ship, Foreuse):
                        if ship.est_a_cote_planete(map_obj.grille):
                            ship.gain += PLANETES_REWARD
                        if ship.est_autour_asteroide(map_obj.grille):
                            ship.gain += ASTEROIDES_REWARD

                Turn.players[0].gain()
                res = Turn.next()
                HUD.change_turn()
                for player in Turn.players:
                    mother_ships = [s for s in player.ships if isinstance(s, MotherShip) and s.pv_actuel > 0]
                    if len(mother_ships) == 0:
                        print(f"Le joueur {player.name} a perdu !")
                        gagnant = [p for p in Turn.players if p != player][0]
                        menu.menuFin.main(ecran, gagnant, victoire=True)
                        running = False
                        break


        # --- Clic gauche ---
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # D'abord vérifier si on clique sur un bouton du shop
            shop_clicked = False
            for ship_data in shop.ships:
                if "rect" in ship_data and ship_data["rect"].collidepoint(event.pos):
                    shop_clicked = True
                    type_vaisseau = shop.buy_ship(ship_data)
                    
                    if type_vaisseau:
                        joueur_actuel = Turn.players[0]
                        tailles = {
                            "Petit": (2, 2),
                            "Moyen": (2, 2),
                            "Grand": (3, 3),
                            "Foreuse": (2, 2),
                            "Transporteur": (3, 4)
                        }
                        position = trouver_position_libre_base(map_obj, joueur_actuel.id, tailles[type_vaisseau])
                        
                        if position:
                            nouveau_vaisseau = creer_vaisseau_achete(
                                type_vaisseau, position, next_uid[0],
                                joueur_actuel.id, images, paths
                            )
                            if nouveau_vaisseau:
                                next_uid[0] += 1
                                joueur_actuel.ships.append(nouveau_vaisseau)
                                ships.append(nouveau_vaisseau)
                                nouveau_vaisseau.occuper_plateau(map_obj.grille, Type.VAISSEAU)
                                print(f"Nouveau {type_vaisseau} spawné en position ({position.x}, {position.y})")
                        else:
                            print(f"Impossible de trouver une position libre pour le {type_vaisseau}")
                            joueur_actuel.economie.ajouter(ship_data["price"])
                    break

            # Si on n'a pas cliqué sur le shop
            if not shop_clicked:
                if selection_ship and not interface_transport_active:
                    # Vérifier si on a cliqué sur une case de déplacement possible ou d'attaque
                    positions_deplacement = selection_ship.positions_possibles_adjacentes(map_obj.grille, direction=selection_ship.aperçu_direction)
                    positions_attaque = selection_ship.positions_possibles_attaque(map_obj.grille, direction=selection_ship.aperçu_direction)

                    # 🟦 Si on clique sur une case valide (déplacement ou attaque)
                    if case_souris in positions_deplacement or case_souris in positions_attaque:
                        success = selection_ship.deplacement(case_souris, map_obj.grille, ships)
                        if success:
                            selection_ship, selection_cargo = None, None

                    # 🟥 Si on clique sur le vaisseau sélectionné → on le désélectionne
                    elif (case_souris[0] == selection_ship.cordonner.x and
                          case_souris[1] == selection_ship.cordonner.y):
                        selection_ship, selection_cargo = None, None

                    # ⚪ Sinon → clic en dehors de toute zone utile → désélection
                    else:
                        selection_ship, selection_cargo = None, None

                else:
                    # Tentative de sélection d'un nouveau vaisseau
                    for ship in ships[:]:
                        largeur, hauteur = ship.donner_dimensions(ship.direction)
                        if (ship.cordonner.x <= case_souris[0] < ship.cordonner.x + hauteur and
                            ship.cordonner.y <= case_souris[1] < ship.cordonner.y + largeur):
                            if ship.joueur == Turn.players[0].id:
                                selection_ship = ship
                                selection_ship.aperçu_direction = ship.direction
                                selection_ship.aperçu_cordonner._x = ship.cordonner.x
                                selection_ship.aperçu_cordonner._y = ship.cordonner.y
                            else:
                                print(f"Ce vaisseau appartient au joueur {ship.joueur}")
                            break
                    else:
                        # Aucun vaisseau cliqué → désélection
                        selection_ship, selection_cargo = None, None

        # --- Clic droit ---
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3 and selection_ship:
            if isinstance(selection_ship, Transport):
                clicked_on_mini = False
                for i, ship in enumerate(selection_ship.cargaison):
                    if ship is None:
                        continue
                    rect = pygame.Rect(selection_ship.cordonner.y * TAILLE_CASE + OFFSET_X + i*22,
                                       selection_ship.cordonner.x * TAILLE_CASE - 22, 20, 20)
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
                            success = target.ajouter_cargo(selection_ship)
                            if success:
                                selection_ship.liberer_position(map_obj.grille)
                                ships.remove(selection_ship)
                                selection_ship, selection_cargo, interface_transport_active = None, None, False
                        break

    return running, selection_ship, selection_cargo, interface_transport_active, afficher_grille, next_uid

def draw_game(ecran, stars, map_obj, colors, ships, selection_ship, selection_cargo,
              interface_transport_active, case_souris, font, player, shop, new_cursor, position_souris,
              afficher_grille, dt):
    ecran.fill((0, 0, 0, 0))
    stars.update()
    stars.draw(ecran)

    keys = pygame.key.get_pressed()
    afficher_zones = keys[pygame.K_LSHIFT]

    map_obj.generer_grille(ecran, afficher_zones, afficher_grille, colors)

    for (ax, ay), img in map_obj.asteroide_img_map.items():
        ecran.blit(img, (ax * TAILLE_CASE + OFFSET_X, ay * TAILLE_CASE))

    if selection_ship and isinstance(selection_ship, Transport):
        selection_ship.afficher_cargaison(ecran)

    # --- Preview déplacement / débarquement ---
    if selection_ship:
        if interface_transport_active and selection_cargo:
            # Cases possibles pour débarquer (jaune holographique)
            positions_possibles = selection_ship.positions_debarquement(selection_cargo, map_obj.grille)
            for ligne, colonne in positions_possibles:
                draw_glowing_rect(ecran,
                                colonne * TAILLE_CASE + OFFSET_X,
                                ligne * TAILLE_CASE,
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
                                colonne * TAILLE_CASE + OFFSET_X,
                                ligne * TAILLE_CASE,
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
                            colonne * TAILLE_CASE + OFFSET_X,
                            ligne * TAILLE_CASE,
                            (255, 80, 80))

            # Si astéroïde minable → orange
            if (0 <= ligne < len(map_obj.grille) and 0 <= colonne < len(map_obj.grille[0]) and
                map_obj.grille[ligne][colonne].type == Type.ASTEROIDE and selection_ship.peut_miner):
                draw_glowing_rect(ecran,
                                colonne * TAILLE_CASE + OFFSET_X,
                                ligne * TAILLE_CASE,
                                (255, 180, 80))


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

    shop.draw()
    ecran.blit(new_cursor, position_souris)

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
        start_y, end_y = 0, 15  # Chercher dans une zone plus large autour de la base
        start_x, end_x = 0, 15
    else:  # joueur_id == 2
        # Base en bas à droite
        start_y = max(0, NB_CASE_Y - 15)
        end_y = NB_CASE_Y
        start_x = max(0, NB_CASE_X - 15)
        end_x = NB_CASE_X
    
    largeur, hauteur = taille_vaisseau
    
    # Chercher une position libre dans la zone
    for y in range(start_y, min(end_y, NB_CASE_Y - hauteur + 1)):
        for x in range(start_x, min(end_x, NB_CASE_X - largeur + 1)):
            # Vérifier si toutes les cases sont libres
            position_valide = True
            for dy in range(hauteur):
                for dx in range(largeur):
                    if y + dy >= NB_CASE_Y or x + dx >= NB_CASE_X:
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
    for y in range(NB_CASE_Y - hauteur + 1):
        for x in range(NB_CASE_X - largeur + 1):
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
    classes_vaisseaux = {
        "Petit": Petit,
        "Moyen": Moyen,
        "Grand": Lourd,  # Grand dans le shop correspond à Lourd | TODO : modifier celui du shop
        "Foreuse": Foreuse,
        "Transporteur": Transport
    }
    
    classe = classes_vaisseaux.get(type_vaisseau)
    if classe is None:
        return None
    
    # Type simplifié selon le vaisseau
    type_key = "lourd" if type_vaisseau == "Grand" else type_vaisseau.lower()
    if type_vaisseau == "Transporteur":
        type_key = "transport"
    
    return classe(
        cordonner=position,
        id=next_uid,
        path=paths.get(type_key, paths['petit']),
        image=images.get(type_key, images['petit']),
        joueur=joueur_id
    )

def start_game(ecran, parametres, random_active):
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 30)
    
    new_cursor = pygame.image.load('assets/img/menu/cursor.png')
    new_cursor = pygame.transform.scale(new_cursor, (40, 40))
    pygame.mouse.set_visible(False)
    
    # Générer la map
    screen_width, screen_height = ecran.get_size()
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
    map_obj.generer_planet(parametres["Nombre de planetes"]["valeur"])
    map_obj.generer_asteroides(parametres["Nombre d'asteroides"]["valeur"])
    
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
    
    # TODO : refaire le shop pour que ça soit dans les players
    player = Player("TestPlayer", solde_initial=3000)
    shop = Shop(player, font, ecran)

    # ===== Player =====
    Turn.players = [Player("P1", id=0), Player("P2", id=1)]

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
    smm1 = MotherShip(
        tier=1,
        cordonner=Point(0, 0),
        id=next_uid[0],
        path=img_base_dir,
        joueur=Turn.players[0].id
    )
    next_uid[0] += 1
    Turn.players[0].ships.append(smm1)

    # MotherShip du joueur 2
    smm2 = MotherShip(
        tier=1,
        cordonner=Point(25, 46),
        id=next_uid[0],
        path=img_base_dir,
        joueur=Turn.players[1].id
    )
    next_uid[0] += 1
    Turn.players[1].ships.append(smm2)

    # Petit vaisseau joueur 1
    sp1 = Petit(
        cordonner=Point(5, 1),
        id=next_uid[0],
        path=img_petit_dir,
        image=img_petit,
        joueur=Turn.players[0].id
    )
    next_uid[0] += 1
    Turn.players[0].ships.append(sp1)

    # Vaisseau lourd joueur 2
    sl1 = Lourd(
        cordonner=Point(5, 5),
        id=next_uid[0],
        path=img_lourd_dir,
        image=img_Lourd,
        joueur=Turn.players[1].id
    )
    next_uid[0] += 1
    Turn.players[1].ships.append(sl1)

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

    # --- Placer vaisseaux sur la grille ---
    for s in Turn.get_players_ships():
        s.occuper_plateau(map_obj.grille, Type.VAISSEAU)

    # --- initialisation du HUD ---
    HUD.init(ecran)

    # --- Variables de sélection et contrôle ---
    selection_ship = None
    selection_cargo = None
    interface_transport_active = False
    afficher_grille = False
    running = True

    while running:
        discord.update("En jeu")
        position_souris = pygame.mouse.get_pos()
        case_souris = ((position_souris[1]) // TAILLE_CASE, 
                       (position_souris[0] - OFFSET_X) // TAILLE_CASE)        

        # Appeler handle_events avec les nouveaux paramètres
        running, selection_ship, selection_cargo, interface_transport_active, afficher_grille, next_uid = \
            handle_events(running, selection_ship, selection_cargo, interface_transport_active,
                        afficher_grille, map_obj, Turn.get_players_ships(), shop, ecran, position_souris, case_souris,
                        next_uid, images, paths)  # Ajout des nouveaux paramètres
        
        shop.player = Turn.players[0]  # Mettre à jour le joueur actuel dans le shop

        dt = clock.tick(60) / 1000.0
        
        draw_game(ecran, stars, map_obj, colors, Turn.get_players_ships(), selection_ship, selection_cargo,
                interface_transport_active, case_souris, font, Turn.players[0], shop, new_cursor, position_souris,
                afficher_grille, dt)



        clock.tick(60)

    pygame.quit()
