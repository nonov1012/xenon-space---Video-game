# Credit

## 1. Objectif du Module

Le module `credit.py` implémente l'écran des **Crédits** du jeu. Son rôle est d'afficher les noms des contributeurs sous forme de **défilement vertical** (`roll`) animé, en intégrant un fond spatial dynamique et une fonctionnalité d'interaction par clic unique (explosion de particules).

---

## 2. Architecture des Classes

Le module utilise une seule classe auxiliaire pour la gestion des effets visuels et la fonction `main()` pour la boucle de l'écran.

### 2.1. Classe `Particle`

Gère le comportement et le rendu d'une particule individuelle émise lors de l'explosion d'une ligne de crédit.

| Méthode | Rôle | Détails Techniques |
| :--- | :--- | :--- |
| `__init__` | Initialisation. | Définit la position (`x`, `y`), la couleur, le vecteur de vélocité (`vx`, `vy`), et la durée de vie (`life = 60` frames). |
| `update()` | Physique de la particule. | Met à jour la position. Applique une **accélération verticale positive** (`self.vy += 0.2`) pour simuler l'effet de la gravité (la particule retombe). Décrémente la durée de vie. |
| `draw(surface)` | Rendu. | Dessine la particule comme un petit cercle de rayon 3 tant que sa durée de vie est positive. |

---

## 3. Fonction `main(ecran)` : Logique du Défilement et des Événements

La fonction `main` est la boucle de l'écran et gère tous les états et les interactions.

### 3.1. Initialisation et Rendu du Fond

1.  **Fond** : Les objets **`stars`** et **`planet_manager`** sont initialisés via `create_space_background()`.
2.  **Synchronisation** : Les fonctions `Animator.update_all()`, `PlanetAnimator.update_all()`, etc., sont appelées à chaque frame pour garantir que les animations de fond se poursuivent.
3.  **Position de Départ** : La variable **`credit_y`** est initialisée à **`hauteur_ecran`**, plaçant le bloc de texte des crédits hors champ, juste sous l'écran.

### 3.2. Contrôle du Défilement

| Variable | Rôle | Implémentation |
| :--- | :--- | :--- |
| `vitesse_defilement` | Vitesse par défaut (1 pixel/frame). | Utilisée lorsque la touche ESPACE n'est pas enfoncée. |
| `vitesse_acceleree` | Vitesse rapide (4 pixels/frame). | Utilisée si le drapeau `espace_enfonce` est `True`. |
| `credit_y` | Coordonnée Y centrale pour la ligne actuelle de crédits. | Mis à jour chaque frame par `credit_y -= vitesse`. |
| **Arrêt** | Condition de fin. | Si la position verticale de la dernière ligne de crédit (`y_offset`) est **inférieure à 0**, la boucle s'arrête (`en_cours = False`), revenant au menu principal. |

### 3.3. Gestion de l'Explosion Particulaire (Clic Souris)

Le code gère l'événement `MOUSEBUTTONDOWN` (bouton 1).

1.  **Détection de Clic** : Ictère sur la liste `credits` et calcule le rectangle de collision (`rect_click`) pour chaque ligne de crédit à sa position actuelle (`y_offset_click`).
2.  **Échantillonnage de Pixels** : Si une collision est détectée :
    * Le texte cliqué est traité par une double boucle avec un pas (`step = 6`).
    * **`text_surf_click.get_at((i, j))`** est utilisé pour obtenir la couleur de chaque pixel du texte.
    * Seuls les pixels avec une **composante alpha (`color[3]`) supérieure à 0** (pixels non transparents) génèrent une particule.
3.  **Génération** : Une instance de `Particle` est créée pour chaque pixel échantillonné, avec des vecteurs de vélocité (`vx`, `vy`) aléatoires (`random.uniform()`) pour simuler une dispersion.

### 3.4. Gestion des Particules

La boucle de rendu gère la mise à jour et la suppression des particules :

1.  **Mise à Jour** : `p.update()` est appelée pour appliquer la gravité et le mouvement.
2.  **Rendu** : `p.draw(ecran)` affiche la particule.
3.  **Nettoyage** : Les particules dont `p.life` est inférieur ou égal à 0 sont supprimées de la liste `particles[:]` via `particles.remove(p)` pour libérer de la mémoire et optimiser les performances.