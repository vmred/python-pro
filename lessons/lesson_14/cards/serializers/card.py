from rest_framework import serializers

from ..models.card import Card


class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ['id', 'pan', 'expiry_date', 'issue_date', 'cvv', 'owner_id', 'status']
        read_only_fields = ['created_at', 'updated_at']
