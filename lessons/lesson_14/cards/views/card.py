from rest_framework import viewsets

from ..models.card import Card
from ..serializers.card import CardSerializer


class CardViewSet(viewsets.ModelViewSet):
    queryset = Card.objects.all()
    serializer_class = CardSerializer
