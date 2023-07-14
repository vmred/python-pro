from datetime import datetime, timedelta

import deepdiff
import pytest
from django.contrib.auth.models import User

from ..models.card import Card


@pytest.fixture
def pre_test(request):
    request.cls.user = User.objects.create_user(username='12345', password='12345')


@pytest.mark.django_db
class TestModels:
    time_now = datetime.now()

    def test_card_model_create_no_args(self, pre_test):
        assert Card.objects.create(owner=self.user)  # pylint: disable=no-member

    @pytest.mark.parametrize(
        'model, expected',
        [
            (
                Card(
                    pan='374245455400126',
                    cvv='598',
                    status='new',
                ),
                {
                    'pan': '374245455400126',
                    'expiry_date': time_now + timedelta(days=365 * 2),
                    'issue_date': time_now,
                    'cvv': '598',
                    'status': 'new',
                    'printed_name': '',
                },
            ),
            (
                Card(
                    pan='4111111111111111',
                    cvv='598',
                    status='active',
                    issue_date=time_now,
                    expiry_date=time_now + timedelta(days=365),
                ),
                {
                    'pan': '4111111111111111',
                    'expiry_date': time_now + timedelta(days=365),
                    'issue_date': time_now,
                    'cvv': '598',
                    'status': 'active',
                    'printed_name': '',
                },
            ),
        ],
    )
    def test_create_card_args(self, model, expected, pre_test):
        model.owner = self.user
        model.save()

        model.issue_date, expected['issue_date'] = model.issue_date.date(), expected['issue_date'].date()
        model.expiry_date, expected['expiry_date'] = model.expiry_date.date(), expected['expiry_date'].date()
        print(model.__dict__)
        print(expected)
        assert not deepdiff.DeepDiff(
            model.__dict__,
            expected,
            exclude_paths=[
                "root['_state']",
                "root['id']",
                "root['owner_id']",
                "root['created_at']",
                "root['updated_at']",
            ],
        )
