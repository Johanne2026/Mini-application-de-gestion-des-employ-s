#!/usr/bin/env python
import os
import sys
import django
import glob

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'employe_project.settings')
django.setup()

from django.core.management import call_command

def import_latest_fixture():
    """Importe la fixture la plus récente"""
    fixtures = glob.glob('fixtures/*.json')
    if not fixtures:
        print("❌ Aucune fixture trouvée")
        return
    
    # Prendre la plus récente
    latest = max(fixtures, key=os.path.getctime)
    print(f"📦 Import de {latest}...")
    
    try:
        call_command('loaddata', latest)
        print(f"✅ Import réussi depuis {latest}")
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == '__main__':
    import_latest_fixture()