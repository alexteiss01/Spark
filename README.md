---

# SPARKLE MOVIE

---


Création d'un système de recommandation de films à partir de la base de données MoviesLens.


## 1. Contexte du projet et présentations des données

La base de données **MoviesLens** est un dataset assez connu en apprentissage automatique, aussi bien pour la recherche académique que pour des applications pratiques. Elle est généralement utilisée **pour entraîner des modèles de recommandations, et pour tester et comparer des algorithmes de recommandation, d’analyse de préférences et de filtrage collaboratif**. Nous utilisons pour ce projet la version MovieLens 32M, publiée par le groupe de recherche GroupLens en mai 2024, et qui contient les fichiers suivants:


*   **movies.csv** : les informations sur les films (titre, genres, etc.)
*   **ratings.csv** :  les notes attribuées par les utilisateurs aux films (note de 0.5 à 5 étoiles)
*   **tags.csv** : les tags appliqués par les utilisateurs aux films
*   **links.csv** : des identifiants pour relier les films à d’autres bases (IMDB, TMDb)
*   **README.txt** : des identifiants pour relier les films à d’autres bases (IMDB, TMDb).

Nous travaillons sur ces données en utilisant Spark, car pour de gros volumes de données (32 millions de lignes), cette approche permet de manipuler et d'explorer l'ensemble des données sans risques de crash mémoire. De plus, Spark assure la faisabilité technique des traitements en vue d'entraîner et d'évaluer les systèmes de recommandations. Enfin, il offre toute la flexibilité pour l’industrialisation, la reproductibilité des pipelines et le passage au déploiement à l’échelle réelle (cloud, entreprise).

C’est donc le standard pour traiter, entraîner, et évaluer des systèmes complexes de recommandation sur des jeux de données de cette ampleur.

L'objectif de ce projet est donc de mettre en place des systèmes de recommandations de films, utilisant divers algorithmes, afin de pouvoir suggérer des films aux utilisateurs, d'évaluer la performance des recommandations, puis de discuter des différences/ressemblances entre les diverses approches utilisées.


## 2. Analyse exploratoire des données réalisée dans le cadre du développement des systèmes de recommandation de films.

### 2.1. Objectifs de l'analyse:

- comprendre la structure et évaluer la qualité des données (films, genres, utilisateurs, notes);
- identifier les caractéristiques pertinentes pour la modélisation;
- détecter les éventuels biais ou valeurs manquantes;
- préparer les données pour les étapes de l'ALS, de la vectorisation (TF-IDF), et de la recommandation finale.

### 2.2. Données utilisées: **MovieLens 32M**  

- **movies.csv**: informations sur les films (*movieId*, *title*, *genres*);
- **ratings.csv**: notes attribuées par les utilisateurs (*userId*, *movieId*, *rating*, *timestamp*)

### 2.3. Etapes de l'analyse

#### A. 🔍 Inspection des données brutes

- Aperçu des dimensions et types de colonnes
- Affichage des premiers enregistrements
- Vérification de la présence de doublons ou valeurs nulles

  ##### 🛠️ Pré-traitement appliqué

- Nettoyage des colonnes (`dropna`, suppression de doublons)
- Séparation des genres en liste (`split('|')`)
- Conversion de types (`IntegerType`, `FloatType`, etc.)


#### B. 🎥 Analyse des films (`movies.csv`)

- Distribution des genres
- Fréquence des films par genre
- Détection des films avec genre manquant (`(no genres listed)`)

#### C. ⭐ Analyse des notes (`ratings.csv`)

- Répartition des notes (histogramme)
- Analyse des utilisateurs les plus actifs
- Moyenne et écart-type des notes
- Nombre de films notés par utilisateur
- Nombre d’utilisateurs ayant noté chaque film

#### D. 📊 Croisement films / utilisateurs

- Construction d’un DataFrame joint `df` issue de movies.csv et ratings.csv
- Combien d’utilisateurs ont noté chaque film ?
- Quels films sont les plus populaires ?
- Quelles sont les corrélations entre genre et notation moyenne ?


### 2.4.💡Résultats principaux de l'analyse: 

- Certains genres sont sur-représentés (`Drama`, `Comedy`)
- Les notes sont centrées autour de 3.5 – 4.0
- La distribution des films notés suit une loi de puissance : peu de films sont très notés
- Une partie des `movieId` présents dans les notations n'ont pas de titre associé

  

## 3. Algorithmes de recommandations utilisés

### 3.1. ALS (Alternating Least Squares)


L'algorithme **ALS (Alternating Least Squares)** est une méthode de **factorisation de matrices** utilisée en filtrage collaboratif pour les systèmes de recommandation. Chaque utilisateur et chaque film sont représentés par un vecteur latent (interaction), appris automatiquement à partir des notes observées. L’objectif d’ALS est de remplir la matrice sparse des notes en approximant les préférences manquantes, via une alternance de résolutions de moindres carrés sur les facteurs utilisateurs/films.

L'ALS est **particulièrement adapté aux grandes bases de données** : il est scalable, robuste au manque de données, et implémenté dans Apache Spark MLlib pour les usages big data.

#### Split par proportion stratifiée

Pour préparer l'entraînement et l'évaluation, le dataset a été divisé en **train** et **test** selon une **proportion stratifiée**.
- Lors du split, chaque utilisateur garde la même proportion de notations (interactions) dans le train et dans le test.
- L’échantillonnage stratifié permet de garantir une répartition équitable des utilisateurs et une représentativité cohérente du comportement utilisateur entre train et test, et surtout permet d'éviter les cols start.

#### Optimisation: Grid Search

Les hyperparamètres du modèle ALS sont : le rang des facteurs latents (*rank*), le coefficient de régularisation (*regParam*), et le nombre d’itérations (*maxIter*); ces paramètres ont été optimisés via un **grid search**.*, afin:

- d'entraîner le modèle pour toutes les combinaisons de valeurs prédéfinies sur ces paramètres.
- d'évaluer chaque modèle (par exemple avec la RMSE sur le test), et de retenir la combinaison qui donne les meilleures performances générales (ici rank = 20, regParam = 0.1 et maxIter = 10).

L'ALS apprend les préférences utilisateurs et les caractéristiques des films avec une approche scalable adaptée aux grands jeux de données. L’usage du split stratifié assure une évaluation robuste et représentative, et le grid search permet d’optimiser les performances du modèle en ajustant de façon systématique ses hyperparamètres sur les données de validation.


### 3.2. Recommandation basée sur le contenu



### 3.3. Recommandation Basée sur les Proximités Utilisateurs (KNN)


# 4. Conclusion 
