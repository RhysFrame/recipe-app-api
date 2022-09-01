"""
Serializers for recipe APIs
"""
from rest_framework import serializers

from core.models import Record


class RecordSerializer(serializers.ModelSerializer):
    """Serializer for records."""

    class Meta:
        model = Record
        fields = ['id', 'title', 'region', 'type', 'link']
        read_only_fields = ['id']

class RecordDetailSerializer(RecordSerializer):
    """Serializer for record detail view."""

    class Meta(RecordSerializer.Meta):
        fields = RecordSerializer.Meta.fields + ['description']