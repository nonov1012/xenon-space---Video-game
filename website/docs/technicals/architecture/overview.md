---
sidebar_position: 1
---

# Architecture Globale

Cette page détaille l'architecture technique de Xenon Space, ses patterns de conception et l'organisation du code.

<!-- [img]: Diagramme d'architecture générale du jeu -->

## 🏛️ Vue d'Ensemble

Xenon Space utilise une **architecture modulaire** basée sur des classes Python, avec une séparation claire entre :

- **Logique de jeu** (classes/)
- **Interface utilisateur** (menu/ + HUD)
- **Rendu graphique** (Animators)
- **Gestion des ressources** (ResourceManager)

### Diagramme des Composants

<!-- [img]: Schéma de l'architecture montrant les relations entre :
- Point d'Entrée (main.py, loading_screen.py)
- Configuration (blazyck.py)
- Gestion de Jeu (Turn, Player, Map, Shop)
- Entités (Ship, MotherShip, Petit/Moyen/Lourd, Foreuse/Transport)
- Rendu (Animator, ShipAnimator, PlanetAnimator, ProjectileAnimator)
- Interface (HUD, MenuPrincipal, FloatingText)
-->

## 🎯 Patterns de Conception

### 1. Singleton Pattern

La classe `ResourceManager` utilise le pattern Singleton pour garantir une seule instance de gestion des ressources :

```python
class ResourceManager:
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
```

**Avantages :**
- Évite le rechargement multiple des images
- Point d'accès global aux ressources
- Optimisation mémoire

### 2. Class Variables (Static)

La classe `Turn` utilise des variables de classe pour gérer l'état global du jeu :

```python
class Turn:
    players: list[Player] = []
    sentence = "Tour"
    _nb_turns: float = 1
    
    @classmethod
    def next(cls) -> Optional[Player]:
        # Passe au joueur suivant
        pass
```

**Avantages :**
- État partagé entre tous les composants
- Pas besoin de passer l'instance partout
- Accès direct via `Turn.players`

### 3. Inheritance Hierarchy

Les vaisseaux utilisent une hiérarchie d'héritage claire :

```python
Ship (classe mère)
├── MotherShip
├── Petit
├── Moyen
├── Lourd
├── Foreuse
└── Transport
```

**Exemple :**
```python
class Ship:
    def __init__(self, pv_max, attaque, ...):
        self.pv_max = pv_max
        self.attaque = attaque
    
    def attaquer(self, cible):
        # Logique commune

class Petit(Ship):
    def __init__(self, cordonner, id, ...):
        stats = SHIP_STATS["Petit"]
        super().__init__(
            pv_max=stats["pv_max"],
            attaque=stats["attaque"],
            ...
        )
```

### 4. Observer Pattern (Implicite)

Le système d'animation utilise un pattern observateur via des listes de classe :

```python
class Animator:
    def __init__(self, ...):
        cls = self.__class__
        if not hasattr(cls, "liste_animation"):
            cls.liste_animation = []
        cls.liste_animation.append(self)
    
    @classmethod
    def update_all(cls):
        for animation in cls.liste_animation:
            animation.update_and_draw()
```

## 🔄 Flux de Données

### Cycle de Vie d'une Action

<!-- [img]: Diagramme de séquence montrant :
Utilisateur → main.py → Ship.deplacement() → Ship.a_star() → 
Grille.liberer_position() → Grille.occuper_plateau() → 
ShipAnimator.set_target() → ShipAnimator.update_and_draw() → Animation
-->

**Étapes détaillées :**

1. **Utilisateur** clique sur une case
2. **main.py** détecte le clic et appelle `ship.deplacement(case_cible, grille, ships)`
3. **Ship** calcule le chemin avec `a_star(start, end)`
4. **Ship** libère l'ancienne position sur la grille
5. **Ship** occupe la nouvelle position
6. **ShipAnimator** reçoit la cible avec `set_target()`
7. **ShipAnimator** calcule la trajectoire d'animation
8. **Turn** réduit le `port_deplacement` du vaisseau
9. **main.py** appelle `update_and_draw()` à chaque frame
10. **Utilisateur** voit l'animation de déplacement

### Gestion des Tours

<!-- [img]: Diagramme d'états montrant le cycle :
JoueurA_Actif ⇄ JoueurA_Action → FinTour → GainRessources → 
JoueurB_Actif ⇄ JoueurB_Action → FinTour → CheckVictoire →
Retour JoueurA_Actif (ou Fin de partie si MotherShip détruite)
-->

**Flux du système de tours :**

