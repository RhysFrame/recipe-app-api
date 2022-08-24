"""
Tests for region APIs.
"""
from create_user import create_user

from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Region

from region.serializers import RegionSerializer

REGIONS_URL = reverse('region:region-list')

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
        serializer = RegeionSerializer(regions, many=True)
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





