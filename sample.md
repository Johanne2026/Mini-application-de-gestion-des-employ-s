## Ce fichier de notes est utile pour créer "Un projet Django avec le CRUD"

## Introduction
Ce projet permet de créer une application Django pour gérer les employés en mettant en place un CRUD (Créer, Lire, Mettre à jour, Supprimer) grâce aux modèles (models), aux vues (vues) et aux templates.

TECHNOLOGIES UTILISEES : Django


## Etapes et commandes utiles pour un tel projet


- Préparation de l'environnement virtuel
Créer un environnement virtuel qui permet de créer une boîte dans laquelle on va stocker toutes nos dépendances et bibliothèques Django en Python. Cet environnement permet d'isoler toutes les dépendances des dépendances qui se trouvent directement dans notre ordinateur.

Commandes sur le terminal : 
python -m venv env
env\Scripts\activate

- Préparation de l'environnement Django

Vérifier l'installation de python : python - v ou python -version

Installer Django : pip install django

- Démarrer un projet Django : django-admin startproject nom_du_projet .

- Créer une application Django dans un projet Django : python manage.py startapp nom_de_l'application

On peut créer plusieurs applications Django à l'intérieur d'un même projet Django




## Liens utiles

- Pour savoir comment créer et utiliser l'extension "Markdown All in One" pour la prise de notes : 
https://www.youtube.com/watch?v=QTGWDBtgEI4

- Pour le projet lui-même : https://www.youtube.com/watch?v=qRc0aeohMIg&list=PLxPP6vETpb7ZQkHYG_Ic3xLtMTxFcDHtG


## --------------------------------------------------------------------------

## Coté APIs pour la liaison Frontend-Backend

Il faut utiliser le framework "Django Rest Framework".
Commande pour l'installer : pip3 install django djangorestframework

## Etapes

- Préambule
Il faut aller dans le fichier "Settings.py" dans le dossier de notre projet "employe_project", puis au niveau d' "INSTALLED_APPS", ajouter "rest_framework".
On va créer le fichier "serializers" dans le dossier "employe".

-- Le fichier serializers est celui qui va prendre le modèle de base de données Django et le transformer au format JSON avec lequel nous pourrons travailler. 

- Remplir le fichier "serializers" 
  
On va y définir nos classes et fonctions en fonction du modèle de données de notre application.

On peut avoir plusieurs classes de serializers (leur nombre est fonction du nombres de classes dans notre modèle de données).
Dans ce fichier, on va importer nos models.

- Remplir le fichier "urls" dans le dossier "employe"
On fait un import des vues du fichier "views".
Puis on met les urls sous la forme : 
    path('nom_du_modèle_concerné/',views.la_vue.as_view()),

    path('nom_du_modèle_concerné/<int:id>/',views.la_vue.as_view()),


- Remplir le fichier "views" dans le dossier "employe"

On fait un import des modèles de l'application "Employe".
On fait un import des serializers.
On fait un import de "generics" de rest_framework.

On code les classes qui seront utilisées pour l'API qu'ont a importé dans le fichier "urls".

- NOTES PARTICULIERES POUR LES VUES GENERIQUES

En Django REST Framework (DRF), les vues génériques sont des classes prêtes à l’emploi qui couvrent toutes les opérations CRUD.
Voici la liste complète et organisée, avec explications simples.

-- Vues génériques de base

    --- GenericAPIView

    Fournit les fonctionnalités communes :

    - queryset

    - serializer_class

    - lookup_field

    - Ne gère aucune méthode HTTP seule

    - Sert de base aux autres vues génériques

-- Vues de lecture (READ)

    --- ListAPIView

    ➡️ GET uniquement

    Liste tous les objets

    Exemple : GET /employes/

    --- RetrieveAPIView

    ➡️ GET uniquement

    Récupère un seul objet par pk

    GET /employes/1/

-- Vues d’écriture (CREATE / UPDATE / DELETE)

    --- CreateAPIView

    ➡️ POST uniquement

    Créer un nouvel objet

    --- UpdateAPIView

    ➡️ PUT / PATCH

    Modifier un objet existant

    --- DestroyAPIView

    ➡️ DELETE

    Supprimer un objet

-- Vues combinées (les plus utilisées)

    --- ListCreateAPIView

    ➡️ GET + POST

    Lister

    Créer

    Exemple : GET /employes/
              POST /employes/

    --- RetrieveUpdateAPIView

    ➡️ GET + PUT + PATCH

    Lire

    Modifier

    --- RetrieveDestroyAPIView

    ➡️ GET + DELETE

    Lire

    --- RetrieveUpdateDestroyAPIView

    ➡️ GET + PUT + PATCH + DELETE

    👉 CRUD complet sur un seul objet

    Exemple : GET /employes/1/
              PUT /employes/1/
              DELETE /employes/1/

-- ViewSets (encore plus puissants)

    Pas des Generic Views à proprement parler, mais très liés.

    --- ViewSet

    Tu définis manuellement les méthodes (list, create, etc.)

    --- ModelViewSet

    Le plus utilisé

    CRUD complet automatiquement :

    list

    retrieve

    create

    update

    delete

    class EmployeViewSet(ModelViewSet):
        queryset = Employe.objects.all()
        serializer_class = EmployeSerializer


    ➡️ Associé à un router, il crée toutes les URLs.




## Liens utiles

Le lien du tuto : https://www.youtube.com/watch?v=OJdFj5hPAKs