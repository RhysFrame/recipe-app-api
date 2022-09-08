"""
Tests for the shipwreck API.
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from decimal import Decimal

from rest_framework import status
from rest_framework.test import APIClient
from create_user import create_user

from core.models import Shipwreck

from shipwreck.serializers import (
    ShipwreckSerializer,
    ShipwreckDetailSerializer,
)

SHIPWRECKS_URL = reverse('shipwreck:shipwreck-list')

def detail_url(shipwreck_id):
    return reverse('shipwreck:shipwreck-detail', args=[shipwreck_id])


def create_shipwreck(user, **params):
    defaults = {
        'title':' Satara',
        'public_id':2356,
        'location':'NSW',
        'vessel_type':'Screw Steamer',
        'rig_type':'Sample rig type',
        'year_wrecked':'1910',
        'region':'Hunter',
        'weight': Decimal('5272.0'),
        'gen_history': 'Sample general history'
    }
    defaults.update(params)

    shipwreck = Shipwreck.shipwrecks.create(user=user, **defaults)
    return shipwreck

class PublicShipwreckAPITests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(SHIPWRECKS_URL)
        self.assertEqual(res.status_code,status.HTTP_401_UNAUTHORIZED)

class PrivateShipwreckAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = create_user()
        self.client.force_authenticated(self.user)
    def test_retrieve_shipwrecks(self):
        create_shipwreck(user=self.user)
        create_shipwreck(user=self.user)

        res = self.client.get(SHIPWRECKS_URL)

        shipwrecks = Shipwreck.objects.all().order_by('-id')
        serializer = ShipwreckSerializer(shipwrecks, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_shipwreck_list_limited_to_user(self):
        """Test shipwreck list is limited to authenticated user."""
        other_user = create_user('other@example.com')
        create_shipwreck(user=other_user)
        create_shipwreck(user=self.user)

        res = self.client.get(SHIPWRECKS_URL)

        objects = Shipwreck.objects.filter(user=self.user)
        serializer = ShipwreckSerializer(objects, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_shipwreck_detail(self):
        "Test getting shipwreck detail."
        object = create_shipwreck(user=self.user)

        url = detail_url(object.id)
        res = self.client.get(url)

        serializer = ShipwreckDetailSerializer(object)
        self.assertEqual(res.data, serializer.data)

    def test_create_object(self):
        """Test creating an object."""
        payload = {
            'title':' Satara',
            'public_id':2356,
            'location':'NSW',
            'vessel_type':'Screw Steamer',
            'rig_type':'Sample rig type',
            'year_wrecked':'1910',
            'region':'Hunter',
            'weight': Decimal('5272.0'),
            'gen_history': 'Sample general history'
        }
        res = self.client.post(SHIPWRECKS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        shipwreck = Shipwreck.objects.get(id=res.data['id'])
        for k, v in payload.items():
            self.assertEqual(getattr(shipwreck, k), v)
            self.assertEqual(object.user, self.user)

