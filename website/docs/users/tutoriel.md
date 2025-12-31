---
sidebar_position: 3
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# 📘 Tutoriel - Premiers pas

Bienvenue dans votre première mission, Commandant ! Ce tutoriel vous guidera pas à pas dans les mécaniques essentielles de **Xenon Space**.

---

## 🎯 Objectifs du tutoriel

À la fin de ce tutoriel, vous saurez :

<div className="row">
  <div className="col col--6">
    <div className="card">
      <div className="card__body">
        <h4>✅ Compétences de base</h4>
        <ul>
          <li>Déplacer vos vaisseaux</li>
          <li>Attaquer les ennemis</li>
          <li>Gérer votre économie</li>
          <li>Acheter des unités</li>
        </ul>
      </div>
    </div>
  </div>

  <div className="col col--6">
    <div className="card">
      <div className="card__body">
        <h4>✅ Compétences avancées</h4>
        <ul>
          <li>Améliorer votre base</li>
          <li>Utiliser les foreuses</li>
          <li>Gérer les transporteurs</li>
          <li>Développer une stratégie</li>
        </ul>
      </div>
    </div>
  </div>
</div>

---

## 🚀 Étape 1 : Lancer votre première partie

### Démarrer une nouvelle partie

1. Lancez Xenon Space
2. Dans le menu principal, cliquez sur **"Nouvelle Partie"**
3. Choisissez vos paramètres :
   - **Taille de carte** : Commencez avec "Petite" pour votre première partie
   - **Difficulté** : Sélectionnez "Facile" pour vous familiariser
   - **Joueur** : Choisissez votre couleur (Bleu ou Rouge)

:::tip Conseil pour débutants
Pour votre première partie, choisissez une **carte petite** et la difficulté **Facile**. Cela vous permettra de vous concentrer sur l'apprentissage sans être submergé.
:::

### Comprendre l'interface

Une fois la partie lancée, vous verrez :

<div className="row">
  <div className="col col--4">
    <div className="card">
      <div className="card__header">
        <h4>💰 HUD Supérieur</h4>
      </div>
      <div className="card__body">
        <p>Affiche votre argent actuel et le numéro du tour</p>
      </div>
    </div>
  </div>

  <div className="col col--4">
    <div className="card">
      <div className="card__header">
        <h4>🗺️ Carte centrale</h4>
      </div>
      <div className="card__body">
        <p>Le champ de bataille avec vos vaisseaux, la base et les ennemis</p>
      </div>
    </div>
  </div>

  <div className="col col--4">
    <div className="card">
      <div className="card__header">
        <h4>📊 Panneau latéral</h4>
      </div>
      <div className="card__body">
        <p>Informations sur l'unité sélectionnée et options d'achat</p>
      </div>
    </div>
  </div>
</div>

---

## 🎮 Étape 2 : Contrôles de base

### Commandes essentielles

<Tabs>
  <TabItem value="souris" label="Souris" default>

**Clic gauche :**

<ul>
  <li>Sur un vaisseau allié : Le sélectionner</li>
  <li>Sur une case bleue : Déplacer le vaisseau sélectionné</li>
  <li>Sur un ennemi en zone rouge : Attaquer</li>
</ul>

**Clic droit :**

<ul>
  <li>Sur un astéroïde (avec foreuse) : Miner</li>
  <li>Sur le transporteur : Embarquer un vaisseau</li>
  <li>Sur une mini-icône (transporteur) : Débarquer un vaisseau</li>
</ul>

**Molette :**

<ul>
  <li>Zoomer / Dézoomer sur la carte</li>
</ul>

  </TabItem>

  <TabItem value="clavier" label="Clavier">

**Touches de déplacement :**

<ul>
  <li><code>↑</code> <code>↓</code> <code>←</code> <code>→</code> ou <code>ZQSD</code> : Déplacer la caméra</li>
</ul>

**Touches d'action :**

<ul>
  <li><code>R</code> : Faire pivoter le vaisseau sélectionné</li>
  <li><code>ENTRÉE</code> : Terminer votre tour</li>
  <li><code>ÉCHAP</code> : Menu pause</li>
</ul>

**Raccourcis :**

<ul>
  <li><code>F1</code> : Aide rapide</li>
  <li><code>F11</code> : Plein écran / Fenêtré</li>
</ul>

  </TabItem>
</Tabs>

:::info Astuce
Utilisez la **molette de la souris** pour zoomer et mieux voir le champ de bataille !
:::

