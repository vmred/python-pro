import json
from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.db import models


class Status(models.TextChoices):
    NEW = 'new'
    ACTIVE = 'active'
    BLOCKED = 'blocked'


def is_valid_card_number(card_number: str):
    card_number = str(card_number).replace(' ', '')
    if not card_number.isdigit():
        return False

    digit_sum = 0

    for i, digit in enumerate(reversed(card_number)):
        n = int(digit)

        if i % 2 == 0:
            digit_sum += n
        elif n >= 5:
            digit_sum += n * 2 - 9
        else:
            digit_sum += n * 2

    return digit_sum % 10 == 0


class Card(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    pan = models.CharField(max_length=16, unique=True)
    expiry_date = models.DateField(blank=True)
    cvv = models.CharField()
    issue_date = models.DateField(blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(default=Status.NEW)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    printed_name = models.CharField(max_length=50, blank=True)

    def save(self, *args, **kwargs):
        if not self.issue_date:
            self.issue_date = datetime.now()

        if not self.expiry_date:
            self.expiry_date = datetime.now() + timedelta(days=365 * 2)

        super().save(*args, **kwargs)

    @staticmethod
    def validate_card_requests_fields(request_data: json) -> None:
        fail = ''
        required_fields = ['pan', 'cvv']

        for required_field in required_fields:
            if required_field not in request_data.keys():
                fail += f'Required "{required_field}" not filled \n'

        if fail:
            raise ValueError(fail)

    @staticmethod
    def validate_card_number(pan):
        if not is_valid_card_number(pan):
            raise ValueError(f'Card number "{pan}" is not valid')

    @staticmethod
    def activate_card(pk):
        Card.objects.filter(pk=pk).update(status=Status.ACTIVE)

    @staticmethod
    def deactivate_card(pk):
        Card.objects.filter(pk=pk).update(status=Status.BLOCKED)
