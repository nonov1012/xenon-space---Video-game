# 🚀 Documentation technique – Xenon Space

## 📝 Introduction

Cette documentation technique décrit **Xenon Space**, un jeu de stratégie **tour par tour**, où deux factions s'affrontent pour le contrôle de ressources spatiales limitées. Le jeu a été développé dans le cadre d'un **projet scolaire**.

---

## 🛠️ Architecture du projet

Le projet est organisé en plusieurs dossiers et fichiers, chacun ayant un rôle bien défini. L'architecture est principalement basée sur des classes pour structurer les différentes fonctionnalités du jeu.

### 📁 Dossier *`classes`*

Ce dossier contient toutes les classes du projet, qui gèrent les mécaniques de jeu principales.

#### `Ship.py`
Le fichier `Ship.py` définit la classe **`Ship`**, la classe mère de tous les vaisseaux. Elle regroupe les méthodes fondamentales pour :
- **Déplacement**
  
  le déplacement fonctionne grace a trois fonction principale:
  
  * **a_star** : Trouver le chemin le plus court et le moins coûteux entre la position actuelle du vaisseau et une position cible sur la grille.
  * **positions_possibles_adjacentes** : Déterminer toutes les positions accessibles par le vaisseau selon sa portée de déplacement
  * **deplacement**  : Gérer le déplacement réel du vaisseau sur la grille

- **Attaque**

  le Attaque fonctionne grace a deux fonction principale:

  * **deplacement** : Gérer l'attaque du vaisseau si clique sur un vaisseau ennemie lance attaquer
  * **attaquer** : Gérer les dégàts infigeur mais aussi lancer l'ainimation d'attaque et l'appel de la fonction pour crée un projectile


- **Destruction**

  le déplacement fonctionne grace a trois fonction principale:

  * **est_mort** : verifie si le vaisseau et mort
  * **deplacement** : si le vaisseau et mort il le supprime de la grille


- **Rotation**

  le déplacement fonctionne grace a trois fonction principale:

  * **rotation_aperçu** : il prevois la rotation
  * **rotation_aperçu_si_possible** : il verifie qu'on peut tourner

Ce fichier contient également la majorité des sous-classes de `Ship`, à l'exception de **`Mothership`**.

Les sous-classes de `Ship` sont :
- **`Petit`** : Vaisseau de combat de petite taille.
- **`Moyen`** : Vaisseau de combat de taille moyenne.
- **`Lourd`** : Vaisseau de combat lourd.
- **`Foreuse`** : Vaisseau non-combattant, utilisé pour miner des planètes et générer des ressources. Il est incapable d'attaquer.
- **`Transport`** : Vaisseau capable de transporter d'autres vaisseaux (soit trois `Petit`, soit un `Moyen` et un `Petit`).

---

#### `MotherShip.py`
Le fichier `MotherShip.py` définit la classe **`MotherShip`**, une classe fille de **`Ship`**. Elle gère les fonctionnalités spécifiques aux bases de chaque joueur, incluant leur **animation** et leurs **attaques**.

---

#### `Point.py`
Le fichier `Point.py` contient deux classes : **`Type`** et **`Point`**.
- La classe **`Type`** est une énumération qui définit les différents types de cases sur la carte : `VIDE`, `PLANETE`, `ATMOSPHERE`, `ASTEROIDE`, `BASE`, `VAISSEAU`.
- La classe **`Point`** utilise cette énumération pour stocker les **coordonnées (x, y)** et le **type** de chaque case de la carte.

---

#### `Map.py`
Le fichier `Map.py` contient la classe **`Map`**, qui gère la création et le stockage de la carte de jeu en utilisant la classe **`Point`**. Ses fonctionnalités principales incluent :
- **Création des planètes** : Utilise les méthodes `generer_planet`, `peut_placer` et `placer_planete`.
- **Création des astéroïdes** : Utilise les méthodes `generer_asteroides` et `placer_asteroide`.
- **Génération de la grille** : La méthode `generer_grille` initialise la carte avec des cases de type `VIDE` avant de la peupler de planètes et d'astéroïdes.
- **Réservation de zones** : Au début de la génération, la carte réserve deux zones (en haut à gauche et en bas à droite) pour empêcher la génération d'obstacles à l'emplacement des bases.

---

#### `Player.py`
Le fichier `Player.py` contient la classe **`Player`**, qui gère les aspects liés aux joueurs. Elle permet notamment de :
- Gérer l'argent du joueur via les méthodes `buy` (pour retirer de l'argent) et `gain` (pour en ajouter), en s'appuyant sur la classe **`Economie`**.
- Attribuer chaque vaisseau au joueur correspondant.

---

#### `Economie.py`
Ce fichier contient la classe **`Economie`**, qui gère la monnaie du jeu. Elle dispose de quatre fonctions :
- **`ajouter`** : Ajoute une somme d'argent.
- **`retirer`** : Retire une somme d'argent.
- **`peut_payer`** : Vérifie si le joueur possède suffisamment de fonds.
- **`etat`** : Renvoie le solde actuel du joueur.

---

#### `Animator`
Les fichiers dont le nom contient le mot **`Animator`** gèrent les animations du jeu pour les vaisseaux, les planètes et les projectiles. Ils contiennent tout le code nécessaire pour la lecture des différentes séquences d'animation.

---

#### `Shop.py`
Le fichier `Shop.py` gère la boutique du jeu. La classe **`Shop`** permet aux joueurs d'acheter de nouveaux vaisseaux.

---

#### `Turn.py`
La classe **`Turn`** est responsable de la gestion du déroulement des tours pendant la partie, s'assurant que chaque joueur joue à son tour.

---

### 📁 Dossier *`assets`*

Le dossier **`assets`** contient l'ensemble des ressources multimédia du jeu, comme les images et les sons. Il est organisé de la manière suivante :

- Le dossier `img` contient les images et les animations. Il est subdivisé en plusieurs sous-dossiers thématiques :
    - `asteroides`
    - `menu`
    - `planets`
    - `projectiles`
    - `ships`
        - Le dossier `ships` contient un sous-dossier pour chaque type de vaisseau. Chaque sous-dossier de vaisseau est organisé comme suit :
            - `base.png` : Image du vaisseau au repos.
            - `destruction.png` : Séquence d'images pour l'animation de destruction.
            - `engine.png` : Séquence d'images pour l'animation de déplacement ou au repos.
            - `shield.png` : Séquence d'images pour l'animation de prise de dégâts.
            - `weapons.png` : Séquence d'images pour l'animation d'attaque.

---

### ⚠️ Problème de la Foreuse

Le vaisseau `Foreuse` est une exception et n'a pas d'animation d'attaque. Pour éviter que le programme ne plante si ce vaisseau est amené à attaquer, sa portée d'attaque doit être impérativement fixée à **`0`**. Cela l'empêche d'exécuter l'animation manquante.

---

## 📄 Les fichiers principaux

### main.py
le main.py permet le fonctionnement du programme entier permetant de lancer le jeu


### blazyck.py
blazyck.py contient toute les variable qu'on puisse les modifier pourpouvoir tester le jeu sans avoir besoin d'allez dans les différent programme