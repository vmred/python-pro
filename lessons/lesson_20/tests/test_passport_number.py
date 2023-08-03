import pytest

from ..regex import is_passport_valid


class TestPassportNumber:
    @pytest.mark.parametrize(
        'passport_number, is_valid',
        [
            ('KM123456', True),
            ('KA1234567', False),
            ('KA12345', False),
            ('00123456', False),
            ('', False),
            ('ЯЮ1234009', False),
            ('MT234300\n', True),
            ('MT233400 MT233400', False),
            ('123456', False),
            ('BKMBTC', False),
            ('bk122143', False),
            ('!@#$%^', False),
            (r'.*', False),
        ],
    )
    def test_passport_match(self, passport_number, is_valid):
        assert is_passport_valid(passport_number) == is_valid

    @pytest.mark.parametrize(
        'passport_number, exception', [(None, TypeError), ([], TypeError), ({}, TypeError), (['MT233400'], TypeError)]
    )
    def test_passport_match_exception(self, passport_number, exception):
        with pytest.raises(exception):
            is_passport_valid(passport_number)
