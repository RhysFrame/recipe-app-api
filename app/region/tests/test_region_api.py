"""
Tests for region APIs.
"""
from create_user import create_user

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Region

from region.serializers import RegionSerializer

REGIONS_URL = reverse('region:region-list')

def detail_url(region_id):
    """Create and return a region detail URL."""
    return reverse('region:region-detail', args=[region_id])

def create_region(user, **params):
    """Create and return a sample region."""
    defaults = {
        'title': 'OTHER',
        'data_type': 'Sample data type',
        'description': 'Sample description',
    }
    defaults.update(params)

    region = Region.objects.create(user=user, **defaults)
    return region

class PublicRegionAPITests(TestCase):
    """Test unauthenticated API requests"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API."""
        res = self.client.get(REGIONS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateRegionApiTests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user()
        self.client.force_authenticate(self.user)

    def test_retrieve_region(self):
        """Test retrieving a list of regions."""
        create_region(user=self.user)
        create_region(user=self.user)

        res = self.client.get(REGIONS_URL)

        regions = Region.objects.all().order_by('-id')
        serializer = RegionSerializer(regions, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_region_list_limited_to_user(self):
        """Test list of regions is limited to authenticated user."""
        other_user = get_user_model().objects.create_user(
            'other@example.com',
            'password123',
        )
        create_region(user=other_user)
        create_region(user=self.user)

        res = self.client.get(REGIONS_URL)

        regions = Region.objects.filter(user=self.user)
        serializer = RegionSerializer(regions, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_region(self):
        """Test creating a region."""
        payload = {
            'title': 'OTHER',
            'data_type': 'Manual',
        }
        res = self.client.post(REGIONS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        region = Region.objects.get(id=res.data['id'])
        for k, v in payload.items():
            self.assertEqual(getattr(region, k), v)
        self.assertEqual(region.user, self.user)

    def test_partial_update(self):
        """Test partial update of a region."""
        original_data_type = 'Harvested'
        region = create_region(
            user=self.user,
            title='NSW',
            data_type=original_data_type,
        )
        payload = {'title': 'SA'}
        url = detail_url(region.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        region.refresh_from_db()
        self.assertEqual(region.title, payload['title'])
        self.assertEqual(region.data_type, original_data_type)
        self.assertEqual(region.user, self.user)

    def invalid_title_returns_error(self):
        """Test that giving an invalid title returns an error."""
        payload = {
            'title': 'NSM',
            'data_type': 'Harvested',
            'description': 'New South Wales spelt wrong',
        }
        res = self.client.post(REGIONS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_full_update(self):
        """Test full update of region."""
        region = create_region(
            user=self.user,
            title='WA',
            data_type='Harvested',
            description='Western Australia region',
        )

        payload = {
            'title': 'QLD',
            'data_type': 'Manual',
            'description': 'Queensland region',
        }

        url = detail_url(region.id)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        region.refresh_from_db()
        for k, v in payload.items():
            self.assertEqual(getattr(region, k), v)
        self.assertEqual(region.user, self.user)

    def test_update_user_returns_error(self):
        """Test changing the region user results in an error."""
        new_user = get_user_model().objects.create_user(
            'other@example.com',
            'password123',
        )
        region = create_region(user=self.user)

        payload = {'user': new_user.id}
        url = detail_url(region.id)
        self.client.patch(url, payload)

        region.refresh_from_db()
        self.assertEqual(region.user, self.user)

    def test_delete_region(self):
        """Test deleting a region successful."""
        region = create_region(user=self.user)

        url = detail_url(region.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Region.objects.filter(id=region.id).exists())

    def test_region_other_users_region_error(self):
        """Test trying to delete another users region gives error."""
        new_user = get_user_model().objects.create_user(
            'other@example.com',
            'password123',
        )
        region = create_region(user=new_user)

        url = detail_url(region.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Region.objects.filter(id=region.id).exists())










