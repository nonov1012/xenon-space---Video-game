import pygame
from typing import Optional, Tuple
from classes.Ship import Ship
from classes.Point import Point
from classes.Animator import Animator
from classes.ShipAnimator import ShipAnimator
from classes.ProjectileAnimator import ProjectileAnimator
from blazyck import *
from menu.modifShips import SHIP_STATS

LEVELS = SHIP_STATS["MotherShip"]

class MotherShip(Ship):
    """Base fixe du joueur, ne peut pas se déplacer ni tourner."""

    def __init__(self, tier: int, cordonner: Point, id: Optional[int] = None,
                 path: str = None, show_health: bool = False, joueur: int = 1,
                 taille: Optional[Tuple[int, int]] = None):
        """
        Constructeur de la classe MotherShip.
        
        :param tier: Niveau de la base (1-4)
        :param cordonner: Position initiale
        :param id: Identifiant unique
        :param path: Chemin vers les assets
        :param show_health: Afficher les points de vie
        :param joueur: Numéro du joueur propriétaire
        :param taille: Taille personnalisée (largeur, hauteur). Si None, utilise celle des stats
        """
        stats = LEVELS[tier]
        
        # Utiliser la taille des stats par défaut, ou celle fournie
        taille_finale = taille if taille is not None else stats["taille"]
        
        super().__init__(
            pv_max=stats["pv_max"],
            attaque=stats["attaque"],
            port_attaque=stats["port_attaque"],
            port_deplacement=stats["port_deplacement"],
            cout=stats["cout"],
            taille=taille_finale,
            peut_miner=stats["peut_miner"],
            peut_transporter=stats["peut_transporter"],
            image=pygame.Surface((taille_finale[1]*TAILLE_CASE, taille_finale[0]*TAILLE_CASE)),
            tier=tier,
            cordonner=cordonner,
            id=id,
            path=path,
            joueur=joueur
        )
        
        self.prevision.alpha = 0
        self.animator.show_health = show_health
        self.gain = stats.get("gain", 300)


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
        self.gain = new_conf.get("gain", self.gain)
        self.pv_actuel = self.pv_max

    def upgrade(self, payer_fct) -> bool:
        if not self.can_upgrade(): return False
        price = self.get_next_tier_cost()
        if price is None or not payer_fct(price): return False
        self.apply_level(self.tier + 1)
        return True
    