"""This is a file to refactor the creating of a test user."""
from django.contrib.auth import get_user_model
from core.models import Region

def create_user(email='user@example.com', password='testpass123'):
    """Create and return user."""
    return get_user_model().objects.create_user(email=email, password=password)