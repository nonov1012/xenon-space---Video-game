from classes.MotherShip import MotherShip
#from classes.ship import Ship
from classes.Economie import Economie

class Player:
    def __init__(self, name: str, solde_initial: int = 500) -> None:
        self.name: str = name
        self.economie: Economie = Economie(solde_initial)
        #self.ships: list[Ship] = []
        #self.base: MotherShip = MotherShip()

    # ---------- Gestion de l'argent ----------
    def buy(self, price: int) -> bool:
        """
        Tente de payer un prix via l'économie du joueur.
        Retourne True si le paiement est effectué.
        """
        return self.economie.retirer(price)

    # ---------- Gestion de la base ----------
    #def upgrade_base(self) -> bool:
        """
        Tente d'upgrader la base. Retourne True si upgrade réussie.
        Utilise Player.buy() comme fonction de paiement.
        """
        return self.base.upgrade(self.buy)

    # ---------- Gestion des vaisseaux ----------
    #def add_ship(self, ship: Ship) -> None:
        self.ships.append(ship)

    #def remove_ship(self, ship: Ship) -> None:
        if ship in self.ships:
            self.ships.remove(ship)

    # ---------- Debug / affichage ----------
    def __str__(self) -> str:
        return f"Player({self.name}, solde={self.economie.solde}, base_tier={self.base.tier}, ships={len(self.ships)})"
