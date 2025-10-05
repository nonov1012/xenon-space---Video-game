from typing import List, Optional
from classes.Ship import Ship
from classes.Player import Player

class Turn:
    players : list[Player] = []
    sentence = "Tour"
    _nb_turns : float = 1

    @classmethod
    def next(cls) -> Optional[Player]:
        if not cls.players:
            print("Aucun joueur")
            return None

        if len(Turn.players) > 1 and not Turn.players[1].getMotherShip():
            return Turn.players[0]

        player = cls.players.pop(0)
        cls.players.append(player)
        cls._nb_turns += 1 / len(cls.players)
        return None

    @classmethod
    def describe(cls):
        res : str = f"{cls.sentence} {str(cls.get_nb_turns())} :"
        if not cls.players:
            return "Aucun joueur"
        return f"{res} {cls.players[0].name}"
    
    @classmethod
    def get_players_ships(cls) -> list:
        ships_list = []
        for player in cls.players:
            ships_list.extend(player.ships)
        return ships_list
    
    @classmethod
    def get_nb_turns(cls) -> int:
        return int(cls._nb_turns)
    
    @classmethod
    def get_player_with_id(cls, id : int) -> Player:
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