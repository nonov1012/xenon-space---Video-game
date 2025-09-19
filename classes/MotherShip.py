from time import sleep
from typing import Any, Dict, Optional
import pygame
import sys
from classes.Animator import Animator
import os
from classes.Point import Point
from blazyck import *

# Exemple de configuration des niveaux (tiers).
# Chaque clé est un tier. Les valeurs sont les attributs applicables à la base à ce niveau.
LEVELS: Dict[int, Dict[str, Any]] = {
    1: {
        "cout_upgrade": 1000,    # coût pour passer au niveau suivant
        "PV_max": 500,
        "gains": 300,
        "atk": 0,
        "distance_atk": 0,
    },
    2: {
        "cout_upgrade": 2000,
        "PV_max": 800,
        "gains": 350,
        "atk": 0,
        "distance_atk": 0,
    },
    3: {
        "cout_upgrade": 6000,
        "PV_max": 1300,
        "gains": 400,
        "atk": 0,
        "distance_atk": 0,
    },
    4: {
        "cout_upgrade": None,   # None => pas d'upgrade possible (niveau max)
        "PV_max": 1700,
        "gains": 450,
        "atk": 100,
        "distance_atk": 3,
    },
}


import os
import pygame
from typing import Any, Dict, Optional

# ---------------- Exemple de configuration des niveaux ----------------
LEVELS: Dict[int, Dict[str, Any]] = {
    1: {"cout_upgrade": 1000, "PV_max": 500, "gains": 300, "atk": 0, "distance_atk": 0},
    2: {"cout_upgrade": 2000, "PV_max": 800, "gains": 350, "atk": 0, "distance_atk": 0},
    3: {"cout_upgrade": 6000, "PV_max": 1300, "gains": 400, "atk": 0, "distance_atk": 0},
    4: {"cout_upgrade": None, "PV_max": 1700, "gains": 450, "atk": 100, "distance_atk": 3},
}

class MotherShip:
    """Représente la base d'un joueur avec niveaux, PV, et combat."""

    def __init__(self, screen : pygame.Surface, point : Point, tier: int = 1):
        self.largeur = 4
        self.hauteur = 5
        self.tier = tier

        # Charger les stats du tier
        dict_tier = LEVELS[self.tier]
        self.PV_max = dict_tier["PV_max"]
        self.PV_actuelle = self.PV_max
        self.atk = dict_tier.get("atk", 0)
        self.distance_atk = dict_tier.get("distance_atk", 0)
        self.gains = dict_tier.get("gains", 0)
        self.cout = dict_tier.get("cout_upgrade", 0)

        sprites_path = os.path.join(IMG_PATH, "base")

        # Animation
        self.animator = Animator(screen, sprites_path, (self.largeur, self.hauteur), (point.x, point.y))

    # ---------- Niveaux ----------
    @property
    def max_tier(self) -> int:
        return max(LEVELS.keys())

    def can_upgrade(self) -> bool:
        return (self.tier + 1 in LEVELS) and LEVELS[self.tier].get("cout_upgrade") is not None

    def get_next_tier_cost(self) -> Optional[int]:
        return LEVELS[self.tier].get("cout_upgrade")

    def apply_level(self, tier: int) -> None:
        if tier not in LEVELS:
            raise ValueError(f"Tier inconnu {tier}")
        new_conf = LEVELS[tier]
        self.tier = tier
        self.PV_max = new_conf["PV_max"]
        self.atk = new_conf.get("atk", self.atk)
        self.distance_atk = new_conf.get("distance_atk", self.distance_atk)
        self.gains = new_conf.get("gains", self.gains)
        # PV actuels augmentés proportionnellement
        self.PV_actuelle += self.PV_max

    def upgrade(self, payer_fct) -> bool:
        if not self.can_upgrade():
            return False
        price = self.get_next_tier_cost()
        if price is None or not payer_fct(price):
            return False
        self.apply_level(self.tier + 1)
        return True

    # ---------- Combat ----------
    def take_damage(self, amount: int):
        self.PV_actuelle = max(0, self.PV_actuelle - max(0, amount))
        self.animator.play("shield")
        self.update()

    def heal(self, amount: int):
        self.PV_actuelle = min(self.PV_max, self.PV_actuelle + amount)

    def dead(self) -> bool:
        return self.PV_actuelle <= 0

    def attack(self, cible: Any):
        if hasattr(cible, "take_damage"):
            cible.take_damage(self.atk)

    # ---------- Rendu ----------
    def draw(self, x: int, y: int):
        self.animator.draw_image()
        self.animator.display_health(self.PV_actuelle, self.PV_max)

    # ---------- Autres ----------
    def update(self):
        if self.dead():
            self.animator.play("destruction")
        self.animator.update(self.PV_actuelle, self.PV_max)

    def __del__(self):
        print("Base détruit")

def handle_events(B1):
    """
    Gère les événements clavier/souris et retourne False si on veut quitter.
    """
    
    return True

def main():
    pygame.init()
    screen = pygame.display.set_mode((400, 500))
    clock = pygame.time.Clock()
    pygame.display.set_caption("Test affichage Base")

    # Créer un objet à tester
    B1 = MotherShip(screen, Point(0, 0))
    B1.animator.play("base")
    B1.animator.update_and_draw()
    B1.animator.play("engine")

    running = True
    while running:
        if 'B1' not in locals(): 
            running = False
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 3:  # clic droit : dégâts
                        B1.take_damage(100)
                        print(f"PV actuels : {B1.PV_actuelle}")
                    elif event.button == 1:  # clic gauche : arme
                        B1.animator.play("weapons", reset=True)

            # Mettre à jour l'animation courante
            B1.animator.update_and_draw()

            if B1.dead():
                # Joue l'animation de destruction + fade
                if B1.animator.play_with_fade("destruction", fade_duration=1000):
                    del B1

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
