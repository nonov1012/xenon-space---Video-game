<div align="center">

# 🚀 Xenon Space 🌌

### ⚔️ Jeu de Stratégie Spatiale au Tour par Tour ⚔️

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pygame](https://img.shields.io/badge/Pygame-2.0+-00599C?style=for-the-badge&logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-Academic-green?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Completed-success?style=for-the-badge)

[🎮 Installation](#-installation) • [📖 Comment Jouer](#-comment-jouer) • [🏆 Succès](#-succès) • [👥 Équipe](#-développeurs) • [📄 Documentation](https://nonov1012.github.io/xenon-space---Video-game/)

---

</div>

## 📝 Description

**Xenon Space** est un jeu de stratégie spatiale tactique au tour par tour développé en Python avec Pygame. Affrontez un adversaire (humain ou IA) dans des batailles spatiales épiques où vous devrez gérer votre flotte, collecter des ressources et détruire la base ennemie pour remporter la victoire !

<div align="center">

### ✨ Caractéristiques Principales ✨

</div>

<table>
<tr>
<td width="50%">

🎯 **Gameplay Tactique**
- Système de combat au tour par tour
- Positionnement stratégique sur grille
- Gestion de ressources et économie

🤖 **Intelligence Artificielle**
- IA avancée avec comportements variés
- Pathfinding A* intelligent
- Difficulté adaptative

</td>
<td width="50%">

🎨 **Graphismes & Interface**
- Animations fluides et immersives
- Interface holographique futuriste
- Effets visuels de particules

🌍 **Contenu de Jeu**
- 5 types de vaisseaux uniques
- Génération procédurale de cartes
- Système de succès à débloquer

</td>
</tr>
</table>

---

## 💻 Installation

### 📋 Prérequis

<table>
<tr>
<td>

```bash
🐍 Python 3.8+
```

</td>
<td>

```bash
🎮 Pygame
```

</td>
</tr>
</table>

### ⚙️ Installation des Dépendances

```bash
# Installer Pygame
pip install -r requirements.txt
```

### 🎯 Lancement du Jeu

<table>
<tr>
<td width="50%">

**🚀 Lancement avec python**
```bash
python run_game.py
```

</td>
<td width="50%">

**✨ Lancer l'executable**
```bash
./Xenon-Space
```

</td>
</tr>
</table>

---

## 📖 Comment Jouer

<div align="center">

### 🎯 Objectif

**Détruire le MotherShip (base spatiale) adverse tout en protégeant le vôtre !**

</div>

### ⌨️ Contrôles

<table>
<tr>
<td width="50%">

#### 🖱️ **Souris**

| Action | Bouton |
|--------|--------|
| Sélectionner / Déplacer | 🖱️ Clic gauche |
| Attaquer / Embarquer | 🖱️ Clic droit |
| Acheter (Shop) | 🖱️ Clic gauche |

</td>
<td width="50%">

#### ⌨️ **Clavier**

| Action | Touche |
|--------|--------|
| Menu Pause | `Échap` |
| Grille ON/OFF | `G` |
| Rotation vaisseau | `R` |
| Terminer le tour | `Entrée` |
| Afficher zones | `Z` (maintenir) |

</td>
</tr>
</table>

---

## 🏆 Succès

<div align="center">

### 🎖️ Débloquez les 5 Succès du Jeu ! 🎖️

</div>

<table>
<tr>
<td align="center" width="20%">

🏅
**Victoire Suprême**

Remportez votre première victoire

</td>
<td align="center" width="20%">

🌌
**Explorateur Cosmique**

Parcourez chaque recoin de la galaxie

</td>
<td align="center" width="20%">

🚀
**Maître de Flotte**

Pilotez tous les types de vaisseaux

</td>
<td align="center" width="20%">

🏰
**Architecte Stellaire**

Base au niveau maximum

</td>
<td align="center" width="20%">

⚔️
**Chasseur d'Élite**

Éliminez 10 ennemis

</td>
</tr>
</table>

---

## 📁 Structure du Projet

```
📦 xenon-space/
├── 🚀 main.py                    # Point d'entrée principal
├── ⏳ loading_run.py              # Écran de chargement
├── 📚 classes/                    # Classes du jeu
│   ├── 🚢 Ship.py                # Vaisseaux
│   ├── 🏰 MotherShip.py          # Base spatiale
│   ├── 👤 Player.py              # Joueurs
│   ├── 🗺️ Map.py                 # Génération carte
│   ├── 🛒 Shop.py                # Boutique
│   ├── 💰 Economie.py            # Système économique
│   ├── 🎨 Animator.py            # Animations
│   ├── 📊 HUD/                   # Interface
│   └── ⚙️ ...
├── 🤖 IA/                         # Intelligences artificielles
│   ├── 🧠 AI.py                  # IA de base
│   ├── 🏰 MotherShipAI.py        # IA base
│   ├── 🛡️ IA_Lourd.py            # IA vaisseau lourd
│   ├── ⛏️ foreuse.py             # IA foreuse
│   └── 🚚 IATransport.py         # IA transport
├── 📱 menu/                       # Menus
│   ├── 🏠 menuPrincipal.py       # Menu principal
│   ├── 🎮 menuJouer.py           # Sélection mode
│   ├── ⏸️ menuPause.py           # Pause
│   ├── 🏁 menuFin.py             # Fin de partie
│   └── 🏆 succes.json            # Succès
└── 🎨 assets/                     # Ressources
    ├── 🖼️ img/                   # Images & sprites
    ├── 🔊 sounds/                # Sons & musiques
    └── 🔤 fonts/                 # Polices
```

---

## 🛠️ Technologies Utilisées

<div align="center">

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pygame](https://img.shields.io/badge/Pygame-00599C?style=for-the-badge&logo=python&logoColor=white)
![Discord](https://img.shields.io/badge/Discord_RPC-5865F2?style=for-the-badge&logo=discord&logoColor=white)
![JSON](https://img.shields.io/badge/JSON-000000?style=for-the-badge&logo=json&logoColor=white)

</div>

<table>
<tr>
<td width="50%">

### 🎮 Core Technologies
- **Python 3** : Langage principal
- **Pygame** : Moteur graphique
- **JSON** : Stockage données

</td>
<td width="50%">

### ✨ Features Avancées
- **Discord Rich Presence** : Intégration Discord
- **A* Pathfinding** : IA intelligente
- **Génération Procédurale** : Cartes uniques

</td>
</tr>
</table>

---

## 🌟 Fonctionnalités Avancées

<table>
<tr>
<td width="33%" align="center">

### 🎬 Animations
- Animations fluides
- Système de particules
- Effets de projectiles
- Texte flottant

</td>
<td width="33%" align="center">

### 🧠 Intelligence
- Pathfinding A*
- IA comportementale
- Stratégies variées
- Décisions tactiques

</td>
<td width="33%" align="center">

### ⚙️ Système
- Sauvegarde paramètres
- Résolution adaptative
- Rich Presence Discord
- Multi-résolution

</td>
</tr>
</table>

---

## 👥 Développeurs

<div align="center">

### 🎮 L'Équipe Xenon Space

<table>
<tr>
<td align="center">
<a href="https://github.com/NockXu">
<img src="https://github.com/NockXu.png" width="100px;" alt="Gabriel DAVID"/><br />
<sub><b>Gabriel DAVID</b></sub>
</a>
</td>
<td align="center">
<a href="https://github.com/nonov1012">
<img src="https://github.com/nonov1012.png" width="100px;" alt="Noa VOITURIER"/><br />
<sub><b>Noa VOITURIER</b></sub>
</a>
</td>
<td align="center">
<a href="https://github.com/Reclea">
<img src="https://github.com/Reclea.png" width="100px;" alt="Clément NOËL"/><br />
<sub><b>Clément NOËL</b></sub>
</a>
</td>
<td align="center">
<a href="https://github.com/GitLovox">
<img src="https://github.com/GitLovox.png" width="100px;" alt="Ugo CAVEL"/><br />
<sub><b>Ugo CAVEL</b></sub>
</a>
</td>
<td align="center">
<a href="https://github.com/brian62100">
<img src="https://github.com/brian62100.png" width="100px;" alt="Brian DUPUIS"/><br />
<sub><b>Brian DUPUIS</b></sub>
</a>
</td>
<td align="center">
<a href="https://github.com/tomvanhove2">
<img src="https://github.com/tomvanhove2.png" width="100px;" alt="Tom VANHOVE"/><br />
<sub><b>Tom VANHOVE</b></sub>
</a>
</td>
</tr>
</table>

</div>

---

## 🙏 Remerciements

<div align="center">

Un grand merci à **[Deep-Fold](https://deep-fold.itch.io/pixel-planet-generator)** pour le générateur de planètes pixel art !

🌟 **Merci à tous les testeurs et contributeurs !** 🌟

</div>

---

## 📜 Licence & Copyright

<div align="center">

**Copyright © 2025 - Équipe Xenon Space**

*Tous droits réservés*

Projet réalisé dans le cadre d'un projet académique à l'IUT

⚠️ Merci de ne pas reproduire ou modifier le code sans autorisation

---

### 🎮 Prêt pour la conquête spatiale ? 🚀

<table>
<tr>
<td align="center">

**Que la meilleure stratégie gagne !**
</td>
</tr>
</table>

</div>
