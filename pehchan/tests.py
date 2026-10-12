from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.management import call_command
from datetime import date, timedelta
from io import StringIO
from pehchan.models import Event


class PublicViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home_page(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_about_page(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)

    def test_public_events_page(self):
        response = self.client.get(reverse('public_events'))
        self.assertEqual(response.status_code, 200)

    def test_volunteer_info_page(self):
        response = self.client.get(reverse('public_volunteer'))
        self.assertEqual(response.status_code, 200)

    def test_donate_info_page(self):
        response = self.client.get(reverse('public_donate'))
        self.assertEqual(response.status_code, 200)

    def test_certificate_verify_page(self):
        response = self.client.get(reverse('public_certificate_verify'))
        self.assertEqual(response.status_code, 200)


class AuthenticationTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword123',
            email='testuser@example.com'
        )

    def test_login_page_get(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_signup_page_get(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)

    def test_user_login_valid(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpassword123'
        })
        # Successful login redirects to dashboard
        self.assertEqual(response.status_code, 302)

    def test_user_login_invalid(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)


class EventModelTestCase(TestCase):
    def test_event_status_calculation(self):
        today = date.today()
        upcoming = Event.objects.create(
            name='Future Camp',
            description='Test event',
            event_date=today + timedelta(days=5),
            location='Mumbai'
        )
        self.assertEqual(upcoming.status, 'upcoming')

        past = Event.objects.create(
            name='Past Drive',
            description='Old event',
            event_date=today - timedelta(days=5),
            location='Pune'
        )
        self.assertEqual(past.status, 'completed')


class ManagementCommandTestCase(TestCase):
    def test_create_admin_user_command(self):
        out = StringIO()
        call_command(
            'create_admin_user',
            username='cmdadmin',
            email='cmdadmin@example.com',
            password='cmdpassword123',
            stdout=out
        )
        self.assertTrue(User.objects.filter(username='cmdadmin').exists())
        user = User.objects.get(username='cmdadmin')
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
