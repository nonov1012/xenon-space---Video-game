---
sidebar_position: 2
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# 💾 Installation

Guide complet pour installer et lancer **Xenon Space** sur votre système.

---

## 📋 Configuration requise

Avant de commencer, vérifiez que votre système respecte les exigences minimales.

### Configuration minimale

<div className="card">
  <div className="card__header">
    <h4>💻 Spécifications minimales</h4>
  </div>
  <div className="card__body">
    <table>
      <tbody>
        <tr>
          <td><strong>Système d'exploitation</strong></td>
          <td>Windows 10/11, macOS 10.14+, Linux (Ubuntu 20.04+)</td>
        </tr>
        <tr>
          <td><strong>Processeur</strong></td>
          <td>Intel Core i3 / AMD Ryzen 3 ou équivalent</td>
        </tr>
        <tr>
          <td><strong>Mémoire vive</strong></td>
          <td>4 Go RAM</td>
        </tr>
        <tr>
          <td><strong>Carte graphique</strong></td>
          <td>Support SDL2 (intégré à Pygame)</td>
        </tr>
        <tr>
          <td><strong>Espace disque</strong></td>
          <td>300 Mo disponibles</td>
        </tr>
        <tr>
          <td><strong>Résolution</strong></td>
          <td>1280×720 minimum</td>
        </tr>
      </tbody>
    </table>
  </div>
</div>

:::info Python requis
Xenon Space nécessite **Python 3.8** ou supérieur pour fonctionner.
:::

---

## 🐍 Installation de Python

Si vous n'avez pas Python installé ou si votre version est obsolète, suivez ces instructions.

<Tabs>
  <TabItem value="windows" label="Windows" default>

### Vérifier la version actuelle

Ouvrez l'invite de commande (CMD) et tapez :

```bash
python --version
```

Si Python n'est pas installé ou si la version est inférieure à 3.8, téléchargez-le.

### Télécharger Python

