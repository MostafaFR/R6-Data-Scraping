# Projet de Scrapping de Données Liquipedia Rainbow Six Siege

Ce projet vise à extraire des données de Liquipedia concernant le jeu Rainbow Six Siege, en se concentrant sur les tournois, les équipes, les cartes, et les statistiques de jeu.

## Objectifs

- Extraire les informations sur les tournois et les équipes.
- Récupérer les détails des matchs, y compris les cartes jouées et les opérateurs bannis.
- Analyser les statistiques des équipes et des joueurs.

## Structure du Projet

### 1. Configuration de l'Environnement

- Utiliser Python 3.x.
- Installer les bibliothèques nécessaires : `requests`, `BeautifulSoup` pour le scrapping HTML, et `pandas` pour la manipulation des données.

### 2. Modules du Projet

#### a. Tournois & Tiers

- Identifier les différents tournois et leurs niveaux (Tier 1, Tier 2, etc.).
- Extraire les informations de base : nom, date, équipes participantes.

#### b. Équipes

- Récupérer les informations sur les équipes : nom, membres, classement.
- Distinguer les équipes par Tiers si possible.

#### c. Cartes

- Identifier les cartes bannies lors des matchs en BO1, BO3, et BO5.
- Extraire l'ordre de bannissement des cartes par équipe.

#### d. Opérateurs

- Extraire les opérateurs bannis par carte et de manière générale.
- Distinguer entre opérateurs d'attaque et de défense bannis.

### 3. Extraction et Analyse des Données

- Utiliser des requêtes HTTP pour récupérer les pages web.
- Analyser le HTML avec BeautifulSoup pour extraire les données.
- Stocker les données extraites dans des DataFrame pandas pour analyse.

### 4. Visualisation des Résultats

- Créer des graphiques comparatifs pour les équipes et les statistiques sélectionnées.
- Analyser les tendances des victoires/défaites sur les cartes, ainsi que l'efficacité en attaque et en défense.

### 5. Automatisation et Mise à Jour des Données

- Mettre en place des scripts pour automatiser l'extraction périodique des données.
- Assurer la mise à jour des bases de données pour refléter les derniers tournois et matchs.

## Documentation et Ressources

- Documentation officielle de Python, Requests, et BeautifulSoup.
- [Page des équipes sur Liquipedia](https://liquipedia.net/rainbowsix/Portal:Teams)
- [Page des tournois sur Liquipedia](https://liquipedia.net/rainbowsix/Portal:Tournaments)
- [Page des cartes sur Liquipedia](https://liquipedia.net/rainbowsix/Portal:Maps)


/Special:RunQuery/
https://www.mediawiki.org/wiki/Extension:Page_Forms/Creating_query_forms#Displaying_results_automatically

https://liquipedia.net/rainbowsix/Special:RunQuery/MapWLOverview?_run=
https://liquipedia.net/rainbowsix/Category:Semantic_query_templates
https://liquipedia.net/rainbowsix/Special:RunQuery/Notability_Checker


/rainbowsix/Portal:
https://liquipedia.net/rainbowsix/Portal:Teams
https://liquipedia.net/rainbowsix/Portal:Tournaments
https://liquipedia.net/rainbowsix/Portal:Maps


https://liquipedia.net/rainbowsix/Help:Mediawiki
https://liquipedia.net/rainbowsix/Help:Magic_Words
https://liquipedia.net/rainbowsix/Special:SpecialPages 
