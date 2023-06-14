import uuid
import deepdiff

import pytest

from lessons.lesson_6.app.card_controller import CardController
from lessons.lesson_6.app.card_model import Card, Status


class TestCard:

    @pytest.fixture
    def card_controller(self):
        yield CardController()

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
    def test_save_card_in_db(self, input_data, expected_data, card_controller):
        card_controller.save_card(input_data)
        created_card = card_controller.get_card(input_data.pan)
        assert deepdiff.DeepDiff(input_data.__dict__, created_card.__dict__, exclude_paths=["root['owner_id']"]) == {}

    def test_get_card_from_db(self, card_controller):
        card = card_controller.get_card('1111 1111 1111 1111')
        assert card.__dict__ == {
            'pan': '1111 1111 1111 1111',
            'expiry_date': '06/25',
            'cvv': 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3',
            'issue_date': '06/24',
            'owner_id': '52013b76-2310-4619-a34d-6d35a3f0cdb6',
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