1. Rendez-vous sur [python.org](https://www.python.org/downloads/)
2. Téléchargez **Python 3.11** ou supérieur pour Windows
3. Lancez l'installateur `.exe`
4. **IMPORTANT :** Cochez **"Add Python to PATH"** lors de l'installation
5. Cliquez sur "Install Now"

### Vérifier l'installation

Redémarrez votre terminal et vérifiez :

```bash
python --version
pip --version
```

Vous devriez voir quelque chose comme :

```
Python 3.11.x
pip 23.x.x from ...
```

  </TabItem>

  <TabItem value="macos" label="macOS">

### Vérifier la version actuelle

Ouvrez le Terminal et tapez :

```bash
python3 --version
```

### Installation manuelle

1. Téléchargez [Python depuis python.org](https://www.python.org/downloads/macos/)
2. Ouvrez le fichier `.pkg`
3. Suivez l'assistant d'installation

### Vérifier l'installation

```bash
python3 --version
pip3 --version
```

:::info Note
Sur macOS, utilisez `python3` et `pip3` au lieu de `python` et `pip`.
:::

  </TabItem>

  <TabItem value="linux" label="Linux">

### Ubuntu/Debian

```bash
sudo apt update
sudo apt install python3 python3-pip python3-dev
```

### Fedora

```bash
sudo dnf install python3 python3-pip
```

### Arch Linux

```bash
sudo pacman -S python python-pip
```

### Vérifier l'installation

```bash
python3 --version
pip3 --version
```

  </TabItem>
</Tabs>

:::tip Astuce
Redémarrez votre terminal après l'installation de Python pour vous assurer que toutes les variables d'environnement sont correctement configurées.
:::

---

## 🎮 Télécharger Xenon Space

### Option 1 : Téléchargement des releases (recommandé)

<div className="hero hero--primary">
  <div className="container">
    <h3 className="hero__title">📦 Dernière version stable</h3>
    <p className="hero__subtitle">
      Téléchargez la version packagée prête à l'emploi
    </p>
    <div className="margin-top--md">
      <a href="https://github.com/nonov1012/xenon-space---Video-game/" className="button button--secondary button--lg">
        Télécharger la dernière version →
      </a>
    </div>
  </div>
</div>

**Fichiers disponibles :**
- `xenon-space-windows.zip` - Pour Windows (exécutable standalone)
- `xenon-space-macos.zip` - Pour macOS (application .app)
- `xenon-space-linux.tar.gz` - Pour Linux (AppImage ou script)
- `xenon-space-source.zip` - Code source complet

### Option 2 : Installation depuis les sources (recommandé pour développeurs)

<details>
<summary>Cliquez pour voir les instructions d'installation depuis le code source</summary>

**Prérequis :**
- Python 3.8+
- pip (gestionnaire de paquets Python)
- Git

**Étapes d'installation :**

```bash
# 1. Cloner le dépôt
git clone https://github.com/nonov1012/xenon-space---Video-game.git
cd xenon-space

# 2. (Optionnel mais recommandé) Créer un environnement virtuel
python -m venv venv

# 3. Activer l'environnement virtuel
# Sur Windows :
venv\Scripts\activate
# Sur macOS/Linux :
source venv/bin/activate

# 4. Installer les dépendances
pip install -r requirements.txt

# 5. Lancer le jeu
python loading_run.py
```

**Dépendances requises :**
Les bibliothèques suivantes seront installées automatiquement :
- `pygame` (≥2.1.2) - Moteur de jeu
- `Pillow` (≥11.0.0) - Traitement d'images
- `pypresence` (≥4.3.0) - Intégration Discord Rich Presence
- `numpy` (≥1.26.4) - Calculs mathématiques

</details>

---

## 🚀 Lancer le jeu

### Méthode 1 : Versions packagées (double-clic)

<Tabs>
  <TabItem value="windows-exe" label="Windows" default>

1. Décompressez `xenon-space-windows.zip`
2. Double-cliquez sur `xenon-space.exe`
3. Si Windows affiche un avertissement de sécurité :
   - Cliquez sur **"Informations complémentaires"**
   - Puis **"Exécuter quand même"**

:::caution Windows Defender
Il est normal que Windows affiche un avertissement pour les applications non signées.
:::

  </TabItem>

  <TabItem value="macos-app" label="macOS">

1. Décompressez `xenon-space-macos.zip`
2. Faites glisser `Xenon Space.app` dans votre dossier Applications
3. Double-cliquez sur l'application
4. Si macOS bloque le lancement :
   - Ouvrez **Préférences Système** → **Confidentialité et sécurité**
   - Cliquez sur **"Ouvrir quand même"**

Ou utilisez cette commande dans le Terminal :

```bash
xattr -cr "/Applications/Xenon Space.app"
```

  </TabItem>

  <TabItem value="linux-bin" label="Linux">

```bash
# Décompresser l'archive
tar -xzf xenon-space-linux.tar.gz
cd xenon-space

# Rendre le script exécutable
chmod +x run.sh

# Lancer le jeu
./run.sh
```

  </TabItem>
</Tabs>

---

### Méthode 2 : Depuis le code source

Si vous avez installé depuis les sources (Option 2) :

```bash
# Assurez-vous d'être dans le bon dossier
cd xenon-space

# Activez l'environnement virtuel si vous en avez créé un
# Windows :
venv\Scripts\activate
# macOS/Linux :
source venv/bin/activate

# Lancez le jeu
python loading_run.py
```

---

## 🎨 Premier lancement

### Écran de démarrage

Au premier lancement, vous verrez :

1. **Logo Xenon Space** - Écran de chargement
2. **Menu principal** avec les options suivantes :
   - Nouvelle partie
   - Charger une partie (si sauvegardes disponibles)
   - Options
   - Crédits
   - Quitter

### Configuration initiale

Avant de commencer, nous recommandons de :

<div className="row">
  <div className="col col--6">
    <div className="card">
      <div className="card__header">
        <h4>🔊 Audio</h4>
      </div>
      <div className="card__body">
        <ul>
          <li>Réglez le volume général</li>
          <li>Activez/désactivez la musique</li>
          <li>Ajustez les effets sonores</li>
        </ul>
      </div>
    </div>
  </div>

  <div className="col col--6">
    <div className="card">
      <div className="card__header">
        <h4>🖥️ Affichage</h4>
      </div>
      <div className="card__body">
        <ul>
          <li>Choisir plein écran ou fenêtré</li>
          <li>Sélectionner la résolution</li>
          <li>Activer/désactiver VSync</li>
        </ul>
      </div>
    </div>
  </div>
</div>

---

## 🛠️ Résolution des problèmes

### Le jeu ne se lance pas

<Tabs>
  <TabItem value="python-error" label="Erreur Python" default>

**Symptôme :** Message "Python not found" ou "command not found"

**Solution :**

1. Vérifiez votre version Python :
   ```bash
   python --version
   # ou sur macOS/Linux :
   python3 --version
   ```
2. Assurez-vous d'avoir **Python 3.8+**
3. Vérifiez que Python est dans le PATH
4. Réinstallez Python si nécessaire (voir section précédente)

  </TabItem>

  <TabItem value="dependencies" label="Erreurs de dépendances">

**Symptôme :** "ModuleNotFoundError: No module named 'pygame'" ou autres imports manquants

**Solutions :**

1. Réinstallez les dépendances :
   ```bash
   pip install -r requirements.txt --force-reinstall
   ```

2. Vérifiez que vous utilisez le bon Python/pip :
   ```bash
   # Windows
   python -m pip install -r requirements.txt

   # macOS/Linux
   python3 -m pip install -r requirements.txt
   ```

3. Si vous avez créé un environnement virtuel, assurez-vous qu'il est activé

  </TabItem>

  <TabItem value="graphics-error" label="Problèmes graphiques">

**Symptôme :** Écran noir, textures manquantes, erreur SDL

**Solutions :**

1. Mettez à jour vos pilotes graphiques
2. Réinstallez pygame :
   ```bash
   pip uninstall pygame
   pip install pygame
   ```
3. Sur Linux, installez les dépendances SDL2 :
   ```bash
   # Ubuntu/Debian
   sudo apt install libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev

   # Fedora
   sudo dnf install SDL2-devel SDL2_image-devel SDL2_mixer-devel
   ```
4. Réduisez la résolution dans les paramètres du jeu

  </TabItem>

  <TabItem value="performance" label="Performance">

**Symptôme :** Ralentissements, FPS bas

**Solutions :**

1. Fermez les applications en arrière-plan
2. Réduisez la taille de la carte dans les paramètres de jeu
3. Désactivez la Rich Presence Discord si activée
4. Vérifiez que vous n'utilisez pas trop de vaisseaux simultanément
5. Sur laptop, assurez-vous d'être branché et en mode haute performance

  </TabItem>

  <TabItem value="crash" label="Crash/Freeze">

**Symptôme :** Le jeu plante aléatoirement

**Solutions :**

1. Vérifiez les logs dans le dossier du jeu
2. Lancez en mode debug pour plus d'informations :
   ```bash
   python loading_run.py --debug
   ```
3. Vérifiez les erreurs dans la console
4. Reportez le bug sur [GitHub Issues](https://github.com/nonov1012/xenon-space---Video-game/issues) avec :
   - Le message d'erreur complet
   - Votre système d'exploitation
   - Votre version de Python
   - Les étapes pour reproduire le bug

  </TabItem>

  <TabItem value="audio" label="Problèmes audio">

**Symptôme :** Pas de son, crackling, erreur mixer

**Solutions :**

1. Vérifiez que votre système audio fonctionne
2. Réinstallez pygame avec support audio
3. Sur Linux, installez les bibliothèques audio :
   ```bash
   sudo apt install libsdl2-mixer-2.0-0
   ```
4. Lancez sans audio pour tester :
   ```bash
   python loading_run.py --no-audio
   ```

  </TabItem>
</Tabs>

### Fichiers de logs

Les fichiers de logs s'affichent directement dans la console/terminal lors de l'exécution du jeu.

Pour sauvegarder les logs, redirigez la sortie :

```bash
# Sauvegarder les logs dans un fichier
python loading_run.py > xenon-space.log 2>&1
```

---

## 📁 Structure des fichiers

Après installation, voici l'organisation des dossiers :

```
xenon-space/
├── loading_run.py                  # Point d'entrée du jeu
├── requirements.txt         # Liste des dépendances Python
├── classes/                 # Classes du jeu
│   ├── Game.py
│   ├── Ship.py
│   ├── Map.py
│   └── ...
├── menu/                    # Menus du jeu
│   ├── menuPrincipal.py
│   ├── menuParam.py
│   └── ...
├── assets/                  # Ressources du jeu
│   ├── ships/              # Sprites des vaisseaux
│   ├── planets/            # Textures des planètes
│   ├── sounds/             # Effets sonores
│   └── music/              # Musiques
```

---

## 🔄 Mise à jour du jeu

### Via Git (si installé depuis les sources)

Si vous avez cloné le dépôt avec Git :

```bash
# Allez dans le dossier du jeu
cd xenon-space

# Récupérez les dernières modifications
git pull origin main

# Mettez à jour les dépendances (au cas où)
pip install -r requirements.txt --upgrade
```

### Installation manuelle

1. Téléchargez la nouvelle version depuis [GitHub Releases](https://github.com/nonov1012/xenon-space---Video-game/releases)
2. Remplacez les fichiers du jeu par la nouvelle version

---

## 🗑️ Désinstallation

### Installation depuis les sources

```bash
# Allez dans le dossier parent
cd ..

# Supprimez le dossier du jeu
rm -rf xenon-space

# Sur Windows, utilisez :
# rmdir /s xenon-space
```

### Version packagée

**Windows :**
1. Supprimez le dossier d'installation du jeu
2. Supprimez les sauvegardes si vous ne voulez pas les conserver

**macOS :**
1. Faites glisser `Xenon Space.app` vers la corbeille
2. Videz la corbeille

**Linux :**
```bash
# Supprimer le dossier d'installation
rm -rf ~/xenon-space
```

---

## 📞 Support

Besoin d'aide ? Plusieurs options s'offrent à vous :

<div className="row">
  <div className="col col--4">
    <div className="card">
      <div className="card__body">
        <h4>📖 Documentation</h4>
        <p>Consultez le <a href="./tutoriel">tutoriel</a> et le <a href="./gameplay">guide de gameplay</a></p>
      </div>
    </div>
  </div>

  <div className="col col--4">
    <div className="card">
      <div className="card__body">
        <h4>🐛 Signaler un bug</h4>
        <p>Ouvrez une issue sur <a href="https://github.com/nonov1012/xenon-space---Video-game/issues">GitHub</a></p>
      </div>
    </div>
  </div>

  <div className="col col--4">
    <div className="card">
      <div className="card__body">
        <h4>💬 Communauté</h4>
        <p>Rejoignez notre serveur Discord (lien à venir)</p>
      </div>
    </div>
  </div>
</div>

---

## ✅ Prochaines étapes

<div className="hero hero--success">
  <div className="container">
    <h3 className="hero__title">🎉 Installation terminée !</h3>
    <p className="hero__subtitle">
      Vous êtes prêt à conquérir l'espace !
    </p>
    <div className="margin-top--md">
      <a href="./tutoriel" className="button button--primary button--lg margin-right--md">
        Commencer le tutoriel
      </a>
      <a href="./gameplay" className="button button--outline button--lg">
        Découvrir les règles
      </a>
    </div>
  </div>
</div>

---

> « L'aventure commence ici, Commandant.
> Les étoiles vous attendent. »
