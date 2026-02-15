import pytest
from decimal import Decimal
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from employe.models import Employe
from employe.serializers import EmployeSerializer
from employe.forms import EmployeForm


# Tests du modèle Employe
class EmployeModelTest(TestCase):
    """Tests pour le modèle Employe"""
    
    def setUp(self):
        self.employe = Employe.objects.create(
            nom="Jean Dupont",
            email="jean.dupont@example.com",
            poste="Développeur",
            salaire=Decimal("50000.00")
        )
    
    def test_employe_creation(self):
        """Test la création d'un employé"""
        self.assertEqual(self.employe.nom, "Jean Dupont")
        self.assertEqual(self.employe.email, "jean.dupont@example.com")
        self.assertEqual(self.employe.poste, "Développeur")
        self.assertEqual(self.employe.salaire, Decimal("50000.00"))
    
    def test_employe_str(self):
        """Test la méthode __str__ du modèle"""
        self.assertEqual(str(self.employe), "Jean Dupont")
    
    def test_employe_fields(self):
        """Test que tous les champs sont correctement définis"""
        self.assertIsNotNone(self.employe.nom)
        self.assertIsNotNone(self.employe.email)
        self.assertIsNotNone(self.employe.poste)
        self.assertIsNotNone(self.employe.salaire)
    
    def test_email_field_type(self):
        """Test que le champ email est bien un EmailField"""
        field = Employe._meta.get_field('email')
        from django.db.models import EmailField
        self.assertIsInstance(field, EmailField)
    
    def test_salaire_decimal_places(self):
        """Test que le salaire a 2 décimales"""
        field = Employe._meta.get_field('salaire')
        self.assertEqual(field.decimal_places, 2)
        self.assertEqual(field.max_digits, 10)


# Tests du serializer
class EmployeSerializerTest(TestCase):
    """Tests pour le serializer Employe"""
    
    def setUp(self):
        self.employe_data = {
            'nom': 'Marie Martin',
            'email': 'marie.martin@example.com',
            'poste': 'Designer',
            'salaire': '45000.00'
        }
        self.employe = Employe.objects.create(**self.employe_data)
        self.serializer = EmployeSerializer(instance=self.employe)
    
    def test_serializer_contains_expected_fields(self):
        """Test que le serializer contient tous les champs attendus"""
        data = self.serializer.data
        self.assertIn('id', data)
        self.assertIn('nom', data)
        self.assertIn('email', data)
        self.assertIn('poste', data)
        self.assertIn('salaire', data)
    
    def test_serializer_field_content(self):
        """Test que le contenu des champs est correct"""
        data = self.serializer.data
        self.assertEqual(data['nom'], 'Marie Martin')
        self.assertEqual(data['email'], 'marie.martin@example.com')
        self.assertEqual(data['poste'], 'Designer')
        self.assertEqual(data['salaire'], '45000.00')
    
    def test_serializer_with_valid_data(self):
        """Test la validation avec des données valides"""
        serializer = EmployeSerializer(data=self.employe_data)
        self.assertTrue(serializer.is_valid())
    
    def test_serializer_with_invalid_email(self):
        """Test la validation avec un email invalide"""
        invalid_data = self.employe_data.copy()
        invalid_data['email'] = 'email_invalide'
        serializer = EmployeSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('email', serializer.errors)


# Tests du formulaire
class EmployeFormTest(TestCase):
    """Tests pour le formulaire Employe"""
    
    def test_form_with_valid_data(self):
        """Test le formulaire avec des données valides"""
        form_data = {
            'nom': 'Pierre Durand',
            'email': 'pierre.durand@example.com',
            'poste': 'Manager',
            'salaire': '60000.00'
        }
        form = EmployeForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_form_with_missing_nom(self):
        """Test le formulaire sans nom"""
        form_data = {
            'email': 'test@example.com',
            'poste': 'Manager',
            'salaire': '60000.00'
        }
        form = EmployeForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('nom', form.errors)
    
    def test_form_with_invalid_email(self):
        """Test le formulaire avec un email invalide"""
        form_data = {
            'nom': 'Test User',
            'email': 'email_invalide',
            'poste': 'Manager',
            'salaire': '60000.00'
        }
        form = EmployeForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
    
    def test_form_fields(self):
        """Test que le formulaire contient tous les champs nécessaires"""
        form = EmployeForm()
        self.assertIn('nom', form.fields)
        self.assertIn('email', form.fields)
        self.assertIn('poste', form.fields)
        self.assertIn('salaire', form.fields)


