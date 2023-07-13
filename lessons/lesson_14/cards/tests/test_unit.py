from datetime import datetime, timedelta

import deepdiff
import pytest

from ..models.card import Card, is_valid_card_number


@pytest.mark.django_db
@pytest.mark.usefixtures('created_user')
class TestUnit:
    time_now = datetime.now()

    @pytest.mark.parametrize(
        'card_number, is_valid',
        [
            ('374245455400126', True),
            ('378282246310005', True),
            ('4111111111111111', True),
            ('38520000023237', True),
            ('0000 0000 0000 0000', True),
            ('4111 1111 1111 1112', False),
            ('1234', False),
            (None, False),
            ([], False),
            ('', False),
            ({}, False),
        ],
    )
    def test_validate_card_number(self, card_number, is_valid):
        assert is_valid_card_number(card_number) == is_valid

    def test_card_model_create_no_args(self):
        assert Card.objects.create(owner=self.created_user)  # pylint: disable=no-member

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
    def test_create_card_args(self, model, expected):
        model.owner = self.created_user
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
