# `Shop`

La classe `Shop` gère la **boutique de vaisseaux** dans Xenon Space. Elle fournit une interface graphique interactive permettant aux joueurs d'acheter des vaisseaux et d'améliorer leur base pendant la partie.

:::tip Principe de conception
Cette classe suit le principe de **séparation des préoccupations** : elle gère à la fois la logique métier (transactions) et l'affichage (interface graphique), tout en déléguant la gestion financière à la classe `Economie`.
:::

---

## 📋 Vue d'ensemble

```python
import pygame
from blazyck import *

class Shop:
    def __init__(self, player, font, screen):
        self.player = player
        self.font = font
        self.screen = screen
        self.base_level = 1
```

**Rôle principal :** Gérer l'achat de vaisseaux et l'amélioration de la base du joueur via une interface graphique.

**Dépendances :**
- [`Player`](./Player.md) - Propriétaire de la boutique
- [`Economie`](./Economie.md) - Gestion des transactions
- [`pygame`](https://www.pygame.org/) - Rendu graphique
- [`blazyck`](../3-constantes.md) - Constantes d'interface

---

## 🏗️ Constructeur

```python
def __init__(self, player, font, screen):
```

### Paramètres

| Paramètre | Type | Description |
|-----------|------|-------------|
| `player` | [`Player`](./Player.md) | Joueur propriétaire de la boutique |
| `font` | `pygame.font.Font` | Police pour le texte des boutons |
| `screen` | `pygame.Surface` | Surface d'affichage du jeu |

### Attributs initialisés

| Attribut | Type | Valeur initiale | Description |
|----------|------|-----------------|-------------|
| `self.player` | `Player` | Paramètre | Référence au joueur |
| `self.font` | `Font` | Paramètre | Police de texte |
| `self.screen` | `Surface` | Paramètre | Surface de rendu |
| `self.base_level` | `int` | `1` | Niveau actuel de la base |
| `self.base_image` | `Surface` | Chargée | Image de la base |
| `self.ships` | `list[dict]` | Catalogue | Liste des vaisseaux disponibles |
| `self.base_upgrades` | `list[dict]` | Upgrades | Liste des améliorations de base |

---

## 📦 Catalogue de vaisseaux

### Structure du catalogue

```python
self.ships = [
    {"name": "Petit", "price": 325, "image": self.load_image("assets/img/ships/shop/petit.png")},
    {"name": "Moyen", "price": 650, "image": self.load_image("assets/img/ships/shop/moyen.png")},
    {"name": "Grand", "price": 1050, "image": self.load_image("assets/img/ships/shop/grand.png")},
    {"name": "Foreuse", "price": 400, "image": self.load_image("assets/img/ships/shop/foreuse.png")},
    {"name": "Transporteur", "price": 500, "image": self.load_image("assets/img/ships/shop/transporteur.png")}
]
```

### Format d'un vaisseau

| Clé | Type | Description |
|-----|------|-------------|
| `name` | `str` | Nom du vaisseau (identifiant) |
| `price` | `int` | Coût en monnaie (₿) |
| `image` | `pygame.Surface` | Image de prévisualisation |

### Tableau des vaisseaux

| Vaisseau | Prix | Rôle |
|----------|------|------|
| 🏃 **Petit** | 325₿ | Vaisseau léger, rapide |
| ⚖️ **Moyen** | 650₿ | Vaisseau équilibré |
| 🛡️ **Grand** | 1050₿ | Vaisseau lourd, résistant |
| ⛏️ **Foreuse** | 400₿ | Minage de ressources |
| 🚚 **Transporteur** | 500₿ | Transport de vaisseaux |

---

## 🏰 Système d'amélioration de base

### Structure des upgrades

```python
self.base_upgrades = [
    {"level": 2, "price": 1000},
    {"level": 3, "price": 2000},
    {"level": 4, "price": 6000}
]
```

### Tableau de progression

| Niveau | PV | Gain/tour | Coût upgrade | ROI (tours) |
|--------|----|-----------|--------------:|------------:|
| **1** | 500 | 300₿ | — | — |
| **2** | 700 | 400₿ | 1000₿ | 10 |
| **3** | 1200 | 500₿ | 2000₿ | 20 |
| **4** | 1600 | 600₿ | 6000₿ | 60 |

:::info Calcul ROI
ROI = Coût ÷ (Nouveau gain - Ancien gain)

Exemple Nv1→2 : 1000₿ ÷ (400-300) = **10 tours** pour rentabiliser
:::

---

## 🖼️ Chargement des ressources

### `load_image`

Charge et redimensionne une image, avec gestion des erreurs.

```python
def load_image(self, path, size=(ICON_SIZE, ICON_SIZE)):
    try:
        img = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(img, size)
    except pygame.error:
        placeholder = pygame.Surface(size, pygame.SRCALPHA)
        placeholder.fill((150, 150, 150))
        return placeholder
```

#### Paramètres

| Paramètre | Type | Valeur par défaut | Description |
|-----------|------|-------------------|-------------|
| `path` | `str` | — | Chemin vers l'image |
| `size` | `tuple[int, int]` | `(ICON_SIZE, ICON_SIZE)` | Dimensions finales |

#### Retour

| Type | Description |
|------|-------------|
| `pygame.Surface` | Image chargée et redimensionnée, ou placeholder gris en cas d'erreur |

#### Comportement

```mermaid
graph TD
    A[load_image] --> B{Fichier existe?}
    B -->|Oui| C[Charger image]
    B -->|Non| D[Créer placeholder gris]
    C --> E[Redimensionner]
    E --> F[Retourner Surface]
    D --> F
    
    style F fill:#00C864
```

:::tip Robustesse
Le placeholder gris **garantit** que le jeu ne crash pas même si des images sont manquantes.
:::

---

## 💰 Gestion des transactions

### `buy_ship`

Tente d'acheter un vaisseau et retourne son nom en cas de succès.

```python
def buy_ship(self, ship):
    """Achète un vaisseau et retourne son nom si l'achat réussit"""
    if self.player.economie.retirer(ship["price"]):
        return ship["name"]
    else:
        return None
```

#### Paramètres

| Paramètre | Type | Description |
|-----------|------|-------------|
| `ship` | `dict` | Dictionnaire du vaisseau (doit contenir `"name"` et `"price"`) |

#### Retour

| Type | Valeur | Condition |
|------|--------|-----------|
| `str` | Nom du vaisseau | Achat réussi |
| `None` | — | Fonds insuffisants |

#### Séquence d'achat

```mermaid
sequenceDiagram
    participant S as Shop
    participant P as Player
    participant E as Economie
    
    S->>P: Demande achat (ship)
    P->>E: retirer(ship["price"])
    
    alt Fonds suffisants
        E->>E: solde -= price
        E->>P: True
        P->>S: ship["name"]
        Note over S: Retourner "Petit"
    else Fonds insuffisants
        E->>P: False
        P->>S: None
        Note over S: Achat échoué
    end
```

#### Exemple d'utilisation

```python
shop = Shop(player, font, screen)

# Tentative d'achat
ship_data = {"name": "Moyen", "price": 650}
result = shop.buy_ship(ship_data)

if result:
    print(f"✅ Achat de {result} réussi !")
else:
    print("❌ Fonds insuffisants")
```

:::info Délégation
La méthode **délègue** la vérification financière à `Economie.retirer()`, respectant l'encapsulation.
:::

---

### `upgrade_base`

Améliore la base du joueur si possible.

```python
def upgrade_base(self):
    """Améliore la base si possible"""
    if self.base_level >= 4:
        return False
    
    # Trouve le prix de l'amélioration suivante
    next_upgrade = self.base_upgrades[self.base_level - 1]
    
    if self.player.economie.retirer(next_upgrade["price"]):
        self.base_level = next_upgrade["level"]
        return True
    else:
        return False
```

#### Retour

| Type | Valeur | Condition |
|------|--------|-----------|
| `bool` | `True` | Amélioration réussie |
| `bool` | `False` | Niveau max atteint ou fonds insuffisants |

#### Comportement

```mermaid
graph TD
    A[upgrade_base] --> B{base_level >= 4?}
    B -->|Oui| C[return False]
    B -->|Non| D[Trouver prix upgrade]
    D --> E{Retrait réussi?}
    E -->|Oui| F[base_level++]
    E -->|Non| G[return False]
    F --> H[return True]
    
    style H fill:#00C864
    style C fill:#FF6B6B
    style G fill:#FF6B6B
```

#### Exemples

```python
shop = Shop(player, font, screen)

# Niveau 1, solde = 1200₿
shop.upgrade_base()  # True, niveau = 2, solde = 200₿

# Niveau 2, solde = 200₿
shop.upgrade_base()  # False (fonds insuffisants)

# Niveau 4 (max)
shop.upgrade_base()  # False (niveau max)
```

---

## 🎨 Affichage graphique

### `get_base_color_filter`

Retourne la couleur de bordure selon le niveau de base.

```python
def get_base_color_filter(self):
    """Retourne la couleur de bordure selon le niveau de base"""
    if self.base_level == 1:
        return (80, 150, 200)  # Bleu
    elif self.base_level == 2:
        return (150, 100, 200)  # Violet
    elif self.base_level == 3:
        return (200, 150, 50)  # Or
    else:  # Niveau 4
        return (50, 200, 150)  # Turquoise
```

#### Palette de couleurs

| Niveau | Couleur | RGB | Signification |
|--------|---------|-----|---------------|
| **1** | 🔵 Bleu | `(80, 150, 200)` | Niveau de base |
| **2** | 🟣 Violet | `(150, 100, 200)` | Première amélioration |
| **3** | 🟡 Or | `(200, 150, 50)` | Deuxième amélioration |
| **4** | 🟢 Turquoise | `(50, 200, 150)` | Niveau maximum |

---

### `draw`

Dessine l'interface complète du shop sur l'écran.

```python
def draw(self):
```

Cette méthode est **complexe** et se décompose en plusieurs étapes :

#### 1. Fond du shop

```python
shop_y = self.screen.get_height() - BAR_HEIGHT
shop_width = self.screen.get_width()

# Fond avec dégradé
shop_bg = pygame.Surface((shop_width, BAR_HEIGHT), pygame.SRCALPHA)
for i in range(BAR_HEIGHT):
    alpha = int(200 - (i / BAR_HEIGHT) * 50)
    color = (20 + i // 5, 25 + i // 5, 35 + i // 5, alpha)
    pygame.draw.line(shop_bg, color, (0, i), (shop_width, i))
self.screen.blit(shop_bg, (0, shop_y))
```

**Effet visuel :** Dégradé vertical semi-transparent (alpha 200→150).

---

#### 2. Bordures décoratives

```python
# Bordure supérieure
pygame.draw.line(self.screen, (100, 150, 200), (0, shop_y), (shop_width, shop_y), 3)
pygame.draw.line(self.screen, (150, 200, 255), (0, shop_y + 1), (shop_width, shop_y + 1), 1)

# Coins décoratifs
corner_size = 20
pygame.draw.line(self.screen, (150, 200, 255), (0, shop_y), (corner_size, shop_y), 4)
pygame.draw.line(self.screen, (150, 200, 255), (0, shop_y), (0, shop_y + corner_size), 4)
```

**Effet visuel :** Lignes cyan lumineuses pour un style futuriste.

---

#### 3. Calcul de la disposition

```python
num_ships = len(self.ships)
total_width = num_ships * (ICON_SIZE + 2 * CASE_PADDING) + (num_ships - 1) * ICON_MARGIN
start_x = (self.screen.get_width() - total_width) // 2
y = self.screen.get_height() - BAR_HEIGHT + (BAR_HEIGHT - ICON_SIZE) // 2
```

**Résultat :** Les icônes sont **centrées horizontalement** avec espacement régulier.

```
┌─────────────────────────────────────────────┐
│                                             │
├─────────────────────────────────────────────┤ ← shop_y
│    [Petit] [Moyen] [Grand] [Foreuse] [Tr]  │ ← Centré
│              ↑                               │
│          start_x                            │
└─────────────────────────────────────────────┘
```

---

#### 4. Dessin des vaisseaux

Pour chaque vaisseau :

```python
for i, ship in enumerate(self.ships):
    x = start_x + i * (ICON_SIZE + 2 * CASE_PADDING + ICON_MARGIN)
    case_rect = pygame.Rect(x, y, ICON_SIZE + 2 * CASE_PADDING, ICON_SIZE + 2 * CASE_PADDING)
    
    hovered = case_rect.collidepoint(mouse_pos)
```

**a. Effet d'ombre**

```python
shadow_rect = case_rect.copy()
shadow_rect.x += 3
shadow_rect.y += 3
pygame.draw.rect(self.screen, (20, 20, 20), shadow_rect, border_radius=8)
```

**b. Fond avec hover**

```python
color = (60, 60, 80) if not hovered else (90, 90, 120)
pygame.draw.rect(self.screen, color, case_rect, border_radius=8)
```

**c. Bordure animée**

```python
border_color = (100, 100, 140) if not hovered else (150, 200, 255)
pygame.draw.rect(self.screen, border_color, case_rect, border_radius=8, width=2)
```

**d. Icône avec glow au survol**

```python
icon_size = ICON_SIZE + 8 if hovered else ICON_SIZE
icon_img = pygame.transform.scale(ship["image"], (icon_size, icon_size))
icon_x = x + CASE_PADDING + (ICON_SIZE - icon_size) // 2
icon_y = y + CASE_PADDING + (ICON_SIZE - icon_size) // 2

if hovered:
    glow_surface = pygame.Surface((icon_size + 8, icon_size + 8), pygame.SRCALPHA)
    pygame.draw.circle(glow_surface, (255, 255, 255, 30), 
                     (icon_size // 2 + 4, icon_size // 2 + 4), icon_size // 2 + 4)
    self.screen.blit(glow_surface, (icon_x - 4, icon_y - 4))

self.screen.blit(icon_img, (icon_x, icon_y))
```

**e. Tooltip au survol**

```python
if hovered:
    info_bg = pygame.Surface((250, 30), pygame.SRCALPHA)
    pygame.draw.rect(info_bg, (0, 0, 0, 200), info_bg.get_rect(), border_radius=6)
    pygame.draw.rect(info_bg, (255, 215, 0), info_bg.get_rect(), border_radius=6, width=2)
    
    info_text = self.font.render(f"{ship['name']} - {ship['price']} coins", True, (255, 255, 100))
    text_rect = info_text.get_rect(center=(125, 15))
    info_bg.blit(info_text, text_rect)
    
    bg_rect = info_bg.get_rect(center=(case_rect.centerx, case_rect.top - 20))
    self.screen.blit(info_bg, bg_rect)
```

---

#### 5. Dessin de la base (amélioration)

```python
base_x = start_x + total_width + ICON_MARGIN * 3
case_rect = pygame.Rect(base_x, y, ICON_SIZE + 2 * CASE_PADDING, ICON_SIZE + 2 * CASE_PADDING)
hovered = case_rect.collidepoint(mouse_pos)
```

**a. Effet arc-en-ciel (niveau max)**

```python
if self.base_level >= 4:
    gradient_colors = [(255, 215, 0), (255, 140, 0), (255, 69, 0)]
    for i, col in enumerate(gradient_colors):
        offset = i * 2
        inner_rect = case_rect.inflate(-offset, -offset)
        pygame.draw.rect(self.screen, col, inner_rect, border_radius=8, width=2)
```

**b. Bordure selon niveau**

```python
border_color = self.get_base_color_filter() if self.base_level < 4 else (255, 215, 0)
if hovered:
    border_color = tuple(min(c + 50, 255) for c in border_color)
pygame.draw.rect(self.screen, border_color, case_rect, border_radius=8, width=3)
```

**c. Indicateurs de niveau**

```python
star_color = (255, 255, 100) if self.base_level < 4 else (255, 215, 0)
star_positions = [
    (icon_x + icon_size * 0.2, icon_y + icon_size * 0.2),
    (icon_x + icon_size * 0.8, icon_y + icon_size * 0.2),
    (icon_x + icon_size * 0.2, icon_y + icon_size * 0.8),
    (icon_x + icon_size * 0.8, icon_y + icon_size * 0.8)
]

for i in range(min(self.base_level, 4)):
    star_x, star_y = star_positions[i]
    pygame.draw.circle(self.screen, star_color, (int(star_x), int(star_y)), 4)
    pygame.draw.circle(self.screen, (255, 255, 255), (int(star_x), int(star_y)), 2)
```

**Disposition des étoiles :**

```
Niveau 1:     Niveau 2:     Niveau 3:     Niveau 4:
⭐ .          ⭐ ⭐          ⭐ ⭐          ⭐ ⭐
. .          . .          ⭐ .          ⭐ ⭐
```

---

## 🎮 Gestion des clics

### `handle_click`

Détecte les clics et effectue l'action correspondante.

```python
def handle_click(self, pos):
    """Gère les clics sur les boutons du shop et retourne le type de vaisseau acheté ou 'base_upgrade'"""
    # Vérifier clic sur amélioration de base
    if hasattr(self, 'base_rect') and self.base_rect.collidepoint(pos):
        if self.upgrade_base():
            return "base_upgrade"
        return None
    
    # Vérifier clic sur vaisseaux
    for ship in self.ships:
        if "rect" in ship and ship["rect"].collidepoint(pos):
            return self.buy_ship(ship)
    
    return None
```

#### Paramètres

| Paramètre | Type | Description |
|-----------|------|-------------|
| `pos` | `tuple[int, int]` | Position du clic `(x, y)` |

#### Retour

| Type | Valeur | Signification |
|------|--------|---------------|
| `str` | Nom vaisseau | Achat de vaisseau réussi |
| `str` | `"base_upgrade"` | Amélioration de base réussie |
| `None` | — | Aucun achat (clic hors zone ou fonds insuffisants) |

#### Flux de détection

```mermaid
graph TD
    A[handle_click] --> B{Clic sur base?}
    B -->|Oui| C[upgrade_base]
    B -->|Non| D{Clic sur vaisseau?}
    
    C --> E{Succès?}
    E -->|Oui| F[return 'base_upgrade']
    E -->|Non| G[return None]
    
    D -->|Oui| H[buy_ship]
    D -->|Non| G
    
    H --> I{Succès?}
    I -->|Oui| J[return nom_vaisseau]
    I -->|Non| G
    
    style F fill:#00C864
    style J fill:#00C864
    style G fill:#FFB86C
```

---

## 🎯 Intégration dans le jeu

### Initialisation dans `main.py`

```python
from classes.Shop import Shop
from classes.Player import Player

# Création des joueurs
player1 = Player("Alice", solde_initial=500)
player2 = Player("Bob", solde_initial=500)

# Création des shops
font = pygame.font.Font("assets/fonts/SpaceNova.otf", 22)
shop1 = Shop(player1, font, screen)
shop2 = Shop(player2, font, screen)
```

---

### Boucle de jeu

```python
while running:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Déterminer le shop actif selon le joueur
            shop = shop1 if Turn.players[0].id == 0 else shop2
            
            # Gérer le clic
            type_action = shop.handle_click(event.pos)
            
            if type_action:
                joueur_actuel = Turn.players[0]
                
                # Achat de vaisseau
                if type_action in ["Petit", "Moyen", "Grand", "Foreuse", "Transporteur"]:
                    position = trouver_position_libre_base(map_obj, joueur_actuel.id)
                    
                    if position:
                        nouveau_vaisseau = creer_vaisseau_achete(
                            type_action, position, next_uid[0],
                            joueur_actuel.id, images, paths
                        )
                        if nouveau_vaisseau:
                            next_uid[0] += 1
                            joueur_actuel.ships.append(nouveau_vaisseau)
                            nouveau_vaisseau.occuper_plateau(map_obj.grille, Type.VAISSEAU)
                    else:
                        # Rembourser si pas de place
                        for ship_data in shop.ships:
                            if ship_data["name"] == type_action:
                                joueur_actuel.economie.ajouter(ship_data["price"])
                
                # Amélioration de base
                elif type_action == "base_upgrade":
                    mothership = joueur_actuel.getMotherShip()
                    mothership.apply_level(mothership.tier + 1)
    
    # Affichage
    shop.draw()
```

---

## 📊 Diagramme de séquence complet

### Achat de vaisseau avec placement

```mermaid
sequenceDiagram
    participant U as Utilisateur
    participant M as Main Loop
    participant S as Shop
    participant P as Player
    participant E as Economie
    participant Map as Map
    
    U->>M: Clic sur vaisseau
    M->>S: handle_click(pos)
    S->>S: Identifier vaisseau
    S->>S: buy_ship(ship)
    S->>P: economie.retirer(price)
    P->>E: retirer(price)
    
    alt Fonds suffisants
        E->>E: solde -= price
        E->>P: True
        P->>S: True
        S->>M: "Petit"
        M->>M: trouver_position_libre_base()
        
        alt Position trouvée
            M->>M: creer_vaisseau_achete()
            M->>P: ships.append(vaisseau)
            M->>Map: occuper_plateau()
            Note over U: ✅ Vaisseau créé
        else Aucune position
            M->>E: ajouter(price)
            Note over U: ⚠️ Remboursé
        end
    else Fonds insuffisants
        E->>P: False
        P->>S: False
        S->>M: None
        Note over U: ❌ Achat échoué
    end
```

---

## 🎨 Effets visuels

### États des boutons

<div className="row">
  <div className="col col--6">
    <div className="card">
      <div className="card__header">
        <h4>Normal</h4>
      </div>
      <div className="card__body">
        <ul>
          <li>Fond : <code>(60, 60, 80)</code></li>
          <li>Bordure : <code>(100, 100, 140)</code></li>
          <li>Icône : Taille normale (50px)</li>
          <li>Ombre : Visible</li>
        </ul>
      </div>
    </div>
  </div>
  
  <div className="col col--6">
    <div className="card">
      <div className="card__header">
        <h4>Survol (Hover)</h4>
      </div>
      <div className="card__body">
        <ul>
          <li>Fond : <code>(90, 90, 120)</code></li>
          <li>Bordure : <code>(150, 200, 255)</code></li>
          <li>Icône : Agrandie (58px)</li>
          <li>Glow : Halo blanc semi-transparent</li>
          <li>Tooltip : Nom + Prix</li>
        </ul>
      </div>
    </div>
  </div>
</div>

---

### Animation de la base

**Niveau < 4 :**
- Bordure de couleur selon niveau
- Hover : Éclaircissement +50

**Niveau 4 (max) :**
- Triple bordure dégradée (Or → Orange → Rouge-Orange)
- Étoiles dorées
- Effet arc-en-ciel

---

## 🧪 Tests et validation

### Test des achats

```python
import unittest
from classes.Shop import Shop
from classes.Player import Player

class TestShop(unittest.TestCase):
    def setUp(self):
        self.player = Player("Test", solde_initial=1000)
        self.shop = Shop(self.player, None, None)
    
    def test_buy_ship_success(self):
        ship = {"name": "Petit", "price": 325}
        result = self.shop.buy_ship(ship)
        
        self.assertEqual(result, "Petit")
        self.assertEqual(self.player.economie.solde, 675)
    
    def test_buy_ship_insufficient(self):
        ship = {"name": "Grand", "price": 1050}
        result = self.shop.buy_ship(ship)
        
        self.assertIsNone(result)
        self.assertEqual(self.player.economie.solde, 1000)
    
    def test_upgrade_base_success(self):
        result = self.shop.upgrade_base()
        
        self.assertTrue(result)
        self.assertEqual(self.shop.base_level, 2)
        self.assertEqual(self.player.economie.solde, 0)
    
    def test_upgrade_base_max_level(self):
        self.shop.base_level = 4
        result = self.shop.upgrade_base()
        
        self.assertFalse(result)
        self.assertEqual(self.shop.base_level, 4)
```

---

## 🔍 Cas limites

### 1. Achat avec solde exact

```python
player = Player("Alice", solde_initial=325)
shop = Shop(player, font, screen)

ship = {"name": "Petit", "price": 325}
result = shop.buy_ship(ship)

# ✅ Succès
assert result == "Petit"
assert player.economie.solde == 0
```

---

### 2. Amélioration au niveau max

```python
shop.base_level = 4

result = shop.upgrade_base()

# ❌ Refus
```python
assert result == False
assert shop.base_level == 4  # Inchangé
```

---

### 3. Images manquantes

```python
# Si assets/img/ships/shop/petit.png n'existe pas
shop = Shop(player, font, screen)

# load_image crée automatiquement un placeholder gris
assert shop.ships[0]["image"] is not None
assert shop.ships[0]["image"].get_size() == (50, 50)
```

:::tip Gestion d'erreur
Le jeu **ne crash jamais** même si toutes les images sont absentes grâce aux placeholders.
:::

---

### 4. Clics hors zone

```python
# Clic en dehors du shop
result = shop.handle_click((0, 0))

assert result is None  # Aucune action
```

---

### 5. Amélioration sans fonds

```python
player = Player("Bob", solde_initial=500)
shop = Shop(player, font, screen)

# Niveau 1 → 2 coûte 1000₿
result = shop.upgrade_base()

# ❌ Échec
assert result == False
assert shop.base_level == 1  # Inchangé
assert player.economie.solde == 500  # Non débité
```

---

## 🎯 Optimisations possibles

### 1. Cache des rectangles

**Problème actuel :** Les rectangles (`ship["rect"]`) sont recalculés à chaque frame dans `draw()`.

**Solution :**

```python
class Shop:
    def __init__(self, player, font, screen):
        # ... init existant ...
        self._rects_cached = False
        self._ship_rects = []
        self._base_rect = None
    
    def _cache_rects(self):
        """Calcule et met en cache les rectangles une seule fois"""
        if self._rects_cached:
            return
        
        num_ships = len(self.ships)
        total_width = num_ships * (ICON_SIZE + 2 * CASE_PADDING) + (num_ships - 1) * ICON_MARGIN
        start_x = (self.screen.get_width() - total_width) // 2
        y = self.screen.get_height() - BAR_HEIGHT + (BAR_HEIGHT - ICON_SIZE) // 2
        
        for i, ship in enumerate(self.ships):
            x = start_x + i * (ICON_SIZE + 2 * CASE_PADDING + ICON_MARGIN)
            ship["rect"] = pygame.Rect(x, y, ICON_SIZE + 2 * CASE_PADDING, ICON_SIZE + 2 * CASE_PADDING)
        
        base_x = start_x + total_width + ICON_MARGIN * 3
        self._base_rect = pygame.Rect(base_x, y, ICON_SIZE + 2 * CASE_PADDING, ICON_SIZE + 2 * CASE_PADDING)
        self.base_rect = self._base_rect
        
        self._rects_cached = True
    
    def draw(self):
        self._cache_rects()  # Calculer une seule fois
        # ... reste du code ...
```

**Gain :** Évite ~6 calculs de rectangles par frame (60 FPS = 360 calculs/seconde).

---

### 2. Sprite batching

**Problème actuel :** Chaque icône est dessinée individuellement avec plusieurs `blit()`.

**Solution :**

```python
def draw(self):
    # Créer une surface temporaire pour tout le shop
    shop_surface = pygame.Surface((shop_width, BAR_HEIGHT), pygame.SRCALPHA)
    
    # Dessiner tout sur shop_surface
    # ...
    
    # Un seul blit final
    self.screen.blit(shop_surface, (0, shop_y))
```

**Gain :** Réduit les appels `blit()` de ~20 à 1.

---

### 3. Préchargement des tooltips

**Problème actuel :** Les surfaces de tooltip sont recréées à chaque hover.

**Solution :**

```python
class Shop:
    def __init__(self, player, font, screen):
        # ... init existant ...
        self._tooltip_cache = {}
    
    def _get_tooltip(self, ship_name, ship_price):
        key = (ship_name, ship_price)
        
        if key not in self._tooltip_cache:
            info_bg = pygame.Surface((250, 30), pygame.SRCALPHA)
            pygame.draw.rect(info_bg, (0, 0, 0, 200), info_bg.get_rect(), border_radius=6)
            pygame.draw.rect(info_bg, (255, 215, 0), info_bg.get_rect(), border_radius=6, width=2)
            
            info_text = self.font.render(f"{ship_name} - {ship_price} coins", True, (255, 255, 100))
            text_rect = info_text.get_rect(center=(125, 15))
            info_bg.blit(info_text, text_rect)
            
            self._tooltip_cache[key] = info_bg
        
        return self._tooltip_cache[key]
```

---

## 🎨 Variantes de design

### Shop minimaliste

```python
def draw_minimal(self):
    """Version simplifiée sans effets visuels"""
    shop_y = self.screen.get_height() - BAR_HEIGHT
    
    # Fond plat
    pygame.draw.rect(self.screen, (30, 30, 50), 
                    (0, shop_y, self.screen.get_width(), BAR_HEIGHT))
    
    # Icônes simples sans hover
    for i, ship in enumerate(self.ships):
        x = 50 + i * 80
        self.screen.blit(ship["image"], (x, shop_y + 10))
        
        # Prix
        price_text = self.font.render(f"{ship['price']}₿", True, (255, 255, 255))
        self.screen.blit(price_text, (x, shop_y + 65))
```

---

### Shop avec animations

```python
class AnimatedShop(Shop):
    def __init__(self, player, font, screen):
        super().__init__(player, font, screen)
        self._icon_offsets = [0] * len(self.ships)
        self._icon_speeds = [random.uniform(0.5, 1.5) for _ in self.ships]
    
    def update(self, dt):
        """Anime les icônes (à appeler avant draw)"""
        for i in range(len(self.ships)):
            self._icon_offsets[i] += self._icon_speeds[i] * dt
    
    def draw(self):
        # ... code existant ...
        
        # Modifier icon_y pour ajouter un flottement
        for i, ship in enumerate(self.ships):
            offset_y = math.sin(self._icon_offsets[i]) * 3  # ±3px
            icon_y = y + CASE_PADDING + offset_y
            # ... dessiner l'icône ...
```

**Usage :**

```python
# Dans la boucle de jeu
dt = clock.tick(60) / 1000.0  # Delta time en secondes
shop.update(dt)
shop.draw()
```

---

## 🔗 Interactions avec d'autres classes

```mermaid
graph TD
    S[Shop] --> P[Player]
    S --> E[Economie]
    S --> Sc[pygame.Screen]
    S --> F[pygame.Font]
    
    P --> E
    P --> MS[MotherShip]
    P --> Sh[Ship]
    
    M[Main Loop] --> S
    M --> T[Turn]
    M --> Map[Map]
    
    style S fill:#50C8FF
    style P fill:#FFC800
    style E fill:#00C864
```

### Relations clés

| Classe | Relation | Description |
|--------|----------|-------------|
| **Player** | Composition | Shop possède une référence à Player |
| **Economie** | Utilisation | Shop délègue les transactions à Economie |
| **MotherShip** | Modification | Shop déclenche l'amélioration de la base |
| **Main Loop** | Orchestration | Main gère les clics et la création de vaisseaux |
| **Turn** | Contexte | Détermine quel shop est actif |

---

## 📐 Calculs de disposition

### Formules de positionnement

```python
# Largeur totale occupée par N vaisseaux
total_width = N * (ICON_SIZE + 2*CASE_PADDING) + (N-1) * ICON_MARGIN

# Position X de l'icône i (centrage)
start_x = (SCREEN_WIDTH - total_width) / 2
x_i = start_x + i * (ICON_SIZE + 2*CASE_PADDING + ICON_MARGIN)

# Position Y (centrage vertical dans la barre)
y = SCREEN_HEIGHT - BAR_HEIGHT + (BAR_HEIGHT - ICON_SIZE) / 2

# Position de la base (décalée)
base_x = start_x + total_width + ICON_MARGIN * 3
```

### Exemple numérique (1920×1080)

```python
N = 5  # 5 vaisseaux
ICON_SIZE = 50
CASE_PADDING = 8
ICON_MARGIN = 20
BAR_HEIGHT = 85

total_width = 5*(50+16) + 4*20 = 330 + 80 = 410px

start_x = (1920 - 410) / 2 = 755px

# Positions X des icônes
x_0 = 755px
x_1 = 755 + 86 = 841px
x_2 = 841 + 86 = 927px
x_3 = 927 + 86 = 1013px
x_4 = 1013 + 86 = 1099px

# Position de la base
base_x = 755 + 410 + 60 = 1225px

y = 1080 - 85 + (85-50)/2 = 995 + 17.5 = 1012.5px
```

---

## 🎓 Bonnes pratiques

<div className="alert alert--success">
  <h4>✅ Recommandations</h4>
  <ul>
    <li>Toujours appeler <code>draw()</code> <strong>après</strong> le rendu du jeu</li>
    <li>Gérer <code>handle_click()</code> dans la boucle d'événements</li>
    <li>Vérifier le retour de <code>handle_click()</code> pour confirmer l'achat</li>
    <li>Rembourser si le vaisseau ne peut pas être placé</li>
    <li>Utiliser des constantes de <code>blazyck.py</code> pour les dimensions</li>
  </ul>
</div>

<div className="alert alert--danger">
  <h4>❌ À éviter</h4>
  <ul>
    <li>Modifier <code>player.economie.solde</code> directement au lieu de passer par les méthodes</li>
    <li>Oublier de mettre à jour <code>base_level</code> après un upgrade</li>
    <li>Appeler <code>draw()</code> plusieurs fois par frame (coûteux)</li>
    <li>Ne pas gérer le cas où aucune position libre n'est trouvée</li>
    <li>Ignorer les valeurs de retour des méthodes d'achat</li>
  </ul>
</div>

---

## 🐛 Problèmes connus

### 1. Pas de limite de vaisseaux

**Problème :** Un joueur peut acheter autant de vaisseaux qu'il veut, même s'il n'y a plus de place sur la carte.

**Symptôme :** Argent débité mais vaisseau non créé.

**Solution temporaire :** Rembourser si `trouver_position_libre_base()` retourne `None`.

**Solution idéale :**

```python
def buy_ship(self, ship):
    """Achète un vaisseau seulement si une position libre existe"""
    # Vérifier l'espace avant de débiter
    if not self._can_place_ship(ship["name"]):
        return None
    
    if self.player.economie.retirer(ship["price"]):
        return ship["name"]
    return None
```

---

### 2. Shop ne se met pas à jour visuellement

**Problème :** Le niveau de la base affiché ne correspond pas au `MotherShip.tier`.

**Cause :** `shop.base_level` et `mothership.tier` sont désynchronisés.

**Solution :**

```python
def upgrade_base(self):
    """Améliore la base ET met à jour le MotherShip"""
    if self.base_level >= 4:
        return False
    
    next_upgrade = self.base_upgrades[self.base_level - 1]
    
    if self.player.economie.retirer(next_upgrade["price"]):
        self.base_level = next_upgrade["level"]
        
        # Synchroniser avec le MotherShip
        mothership = self.player.getMotherShip()
        if mothership:
            mothership.apply_level(self.base_level)
        
        return True
    return False
```

---

### 3. Collision de clics

**Problème :** Cliquer sur un vaisseau alors qu'un autre élément UI est devant.

**Solution :** Vérifier l'ordre Z (le shop est toujours au premier plan).

```python
# Dans main.py
for event in pygame.event.get():
    if event.type == pygame.MOUSEBUTTONDOWN:
        # 1. Vérifier le shop EN PREMIER
        shop_action = shop.handle_click(event.pos)
        if shop_action:
            # Traiter l'achat
            continue  # Ne pas propager le clic
        
        # 2. Ensuite vérifier les autres éléments
        # ...
```

---

## 📊 Métriques de performance

### Temps de rendu (approximatif)

| Opération | Temps | Pourcentage |
|-----------|-------|-------------|
| Dégradé de fond | ~2ms | 40% |
| Dessin des 5 icônes | ~1.5ms | 30% |
| Effets de survol | ~0.8ms | 16% |
| Bordures décoratives | ~0.5ms | 10% |
| Tooltip | ~0.2ms | 4% |
| **Total** | **~5ms** | **100%** |

:::info Impact
À 60 FPS, le shop utilise **~30% du budget de frame** (16.67ms). Les optimisations suggérées peuvent réduire cela à ~15%.
:::

---

## 🔮 Fonctionnalités futures

### 1. Onglets de catégories

```python
class ShopWithTabs(Shop):
    def __init__(self, player, font, screen):
        super().__init__(player, font, screen)
        self.categories = {
            "Combat": ["Petit", "Moyen", "Grand"],
            "Support": ["Foreuse", "Transporteur"]
        }
        self.active_category = "Combat"
```

---

### 2. Aperçu des statistiques

```python
def draw_ship_stats(self, ship_name):
    """Affiche les stats détaillées au survol"""
    stats = SHIP_STATS[ship_name]
    
    stat_text = [
        f"PV: {stats['pv_max']}",
        f"ATK: {stats['attaque']}",
        f"Portée: {stats['port_attaque']}",
        f"Vitesse: {stats['port_deplacement']}"
    ]
    
    # Dessiner un panneau détaillé
    # ...
```

---

### 3. Raccourcis clavier

```python
SHOP_HOTKEYS = {
    pygame.K_1: "Petit",
    pygame.K_2: "Moyen",
    pygame.K_3: "Grand",
    pygame.K_4: "Foreuse",
    pygame.K_5: "Transporteur",
    pygame.K_b: "base_upgrade"
}

def handle_keypress(self, key):
    """Achat rapide par touche"""
    if key in SHOP_HOTKEYS:
        action = SHOP_HOTKEYS[key]
        if action == "base_upgrade":
            return self.upgrade_base()
        else:
            ship = next((s for s in self.ships if s["name"] == action), None)
            if ship:
                return self.buy_ship(ship)
    return None
```

---

## 📚 Références

- [Classe Player](./Player.md) - Propriétaire du shop
- [Classe Economie](./Economie.md) - Gestion des transactions
- [Constantes blazyck](../3-constantes.md) - Dimensions UI
- [MotherShip](./ship/MotherShip.md) - Amélioration de base
- [Classe Ship](./ship/Ship.md) - Vaisseaux achetables

---

## 💡 Conseils d'intégration

### Pattern recommandé

```python
# === Initialisation (une seule fois) ===
shops = {
    0: Shop(player1, font, screen),
    1: Shop(player2, font, screen)
}

# === Boucle de jeu ===
while running:
    # 1. Événements
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            current_shop = shops[Turn.players[0].id]
            action = current_shop.handle_click(event.pos)
            
            if action:
                process_shop_action(action, Turn.players[0])
    
    # 2. Affichage
    # ... dessiner le jeu ...
    
    # 3. Shop (toujours en dernier pour être au-dessus)
    current_shop = shops[Turn.players[0].id]
    current_shop.draw()
    
    pygame.display.flip()
```