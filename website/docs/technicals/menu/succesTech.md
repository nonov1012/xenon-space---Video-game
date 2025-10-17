# Documentation Technique : Menu Succès (Fonction `main`)

## 1. Objectif Principal

La fonction `main(ecran)` implémente l'interface utilisateur du menu des succès. Elle affiche une grille de succès débloqués/verrouillés avec descriptions au survol, un fond spatial animé, et permet le scroll vertical. Les succès sont chargés depuis un fichier JSON et leurs images sont affichées dans une grille de 3 colonnes.

---

## 2. Structure et Composants

### 2.1. Initialisation (Début de `main`)

* **Couleurs et Polices** : Définition des constantes de couleur (`BLANC`, `GRIS_*`, `OR`, `BLEU_ACCENT`) et chargement de 4 polices SpaceNova.otf de différentes tailles (60px titre, 24px boutons, 22px succès, 16px descriptions).
* **Animation de Fond** : Appel à `create_space_background()` pour générer un fond spatial dynamique avec étoiles, planètes et vaisseau.
* **Curseur** : Désactivation du curseur système et chargement du curseur personnalisé (40x40px).
* **Bouton Retour** : Calcul de sa position et de son image avec gestion du zoom au survol.

### 2.2. Chargement des Succès

* **Fichier JSON** : Charge `succes.json` depuis le même répertoire (`menu/succes.json`).
* **Gestion des Erreurs** : Affichage de messages debug et fallback vers liste vide en cas d'erreur.
* **Chargement des Images** : Pour chaque succès, charge l'image depuis le chemin JSON ou crée un placeholder gris si le fichier manque.
* **Structure JSON** :
  ```json
  [
    {
      "id": "string",
      "titre": "string",
      "description": "string",
      "image": "chemin/vers/image.png",
      "debloque": boolean
    }
  ]
  ```

### 2.3. Configuration de la Grille

* **Disposition** : 3 colonnes, espacement de 30px, taille de case 140x140px
* **Centrage** : La grille est centrée horizontalement dans le panneau
* **Scroll** : Gestion du défilement vertical avec calcul du contenu total et offset maximum

---

## 3. Logique de la Boucle Principale

La fonction utilise une boucle `while en_cours:` pour gérer le rendu et les événements à 60 FPS (`horloge.tick(60)`).

### 3.1. Récupération Input

```python
souris = pygame.mouse.get_pos()
```

Position de la souris mise à jour à chaque frame pour la détection des survols.

### 3.2. Rendu (Phase de Dessin)

1. **Nettoyage et Fond Spatial**
   * Remplit l'écran en noir
   * Met à jour et affiche les étoiles, planètes et animateurs
   * Résultat : fond dynamique et vivant

2. **Titre**
   * "SUCCES" affiché en OR (255, 200, 0), 60px, centré en haut

3. **Panneau Principal**
   * Rectangle arrondi en `GRIS_FONCE` avec bordure `GRIS_MOYEN`
   * Dimensions : 800x500px, centré horizontalement
   * Bordure : 3px

4. **Grille de Succès (avec Clipping)**
   * Utilise `ecran.set_clip()` pour limiter le rendu à la zone du panneau
   * Pour chaque succès visible :
     
     a. **Calcul de position avec scroll**
        ```python
        rect_affiche = rect_succes.copy()
        rect_affiche.y -= scroll_offset
        ```
     
     b. **Vérification de visibilité**
        ```python
        if rect_affiche.bottom < panneau_y or rect_affiche.top > panneau_y + panneau_hauteur:
            continue  # Ne pas dessiner
        ```
     
     c. **Détection du survol**
        ```python
        est_survole = rect_affiche.collidepoint(souris)
        ```
     
     d. **Couleur selon état de déblocage**
        ```python
        if succes["debloque"]:
            couleur_fond = BLEU_ACCENT
            couleur_bordure = OR
        else:
            couleur_fond = GRIS_MOYEN
            couleur_bordure = GRIS_CLAIR
        ```
     
     e. **Effet de survol**
        ```python
        if est_survole:
            rect_hover = rect_affiche.inflate(10, 10)
            pygame.draw.rect(ecran, OR, rect_hover, border_radius=10)
        ```
     
     f. **Rendu du succès**
        * Fond du succès avec bordure arrondie
        * Image du succès (120x120px) centrée
        * Overlay sombre + cadenas (🔒) si verrouillé
     
     g. **Tracage du succès survolé**
        ```python
        if est_survole:
            succes_survole = succes  # Utilisé pour le tooltip
        ```

