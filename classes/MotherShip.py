import os
import pygame
from typing import Any, Dict, Optional
from classes.Ship import Ship
from classes.Animator import Animator

# Configuration des niveaux
LEVELS: Dict[int, Dict[str, Any]] = {
    1: {"cout_upgrade": 1000, "pv_max": 500, "gains": 300, "attaque": 0, "port_attaque": 0},
    2: {"cout_upgrade": 2000, "pv_max": 800, "gains": 350, "attaque": 0, "port_attaque": 0},
    3: {"cout_upgrade": 6000, "pv_max": 1300, "gains": 400, "attaque": 0, "port_attaque": 0},
    4: {"cout_upgrade": None, "pv_max": 1700, "gains": 450, "attaque": 100, "port_attaque": 3},
}

# Chemin vers le dossier contenant base.png
current_dir = os.path.dirname(__file__)
BASE_IMG_DIR = os.path.join(current_dir, "..", "assets", "img", "ships", "base")

# Vérification rapide
base_file = os.path.join(BASE_IMG_DIR, "base.png")
print("BASE_IMG_DIR =", BASE_IMG_DIR)
print("base.png exists?", os.path.isfile(base_file))


class MotherShip(Ship):
    """Vaisseau mère : ne peut ni bouger ni tourner, mais peut être amélioré."""

    def __init__(self, screen: pygame.Surface, position: tuple[int, int], tier: int = 1, uid: Optional[int] = 1):
        taille = (4, 5)
        self.tier = tier
        self.screen = screen

        tier_conf = LEVELS[tier]
        pv_max = tier_conf["pv_max"]
        attaque = tier_conf.get("attaque", 0)
        port_attaque = tier_conf.get("port_attaque", 0)
        port_deplacement = 0
        cout = tier_conf.get("cout_upgrade", 0)
        valeur_mort = 0
        peut_miner = False
        peut_transporter = False
        self.is_dead_anim_playing = False


        # Placeholder image
        image = pygame.Surface((taille[0]*35, taille[1]*35))
        image.fill((200, 200, 200))


        super().__init__(
            pv_max=pv_max,
            attaque=attaque,
            port_attaque=port_attaque,
            port_deplacement=port_deplacement,
            cout=cout,
            valeur_mort=valeur_mort,
            taille=taille,
            peut_miner=peut_miner,
            peut_transporter=peut_transporter,
            image=image,
            tier=tier,
            ligne=position[0],
            colonne=position[1],
            uid=uid
        )

        # Animator avec tile_size = 32 pour que l'image soit visible
        self.animator = Animator(
            screen,
            BASE_IMG_DIR,
            taille,
            (position[1]*32, position[0]*32),
            tile_size=32
        )

    # Déplacement et rotation désactivés
    def deplacement(self, *args, **kwargs): return False
    def rotation_aperçu(self, *args, **kwargs): pass
    def rotation_aperçu_si_possible(self, *args, **kwargs): pass

    # Gestion des niveaux / upgrade
    @property
    def max_tier(self) -> int: return max(LEVELS.keys())
    def can_upgrade(self) -> bool:
        return (self.tier + 1 in LEVELS) and LEVELS[self.tier].get("cout_upgrade") is not None
    
    def get_next_tier_cost(self) -> Optional[int]: return LEVELS[self.tier].get("cout_upgrade")

    def apply_level(self, tier: int) -> None:
        if tier not in LEVELS: raise ValueError(f"Tier inconnu {tier}")
        new_conf = LEVELS[tier]
        self.tier = tier
        self.pv_max = new_conf["pv_max"]
        self.attaque = new_conf.get("attaque", self.attaque)
        self.port_attaque = new_conf.get("port_attaque", self.port_attaque)
        self.cout = new_conf.get("cout_upgrade", self.cout)
        self.pv_actuel += self.pv_max

    def upgrade(self, payer_fct) -> bool:
        if not self.can_upgrade(): return False
        price = self.get_next_tier_cost()
        if price is None or not payer_fct(price): return False
        self.apply_level(self.tier + 1)
        return True
    
    def subir_degats(self, amount: int):
        """Compatible avec Ship. Joue animation shield à chaque attaque."""
        self.take_damage(amount)

    # Combat / dégâts
    def take_damage(self, amount: int):
        self.pv_actuel = max(0, self.pv_actuel - max(0, amount))
        if self.pv_actuel > 0:
            self.animator.play("shield")  # animation bouclier
        else:
            if not self.is_dead_anim_playing:
                self.animator.play("destruction")  # animation mort
                self.is_dead_anim_playing = True


    def dead(self) -> bool:
        """Retourne True si le vaisseau est mort et que l'animation destruction est terminée"""
        return self.pv_actuel <= 0 and self.is_dead_anim_playing and self.animator.is_animation_finished("destruction")

    def update(self):
        self.animator.update(self.pv_actuel, self.pv_max)

    def heal(self, amount: int):
        self.pv_actuel = min(self.pv_max, self.pv_actuel + amount)


    
    def attack(self, cible: Any):
        if hasattr(cible, "take_damage"): cible.take_damage(self.attaque)

    # Rendu
    def dessiner(self, surface, taille_case):
        self.update()
        self.animator.update_and_draw()


    def __del__(self):
        print("Vaisseau mère détruit")

