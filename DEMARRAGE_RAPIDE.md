# 🚀 Démarrage Rapide - Application Gestion des Employés

## Étapes pour lancer l'application

### 1️⃣ Créer des données de test (optionnel)
```bash
python create_sample_data.py
```
Cela créera 8 employés de démonstration.

### 2️⃣ Lancer le serveur
```bash
python manage.py runserver
```

### 3️⃣ Ouvrir l'application
Ouvrez votre navigateur et allez sur :
```
http://127.0.0.1:8000/
```

## 🎯 Fonctionnalités disponibles

### Interface principale
- **Tableau de bord** avec 3 statistiques en temps réel :
  - Total des employés
  - Salaire moyen
  - Nombre de postes différents

### Actions disponibles
- ➕ **Ajouter** un employé (bouton en haut à droite)
- ✏️ **Modifier** un employé (bouton bleu dans le tableau)
- 🗑️ **Supprimer** un employé (bouton rouge dans le tableau)
- 🔍 **Rechercher** par nom, email ou poste (barre de recherche)

### Formulaire d'ajout/modification
- Nom (obligatoire)
- Email (obligatoire, format email validé)
- Poste (obligatoire)
- Salaire (obligatoire, format décimal)

## 🎨 Design

L'interface utilise :
- **Tailwind CSS** pour un design moderne et responsive
- **Font Awesome** pour les icônes
- **Gradient violet/indigo** pour un look professionnel
- **Animations fluides** pour une meilleure expérience utilisateur

## 🧪 Tester l'API directement

Vous pouvez aussi tester l'API REST directement :

### Lister tous les employés
```bash
curl http://127.0.0.1:8000/employe/
```

### Ajouter un employé
```bash
curl -X POST http://127.0.0.1:8000/employe/ajouter/ \
  -H "Content-Type: application/json" \
  -d '{"nom":"Test User","email":"test@example.com","poste":"Testeur","salaire":"45000.00"}'
```

### Modifier un employé (remplacer {id})
```bash
curl -X PUT http://127.0.0.1:8000/employe/modifier/{id}/ \
  -H "Content-Type: application/json" \
  -d '{"nom":"Test Updated","email":"test@example.com","poste":"Testeur Senior","salaire":"50000.00"}'
```

### Supprimer un employé (remplacer {id})
```bash
curl -X DELETE http://127.0.0.1:8000/employe/supprimer/{id}/
```

## 📝 Notes importantes

- L'application fonctionne en mode développement (DEBUG=True)
- Les données sont stockées dans SQLite (db.sqlite3)
- CORS est activé pour permettre les requêtes API
- Aucune authentification n'est requise

## 🐛 En cas de problème

Si le serveur ne démarre pas :
1. Vérifiez que toutes les dépendances sont installées : `pip install -r requirements.txt`
2. Vérifiez que les migrations sont appliquées : `python manage.py migrate`
3. Vérifiez le fichier `.env` existe avec les bonnes variables

Si l'interface ne charge pas les données :
1. Ouvrez la console du navigateur (F12) pour voir les erreurs
2. Vérifiez que le serveur Django est bien lancé
3. Vérifiez que l'URL de l'API est correcte dans le code JavaScript

## ✅ Tout fonctionne !

Vous devriez maintenant voir :
- Une interface moderne avec un dégradé violet
- 8 employés dans le tableau (si vous avez exécuté le script de données de test)
- Des statistiques mises à jour automatiquement
- Un formulaire modal pour ajouter/modifier des employés
