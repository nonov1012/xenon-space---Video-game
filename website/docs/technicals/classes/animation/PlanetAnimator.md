# `PlanetAnimator`

La classe `PlanetAnimator` hérite de la classe `Animator` et est spécifiquement conçue pour gérer l'affichage et l'animation des planètes. Elle ajoute une fonctionnalité clé : la génération et l'affichage d'une **atmosphère** autour de l'entité.

Elle utilise le chemin de base défini par la constante `PLANETES_PATH` pour charger les assets.

## Hérite de [`Animator`](./Animator.md)

-----

## Constructeur

```python
def __init__(self, dimensions, coord, default_fps=10, speed=1):
```

### Paramètres

| Nom | Type | Description |
| :--- | :--- | :--- |
| `dimensions` | `Tuple[int, int]` | Dimensions de la planète en **nombre de cases** (`width_tiles`, `height_tiles`). |
| `coord` | `Tuple[int, int]` | Coordonnées initiales **en cases** (`x`, `y`). |
| `default_fps` | `int` | Nombre de frames par seconde par défaut pour l'animation (défaut : 10). |
| `speed` | `int` | Vitesse de mouvement de la planète (défaut : 1). |

### Fonctionnement

  * Appelle le constructeur de la classe parente (`Animator`) en utilisant `PLANETES_PATH` comme chemin de base.
  * Initialise deux attributs privés pour l'atmosphère :
      * `self._atmosphere_surface`: Surface Pygame pré-générée de l'atmosphère (`Optional[pygame.Surface]`). Initialisé à `None`.
      * `self._atmosphere_offset`: Décalage de position pour le dessin de l'atmosphère (`Tuple[int, int]`).

-----

## Méthodes Surchargées

### `update_and_draw`

Met à jour et dessine l'animation de la planète et son atmosphère.

```python
def update_and_draw(self):
```

  * **Ordre de Dessin :** Assure que l'atmosphère est dessinée **avant** la planète (`self.draw_atmosphere()`), puis appelle `super().update_and_draw()` pour dessiner la planète elle-même.

### `play`

Démarre ou continue une animation spécifique de la planète.

```python
def play(self, name: str, reset: bool = False):
```

| Paramètre | Type | Description |
| :--- | :--- | :--- |
| `name` | `str` | Le nom de l'animation à jouer. |
| `reset` | `bool` | Si `True`, réinitialise l'animation (défaut : `False`). |

  * Appelle `super().play()`, mais **force** la taille de frame à la valeur de la constante globale `PLANETES_FRAME_SIZE` pour toutes les animations de planète.

-----

## Méthodes Spécifiques à l'Atmosphère

### `draw_atmosphere`

Dessine l'atmosphère de la planète, en la générant une seule fois si elle n'existe pas encore.

```python
def draw_atmosphere(self,
                    color_atmosphere=(0, 200, 255),
                    thickness_ratio: float = 0.12,
                    layers: int = 20,
                    edge_alpha: int = 180):
```

| Paramètre | Type | Description |
| :--- | :--- | :--- |
| `color_atmosphere` | `Tuple[int, int, int]` | Couleur RVB de l'atmosphère (défaut : bleu ciel). |
| `thickness_ratio` | `float` | Proportion de la taille de la planète utilisée pour l'épaisseur du halo atmosphérique (défaut : 0.12). |
| `layers` | `int` | Nombre de cercles concentriques dessinés pour créer le dégradé (défaut : 20). |
| `edge_alpha` | `int` | Transparence maximale (alpha, 0-255) à la bordure extérieure (défaut : 180). |

  * Si `self._atmosphere_surface` est `None`, appelle `self._generate_atmosphere` pour créer la surface.
  * Dessine la surface de l'atmosphère sur `Animator.screen` en utilisant l'offset calculé.

### `_generate_atmosphere` (Méthode Interne)

Génère la surface Pygame de l'atmosphère avec un effet de dégradé.

```python
def _generate_atmosphere(self, color_atmosphere, thickness_ratio, layers, edge_alpha) -> Tuple[pygame.Surface, Tuple[int, int]]:
```

| Retour | Type | Description |
| :--- | :--- | :--- |
| `Tuple[pygame.Surface, Tuple[int, int]]` | La surface de l'atmosphère (avec `SRCALPHA`) et l'offset `(dx, dy)` à appliquer lors du dessin. |

  * Utilise `pygame.draw.circle` en itérant de l'extérieur vers l'intérieur pour créer un dégradé de transparence (canal alpha).

### `invalidate_atmosphere`

Force la régénération de l'atmosphère lors du prochain appel à `draw_atmosphere`.

```python
def invalidate_atmosphere(self):
```

  * Définit `self._atmosphere_surface` à `None`.

J'ai fait en sorte de livrer le texte directement ici, vous devriez pouvoir le sélectionner facilement et le coller dans votre éditeur \!