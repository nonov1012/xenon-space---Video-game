# Maintenance

La maintenance du jeu a pour objectif de garantir son **bon fonctionnement**, de **faciliter les mises à jour** et de permettre une **gestion efficace du code et des ressources**. Étant donné que le jeu est entièrement hors ligne et ne collecte aucune donnée personnelle, les procédures de sécurité et de sauvegarde sont minimales.

---

## Mises à jour 🔄

Toutes les mises à jour du jeu sont effectuées via **GitHub**.

### Procédure pour mettre à jour le jeu sur une machine :

1.  Ouvrir le **terminal** ou l’interface Git.
2.  Se rendre dans le **dossier du projet local**.
3.  Exécuter la commande :
    ```bash
    git pull origin main
    ```
    *(ou la branche principale que vous utilisez)*
4.  **Vérifier que le jeu fonctionne** après chaque mise à jour.

---

## Sauvegardes 💾

Aucune sauvegarde automatique n’est nécessaire pour le jeu.

### Procédure pour conserver une copie du projet (prévention contre la perte de code) :

Cloner le dépôt Git sur un autre ordinateur ou disque externe :

```bash
git clone <URL-du-dépôt>
```

## Supervision et contrôle

Étant donné que le jeu est hors ligne et ne nécessite pas de serveur, la supervision se limite à l’observation de son bon fonctionnement lors de son lancement.

* Vérifiez que le jeu démarre correctement et que toutes les ressources graphiques et sonores sont chargées.

## Problèmes fréquents

* **Erreur lors du lancement** : vérifier que tous les fichiers du projet sont à jour via Git.
* **Ressources manquantes (images, sons)** : vérifier le dossier du projet et que les fichiers ont été correctement récupérés lors du `pull` Git.
* **Bug de jeu** : remonter l’erreur au développeur responsable et créer une nouvelle branche pour corriger le bug sans affecter la version principale.