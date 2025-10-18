# `Animator`

-----

## Fonction `load_spritesheet`

Charge une **spritesheet** à partir d'un fichier image et la divise en une liste de surfaces **`pygame.Surface`**.

### Signature

```python
def load_spritesheet(path: str, frame_width: int, frame_height: int) -> List[pygame.Surface]:
```

### Paramètres

| Nom | Type | Description |
| :--- | :--- | :--- |
| `path` | `str` | Chemin vers le fichier image de la spritesheet. |
| `frame_width` | `int` | Largeur (en pixels) de chaque frame dans la spritesheet. |
| `frame_height` | `int` | Hauteur (en pixels) de chaque frame dans la spritesheet. |

### Retour

| Type | Description |
| :--- | :--- |
| `List[pygame.Surface]` | Liste des surfaces `pygame.Surface`, chacune représentant une frame de l'animation. |

### Description

La fonction lit l'image spécifiée, itère sur sa largeur et sa hauteur en utilisant les dimensions de frame fournies, et extrait chaque frame comme une sous-surface. Elle utilise `convert_alpha()` pour gérer la transparence.

-----

## Classe `Animator`

Gère l'affichage d'une image statique et de multiples animations basées sur des spritesheets pour une entité, incluant la gestion de la position, de la taille, de la vitesse et de la rotation.

### Attribut de Classe

| Nom | Type | Description |
| :--- | :--- | :--- |
| `screen` | `pygame.Surface` | Surface **statique** de l'écran où dessiner les animations. Doit être défini via `Animator.set_screen()`. |

### Méthode Statique : `set_screen`

Définit la surface de l'écran utilisée pour le dessin.

```python
@staticmethod
def set_screen(screen: pygame.Surface)
```

| Paramètre | Type | Description |
| :--- | :--- | :--- |
| `screen` | `pygame.Surface` | La surface Pygame de l'écran principal. |

-----

## Constructeur

```python
def __init__(
    self,
    path: str,
    dimensions: Tuple[int, int],  # (width_tiles, height_tiles)
    coord: Tuple[int, int],       # (x, y) en pixels
    tile_size: int = TAILLE_CASE,
    default_fps: int = 10,
    speed: int = 1
)
```

### Paramètres

| Nom | Type | Description |
| :--- | :--- | :--- |
| `path` | `str` | Chemin vers le **dossier** contenant l'image statique (`base.png`) et les spritesheets d'animation. |
| `dimensions` | `Tuple[int, int]` | Dimensions de l'entité en **nombre de cases** (`width_tiles`, `height_tiles`). |
| `coord` | `Tuple[int, int]` | Coordonnées initiales **en cases** (`x`, `y`). |
| `tile_size` | `int` | Taille d'une case en pixels (par défaut : `TAILLE_CASE`). |
| `default_fps` | `int` | Nombre de frames par seconde par défaut pour l'animation (par défaut : 10). |
| `speed` | `int` | Vitesse de déplacement de l'entité (par défaut : 1). |

### Fonctionnement

  * Calcule les dimensions en pixels (`self.pixel_w`, `self.pixel_h`) et la position en pixels (`self.x`, `self.y`).
  * Charge l'image statique **`base.png`** si elle existe dans le dossier `path` et la redimensionne.
  * Initialise les variables de gestion d'animation et de mouvement (`self.animations`, `self.current_anim`, `self.vx`, `self.vy`, `self.target`, `self.angle`, etc.).
  * Ajoute l'instance à la liste de classe `liste_animation` pour permettre la mise à jour globale.

-----

## Méthodes d'Animation et d'Affichage

### `load_animation`

Charge une spritesheet d'animation et l'ajoute au dictionnaire `self.animations`.

```python
def load_animation(self, name: str, filename: str, frame_size: Optional[Tuple[int, int]] = None)
```

| Paramètre | Type | Description |
| :--- | :--- | :--- |
| `name` | `str` | Identifiant de l'animation (ex : "idle", "run"). |
| `filename` | `str` | Nom du fichier spritesheet (relatif à `self.path`). |
| `frame_size` | `Optional[Tuple[int, int]]` | Taille explicite des frames `(w, h)` si elles ne sont pas carrées (par défaut : `None`, utilise `sheet_h` pour `fw` et `fh`). |

  * **Conversion GIF :** Si le fichier est un `.gif`, il est automatiquement converti en `.png` spritesheet (via `gif_to_spritesheet`) s'il n'existe pas déjà.
  * Les frames sont chargées via `load_spritesheet` et **redimensionnées** aux dimensions de l'entité (`self.pixel_w`, `self.pixel_h`).

### `play`

Démarre ou continue une animation spécifique.

```python
def play(self, name: str, reset: bool = False, frame_size: Optional[Tuple[int, int]] = None)
```

