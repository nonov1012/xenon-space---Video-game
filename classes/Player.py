from typing import Optional
from classes.Economie import Economie
from classes.Ship import Ship, Foreuse
from classes.MotherShip import MotherShip
from classes.FloatingText import FloatingText

class Player:
    def __init__(self, name: str, solde_initial: int = 500, id : int = 1, is_ia : bool = True) -> None:
        """
        Constructeur de la classe Player.
        
        :param name: Nom du joueur
        :param solde_initial: Solde initial du joueur
        :param id: Identifiant unique du joueur
        """
        self.name: str = name
        self.economie: Economie = Economie(solde_initial)
        self._start_loadout()
        self.is_ia = is_ia # Nouvel attribut
        self.id = id
        self.ships: list[Ship] = []  # liste de vaisseaux du joueur

    def _start_loadout(self) -> list[Ship]:
        """
        Méthode qui charge les vaisseaux du joueur.
        
        Retourne une liste de vaisseaux.
        """
        ships = []

        # TODO : implémentation de l'ajout des vaisseaux
        # ??? : Faire un truc pour que les stat du vaisseau soit paramétrable (donc avec les constantes ou le json des stats jsp) (optionel)
        # Noa : Finit ton truc pour donner des coordonnées valides aux vaisseaux.
        
        return ships

    # ---------- Gestion de l'argent ----------
    def buy(self, price: int) -> bool:
        """
        Tente de payer un prix via l'économie du joueur.
        
        :param price: Prix à payer
        :return: True si le paiement est effectué, False sinon
        """
        # On tente de retirer le prix de l'économie du joueur
        # Si le joueur a assez d'argent, on retire le prix et on retourne True
        # Sinon, on retourne False
        return self.economie.retirer(price)
    
    def gain(self):
        """
        Calcul du gain total des vaisseaux du joueur.
        Le gain est ajouté à l'économie du joueur.
        """
        total_gain = 0
        for ship in self.ships:
            if ship.gain > 0:
                total_gain += ship.gain
                # Affichage du gain en surbrillance
                FloatingText(f"+{ship.gain}₿", pos=(ship.animator.x + ship.animator.pixel_w, ship.animator.y + ship.animator.pixel_h / 2))
                if not isinstance(ship, MotherShip):
                    ship.gain = 0
                    if isinstance(ship, Foreuse):
                        # Le vaisseau prend des dégâts en fonction de son gain
                        ship.subir_degats(ship.pv_max * 0.1)
        # Ajout du gain à l'économie du joueur
        self.economie.ajouter(total_gain)
        return

    # ---------- Gestion de la base ----------
    def upgrade_base(self) -> bool:
        """
        Tente d'upgrader la base.
        Retourne True si l'upgrade est réussie.
        Utilise Player.buy() comme fonction de paiement.
        """
        return self.base.upgrade(self.buy)
    
    def getMotherShip(self) -> Optional[MotherShip]:
        """
        Renvoie la mère des vaisseaux du joueur si elle existe.
        
        :return: La mère des vaisseaux du joueur si elle existe, None sinon
        """
        for ship in self.ships:
            if isinstance(ship, MotherShip):
                return ship
        return None

    # ---------- Gestion des vaisseaux ----------
    #def add_ship(self, ship: Ship) -> None:
        # """Ajoute un vaisseau à la flotte du joueur."""
        # self.ships.append(ship)

    #def remove_ship(self, ship: Ship) -> None:
        # """Retire un vaisseau de la flotte du joueur."""
        # if ship in self.ships:
        #     self.ships.remove(ship)

    # ---------- Debug / affichage ----------
    def __str__(self) -> str:
        """
        Retourne une représentation en forme de chaîne du joueur.
        
        :return: Une représentation en forme de chaîne du joueur
        """
        return f"Player({self.name}, solde={self.economie.solde}, base_tier={self.base.tier}, ships={len(self.ships)}"