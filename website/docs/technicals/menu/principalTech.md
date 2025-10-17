# Documentation Technique : Menu Principal (Fonction `main`)

## 1. Objectif Principal

La fonction `main()` implémente l'interface utilisateur du menu principal du jeu. Elle affiche une interface avec un titre animé, cinq boutons interactifs avec effet de zoom, et un fond spatial dynamique. Elle utilise Pygame pour le rendu et une boucle événementielle à 30 FPS pour l'interactivité.

---

## 2. Structure et Composants

### 2.1. Initialisation (Début de `main`)

* **Couleurs et Polices** : Définition des constantes de couleur (`BLANC`) et chargement de la police SpaceNova.otf en deux tailles (25px pour les boutons, 100px pour le titre).
* **Curseur** : Désactivation du curseur système et chargement du curseur personnalisé (48x48px) depuis `assets/img/menu/cursor.png`.
* **Sons** : Initialisation du gestionnaire `SoundManager` avec :
    * Musique de fond : `music_ingame.mp3`
    * Effet survol : `button_hover.mp3`
    * Effet clic : `button_pressed.mp3`
* **Animation de Fond** : Appel à `create_space_background()` pour générer un fond spatial dynamique avec :
    * Champ d'étoiles animées
    * Gestionnaire de planètes
    * Vaisseau mère (B1) pour animation
* **Titre Animé** : Création du titre "XENON-SPACE" avec gradient jaune → magenta, utilisant la classe `TitreAnime`.
* **Boutons Principaux** : Calcul des rectangles et des images pour les 5 boutons avec gestion des états de zoom (`zoom_states`) et survol (`hover_states`).
* **Icône de Fenêtre** : Chargement depuis `assets/img/menu/logo.png`.

### 2.2. Zones d'Interface

* **Titre** : Centré horizontalement, positionné à y=200.
* **Boutons Jouer/Paramètres/Succès/Quitter** : Décalés à -500px (gauche), espacés verticalement de 100px, centré au y=screen_height/2.
* **Bouton Crédits** : Position fixe en bas-droit de l'écran.

---

## 3. Logique de la Boucle Principale

La fonction utilise une boucle `while en_cours:` pour gérer le rendu et les événements à 30 FPS (`clock.tick(30)`).

### 3.1. Récupération Input

```python
try:
    souris = pygame.mouse.get_pos()
except pygame.error:
    souris = (0, 0)  # Fallback de sécurité
```

Récupère la position de la souris avec gestion d'exception.

### 3.2. Rendu (Phase de Dessin)

1. **Nettoyage et Vérification de l'Écran**
   * Remplit l'écran en noir (0,0,0)
   * Vérifie l'état du verrou de l'écran avant le rendu

2. **Fond Spatial**
   * `stars.update()` : Met à jour les positions des étoiles
   * `stars.draw()` : Dessine le champ d'étoiles
   * `planet_manager.update_and_draw()` : Met à jour et affiche les planètes
   * `Animator.update_all()`, `PlanetAnimator.update_all()`, `ShipAnimator.update_all()` : Met à jour toutes les animations

3. **Titre**
   * `titre.draw()` : Affiche le titre animé (gradient appliqué automatiquement par la classe)

4. **Boutons**
   * Pour chaque bouton (5 au total) :
     
     a. **Initialisation d'état** (première itération)
        ```python
        if i not in zoom_states:
            zoom_states[i] = 1.0
        if i not in hover_states:
            hover_states[i] = False
        ```
     
     b. **Détection du survol**
        ```python
        zone_survol = bouton.inflate(0, -100)  # Réduit hauteur de 100px
        est_survol = zone_survol.collidepoint(souris)
        ```
     
     c. **Effet sonore au survol** (une seule fois)
        ```python
        if est_survol and not hover_states[i]:
            sm.play_sfx("son_hover")
        hover_states[i] = est_survol
        ```
     
     d. **Animation du zoom (interpolation linéaire)**
        ```python
        zoom_cible = 1.1 if est_survol else 1.0
        zoom_states[i] += (zoom_cible - zoom_states[i]) * zoom_speed
        ```
        * Au survol : zoom jusqu'à 1.1 (10% d'augmentation)
        * En dehors : zoom jusqu'à 1.0 (normal)
        * `zoom_speed = 0.08` : Vitesse de transition
     
     e. **Redimensionnement et rendu**
        ```python
        bouton_zoom = pygame.transform.scale(
            image_bouton,
            (int(largeur_bouton * zoom_states[i]), 
             int(hauteur_bouton * zoom_states[i]))
        )
        rect_zoom = bouton_zoom.get_rect(center=bouton.center)
        ecran.blit(bouton_zoom, rect_zoom.topleft)
        ```
     
     f. **Rendu du texte**
        ```python
        rect_texte = texte.get_rect(center=rect_zoom.center)
        ecran.blit(texte, rect_texte.topleft)
        ```
        Le texte reste centré sur le bouton zoomed

5. **Curseur Personnalisé**
   * `ecran.blit(new_cursor, souris)` : Affiche le curseur à la position de la souris

