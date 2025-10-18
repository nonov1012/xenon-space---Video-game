# MenuParametres

## 1. Objectif Principal

La classe `MenuParametres` implémente l'interface utilisateur pour la configuration des paramètres du jeu (touches, audio). Elle utilise Pygame pour le rendu et une architecture orientée objet pour une meilleure maintenabilité et extensibilité.

---

## 2. Architecture Générale

### 2.1 Structure de Classe

```
MenuParametres
├── Initialisation (_init_*)
├── Actions des boutons (_action_*)
├── Gestion des événements (_handle_*)
├── Mise à jour (_update)
├── Rendu (_draw_*)
└── Boucle principale (run)
```

### 2.2 Classes Utilitaires

**Slider** : Élément graphique pour l'ajustement des volumes (0-100%)
- `update_valeur(mouse_x)` : Met à jour la valeur selon la position de la souris
- `draw(surface)` : Affiche la barre de progression et le curseur

**ButtonParam** : Bouton interactif avec effet de zoom au survol
- `update(mouse_pos)` : Gère l'animation de zoom
- `draw(surface)` : Affiche le bouton avec texte
- `is_clicked(mouse_pos)` : Vérifie si le bouton est cliqué

---

## 3. Phase d'Initialisation

### 3.1 _init_colors()
Définit les constantes de couleur pour l'interface :
- Teintes de base : `BLANC`, `NOIR`, `GRIS_FONCE`, `GRIS_MOYEN`, `GRIS_CLAIR`
- Teintes d'accent : `VERT`, `BLEU_ACCENT`, `ORANGE`

### 3.2 _init_fonts()
Charge les polices depuis `assets/fonts/SpaceNova.otf` :
- `police_titre` (60px) : Titre principal
- `police_param` (22px) : Textes des paramètres
- `police_bouton` (28px) : Textes des boutons

### 3.3 _init_cursor()
Charge et dimensionne le curseur personnalisé (40x40px) depuis `assets/img/menu/cursor.png`

### 3.4 _init_background()
Crée le fond animé spacial via `create_space_background()` avec :
- Champ d'étoiles (`self.stars`)
- Gestionnaire de planètes (`self.planet_manager`)

### 3.5 _init_ui_elements()
Configure les éléments d'interface :
- Dimensions du panneau (800x500px)
- Positionnement centré
- Définition des onglets : "Touches" et "Audio"
- Configuration des touches (rotation, terminer tour, afficher grille, etc.)

### 3.6 _init_sliders()
Crée les trois sliders audio :
- Volume général (0-100%)
- Volume musique (0-100%)
- Volume sons (0-100%)

Chaque slider est positionné à l'intérieur du panneau avec un espacement régulier.

### 3.7 _init_buttons()
Génère les trois boutons principaux (SAUVEGARDER, RESET, RETOUR) avec :
- Image de base redimensionnée selon la taille du texte
- Association à une action de rappel
- Positionnement bas de l'écran avec espacement régulier

---

## 4. Gestion des Événements

### 4.1 _handle_events()
Boucle principal d'événements qui traite :
- `pygame.QUIT` : Ferme le menu
- `pygame.KEYDOWN` : Capture des touches
- `pygame.MOUSEBUTTONDOWN` : Clics de souris
- `pygame.MOUSEBUTTONUP` : Relâchement de souris

### 4.2 _handle_keydown()
Si le mode capture est actif (`self.capture_touche`), enregistre la touche pressée dans `self.settings["touches"]`

### 4.3 _handle_click()
Gère les clics selon le contexte :
- Clic sur onglets : change l'onglet actif
- Onglet "Touches" : active le mode capture sur le bouton de touche cliqué
- Onglet "Audio" : active le slider cliqué
- Clics sur boutons : déclenche l'action associée

### 4.4 _check_slider_click()
Détecte le clic sur un slider audio et l'active en mode glisser

---

## 5. Mise à Jour et Rendu

### 5.1 _update()
Exécutée à chaque frame (60 FPS) :
- Mise à jour du zoom des boutons
- Mise à jour du slider actif si la souris est maintenue pressée

### 5.2 _draw_background()
Affiche le fond spatial :
- Remplit l'écran en noir
- Met à jour et dessine les étoiles
- Met à jour et dessine les planètes (si animation activée)

### 5.3 _draw_title()
Affiche le titre "Parametres" centré en haut de l'écran

### 5.4 _draw_panel()
Dessine le panneau principal (rectangle arrondi avec bordure) en couleur `GRIS_FONCE`

### 5.5 _draw_tabs()
Affiche les deux onglets ("Touches" et "Audio") :
- Couleur `BLEU_ACCENT` pour l'onglet actif
- Couleur `GRIS_CLAIR` pour les inactifs
- Texte blanc/gris selon l'état

### 5.6 _draw_touches_tab()
Affiche l'onglet des touches :
- Liste des 5 touches configurables avec labels
- Bouton pour chaque touche affichant le nom actuel
- Bouton en orange "Appuyez..." lors de la capture

### 5.7 _draw_audio_tab()
Affiche l'onglet audio :
- Label pour chaque paramètre
- Pourcentage actuel en couleur `BLEU_ACCENT`
- Slider correspondant

### 5.8 _draw_buttons()
Affiche les trois boutons du bas avec l'effet de zoom

### 5.9 _draw_cursor()
Affiche le curseur personnalisé à la position de la souris

### 5.10 _render()
Effectue le rendu complet dans l'ordre :
1. Fond spacial
2. Titre
3. Panneau et onglets
4. Contenu de l'onglet actif
5. Boutons
6. Curseur

---

## 6. Actions des Boutons

### 6.1 _action_sauvegarder()
Sauvegarde les paramètres actuels dans `save_parametre.json` via la fonction `sauvegarder_parametres()`

### 6.2 _action_reset()
Réinitialise les paramètres aux valeurs par défaut (`DEFAULT_SETTINGS`) et réinitialise les sliders

### 6.3 _action_retour()
Ferme le menu en mettant `self.running = False`

---

## 7. Boucle Principale

### 7.1 run()
Boucle principale du menu :
```
while self.running:
    _handle_events()    # Traite les événements
    _update()           # Met à jour la logique
    _render()           # Affiche tous les éléments
    clock.tick(60)      # Limite à 60 FPS
```

---

## 8. Persistance des Données

### 8.1 Sauvegarde
Fichier : `save_parametre.json`
Format JSON contenant :
- `touches` : Codes des touches (pygame.K_*)
- `audio` : Niveaux de volume (0-100)

### 8.2 Chargement
- Au démarrage : Charge les paramètres sauvegardés
- En cas d'erreur : Utilise les paramètres par défaut

---

## 9. Interface Utilisateur

### 9.1 État Persistant
- `self.onglet_actif` : Onglet actuellement affiché
- `self.capture_touche` : Touche en cours de capture (None sinon)
- `self.slider_actif` : Slider en cours de glissement
- `self.settings` : Dictionnaire des paramètres actuels

### 9.2 Feedback Utilisateur
- Survol des boutons : Zoom à 1.1x
- Capture de touche : Bouton devient orange avec texte "Appuyez..."
- Sliders : Barre de progression verte avec curseur blanc