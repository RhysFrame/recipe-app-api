"""
URL mappings for the artefact app.
"""
from django.urls import (
    path,
    include,
)
from rest_framework.routers import DefaultRouter

from artefact import views

router = DefaultRouter()
router.register('artefacts', views.ArtefactViewSet)

app_name = 'artefact'

urlpatterns = [
    path('', include(router.urls)),
]
