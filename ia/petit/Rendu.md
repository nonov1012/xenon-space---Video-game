# Compte rendu du travail effectuer - 2eme Partie

SAE5A_JV_INFO

## Introduction

NOM Prénom : DAVID Gabriel
Nom du jeux : XENON SPACE
Unité produite : Vaisseau de classe petit

## Comment trouver le fichier ?

Mon IA se situe sur la branche : `IA_DAVID`

```bash
git clone https://github.com/nonov1012/xenon-space---Video-game.git
git fetch origin IA_DAVID
git checkout IA_DAVID
```

Le répertoire de mon IA se situe sur le dossier `ia/petit`

Le fichier de mon IA actuelle est `ia_utils.py`

## Schéma de décision

![Schéma de décision](<schéma de décision.png>)

## Ce que j'ai du coder

Pour la création de mon IA, j'ai utilisé:

- Un algorithme de scoring `evaluate_position()` qui vat évaluer une position de déplacement possible avec deux paramètres : un score d'attaque et un score de défense.
- Le calcul du score d'attaque ce fait dans `utility_attack_pos()` et le score est basé sur la position de l'unité par rapport à chaque unitées ennemies, De plus j'ai rajouter un score par rapport à la disctance de la base ennemi qui vat de 0 à 1.
- Le calcul du score de defense ce fait dans `utility_defend_pos`. Ce score est créé avec le calcul de la distance entre cette unitée et ces alliés ainsi que la distance entre cette allié et d'un autre ennemi.

Le tout est utilisé dans la fonction `choose_best_action` qui vat choisir la case avec le plus gros déplacement possible ou la cible à attaquer.

Pour résumer mon IA est un algorithme glouton qui utilise un système de score pour choisir la meillieur position possible sans devoir calculer toute les possibilités.

## Comment utiliser mon IA ?

Pour utiliser mon IA vous pouvez :

Lancer le main dans la branche `IA_DAVID`

sur Linux:

```bash
python3 -m main
```

sur windows:

```bash
py -m main
```
