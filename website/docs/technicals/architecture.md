# 🏗️ Architecture logicielle

## Vue d’ensemble

Le jeu **Xenon Space** repose sur une architecture orientée objets, où chaque composant du jeu
(vaisseau, carte, joueur, économie, etc.) est représenté par une classe Python.

Le projet est organisé de manière modulaire, avec une architecture basée sur des classes pour structurer les différentes fonctionnalités du jeu. Les principaux composants se trouvent dans les dossiers `classes` et `assets`, ainsi que dans plusieurs fichiers à la racine.

## Composants principaux

| Composant | Rôle |
|------------|------|
| Ship | Classe mère des vaisseaux |
| Mothership | Base principale du joueur |
| Map | Génère et gère la carte |
| Player | Gère les données et actions du joueur |
| Turn | Gère le déroulement des tours |
| Economie | Gère les ressources financières d'un joueur |
| Shop | Interface d’achat des vaisseaux |

### Diagramme simplifié

*A faire*

## 📁 Structure du projet

Le projet est organisé de manière modulaire, avec deux dossiers principaux : `classes` et `assets`, ainsi que des fichiers racine.

### `Ship.py`

Le fichier `Ship.py` définit la classe mère **`Ship`**, qui sert de base à tous les vaisseaux du jeu. Elle inclut des méthodes pour gérer les actions fondamentales des vaisseaux :

* **Déplacement** :
  * **`a_star(start, end)`** : Utilise l'algorithme A* pour trouver le chemin le plus court et le moins coûteux entre la position actuelle du vaisseau (`start`) et la position cible (`end`) sur la grille de jeu.
  * **`positions_possibles_adjacentes(position)`** : Détermine toutes les cases accessibles par le vaisseau depuis une `position` donnée, en tenant compte de sa portée de déplacement.
  * **`deplacement()`** : Exécute le déplacement réel du vaisseau sur la grille en suivant le chemin calculé.
* **Attaque** :
  * **`attaquer(cible)`** : Gère l'attaque du vaisseau sur une cible ennemie. Cette méthode calcule les dégâts infligés, lance l'animation d'attaque et appelle la fonction pour créer un projectile.
* **Destruction** :
  * **`est_mort()`** : Une méthode de vérification qui renvoie `True` si les points de vie du vaisseau sont inférieurs ou égaux à zéro.
  * **`supprimer()`** : Si le vaisseau est `mort`, cette fonction le retire de la grille de jeu et le supprime de la liste des vaisseaux actifs.
* **Rotation** :
  * **`rotation_aperçu(direction)`** : Prépare l'aperçu visuel de la rotation du vaisseau dans une `direction` spécifique.
  * **`rotation_aperçu_si_possible()`** : Vérifie si le vaisseau peut pivoter vers une direction donnée.

Ce fichier regroupe également la majorité des classes filles de `Ship`, à l'exception de `Mothership` :

* **`Petit`** : Vaisseau de combat léger, rapide et maniable.
* **`Moyen`** : Vaisseau de combat de taille moyenne, plus résistant et puissant.
* **`Lourd`** : Vaisseau de combat lourd, avec une armure et une puissance de feu supérieures.
* **`Foreuse`** : Vaisseau non-combattant, spécialisé dans la récolte de ressources. Sa portée d'attaque doit être fixée à `0` pour éviter les erreurs.
* **`Transport`** : Vaisseau utilitaire capable de transporter d'autres vaisseaux (soit trois `Petit`, soit un `Moyen` et un `Petit`).

---

### `MotherShip.py`

Ce fichier définit la classe **`Mothership`**, une classe fille de `Ship`. Le `Mothership` représente la base principale de chaque joueur et est un élément central du gameplay. En plus des fonctionnalités de base héritées de `Ship`, cette classe gère des logiques spécifiques :

* **Rôle de base** : Il sert de point de départ pour la création de nouveaux vaisseaux et est l'objectif principal de l'ennemi. Sa destruction entraîne la défaite du joueur.
* **Attaques de base** : Bien que dérivé de `Ship`, le `Mothership` possède des capacités d'attaque uniques, généralement plus puissantes que celles des vaisseaux standards.
* **Animations spécifiques** : Étant une entité unique, il dispose de ses propres animations pour l'attaque, les dégâts et la destruction, distinctes de celles des autres vaisseaux.

---

### `Point.py`

Ce fichier contient deux classes fondamentales pour la représentation de la carte :

* **`Type`** : Une énumération (`Enum`) qui définit les différents types de cases sur la carte, tels que `VIDE`, `PLANETE`, `ASTEROIDE`, `BASE` et `VAISSEAU`.
* **`Point`** : Une classe qui stocke les **coordonnées (x, y)** et le **type** de chaque case de la grille de jeu.

---

### `Map.py`

Le fichier `Map.py` contient la classe **`Map`**, qui est responsable de la création, du stockage et de la gestion de la carte de jeu. Ses principales fonctionnalités incluent :

