from __future__ import annotations
from typing import List
from classes.Player import Player

class Turn:
    players : list[Player] = []
    sentence = "Tour de"

    @classmethod
    def play(cls):
        if not cls.players:
            print("Aucun joueur")
            return
        player = cls.players.pop(0)
        player.play()
        cls.players.append(player)

    @classmethod
    def describe(cls):
        if not cls.players:
            return "Aucun joueur"
        return f"{cls.sentence} {cls.players[0].name}"

if __name__ == "__main__":
    Turn.players = [Player("Alice"), Player("Bob")]
    print(Turn.describe())
    Turn.play()
    print(Turn.describe())