---

## 🚢 Étape 3 : Déplacer vos vaisseaux

### Sélectionner une unité

1. **Cliquez gauche** sur l'un de vos vaisseaux
2. Vous verrez apparaître :
   - **Zone bleue** : Cases où vous pouvez vous déplacer
   - **Zone rouge** : Ennemis que vous pouvez attaquer

### Effectuer un déplacement

**Mission pratique :** Déplacez votre vaisseau Petit vers l'avant

```
Étapes :
1. Cliquez sur votre vaisseau Petit
2. Observez la zone bleue qui apparaît
3. Cliquez sur une case bleue devant votre base
4. Le vaisseau se déplace !
```

:::caution Important
Une fois qu'un vaisseau s'est déplacé, sa zone bleue diminue selon la distance parcourue. Les points de mouvement se rechargent au début de votre prochain tour.
:::

### Comprendre la portée de déplacement

Chaque type de vaisseau a une portée différente :

| Vaisseau | Portée | Exemples d'utilisation |
|----------|--------|------------------------|
| 🏃 Petit | 6 | Éclaireur, frappe rapide |
| ⚖️ Moyen | 6 | Polyvalent |
| 🛡️ Lourd | 3 | Tank, défense |
| ⛏️ Foreuse | 3 | Exploitation ressources |
| 🚚 Transport | 4 | Logistique |

---

## ⚔️ Étape 4 : Combat et attaque

### Attaquer un ennemi

**Mission pratique :** Détruisez votre premier vaisseau ennemi

```
Étapes :
1. Sélectionnez un de vos vaisseaux
2. Si un ennemi est dans la zone rouge, cliquez dessus
3. Un projectile est lancé !
4. Les PV de l'ennemi diminuent
```

### Comprendre les dégâts

Le système de combat est simple :

```
PV ennemis = PV actuels - Votre Attaque
```

**Exemple concret :**

<div className="card">
  <div className="card__body">
    <p><strong>Situation :</strong></p>
    <ul>
      <li>Vaisseau ennemi Moyen : 400 PV</li>
      <li>Votre vaisseau Petit attaque : 50 ATK</li>
    </ul>
    <p><strong>Résultat :</strong></p>
    <p>400 - 50 = <strong>350 PV restants</strong></p>
    <p>Il faudra <strong>8 attaques</strong> pour le détruire !</p>
  </div>
</div>

:::tip Stratégie
Concentrez vos attaques sur **un seul ennemi** à la fois pour l'éliminer rapidement et récupérer la récompense !
:::

### Récompenses d'élimination

Quand vous détruisez un vaisseau ennemi, vous recevez **60% de son coût** :

- Petit détruit : **+195₿**
- Moyen détruit : **+390₿**
- Lourd détruit : **+630₿**

---

## 💰 Étape 5 : Gérer votre économie

### Vos sources de revenus

À chaque fin de tour, vous recevez de l'argent automatiquement :

<Tabs>
  <TabItem value="base" label="🏰 Base" default>

**Revenu passif garanti**

| Niveau Base | Gain par tour |
|-------------|---------------|
| Niveau 1 | +300₿ |
| Niveau 2 | +400₿ |
| Niveau 3 | +500₿ |
| Niveau 4 | +600₿ |

**C'est votre revenu de base minimum !**

  </TabItem>

  <TabItem value="foreuses" label="⛏️ Foreuses">

**Deux façons de gagner :**

**1. Minage d'astéroïdes :**

<ul>
  <li>Clic droit sur un astéroïde</li>
  <li>Gain : <strong>+100₿</strong> immédiat</li>
  <li>Coût : -10% PV de la foreuse</li>
</ul>

**2. Bonus planète (RECOMMANDÉ) :**

<ul>
  <li>Placez une foreuse à côté d'une planète</li>
  <li>Gain : <strong>+150₿ par tour</strong> automatique</li>
  <li>Aucun coût !</li>
</ul>

  </TabItem>

  <TabItem value="combat" label="💀 Combat">

**Éliminations ennemies**

Chaque vaisseau détruit rapporte **60% de son coût**.

C'est un revenu actif qui nécessite de prendre des risques, mais peut être très rentable !

  </TabItem>
</Tabs>

### Premier achat

**Mission pratique :** Achetez votre premier vaisseau

```
Étapes :
1. Attendez d'avoir au moins 400₿
2. Cliquez sur votre base
3. Dans le panneau latéral, sélectionnez "Foreuse"
4. Cliquez sur une case vide à côté de la base
5. Votre foreuse apparaît !
```

