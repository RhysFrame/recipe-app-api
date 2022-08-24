"""
Tests for region APIs.
"""
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Region

from region.serializers import RegionSerializer

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


