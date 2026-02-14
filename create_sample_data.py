"""Script pour créer des données de test"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'employe_project.settings')
django.setup()

from employe.models import Employe
from decimal import Decimal

# Supprimer les données existantes
Employe.objects.all().delete()

# Créer des employés de test
employes_test = [
    {
        'nom': 'Sophie Martin',
        'email': 'sophie.martin@example.com',
        'poste': 'Directrice Technique',
        'salaire': Decimal('75000.00')
    },
    {
        'nom': 'Thomas Dubois',
        'email': 'thomas.dubois@example.com',
        'poste': 'Développeur Full Stack',
        'salaire': Decimal('55000.00')
    },
    {
        'nom': 'Marie Leroy',
        'email': 'marie.leroy@example.com',
        'poste': 'Designer UX/UI',
        'salaire': Decimal('48000.00')
    },
    {
        'nom': 'Pierre Bernard',
        'email': 'pierre.bernard@example.com',
        'poste': 'Chef de Projet',
        'salaire': Decimal('62000.00')
    },
    {
        'nom': 'Julie Petit',
        'email': 'julie.petit@example.com',
        'poste': 'Développeur Frontend',
        'salaire': Decimal('52000.00')
    },
    {
        'nom': 'Lucas Moreau',
        'email': 'lucas.moreau@example.com',
        'poste': 'Développeur Backend',
        'salaire': Decimal('54000.00')
    },
    {
        'nom': 'Emma Rousseau',
        'email': 'emma.rousseau@example.com',
        'poste': 'Product Owner',
        'salaire': Decimal('58000.00')
    },
    {
        'nom': 'Alexandre Laurent',
        'email': 'alexandre.laurent@example.com',
        'poste': 'DevOps Engineer',
        'salaire': Decimal('60000.00')
    }
]

for emp_data in employes_test:
    Employe.objects.create(**emp_data)

print(f"✅ {len(employes_test)} employés créés avec succès!")
print("\nListe des employés:")
for emp in Employe.objects.all():
    print(f"  - {emp.nom} ({emp.poste}) - {emp.salaire}€")