:::tip Conseil économique
Au début de la partie, achetez **2-3 foreuses** et placez-les près de planètes. C'est l'investissement le plus rentable !
:::

---

## ⛏️ Étape 6 : Utiliser les foreuses

### Déployer une foreuse

Les foreuses sont votre moteur économique. Voici comment les utiliser efficacement :

**Mission pratique :** Installez une foreuse sur une planète

```
Étapes :
1. Achetez une foreuse (400₿)
2. Placez-la ADJACENTE à une planète (1 case de distance)
3. À la fin du tour, vous recevrez +150₿ automatiquement !
```

### Configuration optimale

Maximisez vos revenus en plaçant plusieurs foreuses autour d'une planète :

```
🪐 = Planète
⛏️ = Foreuse
. = Vide

Configuration idéale :
  . ⛏️ .
  ⛏️ 🪐 ⛏️
  . ⛏️ .

4 foreuses × 150₿ = +600₿ par tour !
```

:::caution Attention
Les foreuses ont **0 attaque**. Protégez-les avec d'autres vaisseaux, car elles sont des cibles faciles pour l'ennemi !
:::

---

## 🏗️ Étape 7 : Améliorer votre base

### Pourquoi améliorer ?

Améliorer votre base offre plusieurs avantages :

<div className="row">
  <div className="col col--4">
    <div className="card">
      <div className="card__header">
        <h4>💪 Plus de PV</h4>
      </div>
      <div className="card__body">
        <p>Votre base devient plus résistante aux attaques</p>
      </div>
    </div>
  </div>

  <div className="col col--4">
    <div className="card">
      <div className="card__header">
        <h4>💵 Plus de revenus</h4>
      </div>
      <div className="card__body">
        <p>Augmente le gain passif par tour</p>
      </div>
    </div>
  </div>

  <div className="col col--4">
    <div className="card">
      <div className="card__header">
        <h4>🚀 Nouveaux vaisseaux</h4>
      </div>
      <div className="card__body">
        <p>Débloque l'accès aux vaisseaux supérieurs</p>
      </div>
    </div>
  </div>
</div>

### Coûts et gains

| Amélioration | Coût | Nouveau revenu | PV |
|--------------|------|----------------|-----|
| Nv 1 → 2 | 1000₿ | +400₿/tour | 700 |
| Nv 2 → 3 | 2000₿ | +500₿/tour | 1200 |
| Nv 3 → 4 | 6000₿ | +600₿/tour | 1600 |

**Mission pratique :** Améliorez votre base au niveau 2

```
Étapes :
1. Économisez 1000₿
2. Cliquez sur votre base
3. Cliquez sur "Améliorer la base"
4. Votre revenu passe à +400₿/tour !
```

:::tip Timing
N'améliorez pas trop tôt ! Investissez d'abord dans **des foreuses** pour augmenter vos revenus, puis améliorez la base.
:::

---

## 🚚 Étape 8 : Maîtriser le transporteur

### À quoi sert le transporteur ?

Le transporteur peut contenir **jusqu'à 3 vaisseaux** et les déplacer rapidement sur la carte.

**Utilisations tactiques :**
- 🌍 Déployer des foreuses sur des planètes éloignées
- ⚔️ Attaque surprise sur la base ennemie
- 🏃 Évacuer un vaisseau endommagé

### Embarquer un vaisseau

**Mission pratique :** Embarquez un vaisseau dans le transporteur

```
Étapes :
1. Achetez un transporteur (500₿)
2. Déplacez un vaisseau ADJACENT au transporteur (1 case)
3. Clic DROIT sur le transporteur
4. Le vaisseau disparaît et une mini-icône apparaît au-dessus
```

### Débarquer un vaisseau

```
Étapes :
1. Clic DROIT sur la mini-icône du vaisseau embarqué
2. Des zones jaunes apparaissent autour du transporteur
3. Cliquez sur une zone jaune
4. Le vaisseau est déployé !
```

:::info Capacité
Le transporteur peut contenir 3 vaisseaux petits, ou 1 moyen + 1 petit. Les vaisseaux lourds ne peuvent pas être embarqués.
:::

---

## 🎯 Étape 9 : Terminer votre tour

### Valider vos actions

Quand vous avez terminé vos actions, vous devez passer au tour suivant :

