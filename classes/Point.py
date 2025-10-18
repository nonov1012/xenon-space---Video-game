from enum import Enum

class Type(Enum):
    """
    Représente les différents types de sol.
    Les types de sol sont des constantes de classe qui héritent de l'enum Enum.
    """
    VIDE = 0
    """Type de sol vide (aucune planète, astéroïde, vaisseau, base)"""
    PLANETE = 1
    """Type de sol planète (planète générée aléatoirement)"""
    ATMOSPHERE = 2
    """Type de sol atmosphère (zone de génération d'astéroïdes)"""
    ASTEROIDE = 3
    """Type de sol astéroïde (astéroïde)"""
    BASE = 4
    """Type de sol base (zone de la base)"""
    VAISSEAU = 5
    """Type de sol vaisseau (vaisseau)"""

    def __str__(self):
        """Retourne le nom du type de sol"""
        return self.name


class Point:
    """
    Représente un point dans un plan 2D avec un type de sol et un état de remplissage.

    Attributes:
        x (int): La coordonnée x.
        y (int): La coordonnée y.
        type (Type): Le type de sol (par défaut: VIDE).
    """

    def __init__(self, x: int, y: int, type: Type = Type.VIDE) -> None:
        """
        Initialise un nouveau point avec les coordonnées données.

        Args:
            x (int): La coordonnée x.
            y (int): La coordonnée y.
            type (Type): Le type de sol (par défaut: VIDE).
        """
        self._x: int = x
        self._y: int = y
        self.type: Type = type

    @property
    def x(self) -> int:
        """
        Retourne la coordonnée x du point.
        """
        return self._x

    @property
    def y(self) -> int:
        """
        Retourne la coordonnée y du point.
        """
        return self._y

    def __str__(self) -> str:
        """
        Retourne une représentation lisible du point.
        """
        return f"({self.x}, {self.y}, {self.type.name})"

    def __repr__(self) -> str:
        """
        Retourne une représentation détaillée (utile pour le debug).
        """
        return (
            f"Point(x={self.x}, y={self.y}, type={self.type.name})"
        )


if __name__ == "__main__":
    A: Point = Point(1, 2, Type.VIDE)
    B: Point = Point(4, 8, Type.ATMOSPHERE)
    C: Point = Point(3, 5, Type.PLANETE)

    print(B)  # (4, 8, sol=atmosphere)
    print(A)  # (1, 2, sol=vide)
    print(C)  # (3, 5, sol=planete)
