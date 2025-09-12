from typing import Any, Dict, Optional

# Exemple de configuration des niveaux (tiers).
# Chaque clé est un tier (int). Les valeurs sont les attributs applicables à la base à ce niveau.
LEVELS: Dict[int, Dict[str, Any]] = {
    1: {
        "cout_upgrade": 1000,    # coût pour passer au niveau suivant
        "PV_max": 500,
        "gains": 300,
        "att": 0,
        "distance_att": 0,
        "hauteur": 5,
        "largeur": 4,
        "img_key": "base_lvl1",  # clé pour charger une image si tu as un système de ressources
    },
    2: {
        "cout_upgrade": 2000,
        "PV_max": 800,
        "gains": 350,
        "att": 0,
        "distance_att": 0,
        "hauteur": 5,
        "largeur": 4,
        "img_key": "base_lvl2",
    },
    3: {
        "cout_upgrade": 6000,
        "PV_max": 1300,
        "gains": 400,
        "att": 0,
        "distance_att": 0,
        "hauteur": 5,
        "largeur": 4,
        "img_key": "base_lvl3",
    },
    4: {
        "cout_upgrade": None,   # None => pas d'upgrade possible (niveau max)
        "PV_max": 1700,
        "gains": 450,
        "att": 30,
        "distance_att": 3,
        "hauteur": 5,
        "largeur": 4,
        "img_key": "base_lvl4",
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
        PV_actuelle: Optional[int] = None,
    ) -> None:
        # charger les valeurs du tier de départ
        if tier not in LEVELS:
            raise ValueError(f"Tier invalide {tier}. Valeurs valides : {list(LEVELS.keys())}")

        self.img = img
        self.tier = tier

        lvl = LEVELS[self.tier]
        self.PV_max = lvl["PV_max"]
        # si PV_actuelle n'est pas fourni, on initialise à PV_max
        self.PV_actuelle = self.PV_max if PV_actuelle is None else min(PV_actuelle, self.PV_max)

        # autres attributs
        self.att = lvl.get("att", 0)
        self.distance_att = lvl.get("distance_att", 0)
        self.cout = lvl.get("cout_upgrade", 0)
        self.hauteur = lvl.get("hauteur", 1)
        self.largeur = lvl.get("largeur", 1)
        self.gains = lvl.get("gains", 0)
        self.img_key = lvl.get("img_key", None)

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
    def apply_level(self, tier: int, heal_on_upgrade: bool = True) -> None:
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
        self.att = new_conf.get("att", self.att)
        self.distance_att = new_conf.get("distance_att", self.distance_att)
        self.hauteur = new_conf.get("hauteur", self.hauteur)
        self.largeur = new_conf.get("largeur", self.largeur)
        self.gains = new_conf.get("gains", self.gains)
        self.img_key = new_conf.get("img_key", self.img_key)

        # PV_actuelle : augmenter (soigner) lors de l'upgrade selon l'option
        if heal_on_upgrade:
            # option 1 : remettre à PV_max
            self.PV_actuelle = self.PV_max
            # option 2 (alternative) : ajouter la différence au PV_actuelle
            # diff = max(0, self.PV_max - old_PV_max)
            # self.PV_actuelle += diff
        else:
            # clamp PV_actuelle <= PV_max
            self.PV_actuelle = min(self.PV_actuelle, self.PV_max)

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
        """
        Exemple simple : inflige self.att à la cible si dans portée.
        La logique réelle dépendra de la représentation de la cible.
        """
        # stub : la vérification de portée doit être effectuée par le code appelant
        if hasattr(cible, "take_damage"):
            cible.take_damage(self.att)

    # ---------- Rendu ----------
    def draw(self, surface, topleft_pixel: tuple[int, int], tile_size: int):
        pass