"""
Serializers for artefact APIs.
"""
from rest_framework import serializers

from core.models import Artefact

class ArtefactSerializer(serializers.ModelSerializer):
   """Serializer for Artefacts."""

   class Meta:
       model = Artefact
       fields = ['id', 'title', 'public_id', 'location',
                 'origin', 'type', 'material', 'manufacturer',
                 'manufacture_year', 'markings', 'classification',
                 'provenance', 'notes', 'length', 'height', 'width',
                 'diameter', 'volume', 'weight', 'description']
       read_only_fields = ['id']

class ArtefactDetailSerializer(ArtefactSerializer):
   """Serializer for artefact detail view."""

   class Meta(ArtefactSerializer.Meta):
       fields = ArtefactSerializer.Meta.fields + ['description']