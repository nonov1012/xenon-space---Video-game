from typing import Any, Dict, Optional
import pygame
import sys

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


class Base:
    """
    Représente la base d'un joueur.
    La configuration des différents niveaux/tier est dans LEVELS.
    """

    def __init__(
        self,
        img: Optional[Any] = None,
        tier: int = 1,
    ) -> None:
        # charger les valeurs du tier de départ
        if tier not in LEVELS:
            raise ValueError(f"Tier invalide {tier}. Valeurs valides : {list(LEVELS.keys())}")

        # taille
        self.hauteur = 5
        self.largeur = 4

        # récupération des données dans le dictionaire
        self.tier = tier
        dict_tier = LEVELS[self.tier]

        # vie
        self.PV_max = dict_tier["PV_max"]
        self.PV_actuelle = self.PV_max

        # Stats attaques
        self.atk = dict_tier.get("atk", 0)
        self.distance_atk = dict_tier.get("distance_atk", 0)

        # autres attributs
        self.img = img
        
        self.cout = dict_tier.get("cout_upgrade", 0)
        self.gains = dict_tier.get("gains", 0)

    # ---------- Informations niveaux ----------
    @property
    def max_tier(self) -> int:
        """Retourne le tier maximal défini dans LEVELS."""
        return max(LEVELS.keys())

    def get_next_tier_cost(self) -> Optional[int]:
        """
        Retourne le coût pour passer au niveau suivant,
        ou None si on est au niveau max.
        """
        next_tier = self.tier + 1
        if next_tier not in LEVELS:
            return None
        return LEVELS[self.tier]["cout_upgrade"]

    def can_upgrade(self) -> bool:
        """Retourne True si la base peut être upgrade (il existe un niveau suivant)."""
        return (self.tier + 1) in LEVELS and LEVELS[self.tier].get("cout_upgrade") is not None

    # ---------- Upgrade ----------
    def apply_level(self, tier: int) -> None:
        """
        Applique les stats du `tier` à la base.
        Si heal_on_upgrade = True, on augmente PV_actuelle à la nouvelle PV_max
        (ou on ajoute la différence).
        """
        if tier not in LEVELS:
            raise ValueError(f"Tier inconnu {tier}")

        old_PV_max = getattr(self, "PV_max", 0)
        new_conf = LEVELS[tier]

        # appliquer les valeurs
        self.tier = tier
        self.PV_max = new_conf["PV_max"]
        self.atk = new_conf.get("atk", self.atk)
        self.distance_atk = new_conf.get("distance_atk", self.distance_atk)
        self.gains = new_conf.get("gains", self.gains)

        # ajout de pv gagné
        self.PV_actuelle += self.PV_max


    def upgrade(self, payer_fct) -> bool:
        """
        Tente d'upgrader la base au niveau suivant.
        payer_fct doit être une fonction callable(price:int) -> bool qui gère le paiement
        (par ex. Player.buy).
        Retourne True si upgrade réussie.
        """
        if not self.can_upgrade():
            return False

        price = LEVELS[self.tier]["cout_upgrade"]
        if price is None:
            return False

        if not payer_fct(price):
            return False

        # appliquer le niveau suivant
        self.apply_level(self.tier + 1, heal_on_upgrade=True)
        return True

    # ---------- Combat & états ----------
    def take_damage(self, degats: int) -> None:
        """Soustrait des PV et clamp à 0."""
        self.PV_actuelle = max(0, self.PV_actuelle - max(0, int(degats)))

    def dead(self) -> bool:
        """Retourne True si la base est détruite."""
        return self.PV_actuelle <= 0

    def attack(self, cible: Any) -> None:
        # note : la vérification de portée doit être effectuée par le code appelant
        if hasattr(cible, "take_damage"):
            cible.take_damage(self.atk)

    def heal(self, amount : int):
        self.PV_actuelle = min(self.PV_max, self.PV_actuelle + amount)

    # ---------- Rendu ----------
    def draw(self, screen, x : int, y : int):
        # Charger l'image
        image = pygame.image.load(self.img).convert_alpha()

        taille_pixel : int = 100

        # Redimensionner l'image à la taille voulue
        image = pygame.transform.scale(image, (self.largeur*taille_pixel, self.hauteur*taille_pixel)) 

        # Afficher l'image sur l'écran
        screen.blit(image, (x, y))

if __name__ == "__main__":
    # Initialiser Pygame
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Test affichage image")

    # Créer un objet à tester
    B1 = Base("/home/gabriel/Bureau/IUT/BUT3/xenon-space---Video-game/Foozle_2DS0012_Void_EnemyFleet_1/Kla'ed/Base/PNGs/Kla'ed - Dreadnought - Base.png")

    # Boucle principale
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Effacer l'écran (fond blanc)
        screen.fill((255, 255, 255))

        # Dessiner l'objet
        B1.draw(screen, 0, 0)

        # Mettre à jour l'affichage
        pygame.display.flip()

    pygame.quit()
    sys.exit()