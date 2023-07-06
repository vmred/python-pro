from datetime import datetime, timedelta

import deepdiff
import pytest
from django.urls import reverse

from ..models.card import Card


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
                    cvv='598',
                    status='new',
                    owner_id=1,
                ),
                {
                    'pan': '374245455400126',
                    'expiry_date': time_now + timedelta(days=365 * 2),
                    'issue_date': time_now,
                    'cvv': '598',
                    'status': 'new',
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
        response = client.get(url, headers={'accept': 'application/json'})
        response_json = response.json()
        assert response.status_code == 200
        assert response_json[0]['pan'] == '38520000023237'
        assert response_json[0]['issue_date'] == self.time_now.date().strftime('%Y-%m-%d')
        assert response_json[0]['expiry_date'] == (self.time_now + timedelta(days=365 * 2)).date().strftime('%Y-%m-%d')

    def test_cards_template(self, client):
        response = client.get(reverse('cards_create_form'))
        assert response.status_code == 200

    def test_cards_view_form(self, client):
        response = client.get('/cards/', headers=None, cookies=None, secure=False)
        assert response.status_code == 200
        assert (
            response.content
            == b'<!DOCTYPE html>\n<html lang="en">\n<head>\n    <meta charset="UTF-8">\n    <title>Cards</title>\n</head>\n<style>\n\ntable, th, td {border: 1px solid black;  border-collapse: collapse;}\n\n</style>\n<body>\n \n\n\n<p>No data</p>\n\n\n</body>\n</html>'
        )

    def test_cards_create_form(self, client):
        response = client.get('/cards/create')
        assert response.status_code == 200
        csrf_token = response.context.get('csrf_token')
        assert (
            response.content
            == f'<!DOCTYPE html>\n<html lang="en">\n<head>\n    <meta charset="UTF-8">\n    <title>Cards</title>\n</head>\n<style>\n \n</style>\n<body>\n\n<form action="/cards/create" method="post">\n    <input type="hidden" name="csrfmiddlewaretoken" value="{csrf_token}">\n    <fieldset>\n        <legend><h1>Create new card</h1></legend>\n        <div class="pan">\n            <label>Pan</label>\n            <input type="text" name="pan">\n        </div>\n        <div class="issue_date">\n            <label>Issue date</label>\n            <input type="date" name="issue_date">\n        </div>\n\n        <div class="expiry_date">\n            <label>Expiry date</label>\n            <input type="date" name="expiry_date">\n        </div>\n\n        <div class="cvv">\n            <label>cvv</label>\n            <input type="text" name="cvv">\n        </div>\n\n        <div class="owner_id">\n            <label>Owner id</label>\n            <input type="text" name="owner_id">\n        </div>\n\n        <div class="status">\n            <label>Status</label>\n            <select name="status" id="status">\n\n                <option value="new">new</option>\n                <option value="active">active</option>\n        </select>\n        </div>\n    </fieldset>\n    <input type="submit" value="Create">\n</form>\n\n \n</body>\n</html>'.encode()
        )
