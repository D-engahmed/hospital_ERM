from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Address, Specialty, Doctors, Patients


class UserModelTests(TestCase):
    def setUp(self):
        self.address = Address.objects.create(
            address_line='123 Test St',
            region='Test Region',
            city='Test City',
            code_postal='12345'
        )

    def test_create_doctor_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            username='doctor1',
            email='doctor1@test.com',
            password='testpass123',
            first_name='John',
            last_name='Doe',
            is_doctor=True,
            id_address=self.address
        )
        self.assertTrue(user.is_doctor)
        self.assertEqual(user.username, 'doctor1')

    def test_create_patient_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            username='patient1',
            email='patient1@test.com',
            password='testpass123',
            first_name='Jane',
            last_name='Doe',
            is_doctor=False,
            id_address=self.address
        )
        self.assertFalse(user.is_doctor)


class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.address = Address.objects.create(
            address_line='123 Test St',
            region='Test',
            city='Test',
            code_postal='12345'
        )
        self.specialty = Specialty.objects.create(name='Cardiology', description='Heart')

    def test_login_page(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')

    def test_register_page(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')

    def test_register_doctor(self):
        response = self.client.post(reverse('register'), {
            'user_config': 'Doctor',
            'first_name': 'Test',
            'last_name': 'Doctor',
            'username': 'testdoctor',
            'email': 'testdoctor@test.com',
            'gender': 'Male',
            'password': 'testpass123',
            'conf_password': 'testpass123',
            'address_line': '123 Test',
            'region': 'Region',
            'city': 'City',
            'pincode': '12345',
            'Speciality': 'Cardiology',
            'bio': 'Experienced cardiologist',
        }, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_login_with_valid_credentials(self):
        User = get_user_model()
        user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpass123',
            id_address=self.address
        )
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpass123',
        }, follow=True)
        self.assertTrue(response.context['user'].is_authenticated)

    def test_login_with_invalid_credentials(self):
        response = self.client.post(reverse('login'), {
            'username': 'nonexistent',
            'password': 'wrongpassword',
        }, follow=True)
        self.assertFalse(response.context['user'].is_authenticated)
