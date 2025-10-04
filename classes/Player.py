from classes.Economie import Economie
from classes.Ship import Ship, Foreuse
from classes.MotherShip import MotherShip

class Player:
    def __init__(self, name: str, solde_initial: int = 500, id : int = 1) -> None:
        self.name: str = name
        self.economie: Economie = Economie(solde_initial)
        self._start_loadout()
        self.id = id
        self.ships: list[Ship] = []
        #self.base: MotherShip = MotherShip()

    def _start_loadout(self) -> list[Ship]:
        ships = []

        # TODO : implémentation de l'ajout des vaisseaux
        # ??? : Faire un truc pour que les stat du vaisseau soit paramétrable (donc avec les constantes ou le json des stats jsp) (optionel)
        # Noa : Finit ton truc pour donner des coordonnées valides aux vaisseaux.
        
        return ships

    # ---------- Gestion de l'argent ----------
    def buy(self, price: int) -> bool:
        """
        Tente de payer un prix via l'économie du joueur.
        Retourne True si le paiement est effectué.
        """
        return self.economie.retirer(price)
    
    def gain(self) -> None:
        gains = 0
        for ship in self.ships:
            gains += ship.gain
            if isinstance(ship, Foreuse):
                ship.gain = 0
                ship.pv_actuel = ship.pv_max * 0.1

        self.economie.ajouter(gains)
        return
            

    # ---------- Gestion de la base ----------
    #def upgrade_base(self) -> bool:
        """
        Tente d'upgrader la base. Retourne True si upgrade réussie.
        Utilise Player.buy() comme fonction de paiement.
        """
        return self.base.upgrade(self.buy)
    
    def getMotherShip(self) -> MotherShip:
        for ship in self.ships:
            if isinstance(ship, MotherShip):
                return ship
        return

    # ---------- Gestion des vaisseaux ----------
    #def add_ship(self, ship: Ship) -> None:
        self.ships.append(ship)

    #def remove_ship(self, ship: Ship) -> None:
        if ship in self.ships:
            self.ships.remove(ship)

    # ---------- Debug / affichage ----------
    def __str__(self) -> str:
        return f"Player({self.name}, solde={self.economie.solde}, base_tier={self.base.tier}, ships={len(self.ships)})"
