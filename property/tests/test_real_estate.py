from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import RealEstate, Property

from property.serializers import RealEstateSerializer

REAL_ESTATE_URL = reverse('property:realestate-list')


class PublicRealEstatesApiTest(TestCase):
    """Test public available real estates API"""

    def setUp(self):
        """Helper function that run before the tests"""
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required to access the endpoint"""

        res = self.client.get(REAL_ESTATE_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRealEstateApiTest(TestCase):
    """Test Real estate can be retrieved by authorized user"""

    def setUp(self):
        """Helper function that runs before the tests"""
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'itachidev@company.com',
            'testpass'
        )

        self.client.force_authenticate(self.user)

    def test_retrieve_real_estates_list(self):
        """Test retrieve the real-estates list for the authenticated user"""

        RealEstate.objects.create(
            user=self.user,
            name='Imobiliaria SP',
            address='Rua Carlos dias n150'
        )
        RealEstate.objects.create(
            user=self.user,
            name='Imobiliaria SBC',
            address='Vila Duzzi'
        )

        res = self.client.get(REAL_ESTATE_URL)
        real_estates = RealEstate.objects.all().order_by('-name')
        serializer = RealEstateSerializer(real_estates, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_real_estates_limited_for_user(self):
        """Test that 'real estate' can be only return for authenticated user"""

        user2 = get_user_model().objects.create_user(
            'devtwo@company.com',
            'passwordtwo'
        )

        RealEstate.objects.create(
            user=user2,
            name='Imobiliaria Calazans',
            address='Avenida Borges')

        real_estate = RealEstate.objects.create(
            user=self.user,
            name='Imobiliaria Macedo',
            address='Avenida Torres')

        res = self.client.get(REAL_ESTATE_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)

        self.assertEqual(res.data[0]['name'], real_estate.name)

    def test_create_real_estate_successfully(self):
        """Test that the authenticated user create a realestate successfully"""

        payload = {
            'name': 'Imobiliaria São Caetano',
            'address': 'Jundiai n2344'
        }

        self.client.post(REAL_ESTATE_URL, payload)

        exists = RealEstate.objects.filter(
            user=self.user,
            name=payload['name']
        ).exists()

        self.assertTrue(exists)

    def test_create_real_estate_invalid(self):
        """Test create a invalid real estate"""
        payload = {
            'name': '',
            'address': ''
        }

        res = self.client.post(REAL_ESTATE_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_real_estate_unique_item(self):
        """Test that retrieve a unique item for the authenticated user"""
        realestate = RealEstate.objects.create(
            user=self.user,
            name='Imobiliaria Zeus',
            address='Avenida R'
        )

        RealEstate.objects.create(
            user=self.user,
            name='Imobiliaria Carlos',
            address='Avenida GT'
        )

        properties1 = Property.objects.create(
            user=self.user,
            name='Imovel 1',
            address='Endereço 1',
            description='etc',
            features='tex',
            status=False,
            type='Home',
            finality='residential'
        )
        properties2 = Property.objects.create(
            user=self.user,
            name='Imovel 1',
            address='Endereço 1',
            description='etc',
            features='tex',
            status=False,
            type='Home',
            finality='residential'
        )

        properties1.real_estates.add(realestate)
        properties2.real_estates.add(realestate)

        res = self.client.get(REAL_ESTATE_URL, {'assigned_only': 1})
        self.assertEqual(len(res.data), 1)

    def test_retrieve_real_estates_assigned_to_properties(self):
        """Test filtering real estates by those assigned to properties"""
        realestate1 = RealEstate.objects.create(
            user=self.user,
            name='Imobiliaria Zeus',
            address='Avenida R'
        )
        realestate2 = RealEstate.objects.create(
            user=self.user,
            name='Imobiliaria Thor',
            address='Avenida X'
        )

        properties = Property.objects.create(
            user=self.user,
            name='Imovel 1',
            address='Endereço 1',
            description='etc',
            features='tex',
            status=False,
            type='Home',
            finality='residential'
        )

        properties.real_estates.add(realestate1)

        res = self.client.get(REAL_ESTATE_URL, {'assigned_only': 1})

        serializer1 = RealEstateSerializer(realestate1)
        serializer2 = RealEstateSerializer(realestate2)

        self.assertIn(serializer1.data, res.data)
        self.assertNotIn(serializer2.data, res.data)
