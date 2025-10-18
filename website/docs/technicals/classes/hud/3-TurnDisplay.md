# `TurnDisplay`

La classe `TurnDisplay` est responsable de l'affichage d'un panneau d'information central, généralement positionné en haut de l'écran, qui indique le numéro du tour en cours et le nom du joueur dont c'est le tour. Le panneau est rendu avec un effet de semi-transparence.

## Dépendances

  * **Pygame :** Utilisée pour toutes les fonctions graphiques (surfaces, dessin, polices).
  * **[`Player`](../Player.md) :** Représentation des joueurs (utilisé implicitement via la classe [`Turn`](../Turn.md)).
  * **[`Turn`](../Turn.md) :** Classe statique gérant la logique du jeu (compteur de tours et liste des joueurs).

-----

## Constructeur

```python
def __init__(self, screen: pygame.Surface):
```

### Paramètres

| Nom | Type | Description |
| :--- | :--- | :--- |
| `screen` | `pygame.Surface` | La surface principale de l'écran sur laquelle le panneau sera dessiné. |

### Attributs Initialisés

| Attribut | Valeur | Description |
| :--- | :--- | :--- |
| `self.width` | `160` | Largeur fixe du panneau en pixels. |
| `self.height` | `60` | Hauteur fixe du panneau en pixels. |
| `self.margin` | `30` | Marge entre le panneau et le haut de l'écran. |
| `self.font_title` | `pygame.font` | Police utilisée pour le numéro du tour (style futuriste **"Orbitron"**, 20px, gras). |
| `self.font_player` | `pygame.font` | Police utilisée pour le nom du joueur (style **"Consolas"**, 18px). |
| `self.bg_color` | `(20, 25, 40, 180)` | Couleur de fond du panneau (bleu nuit sombre, avec une **opacité de 180** sur 255). |
| `self.border_color` | `(80, 210, 255)` | Couleur de la bordure et du nom du joueur (bleu-cyan lumineux). |
| `self.warn_color` | `(255, 80, 80)` | Couleur utilisée si aucun joueur n'est trouvé (rouge d'avertissement). |

-----

## Méthodes Publiques

### `update`

Méthode de mise à jour du panneau. Actuellement vide, elle est un *placeholder* pour de futures logiques d'animation ou de vérification d'état.

```python
def update(self):
```

### `draw`

Dessine le panneau du tour en cours sur l'écran.

```python
def draw(self):
```

#### Étapes de Dessin

1.  **Calcul de la Position :** Calcule les coordonnées `(x, y)` pour centrer horizontalement le panneau en haut de l'écran.
2.  **Panneau Transparent :**
      * Crée une surface temporaire (`panel_surf`) avec le flag `pygame.SRCALPHA` pour gérer la transparence.
      * Dessine le fond (`self.bg_color` semi-transparent) et la bordure (`self.border_color`) sur cette surface temporaire.
      * Colle (`blit`) `panel_surf` sur la surface principale de l'écran.
3.  **Affichage du Tour :**
      * Récupère le numéro du tour via `Turn.get_nb_turns()` et la phrase d'introduction (`Turn.sentence`).
      * Rend le texte et le centre dans la partie supérieure du panneau.
4.  **Affichage du Joueur Courant :**
      * **Logique du Joueur :** Vérifie si `Turn.players` contient des joueurs.
          * Si oui, affiche le nom du premier joueur de la liste (`Turn.players[0].name`) en couleur `self.border_color`.
          * Si non, affiche un message d'avertissement **"Aucun joueur"** en couleur `self.warn_color`.
      * Rend le texte du joueur et le centre dans la partie inférieure du panneau.

## Exemple d'Utilisation

L'exemple montre comment initialiser `TurnDisplay` et comment simuler le passage au tour suivant (`Turn.next()`) par l'appui de la touche **ESPACE**, mettant à jour le nom du joueur affiché à chaque changement.
