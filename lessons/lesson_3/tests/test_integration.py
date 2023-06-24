import pytest

from lessons.lesson_3.app.utils import get_pb_exchange_rate


class TestsIntegration:
    @pytest.mark.parametrize(
        'currency, bank, date',
        [
            ('USD', 'PB', '31.05.2023'),
            ('USD', 'NB', '31.05.2023'),
        ],
    )
    def test_pb_rates(self, currency, bank, date):
        assert get_pb_exchange_rate(currency, bank, date)
