# `BarDisplay`

La classe `BarDisplay` est responsable de l'affichage d'une barre d'état détaillée pour un joueur. Cette barre affiche des informations clés comme la monnaie du joueur et les points de vie de son vaisseau mère, et inclut un effet d'animation de surbrillance (`highlight`) pulsant.

## Dépendances

  * **Pygame :** Utilisée pour le dessin (`pygame.draw`), les surfaces (`pygame.Surface`), les polices de caractères (`pygame.font`), et les vecteurs (`pygame.Vector2`).
  * **`blazyck` :** Utilisation des constantes `OFFSET_X`, `SCREEN_WIDTH`, `SCREEN_HEIGHT`.
  * **`math` :** Utilisée pour la fonction sinus dans l'animation du *glow*.

-----

## Constructeur

```python
def __init__(self, player, left=True):
```

### Paramètres

| Nom | Type | Description |
| :--- | :--- | :--- |
| `player` | [`Player`](../Player.md) | L'objet joueur auquel la barre d'affichage est liée. |
| `left` | `bool` | Détermine si la barre doit être affichée à gauche (`True`) ou à droite (`False`) de l'écran (défaut : `True`). |

### Attributs Initialisés

  * **Dimensions :**
      * `self.width`: Largeur de la barre (basée sur `OFFSET_X // 2`).
      * `self.height`: Hauteur de la barre (basée sur `SCREEN_HEIGHT // 2`).
      * `self.margin`: Marge par rapport aux bords de l'écran (30 pixels).
  * **Statistiques :**
      * `self.health`, `self.health_max`: Points de vie actuels et maximum du vaisseau mère du joueur. Affiche un message d'erreur si le joueur n'a pas de `MotherShip`.
      * `self.money`: Solde actuel du joueur (issu de `player.economie.solde`).
  * **Graphique :**
      * `self.font_small`, `self.font_medium`: Polices Pygame utilisées.
      * `self.highlight`: Booléen contrôlant l'animation de surbrillance (défaut : `False`).
      * `self._time`: Temps interne utilisé pour l'animation du *glow*.

-----

## Méthodes Publiques

### `set_money`

Met à jour le montant d'argent affiché sur la barre.

```python
def set_money(self, amount):
```

| Paramètre | Type | Description |
| :--- | :--- | :--- |
| `amount` | `int` | Le nouveau solde d'argent. |

### `set_health`

Met à jour les points de vie affichés, en s'assurant que la valeur reste entre 0 et `health_max`.

```python
def set_health(self, value):
```

| Paramètre | Type | Description |
| :--- | :--- | :--- |
| `value` | `int` | La nouvelle valeur des points de vie. |

### `update`

Met à jour les valeurs affichées et le temps interne pour l'animation.

```python
def update(self, dt=0):
```

| Paramètre | Type | Description |
| :--- | :--- | :--- |
| `dt` | `float` | Temps écoulé depuis la dernière mise à jour (en secondes). |

  * Met à jour `self.money` et `self.health` à partir des données du joueur.
  * Incrémente `self._time` de `dt`.

### `draw`

Dessine la barre d'état complète (cadre, glow, barre de vie, textes) sur la surface cible.

```python
def draw(self, surface):
```

| Paramètre | Type | Description |
| :--- | :--- | :--- |
| `surface` | `pygame.Surface` | La surface sur laquelle dessiner (généralement l'écran du jeu). |

#### Étapes de Dessin

1.  **Calcul des Coordonnées :** Détermine la position `(x, y)` de la barre en fonction de `self.left`, `SCREEN_WIDTH`, `SCREEN_HEIGHT`, et des marges.
2.  **Glow Animé (Surbrillance) :**
      * Si `self.highlight` est `True`, dessine un effet de pulsation blanc autour du cadre.
      * L'intensité et la taille du *glow* varient en utilisant `math.sin(self._time * 4)` et `math.sin(self._time * 6)` pour créer une animation fluide.
      * Utilise une surface temporaire avec `pygame.SRCALPHA` pour dessiner le *glow* transparent.
3.  **Cadre Principal :** Dessine le fond gris foncé et le contour bleu-cyan de la barre.
4.  **Barre de Vie :**
      * Calcule la hauteur de la barre de vie actuelle en fonction du ratio `self.health / self.health_max`.
      * Dessine la barre de vie (rouge) dans le cadre.
5.  **Texte Monnaie :** Dessine le symbole "₿" (jaune-orange) et le montant de l'argent (blanc) centrés au-dessus du cadre.
6.  **Texte PV :** Dessine le texte `PV_actuel/PV_max` centré sous le cadre.
