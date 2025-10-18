# `HUD`

La classe `HUD` est une classe utilitaire de type **statique** (n'utilise que des méthodes et attributs de classe) responsable de l'initialisation, de la gestion et du dessin des principaux éléments d'interface utilisateur affichés à l'écran (barres d'état des joueurs et affichage du tour).

Elle agrège les classes [`BarDisplay`](./BarDisplay.md) et [`TurnDisplay`](./TurnDisplay.md).

-----

## Attributs de Classe

La classe `HUD` stocke ses composants d'interface dans des attributs de classe.

| Nom | Type | Description |
| :--- | :--- | :--- |
| `left_bar` | [`BarDisplay`](./BarDisplay.md) | Barre d'état affichant les informations du **Joueur 0**. |
| `right_bar` | [`BarDisplay`](./BarDisplay.md) | Barre d'état affichant les informations du **Joueur 1**. |
| `turn_display` | [`TurnDisplay`](./TurnDisplay.md) | Panneau d'affichage du tour en cours. |

-----

## Méthodes de Classe

### `init`

Initialise les composants du HUD en créant les instances de [`BarDisplay`](./BarDisplay.md) et [`TurnDisplay`](./TurnDisplay.md). Cette méthode doit être appelée **une seule fois** au démarrage du jeu.

```python
@classmethod
def init(cls, screen: pygame.Surface):
```

| Paramètre | Type | Description |
| :--- | :--- | :--- |
| `screen` | `pygame.Surface` | La surface de l'écran sur laquelle les éléments seront dessinés. |

  * Initialise `cls.left_bar` pour `Turn.players[0]`, avec surbrillance activée (`highlight = True`).
  * Initialise `cls.right_bar` pour `Turn.players[1]`, sans surbrillance initiale.
  * Initialise `cls.turn_display`.

### `update`

Met à jour la logique interne de tous les composants du HUD (synchronisation des valeurs PV, argent, temps d'animation).

```python
@classmethod
def update(cls):
```

  * Appelle les méthodes `update()` sur `cls.left_bar`, `cls.right_bar`, et `cls.turn_display`.

### `change_turn`

Inverse l'état de surbrillance (`highlight`) des barres d'état pour indiquer visuellement quel joueur est actif.

```python
@classmethod
def change_turn(cls):
```

  * Inverse la valeur de `highlight` entre `cls.left_bar` et `cls.right_bar`.

### `draw`

Dessine tous les composants du HUD sur l'écran.

```python
@classmethod
def draw(cls):
```

  * Appelle les méthodes `draw()` des barres, en leur passant la surface de l'écran (récupérée de `cls.turn_display.screen`).
  * Appelle la méthode `draw()` sur `cls.turn_display`.

### `update_and_draw`

Méthode combinée pour simplifier l'appel des mises à jour et du dessin dans la boucle principale du jeu.

```python
@classmethod
def update_and_draw(cls):
```

  * Appelle séquentiellement `cls.update()` puis `cls.draw()`.

-----

## Exemple d'Utilisation

Le bloc de test inclus montre la séquence standard d'utilisation :

1.  Initialisation de Pygame et création des objets `Player` et `MotherShip`.
2.  Appel de `HUD.init(screen)` pour initialiser l'interface.
3.  Dans la boucle principale :
      * Les mises à jour des données du jeu (argent, PV) sont effectuées.
      * L'appel de `HUD.update()` et `HUD.draw()` garantit que les barres reflètent les nouvelles données.
      * La touche **ESPACE** simule le passage au tour suivant via `Turn.next()` et `HUD.change_turn()`, inversant la surbrillance des barres.
