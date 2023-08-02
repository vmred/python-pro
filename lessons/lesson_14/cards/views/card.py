from datetime import date

from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models.card import Card, Status
from ..permissions import IsOwner
from ..serializers.card import CardSerializer, UpdateCardSerializer
from ..tasks import task_activate_card


def object_exists(model, request, pk):
    try:
        return model.objects.get(owner=request.user, pk=pk)
    except model.DoesNotExist:
        return None


def get_expired_cards(request):
    cards = Card.objects.filter(~Q(status=Status.BLOCKED), expiry_date__lt=date.today())
    return JsonResponse(CardSerializer(cards, many=True).data, safe=False)


def activate_card_task(request, pk):
    card = object_exists(model=Card, request=request, pk=pk)
    if not card:
        return JsonResponse({}, status=status.HTTP_400_BAD_REQUEST)

    task_activate_card.apply_async(args=[pk], countdown=120)

    return JsonResponse({'success': True})


def activate_card(request, pk):
    card = object_exists(model=Card, request=request, pk=pk)
    if not card:
        return JsonResponse({}, status=status.HTTP_400_BAD_REQUEST)

    Card.activate_card(pk)
    return JsonResponse({'success': True})


def deactivate_card(request, pk):
    card = object_exists(model=Card, request=request, pk=pk)
    if not card:
        return JsonResponse({}, status=status.HTTP_400_BAD_REQUEST)

    Card.deactivate_card(pk)
    return JsonResponse({'success': True})


class CardView(APIView):
    permission_classes = [IsAuthenticated, IsOwner]

    def get(self, request, pk=None):
        if not pk:
            cards = Card.objects.filter(owner=request.user)
            return JsonResponse(CardSerializer(cards, many=True).data, safe=False)

        card = get_object_or_404(Card, pk=pk)
        self.check_object_permissions(self.request, card)
        return JsonResponse(CardSerializer(card).data)

    def post(self, request):
        Card.validate_card_requests_fields(request.data)
        pan = request.data['pan']

        Card.validate_card_number(pan)

        card = Card(
            pan=pan,
            expiry_date=request.data.get('expiry_date'),
            issue_date=request.data.get('issue_date'),
            cvv=request.data['cvv'],
            owner=request.user,
            printed_name=request.data.get('printed_name', ''),
        )
        card.save()
        return JsonResponse({'id': str(card.id)})

    def put(self, request, pk):
        card = object_exists(model=Card, request=request, pk=pk)
        if not card:
            return JsonResponse({}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UpdateCardSerializer(card, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': True})

        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
