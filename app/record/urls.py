"""
URL mappings for the record app.
"""
from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from record import views


router = DefaultRouter()
router.register('records', views.RecordViewSet)

app_name = 'record'

urlpatterns = [
    path('', include(router.urls)),
]