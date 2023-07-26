import pytest
from django.contrib.auth.models import User
from django.test.utils import override_settings

from ..models.card import Card, Status
from ..tests import get_card_cvv, get_card_number, get_name
from ..views.card import task_activate_card


@pytest.mark.django_db
class TestTasks:
    pan = get_card_number()
    cvv = get_card_cvv()
    printed_name = get_name()
    databases = '__all__'

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
