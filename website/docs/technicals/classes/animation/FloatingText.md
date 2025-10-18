# `FloatingText`

La classe `FloatingText` gère l'affichage de messages textuels éphémères qui s'élèvent et disparaissent progressivement (effet de fondu) à l'écran, typiquement utilisés pour afficher les dégâts subis, les gains de points, ou de brèves notifications.

## Attribut de Classe

### `instances`

```python
instances = []
```

Liste globale de toutes les instances actives de `FloatingText`. Chaque nouvelle instance est automatiquement ajoutée à cette liste lors de l'initialisation.

-----

## Constructeur

```python
def __init__(self, text, pos, color=(255, 255, 255), lifetime=1.0, rise_speed=30):
```

### Paramètres

| Nom | Type | Description |
| :--- | :--- | :--- |
| `text` | `str` | Le message à afficher. |
| `pos` | `Tuple[int, int]` | La position initiale du texte en pixels. Stocké dans un `pygame.Vector2`. |
| `color` | `Tuple[int, int, int]` | La couleur RVB du texte (défaut : blanc `(255, 255, 255)`). |
| `lifetime` | `float` | La durée de vie totale du texte en secondes (défaut : 1.0). |
| `rise_speed` | `int` | La vitesse de montée du texte en pixels par seconde (défaut : 30). |

### Attributs Initialisés

  * `self.age`: Âge actuel du texte en secondes, initialisé à `0`.
  * `self.font`: Police Pygame utilisée (`"consolas"`, taille `20`).
  * L'instance est automatiquement ajoutée à `FloatingText.instances`.

-----

## Méthodes d'Instance

### `update`

Met à jour la position et l'âge de l'instance.

```python
def update(self, dt):
```

| Paramètre | Type | Description |
| :--- | :--- | :--- |
| `dt` | `float` | Le temps écoulé depuis la dernière mise à jour, en secondes. |

  * **Âge :** `self.age` est incrémenté de `dt`.
  * **Position :** La coordonnée Y (`self.pos.y`) est diminuée de `self.rise_speed * dt` pour simuler l'élévation.

### `draw`

Dessine le texte sur la surface et gère sa disparition.

```python
def draw(self, surface):
```

| Paramètre | Type | Description |
| :--- | :--- | :--- |
| `surface` | `pygame.Surface` | La surface sur laquelle dessiner le texte. |

  * **Calcul Alpha (Transparence) :** L'opacité est calculée de manière linéaire
  * **Suppression Automatique :** Si `alpha` est inférieur ou égal à 0, l'instance est retirée de la liste globale `FloatingText.instances`, et le dessin est interrompu.
  * **Dessin :** Le texte est rendu, sa transparence est ajustée avec `text_surf.set_alpha(int(alpha))`, puis il est dessiné au centre de sa position X (`self.pos.x - text_surf.get_width()//2`) sur la surface.

-----

## Méthodes de Classe

### `update_all`

Met à jour la position et l'âge de **toutes** les instances de `FloatingText` actives.

```python
@classmethod
def update_all(cls, dt):
```

| Paramètre | Type | Description |
| :--- | :--- | :--- |
| `dt` | `float` | Le temps écoulé en secondes. |

### `draw_all`

Dessine **toutes** les instances de `FloatingText` actives sur la surface donnée.

```python
@classmethod
def draw_all(cls, surface):
```

| Paramètre | Type | Description |
| :--- | :--- | :--- |
| `surface` | `pygame.Surface` | La surface cible du dessin. |

### `update_and_draw_all`

Méthode combinée pour simplifier le cycle de vie du texte flottant dans la boucle principale du jeu.

```python
@classmethod
def update_and_draw_all(cls, surface, dt):
```

| Paramètre | Type | Description |
| :--- | :--- | :--- |
| `surface` | `pygame.Surface` | La surface cible du dessin. |
| `dt` | `float` | Le temps écoulé en secondes. |

  * Appelle séquentiellement `cls.update_all(dt)` puis `cls.draw_all(surface)`.