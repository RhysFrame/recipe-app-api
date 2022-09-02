"""
Tests for record APIs.
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Record

from record.serializers import (
    RecordSerializer,
    RecordDetailSerializer,
)

RECORDS_URL = reverse('record:record-list')

def detail_url(record_id):
    """Create and return a record detail URL."""
    return reverse('record:record-detail', args=[record_id])

def create_record(user, **params):
    """Create and return a sample record."""
    defaults = {
        'title': 'Sample record title',
        'region': 'Sample region',
        'type': 'Sample type',
        'description': 'Sample description',
        'link': 'http://example.com/record.pdf'
    }
    defaults.update(params)

    record = Record.objects.create(user=user, **defaults)
    return record

class PublicRecordAPITests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API."""
        res = self.client.get(RECORDS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateRecordAPITests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'user@example.com',
            'testpass123',
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_records(self):
        """Test retrieving a list of records."""
        create_record(user=self.user)
        create_record(user=self.user)

        res = self.client.get(RECORDS_URL)

        records = Record.objects.all().order_by('-id')
        serializer = RecordSerializer(records, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_record_list_limited_to_user(self):
        """Test list of records is limited to authenticated user."""
        other_user = get_user_model().objects.create_user(
            'other@example.com',
            'pass123',
        )
        create_record(user=other_user)
        create_record(user=self.user)

        res = self.client.get(RECORDS_URL)

        records = Record.objects.filter(user=self.user)
        serializer = RecordSerializer(records, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_record_detail(self):
        """Test get record detail."""
        record = create_record(user=self.user)

        url = detail_url(record.id)
        res = self.client.get(url)

        serializer = RecordDetailSerializer(record)
        self.assertEqual(res.data, serializer.data)

    def test_create_record(self):
        """Test creating a record."""
        payload = {
            'title': 'Sample record',
            'region': 'Sample region',
            'type': 'Sample type',
        }
        res = self.client.post(RECORDS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        record = Record.objects.get(id=res.data['id'])
        for k, v in payload.items():
            self.assertEqual(getattr(record, k), v)
        self.assertEqual(record.user, self.user)