5. **Tooltip au Survol**
   * Affiché uniquement si un succès est survolé
   * Position : +20px du curseur (clamped à l'écran)
   * Dimensions : 350x100px
   * Contenu :
     * Titre du succès en OR
     * Description en gris (max 2 lignes, avec wrapping)
   * Fond semi-transparent noir avec bordure OR

6. **Bouton Retour**
   * Détection du survol : `rect_retour.collidepoint(souris)`
   * Animation de zoom au survol (1.0 → 1.1)
   * Rendu avec texte centré

7. **Curseur Personnalisé**
   * Affiché à `souris` (position de la souris)

8. **Actualisation de l'Écran**
   * `pygame.display.flip()` : Mise à jour complète
   * `horloge.tick(60)` : Limite à 60 FPS

### 3.3. Gestion des Événements (`pygame.event.get()`)

* **Fermeture** (`pygame.QUIT`) : Met `en_cours` à `False`
* **Molette de Souris** (`pygame.MOUSEWHEEL`) :
  ```python
  scroll_offset -= event.y * 30
  scroll_offset = max(0, min(scroll_offset, max_scroll))
  ```
  * Scroll vers le haut : `event.y = +1` → défilement vers le haut
  * Scroll vers le bas : `event.y = -1` → défilement vers le bas
  * Valeur 30px : hauteur du scroll par "cran"
  * Clamping : Empêche le scroll d'aller au-delà des limites

* **Clic Souris** (`pygame.MOUSEBUTTONDOWN`) :
  * Clique sur **RETOUR** : `en_cours = False` (quitte le menu)

---

## 4. Système de Scroll Vertical

### 4.1. Calcul des Dimensions

```python
nb_lignes = (len(succes_liste) + colonnes - 1) // colonnes
hauteur_contenu = nb_lignes * (taille_case + espacement) + 40
max_scroll = max(0, hauteur_contenu - panneau_hauteur + 60)
```

* Nombre de lignes : Arrondi supérieur du nombre de succès / nombre de colonnes
* Hauteur totale : (lignes × hauteur_case) + marge
* Max scroll : Limite pour éviter le "overscroll" (vide en bas du panneau)

### 4.2. Application du Scroll

```python
rect_affiche.y -= scroll_offset
```

Appliqué à chaque succès avant le rendu. Valeur négative = défilement vers le haut.

### 4.3. Clipping pour Limiter le Rendu

```python
zone_scroll = pygame.Rect(panneau_x, panneau_y, panneau_largeur, panneau_hauteur)
ecran.set_clip(zone_scroll)
# ... dessiner les succès ...
ecran.set_clip(None)
```

Seuls les pixels à l'intérieur de `zone_scroll` sont affichés. Empêche les succès de dépasser les bords du panneau.

---

## 5. Système d'Affichage des Succès

### 5.1. États de Succès

**Débloqué** :
- Fond : `BLEU_ACCENT` (70, 130, 255)
- Bordure : `OR` (255, 200, 0)
- Image : Normale
- Overlay : Aucun

**Verrouillé** :
- Fond : `GRIS_MOYEN` (90, 90, 110)
- Bordure : `GRIS_CLAIR` (180, 180, 200)
- Image : Normale
- Overlay : Noir semi-transparent (alpha 150)
- Cadenas : Emoji "🔒" au centre

### 5.2. Effet de Survol

```python
if est_survole:
    rect_hover = rect_affiche.inflate(10, 10)
    pygame.draw.rect(ecran, OR, rect_hover, border_radius=10)
```

Rectangle orange légèrement plus grand (+10px de chaque côté) autour du succès survolé.

### 5.3. Tooltip Multi-lignes

Algoritme de wrapping du texte :
1. Split par mots
2. Ajouter mots tant que `largeur < tooltip_largeur - 30`
3. Passer à la ligne suivante si dépassement
4. Limiter à 2 lignes affichées

---

## 6. Gestion des Ressources

### 6.1. Chargement des Images

* Chemin absolu calculé depuis `succes.json`
* Redimensionnement à 120x120px
* Gestion des erreurs : Placeholder gris 120x120px en cas de problème
* Messages debug : Affichage d'état pour chaque image

### 6.2. Nettoyage des Animateurs

```python
ShipAnimator.clear_list()
PlanetAnimator.clear_list()
```

À la fin, nettoie les listes d'animateurs pour éviter les fuites mémoire.

---

## 7. Considérations Techniques

### 7.1. Fréquence de Rendu

* **60 FPS** pour le menu succès (plus haute que le menu principal)
* Limite : `horloge.tick(60)`

### 7.2. Ratio d'Écran

```python
screen_ratio = (largeur_ecran * 100 / 600) / 100
```

Ajuste dynamiquement les éléments spaciaux selon la résolution.

### 7.3. Chemin Relatif du JSON

```python
chemin_json = os.path.join(os.path.dirname(__file__), "succes.json")
```

Charge `succes.json` depuis le même répertoire que `menuSucces.py` (robuste aux changements de répertoire courant).

### 7.4. Clipping et Performance

Le clipping (`set_clip`) améliore la performance en limitant le rendu aux pixels visibles, notamment important lors du scroll.

---

## 8. Flux d'Utilisateur

```
Menu Succès (60 FPS)
    ↓
[Grille affichée avec succès débloqués/verrouillés]
    ├─ Débloqués : OR/BLEU, image normale
    └─ Verrouillés : GRIS, overlay + cadenas
    ↓
[Survol d'un succès]
    ├─ Bordure orange s'affiche
    └─ Tooltip apparaît (titre + description)
    ↓
[Scroll Molette]
    ├─ Contenu défile verticalement
    └─ Clipping limite à la zone du panneau
    ↓
[Clic sur RETOUR]
    └─ Retour au menu précédent
```

---

## 9. État Persistant

* `scroll_offset` : Position verticale du scroll (en pixels)
* `succes_survole` : Référence au succès actuellement survolé (None sinon)
* `zoom_etat_retour` : État du zoom du bouton retour

---

## 10. Notes Techniques

### 10.1. Pourquoi Utiliser set_clip() ?

Permet le scroll naturel sans perte de performance. Les pixels en dehors de `zone_scroll` ne sont simplement pas affichés.

### 10.2. Cadenas Unicode

```python
texte_cadenas = police_cadenas.render("🔒", True, BLANC)
```

Utilise l'emoji 🔒 pour indiquer un succès verrouillé. Compatible avec Unicode.

### 10.3. Inflation du Rectangle

```python
rect_hover = rect_affiche.inflate(10, 10)
```

Augmente la largeur et hauteur de 10px chacun (5px de chaque côté). Crée un effet de "surbrillance".

### 10.4. Structure JSON Flexible

Le format JSON permet d'ajouter facilement de nouveaux succès sans modifier le code :
```json
{
  "id": "succes_id",
  "titre": "Titre du Succès",
  "description": "Description détaillée...",
  "image": "assets/img/succes/image.png",
  "debloque": true
}
```