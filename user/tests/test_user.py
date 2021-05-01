from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

# from core import models

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')


# ME_URL = reverse('user:me')


def create_user(**params):
    """Helper func that create a new user"""
    return get_user_model().objects.create_user(**params)


class PublicUserApiTest(TestCase):  # Test the user API public

    def setUp(self):
        """Create a set up that run before the tests"""
        self.client = APIClient()

    # Test create a user
    def test_create_valid_user(self):
        """Test create a new user with payload successfully"""

        payload = {
            'email': 'dev@company.com',
            'password': 'testpass',
            'name': 'testname'
        }

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_create_user_exists(self):
        """Test create a user that already exist fails"""

        payload = {
            'email': 'arms@devapp.com',
            'password': 'passtest'
        }

        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test create a new user with a short pass fails"""
        payload = {
            'email': 'dev@company.com',
            'password': 'p'
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    # Test create and validated a token
    def test_create_token_for_user(self):
        """Test create token fort the user"""
        payload = {
            'email': 'dev@company.com',
            'password': 'narutouzumaki'
        }

        create_user(**payload)

        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
