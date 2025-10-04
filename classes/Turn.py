from typing import List
from classes.Ship import Ship
from classes.Player import Player

class Turn:
    players : list[Player] = []
    sentence = "Tour"
    _nb_turns : float = 1

    @classmethod
    def next(cls):
        if not cls.players:
            print("Aucun joueur")
            return
        player = cls.players.pop(0)
        cls.players.append(player)
        cls._nb_turns += 1 / len(cls.players)
        

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

if __name__ == "__main__":
    Turn.players = [Player("Alice"), Player("Bob")]
    print(Turn.describe())
    Turn.next()
    print(Turn.describe())
    Turn.next()
    print(Turn.describe())
    print(Turn.get_players_ships())