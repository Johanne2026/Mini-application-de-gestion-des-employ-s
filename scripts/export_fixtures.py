#!/usr/bin/env python
import os
import sys
import django
from datetime import datetime
from django.core.management import call_command


# Configuration
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'employe_project.settings')
django.setup()


def export_fixtures():
    """Exporte les données avec un timestamp"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Créer le dossier fixtures s'il n'existe pas
    os.makedirs('fixtures', exist_ok=True)
    
    # Export complet
    filename = f'fixtures/backup_{timestamp}.json'
    with open(filename, 'w') as f:
        call_command('dumpdata', 
                    indent=4,
                    natural_foreign=True,
                    natural_primary=True,
                    stdout=f)
    
    print(f"✅ Données exportées vers {filename}")
    
    # Export spécifique à l'app employe
    app_filename = f'fixtures/employes_{timestamp}.json'
    with open(app_filename, 'w') as f:
        call_command('dumpdata', 'employe',
                    indent=4,
                    stdout=f)
    
    print(f"✅ Données employe exportées vers {app_filename}")

if __name__ == '__main__':
    export_fixtures()