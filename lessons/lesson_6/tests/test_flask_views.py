import uuid

import pytest

from lessons.lesson_6.app.card_model import Card, Status
from lessons.lesson_6.app.flask_app import app


@pytest.mark.homework8
class TestFlaskViews:
    create_cases = [
        (
            '/cards',
            200,
            Card(
                pan='1234 5678 9012 3456',
                expiry_date='06/25',
                cvv='123',
                issue_date='06/24',
                owner_id=str(uuid.uuid4()),
                status=Status.new,
            ),
        )
    ]

    @pytest.mark.parametrize('url, status_code, input_data', create_cases, ids=[x[0] for x in create_cases])
    def test_view_create_card(self, url, status_code, input_data):
        with app.test_client() as test_client:
            response = test_client.post(url, json=input_data.__dict__, headers={'Content-Type': 'application/json'})
            assert response.status_code == status_code
            assert 'id' in response.json.keys()

    def test_view_get_card(self):
        with app.test_client() as test_client:
            response = test_client.get('/cards/1', headers={'Content-Type': 'application/json'})
            assert response.status_code == 200
            assert response.json == {
                'card_id': 1,
                'cvv': '173af653133d964edfc16cafe0aba33c8f500a07f3ba3f81943916910c257705',
                'expiry_date': '06/25',
                'issue_date': '06/24',
                'owner_id': 'd01fe1d0-9b19-48b1-bf69-e486cf02b445',
                'pan': '4444555566667777',
                'status': 'new',
            }
