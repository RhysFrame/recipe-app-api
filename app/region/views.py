"""
Views for the region APIS.
"""
from rest_framework import (
    viewsets,
    mixins,
    status,
)
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import (
    Region,
    Record,
)
from region import serializers



class RegionViewSet(viewsets.ModelViewSet):
    """View for manage region APIs."""
    serializer_class = serializers.RegionSerializer
    queryset = Region.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve recipes for authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == 'list':
            return serializers.RegionSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new recipe."""
        serializer.save(user=self.request.user)

class RecordViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """Manage records in the database."""
    serializer_class = serializers.RecordSerializer
    queryset = Record.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter queryset to authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-title')
