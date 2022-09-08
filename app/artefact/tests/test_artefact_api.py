"""
Tests for the artefact api.
"""
import tempfile
import os

from PIL import Image

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from create import create_user

from decimal import Decimal

from core.models import Artefact

from artefact.serializers import (
    ArtefactSerializer,
    ArtefactDetailSerializer,
)

ARTEFACTS_URL = reverse('artefact:artefact-list')

def detail_url(artefact_id):
    """Returns detailed url for artefact."""
    return reverse('artefact:artefact-detail', args=[artefact_id])

def image_upload_url(artefact_id):
    """Create and return an image upload URL."""
    return reverse('artefact:artefact-upload-image', args=[artefact_id])

def create_artefact(user, **params):
    """Create artefact"""
    defaults = {
        'title': 'Sample artefact title',
        'public_id': 9,
        'location':'NSW',
        'origin': 'Satara',
        'type': 'Bronze',
        'material': 'Metal',
        'manufacturer': 'Unknown',
        'manufacture_year': '1901',
        'markings': 'Sample marking description.',
        'classification': 'Ships Furniture and Fittings',
        'provenance': 'Donation',
        'notes': 'Sample notes.',
        'length': Decimal('30'),
        'height': Decimal('24'),
        'width': Decimal('7.5'),
        'weight': Decimal('5000'),
    }
    defaults.update(params)

    artefact = Artefact.objects.create(user=user, **defaults)
    return artefact

class PublicArtefactAPITests(TestCase):
    """Class for public API tests."""
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(ARTEFACTS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateArtefactAPITests(TestCase):
    """Class for authenticated API requests."""
    def setUp(self):
        self.client = APIClient()
        self.user = create_user()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_artefacts(self):
        """Test retrieving a list of artefacts."""
        create_artefact(user=self.user)
        create_artefact(user=self.user)

        res = self.client.get(ARTEFACTS_URL)

        artefacts = Artefact.objects.all().order_by('-id')
        serializer = ArtefactSerializer(artefacts, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_artefact_list_limited_to_user(self):
        """Test list of artefacts is limited to authenticated user."""
        other_user = create_user("other@example.com")
        create_artefact(user=other_user)
        create_artefact(user=self.user)

        res = self.client.get(ARTEFACTS_URL)

        artefacts = Artefact.objects.filter(user=self.user)
        serializer = ArtefactSerializer(artefacts, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_artefact_detail(self):
        """Test getting artefact detail."""
        artefact = create_artefact(user=self.user)

        url = detail_url(artefact.id)
        res = self.client.get(url)

        serializer = ArtefactDetailSerializer(artefact)
        self.assertEqual(res.data, serializer.data)

    def test_create_artefact(self):
       """Test creating an artefact."""
       payload = {
            'title': 'Sample artefact',
            'public_id': 70,
            'location':'NSW',
            'origin': 'Satara',
            'type': 'Bronze',
            'material': 'Metal',
            'manufacturer': 'Unknown',
            'manufacture_year': '1901',
            'markings': 'Sample marking description.',
            'classification': 'Ships Furniture and Fittings',
            'provenance': 'Donation',
            'notes': 'Sample notes.',
       }
       res = self.client.post(ARTEFACTS_URL, payload)

       self.assertEqual(res.status_code, status.HTTP_201_CREATED)
       artefact = Artefact.objects.get(id=res.data['id'])
       for k, v in payload.items():
           self.assertEqual(getattr(artefact, k), v)
       self.assertEqual(artefact.user, self.user)


class ImageUploadTests(TestCase):
    """Tests for the image upload API."""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'user@example.com',
            'password123',
        )
        self.client.force_authenticate(self.user)
        self.artefact = create_artefact(user=self.user)

    def tearDown(self):
        self.artefact.image.delete()

    def test_upload_image(self):
        """Test uploading an image to an artefact."""
        url = image_upload_url(self.artefact.id)
        with tempfile.NamedTemporaryFile(suffix='.jpg') as image_file:
            img = Image.new('RGB', (10, 10))
            img.save(image_file, format='JPEG')
            image_file.seek(0)
            payload = {'image': image_file}
            res = self.client.post(url, payload, format='multipart')

        self.artefact.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('image', res.data)
        self.assertTrue(os.path.exists(self.artefact.image.path))

    def test_upload_image_bad_request(self):
        """Test uploading an invalid image."""
        url = image_upload_url(self.artefact.id)
        payload = {'image': 'notanimage'}
        res = self.client.post(url, payload, format='multipart')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