# Tests des vues API
class EmployeAPITest(APITestCase):
    """Tests pour les vues API REST"""
    
    def setUp(self):
        self.client = APIClient()
        self.employe1 = Employe.objects.create(
            nom="Alice Bernard",
            email="alice.bernard@example.com",
            poste="Chef de projet",
            salaire=Decimal("55000.00")
        )
        self.employe2 = Employe.objects.create(
            nom="Bob Leroy",
            email="bob.leroy@example.com",
            poste="Analyste",
            salaire=Decimal("48000.00")
        )
        self.valid_payload = {
            'nom': 'Claire Dubois',
            'email': 'claire.dubois@example.com',
            'poste': 'Consultante',
            'salaire': '52000.00'
        }
        self.invalid_payload = {
            'nom': '',
            'email': 'email_invalide',
            'poste': 'Consultante',
            'salaire': '52000.00'
        }
    
    def test_get_all_employes(self):
        """Test la récupération de tous les employés"""
        response = self.client.get('/employe/')
        employes = Employe.objects.all()
        serializer = EmployeSerializer(employes, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(len(response.data), 2)
    
    def test_create_valid_employe(self):
        """Test la création d'un employé avec des données valides"""
        response = self.client.post(
            '/employe/ajouter/',
            data=self.valid_payload,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Employe.objects.count(), 3)
        self.assertEqual(Employe.objects.last().nom, 'Claire Dubois')
    
    def test_create_invalid_employe(self):
        """Test la création d'un employé avec des données invalides"""
        response = self.client.post(
            '/employe/ajouter/',
            data=self.invalid_payload,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Employe.objects.count(), 2)
    
    def test_get_single_employe(self):
        """Test la récupération d'un employé spécifique"""
        response = self.client.get(f'/employe/modifier/{self.employe1.id}/')
        employe = Employe.objects.get(id=self.employe1.id)
        serializer = EmployeSerializer(employe)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
    
    def test_update_employe(self):
        """Test la mise à jour d'un employé"""
        updated_payload = {
            'nom': 'Alice Bernard-Updated',
            'email': 'alice.updated@example.com',
            'poste': 'Directrice',
            'salaire': '65000.00'
        }
        response = self.client.put(
            f'/employe/modifier/{self.employe1.id}/',
            data=updated_payload,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.employe1.refresh_from_db()
        self.assertEqual(self.employe1.nom, 'Alice Bernard-Updated')
        self.assertEqual(self.employe1.salaire, Decimal('65000.00'))
    
    def test_partial_update_employe(self):
        """Test la mise à jour partielle d'un employé"""
        partial_payload = {'salaire': '60000.00'}
        response = self.client.patch(
            f'/employe/modifier/{self.employe1.id}/',
            data=partial_payload,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.employe1.refresh_from_db()
        self.assertEqual(self.employe1.salaire, Decimal('60000.00'))
        self.assertEqual(self.employe1.nom, 'Alice Bernard')  # Nom inchangé
    
    def test_delete_employe(self):
        """Test la suppression d'un employé"""
        response = self.client.delete(f'/employe/supprimer/{self.employe1.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Employe.objects.count(), 1)
        self.assertFalse(Employe.objects.filter(id=self.employe1.id).exists())
    
    def test_get_nonexistent_employe(self):
        """Test la récupération d'un employé inexistant"""
        response = self.client.get('/employe/modifier/9999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_update_nonexistent_employe(self):
        """Test la mise à jour d'un employé inexistant"""
        response = self.client.put(
            '/employe/modifier/9999/',
            data=self.valid_payload,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_delete_nonexistent_employe(self):
        """Test la suppression d'un employé inexistant"""
        response = self.client.delete('/employe/supprimer/9999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


# Tests d'intégration
class EmployeIntegrationTest(APITestCase):
    """Tests d'intégration pour le workflow complet"""
    
    def test_complete_crud_workflow(self):
        """Test le workflow CRUD complet"""
        # Créer un employé
        create_data = {
            'nom': 'David Martin',
            'email': 'david.martin@example.com',
            'poste': 'Ingénieur',
            'salaire': '50000.00'
        }
        create_response = self.client.post(
            '/employe/ajouter/',
            data=create_data,
            format='json'
        )
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        employe_id = create_response.data['id']
        
        # Lire l'employé créé
        read_response = self.client.get(f'/employe/modifier/{employe_id}/')
        self.assertEqual(read_response.status_code, status.HTTP_200_OK)
        self.assertEqual(read_response.data['nom'], 'David Martin')
        
        # Mettre à jour l'employé
        update_data = {
            'nom': 'David Martin',
            'email': 'david.martin@example.com',
            'poste': 'Ingénieur Senior',
            'salaire': '60000.00'
        }
        update_response = self.client.put(
            f'/employe/modifier/{employe_id}/',
            data=update_data,
            format='json'
        )
        self.assertEqual(update_response.status_code, status.HTTP_200_OK)
        self.assertEqual(update_response.data['poste'], 'Ingénieur Senior')
        
        # Supprimer l'employé
        delete_response = self.client.delete(f'/employe/supprimer/{employe_id}/')
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Vérifier que l'employé n'existe plus
        verify_response = self.client.get(f'/employe/modifier/{employe_id}/')
        self.assertEqual(verify_response.status_code, status.HTTP_404_NOT_FOUND)

class EmployeFixtureTest(TestCase):
    fixtures = ['test_data.json']
    
    def test_fixtures_chargees(self):
        """Test que les fixtures sont bien chargées"""
        from employe.models import Employe
        self.assertEqual(Employe.objects.count(), 2)
        self.assertEqual(Employe.objects.get(pk=1).nom, "Aboubakar Vincent")
        self.assertEqual(Employe.objects.get(pk=2).nom, "Emmy Dany")