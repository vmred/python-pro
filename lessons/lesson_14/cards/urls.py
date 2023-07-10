from django.urls import path, include
from rest_framework import routers

from .views.card import CardViewSet

router = routers.DefaultRouter()
router.register(r'cards', CardViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
