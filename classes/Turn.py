from typing import List
from classes.Ship import Ship
from classes.Player import Player

class Turn:
    players : list[Player] = []
    sentence = "Tour de"

    @classmethod
    def next(cls):
        if not cls.players:
            print("Aucun joueur")
            return
        player = cls.players.pop(0)
        cls.players.append(player)

    @classmethod
    def describe(cls):
        if not cls.players:
            return "Aucun joueur"
        return f"{cls.sentence} {cls.players[0].name}"
    
    @classmethod
    def get_players_ships(cls) -> list:
        ships_list = []
        for player in cls.players:
            ships_list.extend(player.ships)
        return ships_list

if __name__ == "__main__":
    Turn.players = [Player("Alice"), Player("Bob")]
    print(Turn.describe())
    Turn.next()
    print(Turn.describe())
    print(Turn.get_players_ships())
