"""
Serializers for region APIs
"""
from rest_framework import serializers

from core.models import Region


class RegionSerializer(serializers.ModelSerializer):
    """Serializer for regions."""

    class Meta:
        model = Region
        fields = ['id', 'title', 'time_minutes', 'price', 'link']
        read_only_fields = ['id']