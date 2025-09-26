import pygame
from typing import Optional, Tuple
from classes.Ship import Ship
from classes.Point import Point
from classes.Animator import Animator
from classes.ShipAnimator import ShipAnimator
from classes.ProjectileAnimator import ProjectileAnimator

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
                 valeur_mort: int,
                 taille: Tuple[int,int],
                 tier: int,
                 cordonner: Point,
                 id: Optional[int] = None,
                 path: str = None):

        super().__init__(pv_max, attaque, port_attaque, port_deplacement,
                         cout, valeur_mort, taille, peut_miner=False,
                         peut_transporter=False, image=pygame.Surface((taille[1]*32, taille[0]*32)),
                         tier=tier, cordonner=cordonner, id=id, path=path)

        # Remplir l'image par défaut grise
        self.image.fill((200, 200, 200))

        # Initialisation de l’Animator
        pixel_coord = (cordonner.y * 32, cordonner.x * 32)
        self.animator = ShipAnimator(path, taille, pixel_coord)

        # Charger animations
        for anim in ["base", "engine", "shield", "destruction"]:
            self.animator.load_animation(anim, f"{anim}.png")

        self.animator.play("base")
        self.is_dead_anim_playing = False

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

    # ---------------- Gestion dégâts / combat ----------------
    def subir_degats(self, amount: int):
        self.take_damage(amount)

    def take_damage(self, amount: int):
        self.pv_actuel = max(0, self.pv_actuel - max(0, amount))
        if self.pv_actuel > 0:
            self.animator.play("shield")
        else:
            if not self.is_dead_anim_playing:
                self.animator.play("destruction")
                self.is_dead_anim_playing = True

    def est_mort(self) -> bool:
        if self.pv_actuel > 0: return False
        if not self.is_dead_anim_playing: return False
        frames = self.animator.animations.get("destruction")
        if not frames: return True
        return self.animator.frame_index == len(frames) - 1

    def heal(self, amount: int):
        self.pv_actuel = min(self.pv_max, self.pv_actuel + amount)

    def attaquer(self, cible: "Ship"):
        if hasattr(cible, "subir_degats"):
            cible.subir_degats(self.attaque)

    # ---------------- Rendu ----------------
    def dessiner(self, surface, taille_case):
        self.animator.update_and_draw()
        # barre de vie
        x = self.cordonner.y * taille_case
        y = (self.cordonner.x + self.taille[0]) * taille_case - 15
        largeur_barre = self.taille[1] * taille_case
        proportion = self.pv_actuel / self.pv_max
        pygame.draw.rect(surface, (255,0,0), (x, y, largeur_barre, 15))
        pygame.draw.rect(surface, (0,255,0), (x, y, int(largeur_barre * proportion), 15))

"""
def main():
    pygame.init()
    screen = pygame.display.set_mode((1000, 800))
    clock = pygame.time.Clock()
    pygame.display.set_caption("Test affichage Vaisseau mère")

    Animator.set_screen(screen)

    # Créer un objet à tester
    B1 = MotherShip(Point(0, 0), tier=1, show_health=True, largeur=4, hauteur=5)
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
                        B1.animator.set_target(pygame.mouse.get_pos())
                    elif event.button == 1:  # clic gauche : arme
                        B1.animator.fire("laser", pygame.mouse.get_pos(), True, 10)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    B1.animator.set_target_angle(B1.animator.target_angle + 90)

            # Mettre à jour l'animation courante
            screen.fill((0, 0, 0))

            Animator.update_all()
            ShipAnimator.update_all()
            ProjectileAnimator.update_all()

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
"""