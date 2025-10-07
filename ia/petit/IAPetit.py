import os
from classes.Ship import Petit
from blazyck import SHIPS_PATH

class IAPetit(Petit):
    from __future__ import annotations
    from classes.Point import Point
    from classes.Turn import Turn

    def __init__(self : IAPetit, coordonnees : Point, id : int, joueur_id : int) -> None:
        super().__init__(cordonner=coordonnees, id=id, joueur=joueur_id, path=os.path.join(SHIPS_PATH, "petit")) 
        pass
        
    def valuation(self: IAPetit, grille : list[list[Point]]) -> int:
        pass