# `Turn`

La classe `Turn` est une classe utilitaire de type **statique** (méthodes de classe) qui gère l'état global du jeu, notamment la rotation des joueurs, le suivi du nombre de tours, et l'accès aux données des joueurs et de leurs vaisseaux.

-----

## Attributs de Classe

| Nom | Type | Valeur par défaut | Description |
| :--- | :--- | :--- | :--- |
| `players` | [`List[Player]`](./Player.md) | `[]` | Liste des joueurs dans l'ordre de jeu. Le joueur actuel est toujours en première position (`players[0]`). |
| `sentence` | `str` | `"Tour"` | Préfixe textuel utilisé dans la description du tour. |
| `_nb_turns` | `float` | `1.0` | Compteur interne du nombre de tours. Il est incrémenté d'une fraction à chaque changement de joueur pour permettre un affichage entier (`get_nb_turns`). |

-----

## Méthodes de Classe

### `next`

Passe la main au joueur suivant dans la liste.

```python
@classmethod
def next(cls) -> Optional[Player]:
```

| Retour | Type | Description |
| :--- | :--- | :--- |
| [`Optional[Player]`](./Player.md) | Le joueur actuel (`players[0]`) si la rotation est bloquée (joueur suivant sans vaisseau mère), sinon `None`. |

#### Fonctionnement

1.  Vérifie si la liste des joueurs n'est pas vide.
2.  **Condition de blocage :** Si le joueur suivant (`players[1]`) n'a pas de vaisseau mère (`getMotherShip()` retourne `None`), le tour ne change pas, et la méthode retourne le joueur actuel (`players[0]`).
3.  Le joueur actuel est retiré du début de la liste (`pop(0)`) et placé à la fin (`append(player)`).
4.  Le compteur interne `_nb_turns` est mis à jour : il est incrémenté de : `1 / nombre de joueur` (arrondi au chiffre inférieur).

### `describe`

Fournit une description textuelle de l'état actuel du tour.

```python
@classmethod
def describe(cls):
```

| Retour | Type | Description |
| :--- | :--- | :--- |
| `str` | Une chaîne au format : `"Tour [Numéro du tour] : [Nom du joueur actuel]"`. Retourne `"Aucun joueur"` si la liste est vide. |

### `get_players_ships`

Récupère la liste de tous les vaisseaux appartenant à tous les joueurs.

```python
@classmethod
def get_players_ships(cls) -> list:
```

| Retour | Type | Description |
| :--- | :--- | :--- |
| `list` | Une liste contenant tous les objets [`Ship`](./ship/Ship.md) de tous les joueurs. |

  * La méthode itère sur tous les joueurs et agrège les listes `player.ships` dans une seule liste.

### `get_nb_turns`

Retourne le numéro de tour actuel arrondi à l'entier inférieur.

```python
@classmethod
def get_nb_turns(cls) -> int:
```

| Retour | Type | Description |
| :--- | :--- | :--- |
| `int` | Le nombre de tours entiers effectués. |

  * Retourne la partie entière de `cls._nb_turns` (`int(cls._nb_turns)`).

### `get_player_with_id`

Recherche et retourne un joueur par son identifiant.

```python
@classmethod
def get_player_with_id(cls, id: int) -> Optional[Player]:
```

| Paramètre | Type | Description |
| :--- | :--- | :--- |
| `id` | `int` | L'identifiant du joueur à trouver. |
| Retour | `Optional[Player]` | Le joueur correspondant à l'ID, ou `None` si aucun joueur n'est trouvé. |
