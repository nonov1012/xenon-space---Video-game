from enum import Enum

class Type(Enum):
    """
    Représente les différents types de sol.
    """
    VIDE = 0
    PLANETE = 1
    ATMOSPHERE = 2
    ASTEROIDE = 3

    def __str__(self):
        """Retourne le nom du type de sol."""
        return self.name


class Point:
    """
    Représente un point dans un plan 2D avec un type de sol et un état de remplissage.
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
        self.remplit: bool = False  # Par défaut, un point n'est pas rempli

    @property
    def x(self) -> int:
        """Retourne la coordonnée x du point."""
        return self._x

    @property
    def y(self) -> int:
        """Retourne la coordonnée y du point."""
        return self._y

    def remplir(self) -> None:
        """
        Remplit le point si son type de sol est VIDE ou ATMOSPHERE.
        Sinon, lève une exception.
        """
        if self.type not in (Type.VIDE, Type.ATMOSPHERE):
            raise ValueError(
                f"Impossible de remplir un point de type {self.type.name} "
                f"(seuls les points VIDE ou ATMOSPHERE peuvent être remplis)."
            )
        self.remplit = True

    def vider(self) -> None:
        """Vide le point (met remplit à False)."""
        self.remplit = False

    def vide_remplit(self) -> None:
        """
        Bascule l'état 'remplit' du point.
        - Si le point est actuellement rempli, il est vidé.
        - Sinon, on essaie de le remplir (avec la même logique de sécurité que remplir()).
        """
        if self.remplit:
            self.vider()
        else:
            self.remplir()

    def __str__(self) -> str:
        """Retourne une représentation lisible du point."""
        return f"({self.x}, {self.y}, {self.type}, {self.remplit})"

    def __repr__(self) -> str:
        """Retourne une représentation détaillée (utile pour le debug)."""
        return (
            f"Point(x={self.x}, y={self.y}, type={self.type.name}, "
            f"remplit={self.remplit})"
        )


if __name__ == "__main__":
    A: Point = Point(1, 2, Type.VIDE)
    B: Point = Point(4, 8, Type.ATMOSPHERE)
    C: Point = Point(3, 5, Type.PLANETE)

    A.remplir()
    print(A)  # (1, 2, sol=vide, rempli)

    B.remplir()
    print(B)  # (4, 8, sol=atmosphere, rempli)

    B.vide_remplit()
    print(B)  # (4, 8, sol=atmosphere, rempli)

    try:
        C.remplir()  # Va lever une erreur
    except ValueError as e:
        print("Erreur :", e)
