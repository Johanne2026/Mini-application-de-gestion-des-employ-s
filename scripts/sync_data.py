#!/usr/bin/env python
"""
Script de synchronisation des données
Usage: python scripts/sync_data.py [export|import|status]
"""
import os
import sys
import django
import subprocess
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'employe_project.settings')
django.setup()

def get_fixture_path():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    return f'fixtures/data_{timestamp}.json'

def export_data():
    """Exporte les données actuelles"""
    fixture_path = get_fixture_path()
    print(f"📤 Export des données vers {fixture_path}...")
    
    subprocess.run([
        sys.executable, "manage.py", "dumpdata",
        "--indent", "4",
        "--natural-foreign",
        "--natural-primary",
        "--exclude", "contenttypes",
        "--exclude", "auth.permission",
        "-o", fixture_path
    ])
    
    print(f"✅ Export terminé: {fixture_path}")
    
    # Option Git
    response = input("🔧 Committer sur Git ? (o/n): ")
    if response.lower() == 'o':
        subprocess.run(["git", "add", fixture_path])
        subprocess.run(["git", "commit", "-m", f"Mise à jour données {datetime.now().strftime('%Y-%m-%d %H:%M')}"])
        subprocess.run(["git", "push"])
        print("✅ Données poussées sur Git")

def import_data():
    """Importe la dernière fixture"""
    import glob
    fixtures = glob.glob('fixtures/data_*.json')
    if not fixtures:
        print("❌ Aucune fixture trouvée")
        return
    
    latest = max(fixtures, key=os.path.getctime)
    print(f"📥 Import de {latest}...")
    
    subprocess.run([
        sys.executable, "manage.py", "loaddata",
        latest
    ])
    print("✅ Import terminé")

def show_status():
    """Affiche le statut des fixtures"""
    import glob
    fixtures = glob.glob('fixtures/*.json')
    print(f"📊 {len(fixtures)} fixtures trouvées:")
    for f in sorted(fixtures, key=os.path.getctime, reverse=True)[:5]:
        size = os.path.getsize(f) / 1024
        date = datetime.fromtimestamp(os.path.getctime(f)).strftime('%Y-%m-%d %H:%M')
        print(f"  • {os.path.basename(f)} ({size:.1f} KB) - {date}")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python scripts/sync_data.py [export|import|status]")
        sys.exit(1)
    
    command = sys.argv[1]
    if command == 'export':
        export_data()
    elif command == 'import':
        import_data()
    elif command == 'status':
        show_status()
    else:
        print(f"❌ Commande inconnue: {command}")