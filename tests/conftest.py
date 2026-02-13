import os
import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from employe.models import Employe
from decimal import Decimal

# Configuration de Django pour pytest
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'employe_project.settings')

@pytest.fixture
def api_client():
    """Fixture pour créer un client API non authentifié"""
    return APIClient()

@pytest.fixture
def authenticated_client(api_client):
    """Fixture pour créer un client API authentifié"""
    user, created = User.objects.get_or_create(
        username='testuser',
        defaults={'password': 'testpass123'}
    )
    if created:
        user.set_password('testpass123')
        user.save()
    
    client = APIClient()
    client.force_authenticate(user=user)
    return client

@pytest.fixture
def sample_employe():
    """Fixture pour créer un employé exemple"""
    return Employe.objects.create(
        nom="Jean Dupont",
        email="jean.dupont@example.com",
        poste="Développeur",
        salaire=Decimal("50000.00")
    )

@pytest.fixture
def sample_employe_data():
    """Fixture pour des données d'employé valides"""
    return {
        'nom': 'Marie Martin',
        'email': 'marie.martin@example.com',
        'poste': 'Designer',
        'salaire': '45000.00'
    }

@pytest.fixture
def multiple_employes():
    """Fixture pour créer plusieurs employés"""
    employe1 = Employe.objects.create(
        nom="Alice Bernard",
        email="alice.bernard@example.com",
        poste="Chef de projet",
        salaire=Decimal("55000.00")
    )
    employe2 = Employe.objects.create(
        nom="Bob Leroy",
        email="bob.leroy@example.com",
        poste="Analyste",
        salaire=Decimal("48000.00")
    )
    return [employe1, employe2]