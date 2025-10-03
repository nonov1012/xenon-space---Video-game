# Documentation technique

## Structure du projet
```
nonov1012-xenon-space---video-game/
├── README.md
├── blazyck.py
├── main.py
├── mainshop.py
├── test.py
├── assets/
│   ├── fonts/
│   │   ├── SpaceNova.otf
│   │   ├── SPINC.TTF
│   │   └── temp
│   ├── img/
│   │   ├── planets/
│   │   │   └── temp
│   │   └── ships/
│   │       └── temp
│   └── sounds/
│       └── temp
├── classes/
│   ├── Achievements.py
│   ├── Animator.py
│   ├── Discord.py
│   ├── Economie.py
│   ├── Game.py
│   ├── Gif.py
│   ├── Map.py
│   ├── MenuPrincipal.py
│   ├── MotherShip.py
│   ├── PlanetAnimator.py
│   ├── Player.py
│   ├── Point.py
│   ├── ProjectileAnimator.py
│   ├── Ship.py
│   ├── ShipAnimator.py
│   ├── Shop.py
│   ├── Sounds.py
│   ├── test.py
│   ├── TitreAnime.py
│   ├── Start_Animation/
│   │   ├── main.py
│   │   ├── PlanetManager.py
│   │   └── StarField.py
│   └── Test_Animator/
│       ├── planets.py
│       └── projectiles.py
└── menu/
    ├── menuJouer.py
    ├── menuParam.py
    ├── menuPause.py
    ├── menuPrincipal.py
    └── menuSucces.py
```

## Configuration

L'entièreter des paramètres (constantes) se situe dans le fichier `blazyck.py`. Vous pourrais par exemple retrouver les paramètres :
- Taille de la grille
- Taille des cases
- Taille des **frames** des planètes
- Les chemin des assets
- Les propriété de chaque vaisseaux (vitesse, dégâts, etc.)

## Maintenance

### Mise à jour

Si vous souhaiter mettre votre jeu, ouvrez un terminal dans le dossier du jeu

```bash
git pull
```


