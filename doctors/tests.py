from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from users.models import Address, Specialty, Doctors
from .models import Category, Blogs, Comments
from datetime import date


class BlogTests(TestCase):
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
        self.category = Category.objects.create(name='General Health')

        self.doctor_user = User.objects.create_user(
            username='dr_blog',
            email='drblog@test.com',
            password='testpass123',
            is_doctor=True,
            id_address=self.address
        )
        self.doctor = Doctors.objects.create(user=self.doctor_user, specialty=self.specialty, bio='Test bio')

    def test_create_published_blog(self):
        blog = Blogs.objects.create(
            title='Test Heart Health',
            description='Detailed description about heart health',
            summary='Short summary',
            is_published=True,
            posted_at=date.today(),
            id_category=self.category,
            doctor=self.doctor
        )
        self.assertEqual(blog.title, 'Test Heart Health')
        self.assertTrue(blog.is_published)
        self.assertEqual(str(blog), 'Test Heart Health')

    def test_create_draft_blog(self):
        blog = Blogs.objects.create(
            title='Draft Blog',
            description='Draft content',
            summary='Draft summary',
            is_published=False,
            posted_at=date.today(),
            id_category=self.category,
            doctor=self.doctor
        )
        self.assertFalse(blog.is_published)

    def test_blogs_page(self):
        self.client.login(username='dr_blog', password='testpass123')
        response = self.client.get(reverse('doctor_blogs'))
        self.assertEqual(response.status_code, 200)

    def test_post_comment(self):
        blog = Blogs.objects.create(
            title='Blog for Comments',
            description='Desc',
            summary='Summary',
            is_published=True,
            posted_at=date.today(),
            id_category=self.category,
            doctor=self.doctor
        )
        comment = Comments.objects.create(
            content='Great article!',
            user=self.doctor_user,
            blog=blog
        )
        self.assertEqual(comment.content, 'Great article!')
        self.assertIn('dr_blog', str(comment))
        self.assertIn('Blog for Comments', str(comment))
