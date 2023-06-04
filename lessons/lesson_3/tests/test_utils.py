import pytest

from lessons.lesson_3.app.utils import check_if_bank_supported, reformat_date


class TestUtils:

    @pytest.mark.parametrize('value, expected', [
        ('PB', 'PB'),
        ('pb', 'PB'),
        ('privatbank', 'PB'),
        ('nationalbank', 'NBU'),
        ('NB', 'NBU'),
    ])
    def test_validate_bank_positive(self, value, expected):
        assert check_if_bank_supported(value) == expected

    @pytest.mark.parametrize('value, expected', [
        ('fasd', ValueError),
        ('Privatbank', ValueError),
        ('Nationalbank', ValueError),
        (1, ValueError),
        ('national bank', ValueError),
        ('privat bank', ValueError),
        (None, ValueError),
        ([], ValueError)
    ])
    def test_validate_bank_negative(self, value, expected):
        with pytest.raises(expected):
            check_if_bank_supported(value)

    @pytest.mark.parametrize('value, expected', [
        ('2023-05-31', '31.05.2023'),
        ('31-05-2023', '31.05.2023'),
        ('31.05.2023', '31.05.2023'),
        ('5.31.2023', '31.05.2023'),
        ('29-02-2004', '29.02.2004')
    ])
    def test_reformat_date_positive(self, value, expected):
        assert reformat_date(value) == expected

    @pytest.mark.parametrize('value, expected', [
        ('adf', ValueError),
        ('29.02.2005', ValueError),
        (None, ValueError),
        ([], ValueError),
    ])
    def test_reformat_date_negative(self, value, expected):
        with pytest.raises(expected):
            reformat_date(value)
