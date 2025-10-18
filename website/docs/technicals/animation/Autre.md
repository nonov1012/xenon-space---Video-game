# Autre Fonctionnalitée

La fonction `gif_to_spritesheet` est une utilité qui convertit un fichier d'animation GIF en une unique image statique appelée **spritesheet**. Chaque image (frame) du GIF est extraite et positionnée dans une grille au sein de l'image de sortie.

Elle utilise la librairie `Pillow` (`PIL`) pour le chargement et la manipulation des images.

-----

## Signature

```python
def gif_to_spritesheet(gif_path, output_path, rows=None, cols=None):
```

## Paramètres

| Nom | Type | Description |
| :--- | :--- | :--- |
| `gif_path` | `str` | Chemin d'accès au fichier GIF source. |
| `output_path` | `str` | Chemin d'accès où la spritesheet sera sauvegardée (le format est déduit de l'extension, par ex. `.png`). |
| `rows` | `Optional[int]` | Nombre de lignes souhaité dans la grille de la spritesheet. Si non spécifié, il est calculé. |
| `cols` | `Optional[int]` | Nombre de colonnes souhaité dans la grille de la spritesheet. Si `rows` et `cols` sont `None`, la fonction crée une seule ligne (autant de colonnes que de frames). |

## Dépendances

  * `PIL` (Pillow) : La fonction repose entièrement sur les classes `Image` et `ImageSequence`.

## Fonctionnement Détaillé

1.  **Chargement et Extraction :**

      * Le fichier GIF est ouvert à l'aide de `Image.open(gif_path)`.
      * Toutes les frames du GIF sont itérées et copiées dans une liste. Chaque frame est convertie au format **RGBA** pour conserver la transparence, si présente.
      * La largeur, la hauteur et le nombre total de frames sont récupérés.

2.  **Calcul de la Grille :**

      * Si ni `rows` ni `cols` ne sont spécifiés, la valeur par défaut est une seule ligne : `cols` est égal au nombre total de frames.
      * Si seulement `rows` ou `cols` est spécifié, l'autre dimension est calculée pour contenir toutes les frames.

3.  **Création de la Spritesheet :**

      * Les dimensions totales de la spritesheet (`sheet_width`, `sheet_height`) sont calculées en multipliant les dimensions de la grille par celles d'une frame.
      * Une nouvelle image vide (`Image.new`) est créée avec ces dimensions et le format **RGBA**.

4.  **Assemblage :**

      * Chaque frame est collée (`spritesheet.paste`) dans l'image finale à sa position dans la grille :
          * Coordonnée X : `(i % cols) * frame_width`
          * Coordonnée Y : `(i // cols) * frame_height`

5.  **Sauvegarde :**

      * L'image finale est sauvegardée au chemin spécifié par `output_path`.
      * Un message de confirmation est affiché dans la console.