* **`generer_grille()`** : Initialise la carte avec des cases de type `VIDE`.
* **`generer_planet()`**, **`peut_placer(x, y, taille)`**, et **`placer_planete(x, y)`** : Ces méthodes travaillent ensemble pour générer et placer des planètes de manière aléatoire sur la carte, tout en s'assurant qu'elles ne se chevauchent pas ou ne bloquent pas les zones de départ.
* **`generer_asteroides()`** et **`placer_asteroide()`** : Gèrent la génération et le placement des champs d'astéroïdes.
* **Réservation de zones** : Au début de la génération, deux zones sont réservées (en haut à gauche et en bas à droite) pour garantir que les bases des joueurs ne sont pas entravées par des obstacles.

---

### `Player.py`

La classe **`Player`** gère tous les aspects liés à un joueur. Elle inclut :

* La gestion de la monnaie du joueur à travers les méthodes **`buy(montant)`** et **`gain(montant)`**, qui interagissent avec la classe `Economie`.
* Le lien entre chaque vaisseau et son joueur propriétaire.

---

### `Economie.py`

Ce fichier contient la classe **`Economie`**, qui gère la monnaie du jeu. Elle dispose de plusieurs fonctions :

* **`ajouter(montant)`** : Ajoute un `montant` d'argent au solde du joueur.
* **`retirer(montant)`** : Retire un `montant` d'argent du solde.
* **`peut_payer(montant)`** : Une fonction de vérification qui renvoie `True` si le joueur possède suffisamment de fonds pour effectuer un achat.
* **`etat()`** : Renvoie le solde actuel du joueur.

---

### `Shop.py`

Le fichier `Shop.py` définit la classe **`Shop`**, qui gère la boutique du jeu. Cette classe est l'interface par laquelle les joueurs peuvent étendre leur flotte. Ses responsabilités principales sont :

* **Catalogue de vaisseaux** : Elle contient la liste des types de vaisseaux disponibles à l'achat, avec leurs coûts associés.
* **Gestion des transactions** : Lorsque le joueur sélectionne un vaisseau, le `Shop` vérifie, en utilisant la classe `Economie`, si le joueur a les fonds nécessaires.
* **Création de vaisseaux** : Une fois la transaction validée, le `Shop` instancie le nouveau vaisseau et l'assigne au joueur correspondant, le préparant à être placé sur la carte.

---

### `Turn.py`

La classe **`Turn`** est un gestionnaire d'état crucial pour le déroulement du jeu. Elle est responsable de la gestion du déroulement des tours pendant la partie, s'assurant que chaque joueur joue à son tour. Ses fonctions clés incluent :

* **Suivi du joueur actif** : Elle garde en mémoire l'identité du joueur dont c'est le tour de jeu.
* **Passage de tour** : Une méthode principale permet de passer le tour au joueur suivant une fois le tour du joueur actuel terminé.
* **Déclenchement d'événements** : Elle peut être responsable du déclenchement d'événements de fin de tour (par exemple, la génération de ressources) ou de début de tour.

---

### Fichiers `*Animator.py`

Contrairement à un seul fichier, cette mention désigne un ensemble de fichiers (comme `ShipAnimator.py`, `ProjectileAnimator.py`, etc.) qui sont spécifiquement conçus pour gérer les animations des différents éléments du jeu. Leur rôle est essentiel pour le rendu visuel et le dynamisme du jeu :

* **Lecture de séquences d'images** : Chaque animateur est programmé pour lire et afficher les séquences d'images (sprites) stockées dans le dossier `assets/img`.
* **Gestion des états d'animation** : Ils gèrent les différentes animations de chaque objet (par exemple, l'animation de déplacement, d'attaque, de destruction) et s'assurent que la bonne animation est jouée au bon moment.
* **Synchronisation** : Ils synchronisent les animations avec les actions des objets (un vaisseau qui se déplace, un projectile qui vole, une explosion) pour un rendu fluide et réaliste.

---

### 📁 Dossier *`assets`*

Le dossier **`assets`** centralise toutes les ressources multimédia utilisées dans le jeu. Il est organisé de manière thématique pour faciliter la gestion.

* `img` : Contient toutes les images et les animations.
  * `asteroides`
  * `menu`
  * `planets`
  * `projectiles`
  * `ships` : Chaque sous-dossier de vaisseau est structuré comme suit :
    * **`base.png`** : Image statique du vaisseau.
    * **`destruction.png`** : Séquence d'images pour l'animation de destruction.
    * **`engine.png`** : Séquence d'images pour l'animation de déplacement et au repos.
    * **`shield.png`** : Séquence d'images pour l'animation de prise de dégâts.
    * **`weapons.png`** : Séquence d'images pour l'animation d'attaque.

---

### 📄 Fichiers principaux

#### `main.py`

Le fichier `main.py` est le point d'entrée du programme. C'est lui qui lance l'application et initialise la boucle de jeu principale.

#### `blazyck.py`

Ce fichier agit comme un **fichier de configuration central**. Il contient l'ensemble des variables et paramètres modifiables, ce qui permet de tester et d'ajuster le jeu sans avoir à modifier directement le code des différentes classes.
