import pytest

from ..regex import is_inn_valid


class TestInn:
    @pytest.mark.parametrize(
        'inn, is_valid',
        [
            ('!@#$%^', False),
            (r'.*', False),
            ('1234567897', True),
            ('0000000000', True),
            ('000000009', False),
            ('00000000000', False),
            ('', False),
            ('zxc', False),
            ('qwertyuiop', False),
            ('123456789P', False),
            ('o123456789', False),
            (123, False),
            ([], False),
            ({}, False),
            ((), False),
        ],
    )
    def test_inn_match(self, inn, is_valid):
        assert is_inn_valid(inn) == is_valid
