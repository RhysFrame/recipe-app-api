"""This is a file to refactor the creating of a test user."""
from django.contrib.auth import get_user_model

def sample_user(email='user@example.com', password='testpass123'):
    """Create a return a new user."""
    return get_user_model().objects.create_user(email, password)