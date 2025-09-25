import os
import pygame
from typing import Any, Dict, Optional, Tuple
from classes.Ship import Ship
from classes.Animator import Animator
import sys
from classes.ShipAnimator import ShipAnimator
from classes.ProjectileAnimator import ProjectileAnimator

# Configuration des niveaux
LEVELS: Dict[int, Dict[str, Any]] = {
    1: {"cout_upgrade": 1000, "pv_max": 500, "gains": 300, "attaque": 0, "port_attaque": 0},
    2: {"cout_upgrade": 2000, "pv_max": 800, "gains": 350, "attaque": 0, "port_attaque": 0},
    3: {"cout_upgrade": 6000, "pv_max": 1300, "gains": 400, "attaque": 0, "port_attaque": 0},
    4: {"cout_upgrade": None, "pv_max": 1700, "gains": 450, "attaque": 100, "port_attaque": 3},
}

class MotherShip(Ship):
    """Représente la base d'un joueur avec niveaux, PV, et combat."""

    def __init__(self, screen, position: Tuple[int, int], tier: int = 1, largeur: int = 4, hauteur: int = 5, uid=1, BASE_IMG_DIR = None) -> None:
        self.largeur = largeur   # en cases
        self.hauteur = hauteur   # en cases
        self.tier = tier
        self.screen = screen

        # Charger la config du niveau
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
        image = pygame.Surface((self.largeur*32, self.hauteur*32))
        image.fill((200, 200, 200))

        # Initialisation de Ship (position en cases)
        super().__init__(
            pv_max=pv_max,
            attaque=attaque,
            port_attaque=port_attaque,
            port_deplacement=port_deplacement,
            cout=cout,
            valeur_mort=valeur_mort,
            taille=(largeur, hauteur),
            peut_miner=peut_miner,
            peut_transporter=peut_transporter,
            image=image,
            tier=tier,
            ligne=position[0],   # case Y
            colonne=position[1], # case X
            uid=uid
        )

        # Initialisation de l’Animator (position en pixels)
        pixel_coord = (position[1]*32, position[0]*32)
        self.animator = Animator(
            BASE_IMG_DIR,
            (largeur, hauteur),
            pixel_coord,
            tile_size=32
        )

        # Définir l'animation initiale (ou image statique si pas d'animation)
        # Charger les animations
        pixel_coord = (position[1]*32, position[0]*32)
        self.animator = Animator(
            BASE_IMG_DIR,          # chemin du dossier contenant les images
            (largeur, hauteur),
            pixel_coord,
            tile_size=32
        )

        # Charger les animations
        self.animator.load_animation("base", "base.png")        
        self.animator.load_animation("engine", "engine.png")      
        self.animator.load_animation("shield", "shield.png")          
        self.animator.load_animation("destruction", "destruction.png")

        # Définir l'animation initiale
        self.animator.play("base")
        




       # Déplacement et rotation désactivés
    def deplacement(self, *args, **kwargs): 
        return False
    def rotation_aperçu(self, *args, **kwargs): 
        pass
    def rotation_aperçu_si_possible(self, *args, **kwargs): 
        pass

    # Gestion des niveaux / upgrade
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
        self.pv_max = new_conf["pv_max"]
        self.attaque = new_conf.get("attaque", self.attaque)
        self.port_attaque = new_conf.get("port_attaque", self.port_attaque)
        self.cout = new_conf.get("cout_upgrade", self.cout)

        # Remet les PV au max (plus logique)
        self.pv_actuel = self.pv_max

    def upgrade(self, payer_fct) -> bool:
        if not self.can_upgrade(): 
            return False
        price = self.get_next_tier_cost()
        if price is None or not payer_fct(price): 
            return False
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
        if self.pv_actuel > 0:
            return False
        if not self.is_dead_anim_playing:
            return False

        # Vérifier si l'animation est terminée
        frames = self.animator.animations.get("destruction")
        if not frames:
            return True  # pas d’anim, on considère mort
        return self.animator.frame_index == len(frames) - 1

    def heal(self, amount: int):
        self.pv_actuel = min(self.pv_max, self.pv_actuel + amount)

    def attack(self, cible: Any):
        if hasattr(cible, "take_damage"): 
            cible.take_damage(self.attaque)

    # Rendu
    def dessiner(self, surface, taille_case):
        # Met à jour et affiche l'animation
        self.animator.update_and_draw()

        # Dessiner la barre de vie sous le vaisseau
        x = self.colonne * taille_case
        y = (self.ligne + self.hauteur) * taille_case - 15  # juste sous le vaisseau
        largeur_barre = self.largeur * taille_case
        proportion = self.pv_actuel / self.pv_max

        # Fond rouge
        pygame.draw.rect(surface, (255, 0, 0), (x, y, largeur_barre, 15))
        # Partie verte proportionnelle aux PV
        pygame.draw.rect(surface, (0, 255, 0), (x, y, int(largeur_barre * proportion), 15))


    def __del__(self):
        print("Vaisseau mère détruit")

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