```
Étapes :
1. Appuyez sur ENTRÉE
2. Vos revenus sont calculés et ajoutés
3. Vos vaisseaux rechargent leurs portées
4. C'est au tour de l'IA
```

### Ce qui se passe en fin de tour

<div className="card">
  <div className="card__header">
    <h4>🔄 Séquence de fin de tour</h4>
  </div>
  <div className="card__body">
    <ol>
      <li><strong>Phase Revenus :</strong> Vous recevez l'argent de votre base et de vos foreuses</li>
      <li><strong>Phase Rechargement :</strong> Tous vos vaisseaux récupèrent leur portée complète</li>
      <li><strong>Tour ennemi :</strong> L'IA joue son tour</li>
      <li><strong>Nouveau tour :</strong> C'est à nouveau à vous !</li>
    </ol>
  </div>
</div>

:::caution Irréversible
Une fois que vous avez appuyé sur **ENTRÉE**, impossible de revenir en arrière ! Assurez-vous d'avoir terminé toutes vos actions.
:::

---

## 🎓 Étape 10 : Votre première victoire

### Condition de victoire

<div className="hero hero--success">
  <div className="container">
    <h3 className="hero__title">🏆 Gagner la partie</h3>
    <p className="hero__subtitle">
      Détruisez le <strong>vaisseau-mère ennemi</strong> (réduisez ses PV à 0)
    </p>
  </div>
</div>

### Stratégie pour gagner

**Plan d'action recommandé :**

<Tabs>
  <TabItem value="debut" label="🌅 Début (Tours 1-10)" default>

**Objectif : Développer l'économie**

✅ Actions prioritaires :

<ul>
  <li>Acheter 2-3 foreuses</li>
  <li>Les placer sur des planètes</li>
  <li>Améliorer la base au niveau 2</li>
  <li>Acheter quelques vaisseaux Petits pour défendre</li>
</ul>

💡 Focus sur les **revenus passifs** !

  </TabItem>

  <TabItem value="milieu" label="⚙️ Milieu (Tours 11-20)">

**Objectif : Construire une flotte**

✅ Actions prioritaires :

<ul>
  <li>Acheter des vaisseaux Moyens</li>
  <li>Commencer à attaquer les vaisseaux ennemis</li>
  <li>Améliorer la base au niveau 3</li>
  <li>Protéger vos foreuses</li>
</ul>

💡 Équilibrez **économie** et **armée** !

  </TabItem>

  <TabItem value="fin" label="🎯 Fin (Tours 20+)">

**Objectif : Offensive finale**

✅ Actions prioritaires :

<ul>
  <li>Acheter des vaisseaux Lourds si disponibles</li>
  <li>Concentrer les attaques sur la base ennemie</li>
  <li>Détruire les vaisseaux ennemis pour les récompenses</li>
  <li>Avancer progressivement vers la base</li>
</ul>

💡 **Focus fire** sur la base ennemie !

  </TabItem>
</Tabs>

---

## 💡 Conseils pour débutants

### Les erreurs à éviter

<div className="row">
  <div className="col col--6">
    <div className="alert alert--danger">
      <h4>❌ À NE PAS FAIRE</h4>
      <ul>
        <li>Tout dépenser en vaisseaux dès le début</li>
        <li>Ignorer les foreuses</li>
        <li>Attaquer sans stratégie</li>
        <li>Laisser votre base sans défense</li>
        <li>Oublier de terminer votre tour</li>
      </ul>
    </div>
  </div>

  <div className="col col--6">
    <div className="alert alert--success">
      <h4>✅ BONNES PRATIQUES</h4>
      <ul>
        <li>Investir dans 2-3 foreuses rapidement</li>
        <li>Garder une réserve d'argent (500₿+)</li>
        <li>Protéger vos unités économiques</li>
        <li>Planifier vos déplacements</li>
        <li>Concentrer vos attaques</li>
      </ul>
    </div>
  </div>
</div>

### Astuces tactiques

<details>
<summary><strong>💡 Astuce #1 : Le Kiting</strong></summary>

Attaquez puis reculez pour éviter les contre-attaques :

```
Tour 1 : Avancer → Attaquer
Tour 2 : Reculer hors de portée ennemie
Tour 3 : Avancer → Attaquer de nouveau
```

Cette technique fonctionne bien avec les vaisseaux **Petits** (portée 6).

</details>

<details>
<summary><strong>💡 Astuce #2 : Le Focus Fire</strong></summary>

Concentrez plusieurs vaisseaux sur une seule cible :

