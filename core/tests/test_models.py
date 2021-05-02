from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def sample_user(email='arms@devapp.com', password='testpass'):
    """Create a simple user"""
    return get_user_model().objects.create_user(email, password)


class ModelTest(TestCase):

    # Tests for user creation
    def test_create_user_with_email(self):
        """Test creating a new user with an email successfully"""
        email = 'dev@appdev.com'
        password = 'password'
        user = get_user_model().objects.create_user(
            email=email,
            password=password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email normalized for a new user"""
        email = "dev@APPCOMPANY.COM"
        user = get_user_model().objects.create_user(email, 'testdev')
        self.assertEqual(user.email, email.lower())

    def test_new_email_user_invalid(self):
        """Test create a user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'bademail')

    def test_create_new_superuser(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            'dev@hotmail.com',
            'testsuperuser'
        )

        self.assertTrue(user.is_superuser)

    # Test for real estate
    def test_real_estate_str(self):
        """Test the real estate string representation"""
        real_estate = models.RealEstate.objects.create(
            name='Imobiliaria SBC',
            address='Rua Mirage',
            user=sample_user(),

        )

        self.assertEqual(str(real_estate), real_estate.name)

    # Test for property
    def test_property_str(self):
        """Test the recipe string representation"""
        recipe = models.Property.objects.create(
            user=sample_user(),
            name='Imovel x',
            address='Imobiliaria x',
            description='Etc ...',
            features='etc...',
            status=False,
            type='Casa',
            finality='residencial'
        )

        self.assertEqual(str(recipe), recipe.name)
