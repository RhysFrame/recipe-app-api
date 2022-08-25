"""
Tests for the records API.
"""
from create_user import create_user

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Record

from region.serializers import RecordSerializer


RECORDS_URL = reverse('region:record-list')

def detail_url(record_id):
    """Create and return a record detail URL."""
    return reverse('region:record-detail', args=[record_id])

class PublicRecordsApiTests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required for retrieving ingredients."""
        res = self.client.get(RECORDS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateRecordsApiTests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.user = create_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_records(self):
        """Test retrieving a list of records"""
        Record.objects.create(user=self.user, title='HMS Sirius')
        Record.objects.create(user=self.user, title='HMS Mermaid')

        res = self.client.get(RECORDS_URL)

        records = Record.objects.all().order_by('-title')
        serializer = RecordSerializer(records, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_records_limited_to_user(self):
        """Test list of records is limited to authenticated user."""
        user2 = create_user(email='user2@example.com')
        Record.objects.create(user=user2, title='SS Yongala')
        record = Record.objects.create(user=self.user, title='AHS Centaur')

        res = self.client.get(RECORDS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['title'], record.title)
        self.assertEqual(res.data[0]['id'], record.id)

    def test_update_record(self):
        """Test updating an ingredient."""
        record = Record.objects.create(user=self.user, title='Hive')

        payload = {'title': 'M24'}
        url = detail_url(record.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        record.refresh_from_db()
        self.assertEqual(record.title, payload['title'])

    def test_delete_record(self):
        """Test deleting a record."""
        record = Record.objects.create(user=self.user, title='HMAS Australia')

        url = detail_url(record.id)
        res = self.client.delete(url)
        record.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        records = Record.objects.filter(user=self.user)
        self.assertFalse(records.exists())
