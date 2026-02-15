#!/bin/bash

echo "=== DÉMARRAGE DE L'APPLICATION ==="
echo "PORT: $PORT"
echo "Current directory: $(pwd)"
echo "Listing files: $(ls -la)"

echo "=== EXÉCUTION DES MIGRATIONS ==="
python manage.py migrate --noinput
if [ $? -ne 0 ]; then
    echo "❌ ÉCHEC DES MIGRATIONS"
    exit 1
fi
echo "✓ Migrations OK"

echo "=== COLLECTE DES FICHIERS STATIQUES ==="
python manage.py collectstatic --noinput
if [ $? -ne 0 ]; then
    echo "❌ ÉCHEC DE LA COLLECTE STATIC"
    exit 1
fi
echo "✓ Collectstatic OK"

echo "=== DÉMARRAGE DE GUNICORN SUR LE PORT $PORT ==="
exec gunicorn employe_project.wsgi:application \
    --bind 0.0.0.0:$PORT \
    --workers 3 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile - \
    --log-level debug