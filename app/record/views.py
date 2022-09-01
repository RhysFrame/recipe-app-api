"""
Views for the recipe APIs.
"""
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Record
from record import serializers


class RecordViewSet(viewsets.ModelViewSet):
    """View for manage record APIs."""
    serializer_class = serializers.RecordSerializer
    queryset = Record.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve records for authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def get_serializer_class(self):
        """Return the serialier class for request."""
        if self.action == 'list':
            return serializers.RecordSerializer

        return self.serializer_class