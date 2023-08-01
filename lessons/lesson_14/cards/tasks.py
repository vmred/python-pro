from celery import shared_task
from django.db.models import Q
from django.utils.datetime_safe import date

from .models.card import Card, Status


@shared_task
def block_expired_cards_task():
    cards = Card.objects.filter(~Q(status=Status.BLOCKED), expiry_date__lt=date.today())
    for card in cards:
        print(f'blocking card with id: {card.id}')
        Card.deactivate_card(card.id)
    return True


@shared_task
def task_activate_card(pk: str):
    Card.activate_card(pk)
