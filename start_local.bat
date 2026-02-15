@echo off
echo === DEMARRAGE DE L'APPLICATION (MODE LOCAL WINDOWS) ===
echo PORT: %PORT%

echo === EXECUTION DES MIGRATIONS ===
python manage.py migrate --noinput

echo === COLLECTE DES FICHIERS STATIQUES ===
python manage.py collectstatic --noinput

echo === DEMARRAGE DE WAITRESS SUR LE PORT %PORT% ===
waitress-serve --port=%PORT% employe_project.wsgi:application