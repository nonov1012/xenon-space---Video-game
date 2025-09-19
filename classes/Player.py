from Base import Base
from ship import Ship

class Player:
    def __init__(self, name: str, money: int = 500) -> None:
        self.name: str = name
        self.money: int = money
        self.ships: list[Ship] = []
        self.base: Base = Base()

    # ---------- Gestion de l'argent ----------
    def buy(self, price: int) -> bool:
        """
        Tente de payer un prix. Retourne True si le paiement est effectué.
        """
        if price <= self.money:
            self.money -= price
            return True
        return False

    def get_money_gained(self) -> int: #TODO
        """
        Calcule l'argent gagné à la fin d'un tour :
        - gains de la base
        - gains additionnels selon les vaisseaux si tu en veux
        """
        gains: int = self.base.gains
        for ship in self.ships:
            if hasattr(ship, "gains"):
                gains += ship.gains
        return gains

    # ---------- Gestion de la base ----------
    def upgrade_base(self) -> bool:
        """
        Tente d'upgrader la base. Retourne True si upgrade réussie.
        Utilise Player.buy() comme fonction de paiement.
        """
        return self.base.upgrade(self.buy)

    def collect_income(self) -> None:
        """Ajoute les gains au porte-monnaie du joueur."""
        self.money += self.get_money_gained()

    # ---------- Gestion des vaisseaux ----------
    def add_ship(self, ship: Ship) -> None:
        self.ships.append(ship)

    def remove_ship(self, ship: Ship) -> None:
        if ship in self.ships:
            self.ships.remove(ship)

    # ---------- Debug / affichage ----------
    def __str__(self) -> str:
        return f"Player({self.name}, money={self.money}, base_tier={self.base.tier}, ships={len(self.ships)})"
