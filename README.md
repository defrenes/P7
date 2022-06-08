Ce [dépôt GitHub](https://github.com/defrenes/p7) contient des données relatives au projet n°7 de la [formation *Data Scientist* d'OpenClassrooms](https://openclassrooms.com/fr/paths/164-data-scientist#path-tabs), dans sa version en cours au mois de mai 2022.

---

## Rappel du contexte / Scénario du projet n°7
La société financière, nommée **Prêt à dépenser**, propose des crédits à la consommation à des personnes ayant peu ou pas d'historique de prêt.
L’entreprise souhaite mettre en œuvre un outil de **scoring crédit** pour calculer la probabilité qu’un client rembourse son crédit, puis classifie la demande en crédit accordé ou refusé. Elle souhaite donc développer un algorithme de classification en s’appuyant sur des sources de données variées (données comportementales, données provenant d'autres institutions financières, etc.).
De plus, les chargés de relation client ont fait remonter le fait que les clients sont de plus en plus demandeurs de transparence vis-à-vis des décisions d’octroi de crédit. Cette demande de transparence des clients va tout à fait dans le sens des valeurs que l’entreprise veut incarner.

## Objectifs
Prêt à dépenser décide donc de nous confier le développement des éléments suivants :
- un **modèle de scoring** permettant de déterminer si un client a toutes les chances de rembourser son prêt ou non. Afin de faciliter la préparation des données nécessaires à l’élaboration du modèle de scoring, notre manager nous incite à sélectionner un **kernel kaggle**, qu'il faudra cependant analyser et adapter pour nous assurer qu’il répond aux besoins de votre mission.
- un **dashboard** interactif pour que les chargés de relation client puissent à la fois expliquer de façon la plus transparente possible les décisions d’octroi de crédit, mais également permettre à leurs clients de disposer de leurs informations personnelles et de les explorer facilement.
- une **API** de prédiction, que le dashboard interactif va pouvoir interroger pour obtenir les données à afficher :
  - score et prédiction d‘octroi de prêt,
  - données descriptives,
  - graphiques permettant de comparer le dossier étudié aux autres.


## Données utilisées
Les données utilisées pour la réalisation du projet sont disponibles à l'adresse suivante : [https://www.kaggle.com/c/home-credit-default-risk/data](https://www.kaggle.com/c/home-credit-default-risk/data)

Ces données se présentent sous la forme d‘une archive compressée de 0,7Go, contenant 10 fichiers aux format CSV. Une fois décompressés pour traitement ils occupent au total 2,7Go et représentent différentes tables de la base de donnée de la société *Prêt à dépenser*. Le schéma des tables est visible ci-dessous.

Parmis les 7 tables de la base de données, on en trouve 2 qui contiennent des informations provenant d‘autres institutions financières.

![https://storage.googleapis.com/kaggle-media/competitions/home-credit/home_credit.png](https://storage.googleapis.com/kaggle-media/competitions/home-credit/home_credit.png)

## Structure du projet
Les fichiers du projet sont structurés de la façon suivante :
```
Racine du projet
├── API                         Dossier projet spécifique à l'API.
│   ├── api.py                  Code source de l'API.
│   ├── data                    Dossier data contenant les données nécessaires à l'API.
│   │   ├── data_prod.ftr       DataFrame des données sérialisées au format Feather.
│   │   └── modele_api.joblib   Modèle prédictif sérialisé au format joblib.
│   ├── Procfile                Fichier de configuration WSGI de Herokuapp.
│   ├── requirements.txt        Fichier de configuration Herokuapp : versions de librairies nécessaires.
│   └── runtime.txt             Fichier de configuration avec la version de Python pour Herokuapp.
├── Dashboard                   Dossier projet spécifique au tableau de bord.
│   ├── dashboard.py            Code source du tableau de bord.
│   └── static                  Dossier pour les fichiers statiques du tableau de bord.
│       └── logo.png            Logo de la société "Prêt à dépenser".
├── LICENSE                     Fichier de license.
└── README.md                   Fichier de présentation du projet.
```

## Démonstration
Le **tableau de bord** et l'**API** ont été développé pour pouvoir fonctionner sur des **serveurs indépendants**.
- Le **tableau de bord**, basé sur la librairie **Streamlit**, a été hébergé pour démonstration sur la plateforme d'intégration proposée par **Streamlit**, en profitant de leur offre gratuite :
 - https://share.streamlit.io/defrenes/p7/main/Dashboard/dashboard.py
- L'**API**, basée sur la librairie **Flask** a été hébergée pour démonstration sur la plateforme d'intégration de **Heroku**, en profitant de leur offre gratuite. Les premiers tests ont été faits sur la plateforme **Pythonanywhere**. Malheureusement, l'une des fonctionnalités (*prédiction*) ne fonctionnait pas correctement en profitant de l'offre gratuite de ce service (probablement en raison de la limitation à 1 thread de cette offre). Tout a donc été migré chez Heroku :
 - https://api-p7-ocr.herokuapp.com
 - L'API n'ayant pas d'interface graphique, il vous faudra communiquer avec les endpoints directement. Vous pouvez par exemple consulter la liste des numéros de dossiers en consultant le lien suivant : https://api-p7-ocr.herokuapp.com/clients

Ces applications sont en ligne et accessibles en date du 7 juin 2022. Le chargement des pages peut prendre un peu de temps, étant donné que les applications sont mises en pause au bout de 30min par les fournisseurs de service lorsqu'elles ne sont pas utilisées.
