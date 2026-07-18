from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from users.models import Address, Specialty, Doctors, Patients
from .models import Status, Time, Appointment
from datetime import date, timedelta


class AppointmentTests(TestCase):
    def setUp(self):
        self.client = Client()
        User = get_user_model()

        self.address = Address.objects.create(
            address_line='123 Test',
            region='Test',
            city='Test',
            code_postal='12345'
        )

        self.specialty = Specialty.objects.create(name='Cardiology', description='Heart')
        self.status = Status.objects.create(status='Waited')
        self.time = Time.objects.create(time='09:00')

        self.doctor_user = User.objects.create_user(
            username='dr_test',
            email='dr@test.com',
            password='testpass123',
            is_doctor=True,
            id_address=self.address
        )
        self.doctor = Doctors.objects.create(user=self.doctor_user, specialty=self.specialty, bio='Test bio')

        self.patient_user = User.objects.create_user(
            username='pat_test',
            email='pat@test.com',
            password='testpass123',
            is_doctor=False,
            id_address=self.address
        )
        self.patient = Patients.objects.create(user=self.patient_user, insurance='Test Insurance')

    def test_book_appointment_page_authenticated(self):
        self.client.login(username='pat_test', password='testpass123')
        response = self.client.get(reverse('book_appointment'))
        self.assertEqual(response.status_code, 200)

    def test_book_appointment_redirects_unauthenticated(self):
        response = self.client.get(reverse('book_appointment'))
        self.assertNotEqual(response.status_code, 200)

    def test_create_appointment(self):
        app = Appointment.objects.create(
            doctor=self.doctor,
            patient=self.patient,
            summary='Checkup',
            description='Regular checkup',
            start_date=date.today() + timedelta(days=1),
            status=self.status,
            time=self.time
        )
        self.assertEqual(app.summary, 'Checkup')
        self.assertEqual(str(app.status), 'Waited')

    def test_appointment_str(self):
        app = Appointment.objects.create(
            doctor=self.doctor,
            patient=self.patient,
            summary='Follow-up',
            description='Follow-up visit',
            start_date=date.today() + timedelta(days=7),
            status=self.status,
            time=self.time
        )
        self.assertEqual(str(app), 'Follow-up')
