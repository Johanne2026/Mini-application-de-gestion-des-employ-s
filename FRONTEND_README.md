# Frontend - Gestion des Employés

## 🚀 Démarrage rapide

### 1. Installer les dépendances (si ce n'est pas déjà fait)
```bash
pip install -r requirements.txt
```

### 2. Appliquer les migrations
```bash
python manage.py migrate
```

### 3. Lancer le serveur de développement
```bash
python manage.py runserver
```

### 4. Accéder à l'application
Ouvrez votre navigateur et allez sur : **http://127.0.0.1:8000/**

## ✨ Fonctionnalités

- ✅ Interface moderne et épurée avec Tailwind CSS
- ✅ Tableau de bord avec statistiques en temps réel
- ✅ Ajouter, modifier et supprimer des employés
- ✅ Recherche en temps réel par nom, email ou poste
- ✅ Design responsive (mobile, tablette, desktop)
- ✅ Notifications visuelles pour chaque action
- ✅ Animations fluides et interface intuitive

## 🎨 Technologies utilisées

- **Backend** : Django 5.1.6 + Django REST Framework
- **Frontend** : HTML5, JavaScript (Vanilla), Tailwind CSS
- **Icons** : Font Awesome 6
- **Base de données** : SQLite

## 📱 Captures d'écran

L'interface comprend :
- Un en-tête avec le titre et bouton d'ajout
- 3 cartes de statistiques (Total employés, Salaire moyen, Postes différents)
- Une barre de recherche
- Un tableau avec tous les employés
- Un modal pour ajouter/modifier des employés

## 🔧 Structure des fichiers

```
employe/
├── templates/
│   └── employe/
│       └── index.html          # Page principale du frontend
├── views.py                     # Vue pour servir le frontend
├── urls.py                      # Routes de l'application
├── models.py                    # Modèle Employe
├── serializers.py               # Serializer REST
└── ...
```

## 🌐 API Endpoints

- `GET /employe/` - Liste tous les employés
- `POST /employe/ajouter/` - Créer un nouvel employé
- `GET /employe/modifier/{id}/` - Récupérer un employé
- `PUT /employe/modifier/{id}/` - Modifier un employé
- `DELETE /employe/supprimer/{id}/` - Supprimer un employé

## 💡 Notes

- L'application utilise CORS pour permettre les requêtes API
- Aucune authentification n'est requise (mode développement)
- Les données sont stockées dans SQLite (db.sqlite3)
