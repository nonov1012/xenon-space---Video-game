# `ProjectileAnimator`

La classe `ProjectileAnimator` étend la classe `Animator` pour gérer spécifiquement l'affichage, le mouvement et la durée de vie des projectiles (balles, torpilles, lasers).

Elle utilise le chemin de base défini par la constante `PROJECTILES_PATH` pour charger les assets.

## Hérite de [`Animator`](./1-Animator.md)

---

## Attribut de Classe

### `projectiles_data`

Dictionnaire qui mappe le type de projectile à ses dimensions par défaut en pixels.

| Clé (Type de projectile) | Valeur (Largeur, Hauteur en pixels) |
| :--- | :--- |
| `"bullet"` | `(4, 16)` |
| `"big bullet"` | `(8, 16)` |
| `"torpedo"` | `(11, 32)` |
| `"wave"` | `(64, 64)` |
| `"laser"` | `(18, 38)` |

:::info[*Remarque*]
Le laser n'utilise pas le sprite car il crée directement le laser avec pygame
:::

-----

## Constructeur

```python
def __init__(
    self,
    dimensions: Tuple[int, int],
    coord: Tuple[int, int],
    default_fps: int = 10,
    speed: int = 1,
    movable: bool = True,
    projectile_type: str = "projectile",
    dissipate_speed: Optional[float] = None,
    duration_ms: Optional[int] = 5000
)
```

### Paramètres

| Nom | Type | Description |
| :--- | :--- | :--- |
| `dimensions` | `Tuple[int, int]` | Dimensions du sprite en nombre de cases (`width_tiles`, `height_tiles`). |
| `coord` | `Tuple[int, int]` | Coordonnées initiales `(x, y)` en pixels. |
| `default_fps` | `int` | Nombre de frames par seconde (défaut : 10). |
| `speed` | `int` | Vitesse de mouvement (défaut : 1). |
| `movable` | `bool` | Si `True`, le projectile se déplace vers sa cible (défaut : `True`). |
| `projectile_type` | `str` | Type de projectile (ex : "bullet", "laser") (défaut : "projectile"). |
| `dissipate_speed` | `Optional[float]` | Vitesse de dissipation (ou d'apparition) pour le laser (défaut : `None`). |
| `duration_ms` | `Optional[int]` | Durée de vie maximale en millisecondes avant la suppression (défaut : 5000 ms). |

### Fonctionnement

  * Appelle le constructeur de la classe parente (`Animator`).
  * Initialise le temps de début (`self.start_time`) pour le calcul de la durée de vie.
  * **Cas spécial "laser" :**
      * Décale la position X de l'origine au centre du sprite (`self.x += self.pixel_w / 2`).
      * Calcule ou utilise la vitesse de dissipation (`self.dissipate_speed`). Si non fournie, elle est calculée proportionnellement à la longueur initiale du laser (5% de la longueur).

-----

## Méthodes Surchargées

### `update_and_draw`

Met à jour l'état du projectile (durée de vie) et le dessine.

```python
def update_and_draw(self):
```

  * **Gestion de la Durée de Vie :** Si la durée maximale (`self.duration_ms`) est atteinte, le projectile est marqué comme inactif et est supprimé de la liste de classe via `self.remove_from_list()`.
  * **Dessin :**
      * Si le `projectile_type` est `"laser"`, appelle la méthode privée `self._draw_laser()`.
      * Sinon, appelle la méthode `update_and_draw` de la classe parente pour un dessin classique (basé sur spritesheet).

### `erase`

Efface l'image ou la ligne représentant le projectile de l'écran.

```python
def erase(self, color=(0, 0, 0)):
```

| Paramètre | Type | Description |
| :--- | :--- | :--- |
| `color` | `Tuple[int, int, int]` | Couleur RVB utilisée pour effacer la zone (défaut : noir `(0, 0, 0)`). |

  * **Laser :** Dessine une ligne de la même largeur que le laser mais de la couleur `color` (couleur de fond) pour l'effacer correctement de l'écran.
  * **Autres :** Appelle la méthode `erase` de la classe parente.

-----

## Méthodes Internes

### `_compute_distance`

Calcule la distance en pixels entre l'origine actuelle du projectile (`self.x`, `self.y`) et sa cible (`self.target`).

```python
def _compute_distance(self) -> float:
```

| Retour | Type | Description |
| :--- | :--- | :--- |
| `float` | La distance euclidienne entre l'origine et la cible. |

### `_draw_laser`

Dessine le laser en utilisant un effet de dissipation et de pulsation.

```python
def _draw_laser(self):
```

  * **Animation de Largeur :** Gère la largeur actuelle du laser (`self._laser_width`).
      * S'il est actif (`self._laser_active`), sa largeur augmente jusqu'à `width_max` (effet d'apparition).
      * S'il est inactif, sa largeur diminue jusqu'à 0 (effet de dissipation).
  * **Effet Visuel :** Dessine le laser en tant que lignes superposées de différentes largeurs et alphas, avec des extrémités arrondies (caps). Une fonction interne `draw_line_with_caps` est utilisée pour appliquer un effet de **pulsation** basé sur un sinus pour simuler une intensité variable (pour les couches rouges).
  * Dessine une couche centrale **blanche et opaque** pour l'intensité et plusieurs couches rouges, toutes en utilisant des surfaces Pygame avec canal alpha (`pygame.SRCALPHA`) pour la transparence.
