import pytest

from lessons.lesson_3.app.utils import validate_bank


class TestUtils:

    @pytest.mark.parametrize('value, expected', [
        ('pb', 'PB'),
        ('national bank', 'NBU')
    ])
    def test_validate_bank_positive(self, value, expected):
        assert validate_bank(value) == expected

    @pytest.mark.parametrize('value, expected', [
        ('fasd', ''),
    ])
    def test_validate_bank_negative(self, value, expected):
        pass
