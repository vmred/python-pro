from django.urls import path

from .views.card import CardView

urlpatterns = [
    path('cards/', CardView.as_view(http_method_names=['get', 'post']), name='cards'),
]
