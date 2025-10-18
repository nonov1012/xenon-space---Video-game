# MenuFin

## 1. Objectif du Module

Le module menuFin.py implémente l'écran de fin de partie. Il affiche le résultat du jeu (**VICTOIRE** ou **DEFAITE**) et fournit des options de navigation (retour au menu principal ou quitter). Il utilise une architecture orientée objet avec des classes distinctes pour le menu et les boutons.

---

## 2. Architecture des Classes

### 2.1. Classe EndButton

Gère le comportement et le rendu d'un bouton interactif, intégrant un effet de zoom pour le survol.

| Attribut | Type | Rôle |
| :--- | :--- | :--- |
| `rect` | `pygame.Rect` | Zone de collision et de positionnement de base. |
| `action` | `function` | Callback exécuté lors du clic. |
| `zoom` | `float` | Facteur de mise à l'échelle pour l'animation visuelle (état actuel). |
| `is_hovered` | `bool` | État de survol actuel. |

| Méthode | Rôle | Détails Techniques |
| :--- | :--- | :--- |
| `update(mouse_pos)` | Animation de survol. | Détecte le survol. Gère le zoom via une **interpolation linéaire lissée** (zoom de 1.0 à 1.1) : `self.zoom += (target_zoom - self.zoom) * 0.08`. Retourne `True` au début du survol pour déclencher le son (`son_hover`). |
| `draw(surface)` | Rendu. | Redimensionne l'image (`pygame.transform.scale`) en utilisant `self.zoom` et dessine l'image et la surface texte **centrées** sur le nouveau rectangle zoomé. |
| `is_clicked(mouse_pos)` | Détection de clic. | Vérifie la collision entre la position de la souris et le rectangle de base (`self.rect`). |

---

### 2.2. Classe MenuFin

Classe principale gérant la logique d'état, l'initialisation des composants et le cycle de vie du menu.

#### 2.2.1. Initialisation et Préparation

* **Nettoyage** : Les listes d'animateurs globaux (`ShipAnimator`, `PlanetAnimator`) sont **vidées** (`clear_list()`) pour éviter les conflits de rendu avec les éléments de jeu précédents.
* **Fond** : `_init_background()` utilise `create_space_background()` pour générer le fond spatial animé persistant (étoiles, planètes).
* **Panneau** : `_init_panel()` définit les dimensions et les coordonnées centrées du rectangle central semi-transparent.
* **Boutons** : `_init_buttons()` crée les instances de `EndButton`. La **positionnement horizontal** est calculée pour centrer le groupe de boutons avec un espacement fixe (`espacement = 80`). Les images de boutons sont mises à l'échelle pour s'adapter au texte.
* **Sons** : `_init_sound()` charge et référence les SFX de survol et de clic.

#### 2.2.2. Actions des Boutons (Callbacks)

Ces méthodes sont associées aux boutons et mettent fin à la boucle `MenuFin.run()`.

| Méthode | Rôle | Effet sur l'État |
| :--- | :--- | :--- |
| `_action_menu()` | Déclenché par le bouton "RETOUR AU MENU". | Définit l'action de retour : `self.choix = "menu_principal"` et met fin à la boucle : `self.running = False`. |
| `_action_quitter()`| Déclenché par le bouton "QUITTER" ou la fermeture de la fenêtre (`pygame.QUIT`). | Définit l'action de sortie : `self.choix = "quitter"` et met fin à la boucle : `self.running = False`. |

#### 2.2.3. Boucle Principale et Logique

| Méthode | Rôle | Détails d'Implémentation |
| :--- | :--- | :--- |
| `_handle_events()` | Gestion des événements. | Gère la fermeture de fenêtre et le clic souris. |
| `_handle_click()` | Clic de souris. | Détecte le clic sur un bouton, joue `son_click`, puis exécute le `button.action` associé. |
| `_update()` | Mise à jour de la logique. | Appelle `button.update()` pour gérer l'animation de survol de chaque bouton et joue `son_hover` si nécessaire. |
| `run()` | Boucle principale. | Contient le cycle `_handle_events`, `_update`, `_render` et gère le taux de rafraîchissement à 60 FPS (`self.clock.tick(60)`). Retourne `self.choix` une fois la boucle terminée. |

#### 2.2.4. Rendu

* **`_draw_background()`** : Dessine le fond. Nécessite l'appel à `update()` et `update_all()` pour les étoiles et les classes d'animation (`PlanetAnimator`, `ShipAnimator`).
* **`_draw_panel()`** : Crée une surface `pygame.SRCALPHA` pour dessiner un rectangle semi-transparent (`alpha=200`) avec une bordure, centré sur l'écran.
* **`_draw_title()`** : Affiche le titre ("VICTOIRE" ou "DEFAITE") en utilisant les couleurs (`self.JAUNE` ou `self.ROUGE`) définies en fonction de l'état `self.victoire`.
* **`_draw_cursor()`** : Dessine le curseur personnalisé (`self.cursor`) à la position de la souris (le curseur système est désactivé via `pygame.mouse.set_visible(False)`).

---

## 3. Fonction main (Wrapper d'Exécution)

La fonction `main` sert de point d'entrée pour lancer le menu de fin.

* Elle instancie `MenuFin` et appelle sa méthode `run()` pour exécuter la boucle du menu.
* Elle gère l'action d'arrêt : si l'action retournée par `menu.run()` est `"quitter"`, elle exécute `pygame.quit()` et `sys.exit()`, terminant l'application.
* Elle retourne l'action choisie (`"menu_principal"`) au module de jeu principal pour la transition.