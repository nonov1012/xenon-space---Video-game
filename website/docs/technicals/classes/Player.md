# `Player`

La classe `Player` représente un joueur dans le jeu. Elle centralise la gestion de l'économie, de la flotte de vaisseaux, des actions économiques (achat/gain) et de l'accès à l'entité principale (le vaisseau mère).

## Dépendances

  * **`classes.Economie`** : Gère le solde monétaire et les transactions.
  * **`classes.Ship`, `classes.Foreuse`, `classes.MotherShip`** : Représentent les différents types de vaisseaux sous le contrôle du joueur.
  * **`classes.FloatingText`** : Utilisé pour afficher les gains d'argent à l'écran.

-----

## Constructeur

```python
def __init__(self, name: str, solde_initial: int = 500, id : int = 1) -> None:
```

### Paramètres

| Nom | Type | Description |
| :--- | :--- | :--- |
| `name` | `str` | Nom du joueur. |
| `solde_initial` | `int` | Montant d'argent initial du joueur (défaut : 500). |
| `id` | `int` | Identifiant unique du joueur (défaut : 1). |

### Attributs Initialisés

| Attribut | Type | Description |
| :--- | :--- | :--- |
| `self.name` | `str` | Nom du joueur. |
| `self.economie` | `Economie` | Instance de la classe `Economie` avec le solde initial. |
| `self.id` | `int` | Identifiant unique du joueur. |
| `self.ships` | `List[Ship]` | Liste des vaisseaux et entités sous le contrôle du joueur. |

-----

## Méthodes Privées

### `_start_loadout`

Méthode destinée à être implémentée pour initialiser la flotte de vaisseaux du joueur au début de la partie.

```python
def _start_loadout(self) -> list[Ship]:
```

| Retour | Type | Description |
| :--- | :--- | :--- |
| `list[Ship]` | Liste vide, destinée à contenir les vaisseaux de départ. |

-----

## Gestion de l'Argent

### `buy`

Tente d'effectuer un paiement en retirant le montant spécifié du solde du joueur.

```python
def buy(self, price: int) -> bool:
```

| Paramètre | Type | Description |
| :--- | :--- | :--- |
| `price` | `int` | Prix à payer. |
| Retour | `bool` | `True` si le paiement a réussi (solde suffisant), `False` sinon. |

  * Utilise la méthode `self.economie.retirer(price)`.

### `gain`

Calcule le gain total généré par les vaisseaux du joueur et l'ajoute à son économie.

```python
def gain(self):
```

  * Ière sur tous les vaisseaux (`self.ships`).
  * Si un vaisseau a un `ship.gain > 0`:
      * Le gain est ajouté au `total_gain`.
      * Un `FloatingText` est créé à la position du vaisseau pour visualiser le gain.
      * Si ce n'est pas un `MotherShip`, le gain est remis à zéro (`ship.gain = 0`).
      * **Règle spéciale Foreuse :** Si c'est une `Foreuse`, elle subit également des dégâts équivalents à 10% de ses PV maximum (`ship.subir_degats(ship.pv_max * 0.1)`).
  * Le `total_gain` est finalement ajouté à `self.economie`.

-----

## Gestion des Entités

### `upgrade_base`

Tente d'améliorer la base du joueur. Nécessite que l'attribut `self.base` existe et que la méthode `upgrade` y soit implémentée.

```python
def upgrade_base(self) -> bool:
```

  * Utilise `self.buy` comme fonction de paiement lors de l'appel à `self.base.upgrade()`.

### `getMotherShip`

Recherche et retourne l'instance du `MotherShip` dans la flotte du joueur.

```python
def getMotherShip(self) -> Optional[MotherShip]:
```

| Retour | Type | Description |
| :--- | :--- | :--- |
| `Optional[MotherShip]` | Le vaisseau mère si trouvé, ou `None` sinon. |

-----

## Affichage

### `__str__`

Fournit une représentation textuelle de l'objet `Player`.

```python
def __str__(self) -> str:
```

  * **Format de retour :** `Player([nom], solde=[solde], base_tier=[tier de base], ships=[nombre de vaisseaux])`.
