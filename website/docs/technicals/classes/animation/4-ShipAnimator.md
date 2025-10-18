# `ShipAnimator`

La classe `ShipAnimator` étend la classe `Animator` pour gérer l'affichage et les animations complexes des vaisseaux spatiaux. Elle intègre la gestion des points de vie (PV), de la rotation, des animations prioritaires (bouclier, destruction, armes) et de l'animation moteur en arrière-plan.

## Hérite de [`Animator`](./1-Animator.md)

-----

## Constructeur

```python
def __init__(
    self,
    path: str,
    dimensions: Tuple[int, int],
    coord: Tuple[int, int],
    tile_size: int = TAILLE_CASE,
    default_fps: int = 10,
    PV_actuelle: int = 100,
    PV_max: int = 100,
    angle: int = 0,
    show_health: bool = True,
    color: Tuple[int, int, int] = (0, 255, 0),
    alpha: int = 255
) -> None:
```

### Paramètres

| Nom | Type | Description |
| :--- | :--- | :--- |
| `path` | `str` | Chemin vers le dossier contenant les sprites du vaisseau. |
| `dimensions` | `Tuple[int, int]` | Dimensions du vaisseau en **nombre de cases** (`width_tiles`, `height_tiles`). |
| `coord` | `Tuple[int, int]` | Coordonnées initiales `(x, y)` en **pixels**. |
| `tile_size` | `int` | Taille d'une tuile en pixels (défaut : `TAILLE_CASE`). |
| `default_fps` | `int` | Nombre d'images par seconde pour l'animation par défaut (défaut : 10). |
| `PV_actuelle` | `int` | Points de vie actuels (défaut : 100). |
| `PV_max` | `int` | Points de vie maximum (défaut : 100). |
| `angle` | `int` | Angle de rotation du vaisseau (en degrés) (défaut : 0). |
| `show_health` | `bool` | Affiche ou masque la barre de vie (défaut : `True`). |
| `color` | `Tuple[int, int, int]` | Couleur RVB de la barre de vie (défaut : vert `(0, 255, 0)`). |
| `alpha` | `int` | Niveau de transparence (0 = invisible, 255 = opaque) (défaut : 255). |

### Fonctionnement

  * Charge l'image statique du vaisseau (`base.png`), si elle existe, et la met à l'échelle.
  * Initialise les attributs de gestion d'état : `PV_actuelle`, `PV_max`, `angle`, `alpha`, et `alive`.
  * Initialise les attributs d'animation : `self.animations` (dictionnaire d'animations), `self.current_anim`, `self.idle` (moteur en marche, déf. `True`).

-----

## Méthodes Publiques

### `update_and_draw`

Met à jour la position, la rotation, les animations et dessine le vaisseau, y compris la barre de vie.

```python
def update_and_draw(self) -> bool:
```

| Retour | Type | Description |
| :--- | :--- | :--- |
| `bool` | `True` uniquement si l'animation courante (non-moteur) vient de se terminer (utilisé principalement pour l'animation `"weapons"`). |

  * **Mouvement et Rotation :** Appelle `self.move()` (hérité) et `self.slow_set_angle()` (si une cible d'angle est définie).
  * **Dessin Statique :** Dessine l'image `base.png` (avec rotation et `alpha`) si aucune animation prioritaire (`"sheild"` ou `"destruction"`) n'est en cours.
  * **Dessin Animation Prioritaire :** Gère l'avancement et le dessin de l'animation courante (ex : `"weapons"`, `"destruction"`). Si l'animation est terminée, elle réinitialise `self.frame_index` et met `self.current_anim` à `None`.
  * **Dessin Moteur (`"engine"`) :** Si `self.idle` est `True` et l'animation `"engine"` existe, elle est dessinée sous le vaisseau de manière cyclique.
  * **Barre de Vie :** Appelle `self.display_health()` si `self.show_health` est `True`.
  * **Tir :** Appelle `self.fire()`.

### `display_health`

Dessine une barre de vie horizontale sous le vaisseau, représentant la proportion de `PV_actuelle` par rapport à `PV_max`.

```python
def display_health(self):
```

  * La barre est dessinée avec un fond **rouge** (vie perdue) et une barre de couleur personnalisée (`self.color`) pour la vie restante.

### `disepear`

Applique un effet de fondu progressif sur l'image ou l'animation courante.

```python
def disepear(self, duration_ms: int = 1000) -> bool:
```

| Paramètre | Type | Description |
| :--- | :--- | :--- |
| `duration_ms` | `int` | Durée totale du fondu en millisecondes (défaut : 1000). |
| Retour | `bool` | `True` si la durée de fondu est écoulée. |

  * Réduit la valeur **alpha** de l'image courante de 255 à 0 sur la durée spécifiée.

### `update`

Met à jour les points de vie actuels et maximaux.

```python
def update(self, PV_actuelle: int, PV_max: int):
```

### `play_with_fade`

Lance une animation et applique un fondu simultanément, généralement utilisé pour la disparition/destruction.

```python
def play_with_fade(self, name: str, fade_duration: int = 1000, reset: bool = False):
```

  * Appelle `self.play(name, reset=reset)` puis `self.update_and_draw()`, suivi de `self.disepear()` pour appliquer le fondu sur l'animation en cours.

### `distance`

Calcule la distance euclidienne entre le centre du vaisseau et une cible donnée.

```python
def distance(self, target: Tuple[int, int]) -> float:
```

### `fire`

Gère le déclenchement de l'animation de tir (`"weapons"`) et la création d'un nouvel objet `ProjectileAnimator`.

```python
def fire(self, projectile_type: str = None, target: Tuple[int, int] = None, is_fired: bool = False, projectile_speed: int = None):
```

  * Si `is_fired` est `True`, déclenche l'animation `"weapons"`.
  * Si l'animation `"weapons"` est marquée comme **terminée** (`self.finished` est `True`):
      * Crée un nouvel objet `ProjectileAnimator`.
      * Calcule la position de `spawn` du projectile **devant le nez** du vaisseau en tenant compte de `self.angle`.
      * Initialise le projectile avec sa cible, sa vitesse, sa durée de vie (calculée sur la base de la distance à la cible pour les projectiles non-laser) et le type de projectile.

## Méthode de Classe

### `update_all`

Méthode de classe statique pour mettre à jour tous les `ShipAnimator` actifs.

```python
@classmethod
def update_all(cls):
```

  * Ière sur la liste de toutes les animations enregistrées (`cls.liste_animation`).
  * Si un vaisseau est marqué comme **non-vivant** (`animation.alive` est `False`), il lance l'animation de destruction (`"destruction"`) avec fondu en utilisant `animation.play_with_fade()`.
  * Une fois le fondu de destruction terminé, le vaisseau est retiré définitivement de la liste via `animation.remove_from_list()`.
