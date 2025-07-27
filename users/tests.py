
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User

class RegisterViewTests(APITestCase):
    def setUp(self):
        self.register_url = reverse('register')
        self.user_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpass123'
        }

    def test_user_registration_success(self):
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_user_registration_missing_fields(self):
        data = self.user_data.copy()
        data.pop('email')
        response = self.client.post(self.register_url, data)
        # Email is not required by default, so should succeed
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_authenticated_user_can_retrieve_self(self):
        user = User.objects.create_user(username='getuser', email='getuser@example.com', password='getpass123')
        self.client.login(username='getuser', password='getpass123')
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'getuser')

    def test_unauthenticated_user_can_retrieve(self):
        response = self.client.get(self.register_url)
        # With AllowAny, unauthenticated GET should succeed
        self.assertEqual(response.status_code, status.HTTP_200_OK)
