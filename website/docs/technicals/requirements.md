# Requirements

Avant de vous lancer dans *Xenon-Space*, assurez-vous que votre environnement est correctement configuré.  
Cette page détaille les outils et bibliothèques nécessaires au bon fonctionnement du jeu. 🚀

---

## Environnement

| Élément | Description |
|----------|--------------|
| 🐍 **Langage** | [Python ≥ 3.11.2](https://www.python.org/downloads/) *(version recommandée)* |
| 💻 **OS supportés** | Windows · Linux · macOS |
| 📦 **Gestionnaire de paquets** | [pip](https://pip.pypa.io/en/stable/installation) |

> 🔗 *Cliquez sur les liens pour télécharger les versions adaptées à votre système.*

---

## 📁 Installation des dépendances

Les bibliothèques nécessaires sont listées dans le fichier `requirements.txt` inclus dans le projet.  
Installez-les en utilisant la commande adaptée à votre système :

### Windows & MacOS

```bash
pip install -r requirements.txt
```

### Linux

```bash
sudo apt update
sudo apt install python3-pygame python3-pil python3-numpy
```

:::info[*Vous pouvez également exécuter*]

```bash
pip install -r requirements.txt
```

*sur Linux si votre environnement Python est déjà configuré.*
:::

---

## 🧩 Bibliothèques Python requises

| Bibliothèque | Version minimale | Rôle |
|---------------|------------------|------|
| 🎮 **pygame** | ≥ 2.0 | Gestion des graphismes, du son et des événements du jeu. |
| 🖼️ **Pillow** | ≥ 8.0 | Manipulation et traitement d’images (sprites, textures, etc.). |
| 💬 **pypresence** | ≥ 4.2.0 | Intégration de la Rich Presence Discord. |
| 🔢 **numpy** | ≥ 1.26.4 | Calculs numériques et gestion des tableaux pour la logique du jeu. |

---

:::info[*Vérification de l’installation*]

```bash
python -m main
```

*Si le jeu s’ouvre, tout est prêt ! 🎉*
:::
