import uuid
import deepdiff

import pytest

from lessons.lesson_6.app.card_repository import CardRepository
from lessons.lesson_6.app.card_model import Card, Status


@pytest.mark.homework8
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
        card_id = card_repository_sqlite.save_card(input_data)
        input_data.card_id = card_id
        created_card = card_repository_sqlite.get_card(card_id=card_id)
        assert deepdiff.DeepDiff(input_data.__dict__, created_card.__dict__, exclude_paths=["root['owner_id']"]) == {}

    def test_get_card_from_sqlite(self, card_repository_sqlite):
        card = card_repository_sqlite.get_card(pan='1234 5678 9012 3456')
        assert card.__dict__ == {
            'card_id': 1,
            'pan': '1234 5678 9012 3456',
            'expiry_date': '06/25',
            'cvv': '123',
            'issue_date': '06/24',
            'owner_id': '150b5445-04aa-4dc7-8396-71806b82eef9',
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
        card_id = card_repository_postgres.save_card(input_data)
        input_data.card_id = card_id
        created_card = card_repository_postgres.get_card(card_id=card_id)
        assert deepdiff.DeepDiff(input_data.__dict__, created_card.__dict__, exclude_paths=["root['owner_id']"]) == {}

    def test_get_card_from_postgres(self, card_repository_postgres):
        card = card_repository_postgres.get_card(card_id='1').__dict__
        assert card == {
            'pan': '4444555566667777',
            'expiry_date': '06/25',
            'cvv': '173af653133d964edfc16cafe0aba33c8f500a07f3ba3f81943916910c257705',
            'issue_date': '06/24',
            'owner_id': 'd01fe1d0-9b19-48b1-bf69-e486cf02b445',
            'status': 'new',
            'card_id': 1
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
