from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')


def create_user(**params):
    """Helper func that create a new user"""
    return get_user_model().objects.create_user(**params)


class PublicUserApiTest(TestCase):  # Test the user API public

    def setUp(self):
        """Create a set up that run before the tests"""
        self.client = APIClient()

    # Test create a user with user endpoint
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

    # Test create and validate a token with token endpoint
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

    def test_create_token_invalid_credential(self):
        """Test token that is not created if invalid credentials are given """
        create_user(email='arms@devcompany.com', password='testpass')
        payload = {'email': 'arms@devcompany.com', 'password': 'wrong'
                   }

        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """Test that email and password are required"""
        payload = {'email': 'one', 'password': ''}
        create_user(**payload)

        res = self.client.post(TOKEN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self):
        """Test that authentication is required for users"""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTest(TestCase):
    """Test Api that require authentication"""

    def setUp(self):
        """Helper funcion that create and force an authentication"""
        self.user = create_user(
            email='dev@company.com',
            password='testpassword',
            name='test full name'
        )

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """Test retrieving profile for logged user"""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {'name': self.user.name,
                                    'email': self.user.email})

#     def test_post_me_not_allowed(self):
        """Test that POST is not allowed on 'me' URL"""
        res = self.client.post(ME_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """Test updating the user profile for authenticated user"""
        payload = {'email': 'newdev@newcompany.com', 'password': 'newpass'}

        res = self.client.patch(ME_URL, payload)

        self.user.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.email, payload['email'])
        self.assertTrue(self.user.check_password(payload['password']))
