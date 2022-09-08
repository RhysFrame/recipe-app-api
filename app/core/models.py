"""
Database models.
"""
import uuid
import os

from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)

def artefact_image_file_path(instance, filename):
    """Generate file path for new artefact image."""
    ext = os.path.splitext(filename)[1]
    filename = f'{uuid.uuid4()}{ext}'

    return os.path.join('uploads', 'recipe', filename)

def recipe_image_file_path(instance, filename):
    """Generate file path for new recipe image."""
    ext = os.path.splitext(filename)[1]
    filename = f'{uuid.uuid4()}{ext}'

    return os.path.join('uploads', 'recipe', filename)


class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user."""
        if not email:
            raise ValueError('User must have an email address.')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and return a new superuser."""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Recipe(models.Model):
    """Recipe object."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    time_minutes = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    link = models.CharField(max_length=255, blank=True)
    tags = models.ManyToManyField('Tag')
    ingredients = models.ManyToManyField('Ingredient')
    image = models.ImageField(null=True, upload_to=recipe_image_file_path)

    def __str__(self):
        return self.title


class Tag(models.Model):
    """Tag for filtering recipes."""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Ingredient for recipes."""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name


class Record(models.Model):
    """Record object."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=255)
    region = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    link = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.title

class Artefact(models.Model):
    """Artefact object."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=255)
    public_id = models.IntegerField()
    location = models.CharField(max_length=255)
    origin = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    material = models.CharField(max_length=255)
    manufacturer = models.CharField(max_length=255)
    manufacture_year = models.CharField(max_length=255)
    markings = models.TextField(blank=True)
    classification = models.CharField(max_length=255)
    provenance = models.CharField(max_length=255)
    notes = models.TextField(blank=True)
    length = models.DecimalField(max_digits=10, decimal_places=3, null=True)
    height = models.DecimalField(max_digits=10, decimal_places=3, null=True)
    width = models.DecimalField(max_digits=10, decimal_places=3, null=True)
    diameter = models.DecimalField(max_digits=10, decimal_places=3, null=True)
    volume = models.DecimalField(max_digits=10, decimal_places=3, null=True)
    weight = models.DecimalField(max_digits=10, decimal_places=3, null=True)
    description = models.TextField(blank=True)
    image = models.ImageField(null=True, upload_to=recipe_image_file_path)

    def __str__(self):
        return self.title


class Shipwreck(models.Model):
    """Shipwreck object."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=255)
    public_id = models.IntegerField()
    location = models.CharField(max_length=255)
    vessel_type = models.CharField(max_length=255)
    rig_type = models.CharField(max_length=255)
    year_wrecked = models.CharField(max_length=255)
    region = models.CharField(max_length=255)
    weight = models.DecimalField(max_digits=10, decimal_places=3, null=True)
    gen_history = models.TextField(blank=True)

    def __str__(self):
        return self.title

class Aircraft(models.Model):
    """Aircraft object."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=255)
    public_id = models.IntegerField()
    location = models.CharField(max_length=255)
    vessel_type = models.CharField(max_length=255)
    year_wrecked = models.CharField(max_length=255)
    region = models.CharField(max_length=255)
    weight = models.DecimalField(max_digits=10, decimal_places=3, null=True)
    gen_history = models.TextField(blank=True)

    def __str__(self):
        return self.title
