"""
Serializers for region APIs
"""
from rest_framework import serializers

from core.models import (
    Region,
    Record,
)

class RecordSerializer(serializers.ModelSerializer):
    """Serializer for records."""

    class Meta:
        model = Record
        fields = ['id', 'title']
        read_only_fields = ['id']


class RegionSerializer(serializers.ModelSerializer):
    """Serializer for regions."""

    class Meta:
        model = Region
        fields = ['id', 'title', 'data_type', 'description']
        read_only_fields = ['id']

