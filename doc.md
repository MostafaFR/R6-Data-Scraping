# Documentation en Markdown pour le Script de Scraping sur Liquipedia

Ce document fournit une vue d'ensemble et des instructions pour utiliser un script Python conçu pour extraire des informations de Liquipedia, un site web dédié à l'esport. Le script cible spécifiquement des données sur les équipes et les tournois dans le domaine de Rainbow Six Siege, et sauvegarde les résultats dans des fichiers Excel et JSON.

## Dépendances

Le script utilise plusieurs bibliothèques Python :

- `requests_html` pour les requêtes web et le parsing HTML.
- `openpyxl` pour la création et la manipulation de fichiers Excel.
- `pandas` pour la manipulation de données structurées.
- `jmespath` pour interroger des structures de données JSON.
- `os` et `json` pour diverses opérations sur le système de fichiers et le traitement de JSON.
- `re` pour les expressions régulières.

Assurez-vous d'installer ces bibliothèques avant d'exécuter le script.

## Structure du Script

Le script est structuré autour de plusieurs classes principales :

### `LiquipediaScraper`

C'est la classe principale qui orchestre le scraping. Elle initialise les sessions HTTP, gère les paramètres de scraping (comme les années et les catégories de tournois), et appelle les autres composants pour extraire et sauvegarder les données.

### `ExcelManager`

Cette classe s'occupe de la création, de la manipulation, et de l'enregistrement des fichiers Excel. Elle prépare les feuilles de calcul pour les joueurs, les tournois, et les matchs.

### `JSONManager`

Gère la sauvegarde des données extraites dans un fichier JSON et leur insertion dans des feuilles Excel. Il utilise `jmespath` pour transformer et insérer les données de manière structurée.

### `ImageDownloader`

Télécharge et sauvegarde les images des logos d'équipe et des drapeaux de joueurs à partir de leurs URL.

### `TeamScraper`

Extrait les informations sur les équipes et les joueurs, y compris les images associées.

### `TournamentScraper`

Extrait les informations sur les tournois, y compris les détails des matchs.

### `MatchScraper` et `MatchToJsonConverter`

Extraient et transforment les détails des matchs en JSON pour une insertion ultérieure dans les fichiers de sortie.

## Utilisation

Pour utiliser le script, créez une instance de `LiquipediaScraper` et appelez la méthode `run()`. Le script parcourt automatiquement les pages spécifiées, extrait les données nécessaires, et les sauvegarde dans les fichiers Excel et JSON configurés.

```python
scraper = LiquipediaScraper()
scraper.run()
```

Les fichiers de sortie seront sauvegardés dans le dossier spécifié dans `LiquipediaScraper`, par défaut `out/`.

## Personnalisation

Vous pouvez personnaliser les paramètres de scraping (comme les années et les catégories de tournois) dans le constructeur de `LiquipediaScraper`. Modifiez également les chemins de fichiers de sortie dans `ExcelManager` et `JSONManager` si nécessaire.

## Conclusion

Ce script offre un moyen automatisé d'extraire des informations précieuses sur les équipes et les tournois de Rainbow Six Siege depuis Liquipedia, simplifiant la collecte de données pour l'analyse ou d'autres usages. Assurez-vous de respecter les politiques de Liquipedia concernant le scraping et d'utiliser ce script de manière responsable.