from django.urls import path
from .views.card import CardView, activate_card, deactivate_card

urlpatterns = [
    path('cards/', CardView.as_view()),
    path("cards/<int:pk>", CardView.as_view()),
    path('cards/activate/<int:pk>', activate_card),
    path('cards/deactivate/<int:pk>', deactivate_card)
]
