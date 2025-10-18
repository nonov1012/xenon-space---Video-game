# 🛰️ Documentation — `Ship.py`

## Sommaire
- [Description générale](#description-générale)
- [Structure et responsabilités principales](#structure-et-responsabilités-principales)
- [Méthodes principales](#méthodes-principales)
  - [Déplacement](#déplacement)
  - [Attaque et combat](#attaque-et-combat)
  - [Minage et environnement](#minage-et-environnement)
  - [Rotation et aperçu](#rotation-et-aperçu)
  - [Interactions avec la grille](#interactions-avec-la-grille)
- [Sous-classes spécialisées](#sous-classes-spécialisées)
- [Méthodes spécifiques à `Transport`](#méthodes-spécifiques-à-transport)
- [Notes techniques](#notes-techniques)
- [Résumé fonctionnel](#résumé-fonctionnel)

---

## 🧭 Description générale

Le fichier `Ship.py` définit la classe de base **`Ship`**, qui représente un **vaisseau spatial générique** dans le jeu.  
Elle gère :
- la logique de jeu (déplacement, attaque, destruction, minage, transport) ;
- la représentation visuelle et animée (`ShipAnimator`) ;
- les interactions avec la grille de jeu (`grille` composée de `Point`, `Type`).

Les sous-classes (`Petit`, `Moyen`, `Lourd`, `Foreuse`, `Transport`) spécialisent certains comportements selon leur rôle.

---

## ⚙️ Structure et responsabilités principales

### Attributs principaux

| Attribut | Type | Description |
|-----------|------|-------------|
| `pv_max`, `pv_actuel` | int | Points de vie maximum et actuels |
| `attaque` | int | Dégâts infligés |
| `port_attaque`, `port_attaque_max` | int | Portée d’attaque actuelle et maximale |
| `port_deplacement`, `port_deplacement_max` | int | Portée de déplacement actuelle et maximale |
| `cout` | int | Coût d’achat / production |
| `taille` | (int, int) | Largeur et hauteur sur la grille |
| `peut_miner`, `peut_transporter` | bool | Capacités spéciales |
| `coordonnees` | Point | Position sur la grille |
| `direction` | str | Orientation (`haut`, `bas`, `gauche`, `droite`) |
| `animator`, `prevision` | ShipAnimator | Gestion des animations |
| `cargaison` | list[Ship] | Slots de transport |
| `projectile_type` | str | Type de projectile utilisé |

---

## 🚀 Méthodes principales

### 🔹 Déplacement

#### `a_star(start, end)`
Implémente l’algorithme **A\*** pour calculer un chemin optimal entre deux positions, en tenant compte des obstacles et du coût des cases.

#### `positions_possibles_adjacentes()`
Recherche en **largeur (BFS : (parcours en largeur))** les positions atteignables dans la limite de `port_deplacement`.

#### `deplacement(case_cible, grille, ships)`
Exécute le mouvement réel du vaisseau :  
attaque si un ennemi est présent, sinon déplace le vaisseau sur la grille et met à jour son orientation.

---

### 🔹 Attaque et combat

#### `attaquer(cible)`
Effectue une attaque :
- inflige des dégâts (`subir_degats`),
- joue une animation de tir,
- affiche un texte de dégâts,
- accorde une récompense si la cible est détruite.

#### `subir_degats(degats)`
Applique les dégâts, met à jour les points de vie et déclenche les animations correspondantes.

#### `est_mort()`
Renvoie `True` si le vaisseau est détruit.

---

### 🔹 Minage et environnement

#### `peut_miner_asteroide(grille, x, y)`
Vérifie si le vaisseau peut miner un astéroïde ou une planete.

#### `miner_asteroide(grille, x, y)`
Exécute l’action de minage : supprime l’astéroïde et ajoute les ressources.

#### `est_autour_asteroide()` / `est_a_cote_planete()`
Détecte si le vaisseau est proche d’un élément particulier.

---

### 🔹 Rotation et aperçu

#### `rotation_aperçu(grille)`
Fait pivoter l’aperçu du vaisseau de 90° si la place le permet.

#### `rotation_aperçu_si_possible(case_souris, grille)`
Met à jour la position de l’aperçu et tente une rotation valide.

---

### 🔹 Interactions avec la grille

#### `occuper_plateau(grille, nouveau_type)`
Marque les cases du plateau occupées par le vaisseau.

#### `verifier_collision()`
Vérifie qu’aucune collision ne se produira lors d’un mouvement.

#### `liberer_position()`
Libère les cases précédemment occupées.

---

## 🛠️ Sous-classes spécialisées

| Classe | Description | Particularités |
|---------|--------------|----------------|
| `Petit` | Vaisseau léger et rapide | Grande mobilité, faible PV |
| `Moyen` | Vaisseau équilibré | Bon compromis attaque/vitesse |
| `Lourd` | Vaisseau blindé | Puissant mais lent |
| `Foreuse` | Spécialisé dans le minage | Aucun tir, portée d’attaque = 0 |
| `Transport` | Transporte d’autres vaisseaux | Capacité de cargaison (3 slots) |

---

## ⚓ Méthodes spécifiques à `Transport`

#### `ajouter_cargo(ship, grille)`
Embarque un vaisseau adjacent, le retire de la grille et le rend invisible.

#### `retirer_cargo(index, ligne, colonne, grille, ships)`
Débarque un vaisseau stocké à une position valide.

#### `positions_debarquement(ship_stocke, grille)`
Liste des positions disponibles autour du transporteur pour débarquer un vaisseau.

---

## 🧠 Notes techniques

- L’algorithme de déplacement combine **A\*** et **BFS**.  
- Les coordonnées `(ligne, colonne)` sont converties en pixels via `TAILLE_CASE` et `OFFSET_X`.  
- Le système d’animation (`ShipAnimator`) gère position, rotation et transitions.  
- Les rotations conservent le centre du vaisseau via `_centre_depuis_coin()` et `_coin_depuis_centre()`.

---

## 📘 Résumé fonctionnel

| Catégorie | Méthodes | Rôle |
|------------|-----------|------|
| **Déplacement** | `a_star`, `positions_possibles_adjacentes`, `deplacement` | Calcul et exécution du mouvement |
| **Combat** | `attaquer`, `subir_degats`, `est_mort` | Gestion des attaques et dégâts |
| **Minage** | `peut_miner_asteroide`, `miner_asteroide` | Interaction avec les astéroïdes |
| **Interface** | `rotation_aperçu`, `rotation_aperçu_si_possible` | Gestion des rotations et prévisualisation |
| **Transport** | `ajouter_cargo`, `retirer_cargo`, `positions_debarquement` | Gestion de la cargaison |
| **Grille** | `occuper_plateau`, `liberer_position`, `verifier_collision` | Occupation et collisions |

