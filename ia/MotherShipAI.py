import pygame
from typing import Optional, Tuple, List
from classes.MotherShip import MotherShip
from classes.Ship import Ship, Petit, Moyen, Lourd, Foreuse
from classes.Point import Point, Type
from menu.modifShips import SHIP_STATS


class MotherShipIA(MotherShip):
    """
    Classe MotherShip contrôlée par l'IA.
    Attaque automatiquement les vaisseaux ennemis à portée.
    """
    
    def __init__(self, tier: int, cordonner: Point, id: Optional[int] = None,
                 path: str = None, show_health: bool = False, joueur: int = 1,
                 taille: Optional[Tuple[int, int]] = None):
        """
        Constructeur de la classe MotherShipIA.
        Hérite de MotherShip avec les mêmes paramètres.
        """
        super().__init__(
            tier=tier,
            cordonner=cordonner,
            id=id,
            path=path,
            show_health=show_health,
            joueur=joueur,
            taille=taille
        )
    
    def jouer_tour(self, grille, ships: List[Ship], player, shop, map_obj, next_uid, images, paths) -> bool:
        """
        Exécute le tour de l'IA pour le MotherShip.
        
        :param grille: Grille du jeu
        :param ships: Liste de tous les vaisseaux
        :param player: Le joueur IA
        :param shop: Le shop du joueur IA
        :param map_obj: La carte du jeu
        :param next_uid: Liste contenant l'UID suivant
        :param images: Dictionnaire des images
        :param paths: Dictionnaire des chemins
        :return: True si une action a été effectuée, False sinon
        """
        self.achat_stategique(ships, player, shop, map_obj, next_uid, images, paths)
        
        if self.est_mort():
            return False
        
        if self.port_attaque <= 0:
            print("pas de portée d'attaque")
            return False
        
        # Trouver les cibles potentielles
        cible = self._trouver_meilleure_cible(grille, ships)
        
        if cible:
            # Attaquer la cible
            self.attaquer(cible)
            print("j'attaque le vaisseau:")
            print(cible)
            
            # Si la cible est détruite, la retirer
            if cible.est_mort():
                cible.liberer_position(grille)
                if cible in ships:
                    ships.remove(cible)
            
            return True
        
        return False
    
    def _trouver_meilleure_cible(self, grille, ships: List[Ship]) -> Optional[Ship]:
        """
        Trouve le meilleur vaisseau ennemi à attaquer.
        
        Priorités :
        1. Vaisseaux ennemis les plus proches
        2. Vaisseaux avec le moins de PV (pour tuer rapidement)
        3. Vaisseaux avec le plus de valeur (cout élevé)
        
        :param grille: Grille du jeu
        :param ships: Liste de tous les vaisseaux
        :return: Le vaisseau cible ou None
        """
        positions_attaque = self.positions_possibles_attaque(grille, direction=self.direction)
        
        cibles_potentielles = []
        
        # Trouver tous les vaisseaux ennemis à portée
        for ligne, colonne in positions_attaque:
            vaisseau = self.trouver_vaisseau_a_position(ships, ligne, colonne)
            
            if vaisseau and vaisseau.joueur != self.joueur and not vaisseau.est_mort():
                # Calculer la distance de Manhattan
                distance = abs(self.cordonner.x - vaisseau.cordonner.x) + \
                          abs(self.cordonner.y - vaisseau.cordonner.y)
                
                # Calculer un score de priorité
                # Plus le score est élevé, plus la cible est prioritaire
                score = 0
                
                # Priorité 1 : Distance (plus proche = meilleur)
                score += (self.port_attaque - distance) * 100
                
                # Priorité 2 : Vaisseaux presque morts (pour finir rapidement)
                ratio_pv = vaisseau.pv_actuel / vaisseau.pv_max
                if ratio_pv < 0.3:  # Moins de 30% de PV
                    score += 200
                elif vaisseau.pv_actuel <= self.attaque:  # Peut être tué en un coup
                    score += 300
                
                # Priorité 3 : Valeur du vaisseau (cout élevé = cible intéressante)
                score += vaisseau.cout / 10
                
                cibles_potentielles.append((score, vaisseau))
        
        # Trier par score décroissant et retourner la meilleure cible
        if cibles_potentielles:
            cibles_potentielles.sort(key=lambda x: x[0], reverse=True)
            return cibles_potentielles[0][1]
        
        return None
    
    def _est_vaisseau_ennemi_a_position(self, ships: List[Ship], ligne: int, colonne: int) -> bool:
        """
        Vérifie s'il y a un vaisseau ennemi à une position donnée.
        
        :param ships: Liste de tous les vaisseaux
        :param ligne: Ligne de la position
        :param colonne: Colonne de la position
        :return: True si un ennemi est présent
        """
        vaisseau = self.trouver_vaisseau_a_position(ships, ligne, colonne)
        return vaisseau is not None and vaisseau.joueur != self.joueur and not vaisseau.est_mort()
    
    def _valuation_militaire(self, ships: List[Ship]) -> int:
        """
        Donne une valuation de la situation militaire.
        
        :param ships: Liste de tous les vaisseaux
        :return: Valuation militaire ( > 0 = avantage, < 0 = désavantage )
        """
        valeur_totale = 0
        valeur_totale_ennemie = 0

        for vaisseau in ships:
            if not vaisseau.est_mort() and isinstance(vaisseau, (Petit, Moyen, Lourd)):
                if vaisseau.joueur != self.joueur:
                    valeur_totale_ennemie += vaisseau.cout
                else:
                    valeur_totale += vaisseau.cout

        valuation = valeur_totale - valeur_totale_ennemie
        return valuation

    def achat_stategique(self, ships: List[Ship], player, shop, map_obj, next_uid, images, paths):
        """
        Gère intelligemment l'argent de la base.
        Achète des vaisseaux et les fait spawner correctement.
        
        :param ships: Liste de tous les vaisseaux du jeu
        :param player: Le joueur propriétaire de ce MotherShip
        :param shop: Le shop du joueur
        :param map_obj: La carte du jeu (pour trouver une position libre)
        :param next_uid: Liste contenant l'UID suivant [uid]
        :param images: Dictionnaire des images des vaisseaux
        :param paths: Dictionnaire des chemins vers les assets
        """
        argent_disponible = player.economie.etat()
        print("IA : Argent disponible: ")
        print(argent_disponible)
        print(self._valuation_militaire(ships))
        
        if self._valuation_militaire(ships) < 0:
            # Situation défavorable, acheter des vaisseaux de combat
            for ship_dict in shop.ships:
                if ship_dict["name"] == "Petit":
                    # Vérifier argent et tier requis
                    if argent_disponible >= ship_dict["price"] and self.tier >= ship_dict["tier"]:
                        # Retirer l'argent
                        if player.economie.retirer(ship_dict["price"]):
                            # Trouver une position libre
                            position = self._trouver_position_libre_base(map_obj, player.id, (1, 1))
                            
                            if position:
                                # Créer le vaisseau
                                nouveau_vaisseau = self._creer_vaisseau(
                                    "Petit", position, next_uid[0], player.id, images, paths
                                )
                                if nouveau_vaisseau:
                                    next_uid[0] += 1
                                    player.ships.append(nouveau_vaisseau)
                                    ships.append(nouveau_vaisseau)
                                    nouveau_vaisseau.occuper_plateau(map_obj.grille, Type.VAISSEAU)
                                    print(f"IA : Achat d'un Petit vaisseau (situation défavorable)")
                            else:
                                # Pas de position libre, rembourser
                                player.economie.ajouter(ship_dict["price"])
                                print("IA : Pas de place pour spawner le vaisseau, remboursé")
                    break
        else:
            # Situation favorable, améliorer la base ou acheter des foreuses
            cout_upgrade = self.get_next_tier_cost()
            
            # Essayer d'upgrader la base
            print("Coût upgrade : ")
            print(cout_upgrade)
            print("Argent disponible : ")
            print(argent_disponible)
            if cout_upgrade is not None and argent_disponible >= cout_upgrade:
                if self.upgrade(player.buy):
                    print(f"IA : Base améliorée au tier {self.tier}")
                    return
            
            # Sinon acheter une foreuse
            for ship_dict in shop.ships:
                if ship_dict["name"] == "Foreuse":
                    if argent_disponible >= ship_dict["price"] and self.tier >= ship_dict["tier"]:
                        # Retirer l'argent
                        if player.economie.retirer(ship_dict["price"]):
                            # Trouver une position libre
                            position = self._trouver_position_libre_base(map_obj, player.id, (1, 1))
                            
                            if position:
                                # Créer le vaisseau
                                nouveau_vaisseau = self._creer_vaisseau(
                                    "Foreuse", position, next_uid[0], player.id, images, paths
                                )
                                if nouveau_vaisseau:
                                    next_uid[0] += 1
                                    player.ships.append(nouveau_vaisseau)
                                    ships.append(nouveau_vaisseau)
                                    nouveau_vaisseau.occuper_plateau(map_obj.grille, Type.VAISSEAU)
                                    print(f"IA : Achat d'une Foreuse (situation favorable)")
                            else:
                                # Pas de position libre, rembourser
                                player.economie.ajouter(ship_dict["price"])
                                print("IA : Pas de place pour spawner la foreuse, remboursé")
                    break

    def _trouver_position_libre_base(self, map_obj, joueur_id, taille_vaisseau):
        """
        Trouve une position libre près de la base du joueur pour spawner un vaisseau.
        """
        grille = map_obj.grille
        
        # Définir la zone de recherche selon le joueur
        if joueur_id == 0:
            # Base en haut à gauche
            start_y, end_y = 0, 7
            start_x, end_x = 0, 7
        else:  # joueur_id == 1
            # Base en bas à droite
            start_y = max(0, len(grille) - 7)
            end_y = len(grille)
            start_x = max(0, len(grille[0]) - 7)
            end_x = len(grille[0])
        
        largeur, hauteur = taille_vaisseau
        
        # Chercher une position libre dans la zone préférée
        for y in range(start_y, min(end_y, len(grille) - hauteur + 1)):
            for x in range(start_x, min(end_x, len(grille[0]) - largeur + 1)):
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
        
        return None

    def _creer_vaisseau(self, type_vaisseau, position, uid, joueur_id, images, paths):
        """
        Crée une instance du vaisseau acheté selon son type.
        """
        if type_vaisseau == "Petit":
            return Petit(
                cordonner=position,
                id=uid,
                path=paths.get('petit'),
                image=images.get('petit'),
                joueur=joueur_id
            )
        elif type_vaisseau == "Foreuse":
            return Foreuse(
                cordonner=position,
                id=uid,
                path=paths.get('foreuse'),
                image=images.get('foreuse'),
                joueur=joueur_id
            )
        
        return None