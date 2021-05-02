from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import RealEstate, Property

from property.serializers import PropertySerializer, PropertyDetailSerializer

PROPERTY_URL = reverse('property:property-list')


def detail_url(property_id):
    """Return property detail URL"""
    return reverse('property:property-detail', args=[property_id])


def sample_real_estate(
        user,
        name='Imobiliaria padrão',
        address='Endereço padrão'):
    """Create a sample real state"""
    return RealEstate.objects.create(
        user=user, name=name, address=address
    )


def sample_property(user, **params):
    """Create a sample for property"""
    defaults = {
        'name': 'Imovel Padrão',
        'address': 'Endereço Padrão',
        'description': 'etc',
        'features': 'tex',
        'status': False,
        'type': 'Home',
        'finality': 'residential'}

    defaults.update(params)

    return Property.objects.create(user=user, **defaults)


class PublicPropertyApiTest(TestCase):
    """Test and authenticated property access"""

    def setUp(self):
        """Helper function that run before the tests"""
        self.client = APIClient()

    def test_auth_required(self):
        """Test that authentication is required"""
        res = self.client.get(PROPERTY_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivatePropertyApiTest(TestCase):
    """Test an authenticated recipe API access"""

    def setUp(self):
        """Helper function that run before the tests"""
        self.client = APIClient()
        user = get_user_model()
        self.user = user.objects.create_user(
            'itachidev@company.com',
            'testpass'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_list_property(self):
        """test retrieving a list of property"""
        sample_property(user=self.user)
        sample_property(user=self.user)

        res = self.client.get(PROPERTY_URL)

        properties = Property.objects.all().order_by('-id')
        serializer = PropertySerializer(properties, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        self.assertEqual(res.data, serializer.data)

    def test_property_limited_user(self):
        """Test retrieving properties for authenticate user"""
        user2 = get_user_model().objects.create_user(
            'newdev@company.com',
            'newpassword'
        )

        Property.objects.create(
            user=user2,
            name='Imovel Padrão',
            address='Endereço Padrão',
            description='etc',
            features='tex',
            status=False,
            type='Home',
            finality='residential'
        )

        propert = Property.objects.create(
            user=self.user,
            name='Imovel 1',
            address='Endereço 1',
            description='etc',
            features='tex',
            status=False,
            type='Home',
            finality='residential'
        )

        res = self.client.get(PROPERTY_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], propert.name)

    def test_view_property_detail(self):
        """Test viewing a property detail"""
        propt = sample_property(user=self.user)
        propt.real_estates.add(sample_real_estate(user=self.user))

        url = detail_url(propt.id)
        res = self.client.get(url)

        serializer = PropertyDetailSerializer(propt)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_basic_property(self):
        """Test creating a basic property object"""
        payload = {
            'name': 'Imovel Padrão',
            'address': 'Endereço Padrão',
            'description': 'etc',
            'features': 'tex',
            'status': False,
            'type': 'Home',
            'finality': 'residential'}

        res = self.client.post(PROPERTY_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        propt = Property.objects.get(id=res.data['id'])
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(propt, key))

    def test_create_property_with_real_estate(self):
        """Test create a property with real estate"""
        rlestate1 = sample_real_estate(user=self.user)
        rlestate2 = sample_real_estate(user=self.user)
        payload = {

            'name': 'Imovel x',
            'address': 'Endereço X',
            'description': 'etc...',
            'feature': 'etc...',
            'status': False,
            'type': 'Home',
            'finality': 'residential',
            'real_estates': [rlestate1.id, rlestate2.id]
        }

        res = self.client.post(PROPERTY_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        propert = Property.objects.get(id=res.data['id'])
        rlestates = propert.real_estates.all()

        self.assertEqual(rlestates.count(), 2)
        self.assertIn(rlestate1, rlestates)
        self.assertIn(rlestate2, rlestates)

    def test_partial_update_property(self):
        """Test updating a recipe in patch"""

        propert = sample_property(user=self.user)
        propert.real_estates.add(sample_real_estate(user=self.user))

        new_real_estate = sample_real_estate(
            user=self.user,
            name='Nova Imobiliaria'
        )

        payload = {
            'name': 'Imovel Novo',
            'real_estates': [new_real_estate.id]

        }

        url = detail_url(propert.id)
        self.client.patch(url, payload)

        propert.refresh_from_db()

        self.assertEqual(propert.name, payload['name'])

        rlestates = propert.real_estates.all()

        self.assertEqual(len(rlestates), 1)
        self.assertIn(new_real_estate, rlestates)

    def test_full_update_property(self):
        """Test updating property with put"""

        propert = sample_property(user=self.user)
        propert.real_estates.add(sample_real_estate(user=self.user))

        payload = {
            'name': 'Imovel new 1',
            'address': 'Endereço new 1',
            'description': 'etc...',
            'features': 'etc...',
            'status': False,
            'type': 'Home',
            'finality': 'residential',
        }

        url = detail_url(propert.id)
        self.client.put(url, payload)

        propert.refresh_from_db()

        self.assertEqual(propert.name, payload['name'])
        self.assertEqual(propert.address, payload['address'])
        self.assertEqual(propert.description, payload['description'])
        self.assertEqual(propert.features, payload['features'])
        self.assertEqual(propert.status, payload['status'])
        self.assertEqual(propert.type, payload['type'])
        self.assertEqual(propert.finality, payload['finality'])

        real_estates = propert.real_estates.all()
        self.assertEqual(real_estates.count(), 0)

    def test_filter_recipes_by_tags(self):
        """Test returning recipes with specific tags"""
        propert1 = sample_property(user=self.user, name='Imovel 1')
        propert2 = sample_property(user=self.user, name='Imovel 2')

        real_estetas1 = sample_real_estate(
            user=self.user, name='imobiliaria 1')
        real_estetas2 = sample_real_estate(
            user=self.user, name='imobiliaria 2')

        propert1.real_estates.add(real_estetas1)
        propert2.real_estates.add(real_estetas2)

        propert3 = sample_property(user=self.user, name='Imovel 3')

        res = self.client.get(
            PROPERTY_URL,
            {'real_estates': f'{real_estetas1.id},{real_estetas2.id}'}
        )

        serializer1 = PropertySerializer(propert1)
        serializer2 = PropertySerializer(propert2)
        serializer3 = PropertySerializer(propert3)

        self.assertIn(serializer1.data, res.data)
        self.assertIn(serializer2.data, res.data)
        self.assertNotIn(serializer3.data, res.data)
