"""
File for creation methods.
"""
from django.contrib.auth import get_user_model

def create_user(email='user@example.com', password='testpass123'):
    """Create and return a new user."""
    return get_user_model().objects.create_user(email=email, password=password)