import pytest

from ..models.card import is_valid_card_number


class TestUnit:
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
