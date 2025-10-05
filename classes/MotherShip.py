import pygame
from typing import Optional, Tuple
from classes.Ship import Ship
from classes.Point import Point
from classes.Animator import Animator
from classes.ShipAnimator import ShipAnimator
from classes.ProjectileAnimator import ProjectileAnimator
from blazyck import *

LEVELS = {
    1: {"cout_upgrade": 1000, "pv_max": 500, "gains": 300, "attaque": 0, "port_attaque": 0},
    2: {"cout_upgrade": 2000, "pv_max": 800, "gains": 350, "attaque": 0, "port_attaque": 0},
    3: {"cout_upgrade": 6000, "pv_max": 1300, "gains": 400, "attaque": 0, "port_attaque": 0},
    4: {"cout_upgrade": None, "pv_max": 1700, "gains": 450, "attaque": 100, "port_attaque": 3},
}

class MotherShip(Ship):
    """Base fixe du joueur, ne peut pas se déplacer ni tourner."""

    def __init__(self,
                 pv_max: int,
                 attaque: int,
                 port_attaque: int,
                 port_deplacement: int,
                 cout: int,
                 taille: Tuple[int,int],
                 tier: int,
                 cordonner: Point,
                 id: Optional[int] = None,
                 path: str = None,
                 show_health : bool = False,
                 joueur : int = 1):
        """
        Constructeur de la classe MotherShip.
        
        :param pv_max: Points de vie maximum
        :param attaque: Dégâts infligés par attaque
        :param port_attaque: Portée d'attaque en cases
        :param port_deplacement: Portée de déplacement (points de mouvement)
        :param cout: Coût d'achat
        :param taille: Dimensions du vaisseau (largeur, hauteur en cases)
        :param tier: Niveau technologique
        :param cordonner: Position initiale (coin haut-gauche du vaisseau)
        :param id: Identifiant unique
        :param path: Chemin vers les assets
        :param show_health: Afficher les points de vie
        :param joueur: Numéro du joueur propriétaire
        """
        super().__init__(pv_max, attaque, port_attaque, port_deplacement,
                         cout, taille, peut_miner=False,
                         peut_transporter=False, image=pygame.Surface((taille[1]*TAILLE_CASE, taille[0]*TAILLE_CASE)),
                         tier=tier, cordonner=cordonner, id=id, path=path, joueur=joueur)
        
        self.prevision.alpha = 0
        self.animator.show_health = show_health
        self.gain = 300 # TODO : modifié par une valeur paramétrable

    # ---------------- Déplacement et rotation désactivés ----------------
    def deplacement(self, *args, **kwargs):
        return False

    def rotation_aperçu(self, *args, **kwargs):
        pass

    def rotation_aperçu_si_possible(self, *args, **kwargs):
        pass

    # ---------------- Gestion des niveaux ----------------
    @property
    def max_tier(self) -> int:
        return max(LEVELS.keys())

    def can_upgrade(self) -> bool:
        return (self.tier + 1 in LEVELS) and LEVELS[self.tier].get("cout_upgrade") is not None

    def get_next_tier_cost(self) -> Optional[int]:
        return LEVELS[self.tier].get("cout_upgrade")

    def apply_level(self, tier: int) -> None:
        if tier not in LEVELS: raise ValueError(f"Tier inconnu {tier}")
        new_conf = LEVELS[tier]
        self.tier = tier
        self.pv_max = new_conf["pv_max"]
        self.attaque = new_conf.get("attaque", self.attaque)
        self.port_attaque = new_conf.get("port_attaque", self.port_attaque)
        self.cout = new_conf.get("cout_upgrade", self.cout)
        self.pv_actuel = self.pv_max

    def upgrade(self, payer_fct) -> bool:
        if not self.can_upgrade(): return False
        price = self.get_next_tier_cost()
        if price is None or not payer_fct(price): return False
        self.apply_level(self.tier + 1)
        return True
    