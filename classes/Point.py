from enum import Enum

class Type(Enum):
    VIDE = 0
    PLANETE = 1
    ATMOSPHERE = 2
    ASTEROIDE = 3

    def __str__(self):
        return self.name

class Point:
    """
    Représente un point dans un plan 2D avec type et état rempli.
    Compatible avec Ship.position.x et Ship.position.y modifiables.
    """
    def __init__(self, x: int, y: int, type: Type = Type.VIDE):
        self.x: int = x
        self.y: int = y
        self.type: Type = type
        self.remplit: bool = False

    def remplir(self):
        """Remplit le point si type autorisé."""
        if self.type not in (Type.VIDE, Type.ATMOSPHERE):
            raise ValueError(
                f"Impossible de remplir un point de type {self.type.name}"
            )
        self.remplit = True

    def vider(self):
        """Vide le point."""
        self.remplit = False

    def vide_remplit(self):
        """Bascule l'état rempli."""
        if self.remplit:
            self.vider()
        else:
            self.remplir()

    def deplacer(self, x: int, y: int):
        """Déplace le point."""
        self.x = x
        self.y = y

    def __str__(self):
        return f"Point(x={self.x}, y={self.y}, type={self.type}, remplit={self.remplit})"

    def __repr__(self):
        return str(self)



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