```
3 vaisseaux Petits (50 ATK chacun) vs 1 Moyen ennemi (400 PV) :
- Attaque 1 : 400 - 50 = 350 PV
- Attaque 2 : 350 - 50 = 300 PV
- Attaque 3 : 300 - 50 = 250 PV

En un seul tour, vous avez infligé 150 dégâts !
```

</details>

<details>
<summary><strong>💡 Astuce #3 : La Rotation</strong></summary>

Utilisez la touche **R** pour faire pivoter vos gros vaisseaux et passer dans des espaces étroits entre les planètes.

</details>

---

## 📚 Récapitulatif du tutoriel

### Ce que vous avez appris

<div className="card">
  <div className="card__body">
    <h4>✅ Compétences acquises</h4>
    <div className="row">
      <div className="col col--6">
        <ul>
          <li>✔️ Lancer une partie</li>
          <li>✔️ Utiliser les contrôles</li>
          <li>✔️ Déplacer les vaisseaux</li>
          <li>✔️ Attaquer les ennemis</li>
          <li>✔️ Gérer l'économie</li>
        </ul>
      </div>
      <div className="col col--6">
        <ul>
          <li>✔️ Acheter des unités</li>
          <li>✔️ Utiliser les foreuses</li>
          <li>✔️ Améliorer la base</li>
          <li>✔️ Maîtriser le transporteur</li>
          <li>✔️ Terminer un tour</li>
        </ul>
      </div>
    </div>
  </div>
</div>

### Checklist première partie

Avant de lancer votre première vraie partie, vérifiez que vous savez :

- [ ] Déplacer un vaisseau sur la carte
- [ ] Attaquer un ennemi en zone rouge
- [ ] Acheter une foreuse et la placer sur une planète
- [ ] Acheter un nouveau vaisseau depuis la base
- [ ] Améliorer votre base au niveau supérieur
- [ ] Embarquer/débarquer avec le transporteur
- [ ] Terminer votre tour avec ENTRÉE

:::tip Prêt pour l'aventure ?
Si vous avez coché toutes les cases, vous êtes **prêt à conquérir la galaxie** !
:::

---

## 🔄 Prochaines étapes

<div className="hero hero--primary">
  <div className="container">
    <h3 className="hero__title">🚀 Continuez votre formation</h3>
    <p className="hero__subtitle">
      Approfondissez vos connaissances avec nos guides avancés
    </p>
    <div className="margin-top--md">
      <a href="./gameplay" className="button button--secondary button--lg margin-right--md">
        Guide Gameplay complet →
      </a>
      <a href="./mechanics" className="button button--outline button--lg">
        Mécaniques avancées →
      </a>
    </div>
  </div>
</div>

---

## ❓ Questions fréquentes

<details>
<summary><strong>Combien de temps dure une partie ?</strong></summary>

Une partie dure généralement **15-30 minutes** selon la taille de la carte et votre stratégie. Les parties sur petite carte sont plus rapides (10-15 min).

</details>

<details>
<summary><strong>Puis-je sauvegarder en cours de partie ?</strong></summary>

Actuellement, le jeu ne sauvegarde pas automatiquement en cours de partie. Assurez-vous d'avoir le temps de finir votre session !

</details>

<details>
<summary><strong>Quelle est la meilleure stratégie pour débuter ?</strong></summary>

Focus sur l'**économie** en début de partie :
1. Achetez 2-3 foreuses
2. Placez-les sur des planètes
3. Améliorez la base au niveau 2
4. Ensuite seulement, construisez une armée

Cette approche garantit des revenus solides pour financer votre victoire !

</details>

<details>
<summary><strong>Comment gagner rapidement ?</strong></summary>

Il n'y a pas de stratégie "rush" efficace. Xenon Space récompense la **patience** et la **planification**. Développez votre économie, puis construisez une flotte puissante pour l'assaut final.

</details>

<details>
<summary><strong>Que faire si je suis bloqué ?</strong></summary>

Si vous avez du mal à progresser :
- Relisez le [guide des mécaniques](./mechanics)
- Consultez le [guide gameplay détaillé](./gameplay)
- Réduisez la difficulté pour votre prochaine partie
- Demandez de l'aide sur notre [Discord](#) ou [GitHub](https://github.com/votre-repo/xenon-space/issues)

</details>

---

> « La connaissance est la première arme du commandant.
> Maintenant, montrez ce que vous avez appris ! »
>
> — *Académie Spatiale de Xenon*
