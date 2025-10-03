## Requirements

### Environnement

- **Langage** : [Python](https://www.python.org/downloads/) (version 3.11.2 ou supérieure recommandée)  
- **OS supportés** : Windows, Linux, macOS  
- **Gestionnaire de paquets** : [pip](https://pip.pypa.io/en/stable/installation/)

_Texte cliquable pour télécharger les bonnes versions_

### Bibliothèques Python nécessaires

Ces dépendances doivent être installées à l’aide du fichier `requirements.txt` fourni, via la commande :  

sur windows:

```bash
pip install -r requirements.txt
```

sur linux:

```bash
sudo apt update
sudo apt install python3-pygame python3-pil python3-numpy
```

### Liste des bibliothèques

- `pygame >= 2.0`
Gestion des graphismes, des événements et du son pour le jeu.

- `Pillow >= 8.0`
Manipulation et traitement d’images (pour l'animation des sprites).

- `pypresence >= 4.2.0`
Intégration de la présence riche Discord (Rich Presence).

- `numpy >= 1.26.4`
Calculs numériques et manipulation de matrices/tableaux pour les éléments du jeu.
