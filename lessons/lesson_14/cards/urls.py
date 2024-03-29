from django.urls import path

from .views.card import CardView, activate_card, activate_card_task, deactivate_card, get_expired_cards

urlpatterns = [
    path('cards/', CardView.as_view(), name='cards'),
    path("cards/<int:pk>", CardView.as_view()),
    path('cards/activate/<int:pk>', activate_card),
    path('cards/tasks/activate/<int:pk>', activate_card_task),
    path('cards/expired', get_expired_cards),
    path('cards/deactivate/<int:pk>', deactivate_card),
]
