
# Documentation Technique : Module de Personnalisation (Fonction `draw`)

## 1. Objectif Principal

La fonction `draw(ecran)` implémente l'interface utilisateur pour la personnalisation des paramètres de jeu (environnement) et des statistiques des vaisseaux avant de lancer une partie. Elle utilise Pygame pour le rendu et une boucle événementielle pour l'interactivité.

---

## 2. Structure et Composants

### 2.1. Initialisation (Début de `draw`)

* **Couleurs et Polices** : Définition des constantes de couleur (`BLANC`, `GRIS_FONCE`, `VERT`, etc.) et chargement des différentes tailles de police (`SpaceNova.otf`).
* **Paramètres Globaux** : Initialisation du dictionnaire `parametres` pour les options d'environnement (nombre de planètes/astéroïdes, argent de départ, etc.) et de l'état `random_active`.
* **Vaisseaux** :
    * `types_vaisseaux`: Liste des vaisseaux modifiables.
    * `vaisseau_actif` / `tier_actif`: Suivi du vaisseau et du niveau (Tier) actuellement sélectionnés.
    * Initialisation des icônes de vaisseau (`icones_vaisseaux`) en chargeant les images.
* **Curseur** : Désactivation du curseur système (`pygame.mouse.set_visible(False)`) et chargement du curseur personnalisé.
* **Animation de Fond** : Appel à `create_space_background` pour générer un fond spatial dynamique (étoiles, planètes, vaisseaux animés) utilisant les classes `ShipAnimator`, `PlanetAnimator`, et `Animator`.
* **Boutons Principaux** : Calcul des rectangles et des images pour les boutons **JOUER**, **RESET**, et **RETOUR MENU**, avec gestion des états de zoom (`zoom_etats`).

### 2.2. Zones d'Interface

* **Panneau Central** : Définition des dimensions et du placement du rectangle central (`panneau_x`, `panneau_y`) qui contient les options.
* **Onglets** : Définition des trois onglets : "Classique", "Avance", "Vaisseaux", avec l'état `onglet_actif`.

---

## 3. Logique de la Boucle Principale

La fonction utilise une boucle `while en_cours:` pour gérer le rendu et les événements à 60 FPS (`horloge.tick(60)`).

### 3.1. Rendu (Phase de Dessin)

1.  **Fond** : Mise à jour et dessin de l'animation spatiale (`stars.update()`, `PlanetAnimator.update_all()`, etc.).
2.  **Titre** : Affichage centré du titre "Personnalisation".
3.  **Panneau et Onglets** : Dessin du panneau gris et des onglets cliquables (couleur `BLEU_ACCENT` pour l'actif).
4.  **Contenu des Onglets : Classique / Avance**
    * Affiche les sliders pour les paramètres d'environnement (`parametres`).
    * Gère le dessin des barres de progression et des curseurs.
    * Affiche le bouton **RANDOM ON/OFF**.
5.  **Contenu de l'Onglet : Vaisseaux**
    * Dessine le **DROPDOWN** pour la sélection du vaisseau.
    * Affiche l'**ICÔNE** du vaisseau actif.
    * Affiche le **SÉLECTEUR DE TIER** (uniquement pour "MotherShip").
    * Dessine la **ZONE SCROLLABLE** :
        * Utilise une surface temporaire (`surf_scroll`) pour gérer le contenu défilant.
        * Affiche les paramètres du vaisseau/tier actif avec soit un **SLIDER**, soit des **BOUTONS +/-** (selon le paramètre).
        * Utilise `ecran.set_clip` pour limiter le dessin au rectangle de la zone scrollable.
6.  **Boutons Principaux** : Rendu des boutons du bas avec l'effet de zoom (`zoom_etats` et `vitesse_zoom`).
7.  **Curseur** : Affichage du curseur personnalisé à la position de la souris.

### 3.2. Gestion des Événements (`pygame.event.get()`)

* **Fermeture** : Gère `pygame.QUIT`.
* **Molette de Souris (`pygame.MOUSEWHEEL`)** :
    * Dans l'onglet "Vaisseaux" : Si le dropdown est ouvert, scroll la liste des vaisseaux (`dropdown_scroll`). Sinon, scroll la zone des paramètres des vaisseaux (`scroll_offset`).
* **Clic Souris (`pygame.MOUSEBUTTONDOWN`)** :
    * **Boutons du bas** : Déclenche les actions "JOUER", "RESET", "RETOUR MENU".
    * **Bouton RANDOM** : Inverse l'état `random_active`. Si activé, les paramètres sont randomisés.
    * **Onglets** : Change la valeur de `onglet_actif` et réinitialise les scrolls.
    * **Vaisseaux** :
        * **Dropdown** : Ouvre/ferme la liste.
        * **Liste déroulante** : Met à jour `vaisseau_actif`, réinitialise `tier_actif` et ferme le dropdown.
        * **Tiers** : Met à jour `tier_actif`.
        * **Paramètres de vaisseau** : Met à jour la valeur (si +/-) ou active le mode *glisser* (si slider) via `slider_vaisseau_actif`.
* **Relâchement Clic (`pygame.MOUSEBUTTONUP`)** : Désactive le mode *glisser* en mettant `slider_vaisseau_actif` à `None`.

### 3.3. Glisser Slider

* Un bloc de code séparé après la boucle d'événements gère la mise à jour des valeurs des sliders de vaisseau si `slider_vaisseau_actif` est défini et si le clic est maintenu.

## 4. Sortie de la Fonction

* Si `lancer_partie` est `True` (bouton JOUER cliqué) :
    * Nettoie les listes d'animateurs globaux (`ShipAnimator.clear_list()`, `PlanetAnimator.clear_list()`).
    * Importe `start_game` et lance la partie avec les paramètres définis.
* Sinon (RETOUR MENU ou QUIT), la fonction se termine, signalant la fin de la boucle d'interface.
