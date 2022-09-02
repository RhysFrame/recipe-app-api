"""
Views for the Artefact APIs.
"""
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Artefact
from artefact import serializers

class ArtefactViewSet(viewsets.ModelViewSet):
    """View for manage artefact APIs."""
    serializer_class = serializers.ArtefactDetailSerializer
    queryset = Artefact.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve objects for authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-id')
    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == 'list':
            return serializers.ArtefactSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new artefact."""
        serializer.save(user=self.request.user)
