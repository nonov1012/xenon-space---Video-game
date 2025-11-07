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
            return False
        
        # Trouver les cibles potentielles
        cible = self._trouver_meilleure_cible(grille, ships)
        
        if cible:
            # Attaquer la cible
            self.attaquer(cible)
            print(f"IA : J'attaque {cible.__class__.__name__} ennemi")
            
            # Si la cible est détruite, la retirer
            if cible.est_mort():
                cible.liberer_position(grille)
                if cible in ships:
                    ships.remove(cible)
                print("IA : Cible détruite !")
            
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
        Gère intelligemment l'argent de la base avec une stratégie adaptative.
        
        Stratégie :
        - Situation critique (valuation < -2000) : Acheter des vaisseaux lourds défensifs
        - Situation défavorable (valuation < 0) : Spam de petits vaisseaux
        - Situation équilibrée (0 < valuation < 1500) : Équilibrer économie et armée
        - Situation dominante (valuation > 1500) : Focus économie et upgrades
        
        :param ships: Liste de tous les vaisseaux du jeu
        :param player: Le joueur propriétaire de ce MotherShip
        :param shop: Le shop du joueur
        :param map_obj: La carte du jeu
        :param next_uid: Liste contenant l'UID suivant [uid]
        :param images: Dictionnaire des images
        :param paths: Dictionnaire des chemins
        """
        argent_disponible = player.economie.etat()
        valuation = self._valuation_militaire(ships)
        
        # Compter les foreuses existantes
        nb_foreuses = sum(1 for s in player.ships if isinstance(s, Foreuse) and not s.est_mort())
        nb_petits = sum(1 for s in player.ships if isinstance(s, Petit) and not s.est_mort())
        nb_moyens = sum(1 for s in player.ships if isinstance(s, Moyen) and not s.est_mort())
        nb_lourds = sum(1 for s in player.ships if isinstance(s, Lourd) and not s.est_mort())
        
        print(f"IA : Argent={argent_disponible}, Valuation={valuation}, Tier={self.tier}")
        print(f"IA : Flotte - Foreuses={nb_foreuses}, Petits={nb_petits}, Moyens={nb_moyens}, Lourds={nb_lourds}")
        
        # SITUATION CRITIQUE
        if valuation < -2000:
            print("IA : 🔴 SITUATION CRITIQUE - Défense d'urgence !")
            # Essayer d'acheter un Lourd si possible
            if self._acheter_vaisseau(player, shop, map_obj, next_uid, images, paths, ships, "Grand", (3, 4)):
                return
            # Sinon acheter un Moyen
            if self._acheter_vaisseau(player, shop, map_obj, next_uid, images, paths, ships, "Moyen", (2, 2)):
                return
            # En dernier recours, spam de Petits
            self._acheter_vaisseau(player, shop, map_obj, next_uid, images, paths, ships, "Petit", (1, 1))
            return
        
        # SITUATION DÉFAVORABLE : On perd la bataille
        elif valuation < 0:
            print("IA : 🟠 Situation défavorable - Construction d'armée")
            
            # Si on a assez d'argent pour un Moyen et qu'on en a peu
            if argent_disponible >= 650 and nb_moyens < 2 and self.tier >= 3:
                if self._acheter_vaisseau(player, shop, map_obj, next_uid, images, paths, ships, "Moyen", (2, 2)):
                    return
            
            # Sinon spam de Petits (cost-efficient)
            self._acheter_vaisseau(player, shop, map_obj, next_uid, images, paths, ships, "Petit", (1, 1))
            return
        
        # SITUATION ÉQUILIBRÉE : Développement équilibré
        elif valuation < 1500:
            print("IA : 🟡 Situation équilibrée - Développement mixte")
            
            # Priorité 1 : Upgrade de la base si rentable
            cout_upgrade = self.get_next_tier_cost()
            if cout_upgrade and argent_disponible >= cout_upgrade and self.tier < 4:
                # Upgrade si le coût est inférieur à 2x notre argent (on garde une marge)
                if argent_disponible >= cout_upgrade * 1.2:
                    if self.upgrade(player.buy):
                        print(f"IA : ⬆️ Base améliorée au tier {self.tier} !")
                        return
            
            # Priorité 2 : Maintenir au moins 2 foreuses pour l'économie
            if nb_foreuses < 2:
                if self._acheter_vaisseau(player, shop, map_obj, next_uid, images, paths, ships, "Foreuse", (1, 1)):
                    return
            
            # Priorité 3 : Diversifier l'armée
            # Si on a beaucoup de Petits mais peu de Moyens, acheter un Moyen
            if nb_petits >= 3 and nb_moyens < 2 and argent_disponible >= 650 and self.tier >= 3:
                if self._acheter_vaisseau(player, shop, map_obj, next_uid, images, paths, ships, "Moyen", (2, 2)):
                    return
            
            # Priorité 4 : Acheter un Petit pour maintenir la pression
            if argent_disponible >= 325:
                self._acheter_vaisseau(player, shop, map_obj, next_uid, images, paths, ships, "Petit", (1, 1))
                return
        
        # SITUATION DOMINANTE : Focus économie et tech
        else:
            print("IA : 🟢 Situation dominante - Focus économie et upgrades")
            
            # Priorité 1 : Upgrade de la base (débloquer attaque au tier 4)
            cout_upgrade = self.get_next_tier_cost()
            if cout_upgrade and argent_disponible >= cout_upgrade:
                if self.upgrade(player.buy):
                    print(f"IA : ⭐ Base améliorée au tier {self.tier} !")
                    return
            
            # Priorité 2 : Acheter un Lourd si tier 4 et qu'on en a moins de 2
            if self.tier >= 4 and nb_lourds < 2 and argent_disponible >= 1050:
                if self._acheter_vaisseau(player, shop, map_obj, next_uid, images, paths, ships, "Grand", (3, 4)):
                    return
            
            # Priorité 3 : Maximiser les foreuses (jusqu'à 4)
            if nb_foreuses < 4:
                if self._acheter_vaisseau(player, shop, map_obj, next_uid, images, paths, ships, "Foreuse", (1, 1)):
                    return
            
            # Priorité 4 : Si on a trop d'argent, acheter un Moyen
            if argent_disponible >= 1000 and self.tier >= 3:
                self._acheter_vaisseau(player, shop, map_obj, next_uid, images, paths, ships, "Moyen", (2, 2))

    def _acheter_vaisseau(self, player, shop, map_obj, next_uid, images, paths, ships, nom_vaisseau, taille):
        """
        Fonction helper pour acheter et spawner un vaisseau.
        
        :param nom_vaisseau: Nom du vaisseau dans le shop ("Petit", "Moyen", "Grand", "Foreuse")
        :param taille: Tuple (largeur, hauteur) du vaisseau
        :param ships: Liste globale des vaisseaux
        :return: True si l'achat a réussi, False sinon
        """
        for ship_dict in shop.ships:
            if ship_dict["name"] == nom_vaisseau:
                if player.economie.etat() >= ship_dict["price"] and self.tier >= ship_dict["tier"]:
                    if player.economie.retirer(ship_dict["price"]):
                        position = self._trouver_position_libre_base(map_obj, player.id, taille)
                        
                        if position:
                            # Mapper le nom du shop vers le type de vaisseau
                            type_map = {
                                "Petit": "Petit",
                                "Moyen": "Moyen",
                                "Grand": "Lourd",
                                "Foreuse": "Foreuse"
                            }
                            type_vaisseau = type_map.get(nom_vaisseau)
                            
                            nouveau_vaisseau = self._creer_vaisseau(
                                type_vaisseau, position, next_uid[0], player.id, images, paths
                            )
                            if nouveau_vaisseau:
                                next_uid[0] += 1
                                player.ships.append(nouveau_vaisseau)
                                ships.append(nouveau_vaisseau)  # Ajouter à la liste globale
                                nouveau_vaisseau.occuper_plateau(map_obj.grille, Type.VAISSEAU)
                                print(f"IA : ✅ Achat d'un {nom_vaisseau} réussi !")
                                return True
                        else:
                            player.economie.ajouter(ship_dict["price"])
                            print(f"IA : ❌ Pas de place pour {nom_vaisseau}, remboursé")
                break
        return False

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
        elif type_vaisseau == "Moyen":
            return Moyen(
                cordonner=position,
                id=uid,
                path=paths.get('moyen'),
                image=images.get('moyen'),
                joueur=joueur_id
            )
        elif type_vaisseau == "Lourd":
            return Lourd(
                cordonner=position,
                id=uid,
                path=paths.get('lourd'),
                image=images.get('lourd'),
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