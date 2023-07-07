from django.urls import path

from .views.card import CardView, cards_create_form

urlpatterns = [
    path('cards/', CardView.as_view(http_method_names=['get', 'post']), name='cards'),
    path("cards/create", cards_create_form, name="cards_create_form"),
]
