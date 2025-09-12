from enum import Enum

class TypeSol(Enum):
    """
    Représente les différents types de sol.
    """
    VIDE = 0
    PLANETE = 1
    ATMOSPHERE = 2
    ASTEROIDE = 3

    def __str__(self):
        """Retourne le nom du type de sol."""
        return self.name.lower()


class Point:
    """
    Représente un point dans un plan 2D avec un type de sol et un état de remplissage.
    """

    def __init__(self, x: int, y: int, type_sol: TypeSol = TypeSol.VIDE) -> None:
        """
        Initialise un nouveau point avec les coordonnées données.

        Args:
            x (int): La coordonnée x.
            y (int): La coordonnée y.
            type_sol (TypeSol): Le type de sol (par défaut: VIDE).
        """
        self._x: int = x
        self._y: int = y
        self.type_sol: TypeSol = type_sol
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
        if self.type_sol not in (TypeSol.VIDE, TypeSol.ATMOSPHERE):
            raise ValueError(
                f"Impossible de remplir un point de type {self.type_sol.name} "
                f"(seuls les points VIDE ou ATMOSPHERE peuvent être remplis)."
            )
        self.remplit = True

    def vider(self) -> None:
        """Vide le point (met remplit à False)."""
        self.remplit = False

    def __str__(self) -> str:
        """Retourne une représentation lisible du point."""
        etat = "rempli" if self.remplit else "vide"
        return f"({self.x}, {self.y}, sol={self.type_sol}, {etat})"

    def __repr__(self) -> str:
        """Retourne une représentation détaillée (utile pour le debug)."""
        return (
            f"Point(x={self.x}, y={self.y}, type_sol={self.type_sol.name}, "
            f"remplit={self.remplit})"
        )


if __name__ == "__main__":
    A: Point = Point(1, 2, TypeSol.VIDE)
    B: Point = Point(4, 8, TypeSol.ATMOSPHERE)
    C: Point = Point(3, 5, TypeSol.PLANETE)

    A.remplir()
    print(A)  # (1, 2, sol=vide, rempli)

    B.remplir()
    print(B)  # (4, 8, sol=atmosphere, rempli)

    try:
        C.remplir()  # Va lever une erreur
    except ValueError as e:
        print("Erreur :", e)
