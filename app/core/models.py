"""
Database models.
"""
from pyexpat import model
from tkinter.tix import Tree
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)

class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, email, password=None, **extra_field):
        """Create, save and return a new user."""
        user = self.model(email=email, **extra_field)
        user.set_password(password)
        user.save(using=self.db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