6. **Actualisation de l'Écran**
   * `pygame.display.flip()` : Met à jour l'affichage complet
   * `clock.tick(30)` : Limite à 30 FPS

### 3.3. Gestion des Événements (`pygame.event.get()`)

* **Fermeture** (`pygame.QUIT`) : Met `en_cours` à `False`
* **Clic Souris** (`pygame.MOUSEBUTTONDOWN`) :
    * **JOUER** : Appelle `menu.menuJouer.draw(ecran)` + effet sonore
    * **PARAMETRES** : Appelle `menu.menuParam.main(ecran, True)` + effet sonore
    * **SUCCES** : Appelle `menu.menuSucces.main(ecran)` + effet sonore
    * **CREDITS** : Appelle `menu.credit.main(ecran)` + effet sonore
    * **QUITTER** : `pygame.quit()` + `sys.exit()` + effet sonore

---

## 4. Système d'Animation des Boutons

### 4.1. Zone de Survol Réduite

```python
zone_survol = bouton.inflate(0, -100)
```

Le rectangle de survol est réduit en hauteur (-100px) pour créer un zone de détection plus petite que l'image visuelle du bouton. Cela offre un contrôle plus précis du trigger de survol.

### 4.2. Interpolation du Zoom (Easing)

```python
zoom_states[i] += (zoom_cible - zoom_states[i]) * zoom_speed
```

Formule d'interpolation linéaire progressive :
* `zoom_speed = 0.08` → 8% de la distance par frame
* Résultat : transition fluide et naturelle
* Asymptote : atteint 99% de la cible après ~50 frames (1.7 secondes à 30 FPS)

Exemple : Passage de 1.0 à 1.1
- Frame 1 : 1.0 + (1.1 - 1.0) × 0.08 = 1.008
- Frame 2 : 1.008 + (1.1 - 1.008) × 0.08 = 1.0154
- ...
- Frame 50 : ≈ 1.099

### 4.3. Son au Survol (Déclenché une seule fois)

```python
if est_survol and not hover_states[i]:
    sm.play_sfx("son_hover")
hover_states[i] = est_survol
```

Le son ne joue qu'une seule fois lors de l'activation du survol. La condition `not hover_states[i]` garantit que le son ne joue que quand `hover_states[i]` passe de `False` à `True`.

---

## 5. Considérations Techniques

### 5.1. Fréquence de Rendu

* **30 FPS** pour le menu principal (économe en ressources)
* Limite : `clock.tick(30)`
* Raison : Le menu principal n'est pas critique en performance

### 5.2. Gestion de l'Écran

```python
if ecran is None:
    ecran = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
if ecran.get_locked() is False:
    ecran.fill((0,0,0))
```

Vérifications de sécurité pour éviter les bugs d'affichage et les états incohérents.

### 5.3. Animations Globales

Les classes `Animator`, `PlanetAnimator`, et `ShipAnimator` sont mises à jour chaque frame pour maintenir l'animation fluide du fond spatial.

### 5.4. Ratio d'Écran

```python
screen_ratio = (screen_width * 100 / 600) / 100
```

Ajuste dynamiquement les éléments spaciaux selon la résolution :
- 1920px → 3.2x
- 1280px → 2.13x

---

## 6. Flux d'Utilisateur

```
Menu Principal (30 FPS)
    ↓
[Mouvement Souris sur Bouton]
    ├─ Zoom 1.0 → 1.1 (interpolation progressive)
    ├─ Son "hover" (une seule fois)
    └─ Bouton agrandit visuellement
    ↓
[Clic Souris sur Bouton]
    ├─ Vérification collision `collidepoint()`
    ├─ Son "click"
    └─ Action :
        ├─ JOUER → Menu Jouer
        ├─ PARAMETRES → Menu Paramètres
        ├─ SUCCES → Menu Succès
        ├─ CREDITS → Menu Crédits
        └─ QUITTER → Fermeture Application
```

---

## 7. État Persistant

* `zoom_states` : Dictionnaire associant chaque bouton à son niveau de zoom actuel
* `hover_states` : Dictionnaire associant chaque bouton à son état de survol
* `zoom_speed` : Constante de vitesse d'interpolation (0.08)

---

## 8. Notes Technique

### 8.1. Pourquoi pygame.FULLSCREEN vs pygame.NOFRAME

Le code utilise `pygame.FULLSCREEN` pour un vrai fullscreen, contrairement à `pygame.NOFRAME` qui crée juste une fenêtre sans cadre.

### 8.2. Placement des Boutons

Les boutons JOUER/PARAM/SUCCES/QUITTER sont décalés à gauche (-500px) pour laisser de l'espace à droite. Le bouton CREDITS reste à sa position originale (bas-droit).

### 8.3. Gestion des Polices

Deux polices sont chargées :
- Titre : 100px
- Boutons : 25px

La police est pré-rendue au démarrage (`police.render()`) plutôt que à chaque frame pour éviter les ralentissements.

