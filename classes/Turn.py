from typing import List, Optional
from classes.Ship import Ship
from classes.Player import Player

class Turn:
    players : list[Player] = []
    sentence = "Tour"
    _nb_turns : float = 1

    @classmethod
    def next(cls) -> Optional[Player]:
        """
        Passe au joueur suivant et le place en fin de liste.
        Si le joueur suivant n'a pas de vaisseau mère, le joueur actuel est mis en fin de liste.
        Si le joueur actuel est le dernier de la liste, le premier joueur est mis en fin de liste.
        Retourne le joueur actuel si il n'y a qu'un joueur, None sinon.
        """
        if not cls.players:
            print("Aucun joueur")
            return None

        # Si le joueur suivant n'a pas de vaisseau mère, le joueur actuel est mis en fin de liste
        if len(cls.players) > 1 and not cls.players[1].getMotherShip():
            return cls.players[0]

        # Le joueur actuel est mis en fin de liste
        player = cls.players.pop(0)
        cls.players.append(player)
        # Le nombre de tours est augmenté de 1 divisé par le nombre de joueurs
        cls._nb_turns += 1 / len(cls.players)
        return None

    @classmethod
    def describe(cls):
        """
        Retourne une description de l'objet Tour.
        La description contient le nombre de tours actuels.
        Si il n'y a pas de joueur, la méthode retourne "Aucun joueur".
        :return: Une description de l'objet Tour
        """
        res : str = f"{cls.sentence} {str(cls.get_nb_turns())} :"
        # Si il n'y a pas de joueur, la méthode retourne "Aucun joueur"
        if not cls.players:
            return "Aucun joueur"
        return f"{res} {cls.players[0].name}"
    
    @classmethod
    def get_players_ships(cls) -> list:
        """
        Retourne la liste de tous les vaisseaux des joueurs.
        La méthode itère sur chaque joueur et ajoute ses vaisseaux à la liste.
        :return: La liste de tous les vaisseaux des joueurs
        """
        ships_list = []
        # Itération sur chaque joueur
        for player in cls.players:
            # Ajout des vaisseaux du joueur à la liste
            ships_list.extend(player.ships)
        return ships_list
    
    @classmethod
    def get_nb_turns(cls) -> int:
        """
        Retourne le nombre de tours actuels.
        Le nombre de tours est un entier qui est incrémenté de 1 divisé par le nombre de joueurs à chaque tour.
        :return: Le nombre de tours actuels
        """
        return int(cls._nb_turns)
    
    @classmethod
    def get_player_with_id(cls, id : int) -> Player:
        """
        Retourne le joueur qui correspond à l'identifiant id.
        La méthode itère sur chaque joueur et vérifie si son identifiant est égal à id.
        Si c'est le cas, la méthode retourne le joueur, sinon None.
        :param id: L'identifiant du joueur à trouver
        :return: Le joueur qui correspond à l'identifiant id, ou None si il n'y a pas de joueur
        """
        for player in cls.players:
            if player.id == id:
                return player

if __name__ == "__main__":
    Turn.players = [Player("Alice"), Player("Bob")]
    print(Turn.describe())
    Turn.next()
    print(Turn.describe())
    Turn.next()
    print(Turn.describe())
    print(Turn.get_players_ships())