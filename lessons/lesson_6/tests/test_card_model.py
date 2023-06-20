import uuid
import deepdiff

import pytest

from lessons.lesson_6.app.card_repository import CardRepository
from lessons.lesson_6.app.card_model import Card, Status
from lessons.lesson_6.app.utils import hash_data


class TestCard:

    @pytest.fixture(scope='session')
    def card_repository_sqlite(self):
        yield CardRepository('sqlite')

    @pytest.fixture(scope='session')
    def card_repository_postgres(self):
        yield CardRepository('postgres')

    @pytest.mark.parametrize('input_data, expected_data', [
        [
            Card(
                pan='1234 5678 9012 3456',
                expiry_date='06/25',
                cvv='123',
                issue_date='06/24',
                owner_id=uuid.uuid4(),
                status=Status.new
            ),
            Card(
                pan='1234 5678 9012 3456',
                expiry_date='06/25',
                cvv='123',
                issue_date='06/24',
                owner_id=uuid.uuid4(),
                status=Status.new
            ),
        ]
    ])
    def test_save_card_to_sqlite(self, input_data, expected_data, card_repository_sqlite):
        card_repository_sqlite.save_card(input_data)
        created_card = card_repository_sqlite.get_card(input_data.pan)
        assert deepdiff.DeepDiff(input_data.__dict__, created_card, exclude_paths=["root['owner_id']"]) == {}

    def test_get_card_from_sqlite(self, card_repository_sqlite):
        card = card_repository_sqlite.get_card(pan='1111 1111 1111 1111')
        assert card == {
            'pan': '1111 1111 1111 1111',
            'expiry_date': '06/25',
            'cvv': 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3',
            'issue_date': '06/24',
            'owner_id': '52013b76-2310-4619-a34d-6d35a3f0cdb6',
            'status': 'new'
        }

    @pytest.mark.parametrize('input_data', [
        Card(
            pan='4444555566667777',
            expiry_date='06/25',
            cvv='123',
            issue_date='06/24',
            owner_id=uuid.uuid4(),
            status=Status.new
        )
    ])
    def test_save_card_to_postgres(self, input_data, card_repository_postgres):
        card_repository_postgres.save_card(input_data)
        created_card = card_repository_postgres.get_card(pan=input_data.pan)
        assert deepdiff.DeepDiff(input_data.__dict__, created_card, exclude_paths=["root['owner_id']"]) == {}

    def test_get_card_from_postgres(self, card_repository_postgres):
        card = card_repository_postgres.get_card(card_id='1')
        assert card == {
            'pan': '4444555566667777',
            'expiry_date': '06/25',
            'cvv': '173af653133d964edfc16cafe0aba33c8f500a07f3ba3f81943916910c257705',
            'issue_date': '06/24',
            'owner_id': 'd01fe1d0-9b19-48b1-bf69-e486cf02b445',
            'status': 'new'
        }

    @pytest.mark.parametrize('card', [
        Card(
            pan='1234 5678 9012 3456',
            expiry_date='06/25',
            cvv='123',
            issue_date='06/24',
            owner_id=uuid.uuid4(),
            status=Status.new
        ),
        Card(
            pan='9999 9999 9999 9999',
            expiry_date='06/25',
            cvv='123',
            issue_date='06/24',
            owner_id=uuid.uuid4(),
            status=Status.active
        )
    ])
    def test_activate_card_positive(self, card):
        # no really need to compare with something, just check if executed w/o exception
        assert card.activate_card() is None

    def test_activate_card_negative(self):
        card = Card(
            pan='9999 9999 9999 9999',
            expiry_date='06/25',
            cvv='123',
            issue_date='06/24',
            owner_id=uuid.uuid4(),
            status=Status.blocked
        )

        with pytest.raises(ValueError):
            card.activate_card()

    @pytest.mark.parametrize('card', [
        Card(
            pan='1234 5678 9012 3456',
            expiry_date='06/25',
            cvv='123',
            issue_date='06/24',
            owner_id=uuid.uuid4(),
            status=Status.new
        ),
        Card(
            pan='9999 9999 9999 9999',
            expiry_date='06/25',
            cvv='123',
            issue_date='06/24',
            owner_id=uuid.uuid4(),
            status=Status.active
        ),
        Card(
            pan='1111 1111 1111 1111',
            expiry_date='06/25',
            cvv='123',
            issue_date='06/24',
            owner_id=uuid.uuid4(),
            status=Status.blocked
        )
    ])
    def test_block_card(self, card):
        # no really need to compare with something, just check if executed w/o exception
        assert card.block_card() is None