| Paramètre | Type | Description |
| :--- | :--- | :--- |
| `name` | `str` | Nom de l'animation à jouer. |
| `reset` | `bool` | Si `True`, réinitialise l'animation à la première frame (par défaut : `False`). |
| `frame_size` | `Optional[Tuple[int, int]]` | Taille des frames si l'animation doit être chargée pour la première fois. |

  * Si l'animation n'est pas chargée, tente de la charger automatiquement avec `load_animation` en utilisant `name.png` ou `name.gif`.
  * Réinitialise l'index de frame et le temps de dernière mise à jour si `reset` est `True` ou si l'animation change.

### `erase`

Efface l'image (animation actuelle avec rotation) de l'écran en la recouvrant d'une couleur.

```python
def erase(self, color=(0, 0, 0))
```

| Paramètre | Type | Description |
| :--- | :--- | :--- |
| `color` | `Tuple[int, int, int]` | Couleur RVB pour effacer la zone de l'image (par défaut : noir `(0, 0, 0)`). |

### `update_and_draw`

Met à jour l'état de l'animateur (mouvement, rotation, frame d'animation) et le dessine sur l'écran.

```python
def update_and_draw(self)
```

1.  **Mouvement :** Appelle `self.move()` pour avancer vers la cible.
2.  **Rotation :** Appelle `self.slow_set_angle()` pour tourner progressivement vers `self.target_angle`.
3.  **Frame :** Met à jour `self.frame_index` si le temps écoulé (`self.frame_duration_ms`) est dépassé.
4.  **Dessin :** Dessine la frame actuelle (`self.animations[self.current_anim][self.frame_index]`), en appliquant une **rotation** autour du centre par `pygame.transform.rotate`.

-----

## Méthodes de Position et Mouvement

### `get_center`

Calcule et retourne les coordonnées du centre de l'entité en pixels.

```python
def get_center(self) -> Tuple[int, int]
```

| Retour | Type | Description |
| :--- | :--- | :--- |
| `Tuple[int, int]` | Coordonnées `(x, y)` du centre de l'entité. |

### `set_target`

Définit la cible de déplacement et calcule le vecteur direction et l'angle vers cette cible.

```python
def set_target(self, target: Tuple[int, int], angle_targeted: bool = True, image_facing: str = "up")
```

| Paramètre | Type | Description |
| :--- | :--- | :--- |
| `target` | `Tuple[int, int]` | Les coordonnées `(x, y)` en pixels de la cible. |
| `angle_targeted` | `bool` | Si `True`, met à jour l'angle cible (`self.target_angle`) pour une rotation progressive (par défaut : `True`). Sinon, met à jour `self.angle` immédiatement. |
| `image_facing` | `str` | Orientation par défaut de l'image ("up", "down", "left", "right") pour corriger l'angle de rotation (par défaut : "up"). |

  * Calcule le vecteur de direction unitaire (`self.vx`, `self.vy`).
  * Calcule l'angle de rotation nécessaire (`self.target_angle` ou `self.angle`) en tenant compte de l'orientation par défaut de l'image.

### `move`

Déplace l'entité en direction de la cible à la vitesse `self.speed`.

```python
def move(self)
```

  * Le déplacement cesse (`self.active = False`) lorsque l'entité atteint ou dépasse la cible, déterminé par le produit scalaire.

### `set_angle`

Définit l'angle de rotation de l'entité immédiatement.

```python
def set_angle(self, angle: float)
```

| Paramètre | Type | Description |
| :--- | :--- | :--- |
| `angle` | `float` | Angle cible en degrés (0° = orientation initiale de l'image). |

### `slow_set_angle`

Met à jour l'angle actuel (`self.angle`) pour qu'il se rapproche progressivement de l'`self.target_angle`.

```python
def slow_set_angle(self)
```

  * La rotation est limitée par `self.max_delta` à chaque appel pour créer un mouvement de rotation fluide.

### `set_target_angle`

Définit l'angle cible pour la rotation progressive (utilisé par `slow_set_angle`).

```python
def set_target_angle(self, angle: float)
```

| Paramètre | Type | Description |
| :--- | :--- | :--- |
| `angle` | `float` | Angle cible en degrés (0° = orientation initiale de l'image). |

-----

## Méthodes de Classe pour la Gestion Globale

Ces méthodes n'affectent que les instances de la classe *spécifique* à partir de laquelle elles sont appelées (y compris les sous-classes).

### `update_all`

Met à jour et dessine toutes les instances d'`Animator` (ou d'une sous-classe) qui ont été enregistrées dans `liste_animation`.

```python
@classmethod
def update_all(cls)
```

### `erase_all`

Appelle `erase()` sur toutes les instances d'`Animator` (ou d'une sous-classe) pour effacer leur affichage.

```python
@classmethod
def erase_all(cls)
```

### `remove_from_list`

Retire l'instance actuelle de la liste d'animations de sa classe.

```python
def remove_from_list(self)
```

### `clear_list`

Vide entièrement la liste d'animations (`liste_animation`) pour cette classe.

```python
@classmethod
def clear_list(cls)
```