```python
# État initial
Turn.players = [Player1, Player2]  # Player1 actif

# Pendant le tour
player = Turn.players[0]  # Joueur actif
# ... actions du joueur ...

# Fin de tour (Entrée pressée)
for ship in Turn.players[0].ships:
    ship.reset_porters()  # Réinitialise déplacement/attaque
    if isinstance(ship, Foreuse):
        # Calcul des gains
        if ship.est_a_cote_planete(grille):
            ship.gain += PLANETES_REWARD
        if ship.est_autour_asteroide(grille):
            ship.gain += ASTEROIDES_REWARD

Turn.players[0].gain()  # Collecte les gains
Turn.next()  # Passe au joueur suivant
HUD.change_turn()  # Met à jour l'interface

# Vérification victoire
for player in Turn.players:
    if not player.getMotherShip() or player.getMotherShip().pv_actuel <= 0:
        # Fin de partie !
        winner = [p for p in Turn.players if p != player][0]
        menuFin.main(ecran, winner, victoire=True)
```

## 📦 Modules Principaux

### Module Core (classes/)

| Fichier | Responsabilité | Dépendances |
|---------|----------------|-------------|
| `Ship.py` | Logique des vaisseaux | Point, Economie |
| `MotherShip.py` | Vaisseau-mère | Ship |
| `Player.py` | Gestion joueur | Economie, Ship |
| `Map.py` | Génération carte | Point, ResourceManager |
| `Turn.py` | Système de tours | Player |
| `Economie.py` | Système économique | - |
| `Shop.py` | Boutique | Player, Economie |

### Module Animation (classes/)

| Fichier | Responsabilité | Parent |
|---------|----------------|--------|
| `Animator.py` | Système de base | - |
| `ShipAnimator.py` | Animation vaisseaux | Animator |
| `PlanetAnimator.py` | Animation planètes | Animator |
| `ProjectileAnimator.py` | Animation projectiles | Animator |

### Module Interface (classes/HUD + menu/)

| Fichier | Responsabilité |
|---------|----------------|
| `HUD.py` | Interface en jeu |
| `BarDisplay.py` | Barres de statut |
| `TurnDisplay.py` | Affichage du tour |
| `FloatingText.py` | Textes animés |
| `menuPrincipal.py` | Menu principal |
| `menuJouer.py` | Personnalisation |

## 🔧 Systèmes Transversaux

### 1. Système de Coordonnées

Le jeu utilise **deux systèmes de coordonnées** :

#### Coordonnées Grille (logique)
```python
# (ligne, colonne) - pour la logique
position = Point(x=5, y=10)  # ligne 5, colonne 10
```

#### Coordonnées Écran (pixels)
```python
# Conversion grille → écran
pixel_x = colonne * TAILLE_CASE + OFFSET_X
pixel_y = ligne * TAILLE_CASE
```

**⚠️ Attention :** Les coordonnées sont parfois inversées selon le contexte !

### 2. Système de Collision

La détection de collision vérifie plusieurs critères :

```python
def verifier_collision(self, grille, ligne, colonne, direction):
    largeur, hauteur = self.donner_dimensions(direction)
    
    # Vérification limites
    if ligne < 0 or colonne < 0:
        return False
    
    # Vérification obstacles
    types_bloquants = [Type.PLANETE, Type.ASTEROIDE, 
                       Type.BASE, Type.VAISSEAU]
    for l in range(ligne, ligne + hauteur):
        for c in range(colonne, colonne + largeur):
            if grille[l][c].type in types_bloquants:
                return False
    
    return True
```

### 3. Pathfinding (A*)

Le déplacement utilise l'algorithme A* avec coût variable selon le terrain :

```python
cout_case = {
    Type.VIDE: 1,        # Déplacement normal
    Type.ATMOSPHERE: 2   # Déplacement ralenti
}
```

**Optimisations :**
- Limitation à la portée du vaisseau (`max_portee`)
- Heuristique de Manhattan
- Cache des positions visitées

### 4. Gestion Mémoire des Animations

Les animations sont gérées par des listes de classe pour éviter les fuites mémoire :

```python
@classmethod
def update_all(cls):
    for animation in getattr(cls, "liste_animation", []):
        animation.update_and_draw()

@classmethod
def clear_list(cls):
    if hasattr(cls, "liste_animation"):
        cls.liste_animation.clear()
```

**Usage :**
```python
# Nettoyage en fin de partie
ShipAnimator.clear_list()
PlanetAnimator.clear_list()
```

## ⚙️ Configuration (blazyck.py)

Le fichier `blazyck.py` centralise toutes les constantes :

```python
# Dimensions écran
SCREEN_WIDTH = info.current_w
SCREEN_HEIGHT = info.current_h

# Grille
NB_CASE_X = 50
NB_CASE_Y = 30
TAILLE_CASE = (SCREEN_HEIGHT - BAR_HEIGHT) // NB_CASE_Y

# Gameplay
PLANETES_REWARD = 150
ASTEROIDES_REWARD = 100
POURCENT_DEATH_REWARD = 0.6
```

