from datetime import date, datetime, timedelta

import pytest
from django.contrib.auth.models import User
from django.db.models import Q
from django.test.utils import override_settings

from ..models.card import Card, Status
from ..tests import get_card_cvv, get_card_number, get_name
from ..views.card import block_expired_cards_task, task_activate_card


@pytest.mark.django_db
class TestTasks:
    time_now = datetime.now()

    @override_settings(CELERY_TASK_ALWAYS_EAGER=True, CELERY_TASK_EAGER_PROPOGATES=True)
    def test_task_activate_card(self):
        user = User.objects.create_user(username='12345', password='12345')
        model = Card.objects.create(
            pan=get_card_number(), cvv=get_card_cvv(), status='new', printed_name=get_name(), owner=user
        )
        assert model.status == Status.NEW
        task_activate_card.delay(model.id)
        model.refresh_from_db()
        assert model.status == Status.ACTIVE

    @override_settings(CELERY_TASK_ALWAYS_EAGER=True, CELERY_TASK_EAGER_PROPOGATES=True)
    def test_task_block_all_expired_cards(self):
        user = User.objects.create_user(username='12345', password='12345')
        for _ in range(2):
            Card.objects.create(
                pan=get_card_number(),
                cvv=get_card_cvv(),
                status='new',
                printed_name=get_name(),
                owner=user,
                issue_date=self.time_now - timedelta(days=100),
                expiry_date=self.time_now - timedelta(days=2),
            )

        cards = Card.objects.filter(~Q(status=Status.BLOCKED), expiry_date__lt=date.today())
        assert len(cards) == 2
        block_expired_cards_task.delay()
        cards = Card.objects.filter(~Q(status=Status.BLOCKED), expiry_date__lt=date.today())
        assert len(cards) == 0
