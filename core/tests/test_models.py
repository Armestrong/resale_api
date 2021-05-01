from django.test import TestCase
from django.contrib.auth import get_user_model


# from core import models


class ModelTest(TestCase):

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
