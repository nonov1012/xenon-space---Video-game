# MenuPause

## 1. Objectif Principal

La classe `MenuPause` implémente l'interface de pause du jeu. Elle permet au joueur de reprendre la partie, accéder aux paramètres, retourner au menu principal ou quitter le jeu. Elle utilise une architecture orientée objet pour maintenir l'état et gérer les interactions.

---

## 2. Architecture Générale

### 2.1 Structure de Classe

```
MenuPause
├── Initialisation (_init_*)
├── Actions des boutons (_action_*)
├── Gestion des événements (_handle_*)
├── Mise à jour (_update)
├── Rendu (_draw_*)
└── Boucle principale (run)
```

### 2.2 Classes Utilitaires

**PauseButton** : Bouton interactif avec effet de zoom au survol
- `update(mouse_pos)` : Gère l'animation de zoom
- `draw(surface)` : Affiche le bouton avec texte
- `is_clicked(mouse_pos)` : Vérifie si le bouton est cliqué

---

## 3. Phase d'Initialisation

### 3.1 _init_colors()
Définit les constantes de couleur pour l'interface :
- `BLANC` : (255, 255, 255)
- `NOIR` : (0, 0, 0)

### 3.2 _init_fonts()
Charge les polices depuis `assets/fonts/SpaceNova.otf` :
- `police_bouton` (42px) : Textes des boutons
- `police_titre` (72px) : Titre (réservé pour extension future)

### 3.3 _init_cursor()
Charge et dimensionne le curseur personnalisé (40x40px) depuis `assets/img/menu/cursor.png`

### 3.4 _init_background()
Crée le fond animé spacial via `create_space_background()` avec :
- Champ d'étoiles animées (`self.stars`)
- Pas de planètes (contrairement au menu principal)

### 3.5 _init_buttons()
Génère les quatre boutons du menu de pause :
1. **REPRENDRE** : Retourne au jeu
2. **PARAMETRES** : Ouvre le menu des paramètres
3. **RETOUR AU MENU PRINCIPAL** : Quitte la partie
4. **QUITTER** : Ferme l'application

Chaque bouton est :
- Dimensionné à 500x100px
- Centré horizontalement
- Espacé verticalement de 60px
- Associé à une fonction de rappel

---

## 4. Gestion des Événements

### 4.1 _handle_events()
Boucle principal d'événements qui traite :
- `pygame.QUIT` : Ferme immédiatement l'application
- `pygame.KEYDOWN` : Traitement des touches
- `pygame.MOUSEBUTTONDOWN` : Clics de souris gauche

### 4.2 _handle_keydown()
Gère les touches pressées :
- `pygame.K_ESCAPE` : Reprend le jeu (action rapide)

### 4.3 _handle_click()
Détecte les clics sur les boutons et exécute l'action associée
Arrête la boucle de traitement si un bouton ferme le menu

---

## 5. Actions des Boutons

### 5.1 _action_reprendre()
Reprend la partie :
- Met `self.running` à `False` (sortie de la boucle)
- Stocke le résultat : `"continue"`

### 5.2 _action_parametres()
Ouvre le menu des paramètres :
- Appelle `menuParam.main()` avec `animation=False` (pas de planètes)
- Retour automatique au menu de pause

### 5.3 _action_retour_menu()
Quitte la partie vers le menu principal :
- Nettoie les listes d'animateurs : `ShipAnimator.clear_list()`, `PlanetAnimator.clear_list()`
- Met `self.running` à `False`
- Stocke le résultat : `"go_to_main_menu"`

### 5.4 _action_quitter()
Ferme complètement l'application :
- `pygame.quit()`
- `sys.exit()`

---

## 6. Mise à Jour et Rendu

### 6.1 _update()
Exécutée à chaque frame (60 FPS) :
- Récupère la position actuelle de la souris
- Met à jour le zoom des boutons au survol

### 6.2 _draw_background()
Affiche le fond spacial :
- Remplit l'écran en noir
- Met à jour et dessine les étoiles animées

### 6.3 _draw_buttons()
Affiche les quatre boutons avec effet de zoom

### 6.4 _draw_cursor()
Affiche le curseur personnalisé à la position de la souris

### 6.5 _render()
Effectue le rendu complet dans l'ordre :
1. Fond spacial
2. Boutons
3. Curseur
4. Actualisation d'écran

---

## 7. Boucle Principale

### 7.1 run()
Boucle principale du menu de pause :
```
while self.running:
    _handle_events()    # Traite les événements
    _update()           # Met à jour la logique
    _render()           # Affiche tous les éléments
    clock.tick(60)      # Limite à 60 FPS
    
return self.action_result
```

Retourne le résultat de l'action choisie :
- `"continue"` : Reprendre le jeu
- `"go_to_main_menu"` : Retour au menu principal

---

## 8. Interface Utilisateur

### 8.1 État Persistant
- `self.running` : Bool indiquant si le menu est actif
- `self.action_result` : Résultat de l'action choisie
- `self.jeu_surface` : Surface du jeu (réservée pour overlay futur)

### 8.2 Feedback Utilisateur
- Survol des boutons : Zoom à 1.1x
- Touche ÉCHAP : Raccourci pour reprendre le jeu
- Transitions fluides via `clock.tick(60)`

---

## 9. Flux de Contrôle

```
MenuPause.run()
    ↓
Boucle 60 FPS
    ├─ _handle_events()
    │   └─ Clics/Touches → Actions
    ├─ _update()
    │   └─ Animations boutons
    ├─ _render()
    │   └─ Affichage
    ↓
Action choisie
    ├─ continue → Retour au jeu
    ├─ go_to_main_menu → Retour au menu principal
    └─ quitter → Fermeture application
```

---

## 10. Intégration avec le Reste du Jeu

### 10.1 Appel depuis le Jeu
```python
# Dans handle_events() du jeu
if event.key == pygame.K_ESCAPE:
    action = menu.menuPause.main_pause(ecran)
    if action == "go_to_main_menu":
        # Retour au menu principal
    elif action == "continue":
        # Reprendre le jeu
```

### 10.2 Nettoyage des Ressources
Avant de quitter la partie, les listes d'animateurs sont vidées pour éviter les fuites mémoire :
- `ShipAnimator.clear_list()`
- `PlanetAnimator.clear_list()`