"""
URL mappings for the region app.
"""
from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from region import views



router = DefaultRouter()
router.register('regions', views.RegionViewSet)
router.register('records', views.RecordViewSet)

app_name = 'region'

urlpatterns = [
    path('', include(router.urls)),
]