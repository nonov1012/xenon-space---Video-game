# Xenon Space – Documentation technique  

## Introduction  
Version 1 de la documentation technique  

### Informations sur le jeu  
- Le jeu se nomme **Xenon Space**. C’est un jeu de **base contre base au tour par tour**.  
- L’univers du jeu se déroule dans l’espace, où deux factions s’affrontent pour le contrôle des dernières ressources.  
- Le jeu a été créé dans le cadre d’un **projet scolaire**.  

---

## Architecture du projet  

### Dossier *classes*  
Le dossier **classes** contient toutes les classes du projet. Les plus importantes parmi elles sont :  

#### Ship.py  
Le fichier `Ship.py` contient la classe **Ship**, qui est la classe mère de tous les vaisseaux. Elle regroupe les méthodes principales pour :  
- le déplacement,  
- l’attaque,  
- la destruction des vaisseaux,  
- la rotation.  

Elle contient également toutes les sous-classes de **Ship**, à l’exception de **Mothership** (car cette dernière est une classe trop volumineuse pour être intégrée ici).  

Les sous-classes de **Ship** sont :  
- **Petit** : définit les données du vaisseau de combat de petite taille,  
- **Moyen** : définit les informations du vaisseau de taille moyenne,  
- **Lourd** : définit les caractéristiques du vaisseau de combat lourd,  
- **Foreuse** : contient les méthodes permettant de miner des planètes afin de générer des ressources (mais il ne peut pas attaquer),  
- **Transport** : peut transporter soit 3 vaisseaux de petite taille, soit 1 vaisseau moyen et 1 vaisseau petit.  

---

#### Point.py  
Le fichier `Point.py` contient deux classes : **Type** et **Point**.  

- La classe **Type** définit les différents types de cases de la carte :  
  
        VIDE = 0
        PLANETE = 1
        ATMOSPHERE = 2
        ASTEROIDE = 3
        BASE = 4
        VAISSEAU = 5

- La classe **Point** utilise **Type** pour stocker :  
- les coordonnées **x, y**,  
- ainsi que le type de la case correspondante.  

---

#### Map.py  
Le fichier `Map.py` contient la classe **Map**, qui permet de stocker et de générer la carte du jeu en utilisant la classe **Point**. Elle gère également plusieurs fonctionnalités :  

- **Création des planètes** :  
Utilise la méthode `generer_planet` pour générer une planète aléatoirement.  
- `peut_placer` vérifie que l’endroit choisi est valide.  
- `placer_planete` crée effectivement la planète.  

- **Création des astéroïdes** :  
Utilise la méthode `generer_asteroides` pour créer un astéroïde.  
- `placer_asteroide` se charge de l’ajouter à la carte.  

- **Création de la grille** :  
La méthode `generer_grille` crée toute la grille et initialise chaque case avec le type **VIDE**.  
Ensuite, `generer_planet` et `generer_asteroides` remplissent la carte.  

- **Pré-création des vaisseaux mères** :  
Lors de la génération initiale, la carte réserve deux zones (en **haut à gauche** et en **bas à droite**) pour éviter qu’une planète ou un astéroïde ne s’y génère.  



# à continer la documentation

MotherShip.py
Player.py
Economie.py



* #### dossier assets
* #### les fichier dans les document principale