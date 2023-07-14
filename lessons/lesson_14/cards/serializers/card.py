from rest_framework import serializers

from ..models.card import Card


class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = '__all__'


class UpdateCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ['printed_name']