**Avantages :**
- Modification facile des valeurs
- Pas de magic numbers
- Import unique : `from blazyck import *`

## 🎨 Pipeline de Rendu

Le rendu suit un ordre strict pour gérer la superposition :

```python
def draw_game(ecran, ...):
    # 1. Fond spatial
    stars.update()
    stars.draw(ecran)
    
    # 2. Grille et terrain
    map_obj.generer_grille(ecran)
    
    # 3. Astéroïdes statiques
    for (ax, ay), img in map_obj.asteroide_img_map.items():
        ecran.blit(img, ...)
    
    # 4. Prévisualisations (transparentes)
    if selection_ship:
        selection_ship.prevision.update_and_draw()
    
    # 5. Entités animées
    Animator.update_all()
    PlanetAnimator.update_all()
    ShipAnimator.update_all()
    ProjectileAnimator.update_all()
    
    # 6. Textes flottants
    FloatingText.update_and_draw_all(ecran, dt)
    
    # 7. Interface (HUD + Shop)
    HUD.update_and_draw()
    shop.draw()
    
    # 8. Curseur (toujours au-dessus)
    ecran.blit(new_cursor, position_souris)
```

## 🧪 Points d'Extension

### Ajouter un Nouveau Type de Vaisseau

1. **Définir les stats** dans `menu/modifShips.py` :
```python
SHIP_STATS["NouveauVaisseau"] = {
    "pv_max": 500,
    "attaque": 100,
    # ...
}
```

2. **Créer la classe** dans `classes/Ship.py` :
```python
class NouveauVaisseau(Ship):
    def __init__(self, cordonner, id, ...):
        stats = SHIP_STATS["NouveauVaisseau"]
        super().__init__(...)
```

3. **Ajouter les assets** dans `assets/img/ships/nouveauvaisseau/`

4. **Mettre à jour le Shop** dans `classes/Shop.py`

### Ajouter un Nouveau Type de Terrain

1. **Ajouter l'enum** dans `classes/Point.py` :
```python
class Type(Enum):
    NOUVEAU_TYPE = 6
```

2. **Définir le comportement** dans `classes/Ship.py` :
```python
cout_case = {
    Type.VIDE: 1,
    Type.ATMOSPHERE: 2,
    Type.NOUVEAU_TYPE: 3  # Plus lent
}
```

3. **Ajouter la génération** dans `classes/Map.py`

## 🔍 Debugging et Tests

### Affichage de Debug

Le jeu inclut des modes de visualisation :

```python
# Afficher la grille (LCTRL)
afficher_grille = True

# Afficher les zones (LSHIFT maintenu)
afficher_zones = keys[pygame.K_LSHIFT]

# Couleurs de debug
colors = {
    Type.VIDE: (0, 0, 0, 0),
    Type.PLANETE: (255, 215, 0, 128),
    Type.VAISSEAU: (255, 0, 0, 128),
}
```

### Tests Unitaires des Classes

Plusieurs fichiers incluent des `if __name__ == "__main__":` pour tester isolément :

```python
# classes/Point.py
if __name__ == "__main__":
    A = Point(1, 2, Type.VIDE)
    print(A)  # (1, 2, VIDE)
```

### Fichiers de Test Dédiés

- `classes/Test_Animator/planets.py` - Test animations planètes
- `classes/Test_Animator/projectiles.py` - Test projectiles
- `mainshop.py` - Test du système de boutique

## 📈 Performance

### Optimisations Implémentées

1. **Préchargement des ressources** (ResourceManager)
   - Toutes les images sont chargées au démarrage
   - Évite les IO pendant le jeu

2. **Cache des chemins A***
   - Les positions visitées sont mémorisées
   - Évite les recalculs

3. **Clipping de zone**
   - Seules les zones visibles sont dessinées
   ```python
   ecran.set_clip(zone_scroll)
   # ... dessiner ...
   ecran.set_clip(None)
   ```

4. **Update conditionnel**
   - Les animations hors écran ne sont pas mises à jour

### Métriques Typiques

- **FPS cible** : 60 (main loop) / 30 (menus)
- **Temps de chargement** : ~2-5s (50 planètes)
- **Mémoire** : ~200-300 MB (avec assets)

## 🔗 Liens Utiles

- [Classes Principales →](../core-classes/ship.md)
- [Système de Tours →](../game-systems/turn-system.md)
- [Système d'Animation →](../animation/animator.md)

---

**Prochaine étape** : Explorez les [Classes Principales](../core-classes/ship.md) pour comprendre la logique métier.