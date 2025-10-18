# `Type` et `Point`

Ce module définit deux structures fondamentales pour la représentation des entités et des emplacements dans l'espace de jeu : l'énumération `Type` pour identifier la nature d'un emplacement, et la classe `Point` pour modéliser une position 2D avec cette nature associée.

-----

## Énumération `Type`

L'énumération `Type` représente les différentes catégories de "sol" ou d'entités qu'une coordonnée (point) dans la grille du jeu peut contenir.

```python
from enum import Enum

class Type(Enum):
    # ...
```

### Membres

| Membre | Valeur | Description |
| :--- | :--- | :--- |
| **`VIDE`** | `0` | Type de sol vide (aucune planète, astéroïde, vaisseau, base). |
| **`PLANETE`** | `1` | Type de sol planète (planète générée aléatoirement). |
| **`ATMOSPHERE`** | `2` | Type de sol atmosphère (zone de génération d'astéroïdes). |
| **`ASTEROIDE`** | `3` | Type de sol astéroïde (astéroïde). |
| **`BASE`** | `4` | Type de sol base (zone de la base). |
| **`VAISSEAU`** | `5` | Type de sol vaisseau (vaisseau). |

### Méthode Surchargée

#### `__str__`

```python
def __str__(self):
```

  * **Retour :** `str` - Retourne le nom du membre de l'énumération (ex: `"VIDE"`, `"PLANETE"`).

-----

## Classe `Point`

La classe `Point` représente une coordonnée bidimensionnelle dans l'espace de jeu. Contrairement à un simple tuple `(x, y)`, elle stocke également le `Type` de sol ou d'entité occupant cette position.

```python
class Point:
    # ...
```

### Attributs d'Instance

| Attribut | Type | Description |
| :--- | :--- | :--- |
| `_x` | `int` | La coordonnée X (privée). |
| `_y` | `int` | La coordonnée Y (privée). |
| `type` | `Type` | Le type de sol associé à ce point (défaut : `Type.VIDE`). |

### Constructeur

```python
def __init__(self, x: int, y: int, type: Type = Type.VIDE) -> None:
```

| Paramètre | Type | Description |
| :--- | :--- | :--- |
| `x` | `int` | La coordonnée x. |
| `y` | `int` | La coordonnée y. |
| `type` | `Type` | Le type de sol (défaut : `Type.VIDE`). |

### Propriétés (`@property`)

#### `x`

```python
@property
def x(self) -> int:
```

  * **Retour :** `int` - Retourne la coordonnée x du point.

#### `y`

```python
@property
def y(self) -> int:
```

  * **Retour :** `int` - Retourne la coordonnée y du point.

### Méthodes Surchargées

#### `__str__`

```python
def __str__(self) -> str:
```

  * **Retour :** `str` - Représentation lisible du point, au format `(x, y, Type.NAME)`.

#### `__repr__`

```python
def __repr__(self) -> str:
```

  * **Retour :** `str` - Représentation détaillée pour le débogage, au format `Point(x=..., y=..., type=Type.NAME)`.
