from datetime import datetime, timedelta

import deepdiff
import pytest
from django.urls import reverse

from ..models.card import Card
from ..utils import hash_data


@pytest.mark.django_db
class TestIntegration:
    time_now = datetime.now()

    def test_card_model_create_no_args(self):
        assert Card.objects.create()  # pylint: disable=no-member

    @pytest.mark.parametrize(
        'model, expected',
        [
            (
                Card(
                    pan='374245455400126',
                    cvv='123',
                    status='new',
                    owner_id=1
                ),
                {
                    'pan': '374245455400126',
                    'expiry_date': time_now + timedelta(days=365 * 2),
                    'issue_date': time_now,
                    'cvv': hash_data('123'),
                    'status': 'new',
                },
            ),
            (
                Card(
                    pan='4111111111111111',
                    cvv='123',
                    status='active',
                    issue_date=time_now,
                    expiry_date=time_now + timedelta(days=365),
                ),
                {
                    'pan': '4111111111111111',
                    'expiry_date': time_now + timedelta(days=365),
                    'issue_date': time_now,
                    'cvv': hash_data('123'),
                    'status': 'active',
                },
            ),
        ],
    )
    def test_create_card_args(self, model, expected):
        model.save()

        model.issue_date, expected['issue_date'] = model.issue_date.date(), expected['issue_date'].date()
        model.expiry_date, expected['expiry_date'] = model.expiry_date.date(), expected['expiry_date'].date()

        assert not deepdiff.DeepDiff(
            model.__dict__, expected, exclude_paths=["root['_state']", "root['id']", "root['owner_id']"]
        )

    def test_view_get_cards(self, client):
        card = Card(pan='38520000023237')
        card.save()
        url = reverse('cards')
        response = client.get(url)
        response_json = response.json()
        assert response.status_code == 200
        assert response_json[0]['pan'] == '38520000023237'
        assert response_json[0]['issue_date'] == self.time_now.date().strftime('%Y-%m-%d')
        assert response_json[0]['expiry_date'] == (self.time_now + timedelta(days=365 * 2)).date().strftime('%Y-%m-%d')
