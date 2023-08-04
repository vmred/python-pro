import pytest

from ..regex import is_car_number_valid_dnepr, is_car_number_valid_kharkiv


class TestCarNumber:
    @pytest.mark.parametrize(
        'car_number, is_valid',
        [
            ('!@#$%^', False),
            (r'.*', False),
            ('', False),
            ('XX0000AE', True),
            ('EX0001TP', True),
            ('AX0002HC', True),
            ('KX0003BE', True),
            ('AA1234AA', False),
            ('aa0001AA', False),
            ('KX12345AA', False),
            ('KX123OI', False),
            (123, False),
            ([], False),
            ({}, False),
            ((), False),
        ],
    )
    def test_car_number_match_kharkiv(self, car_number, is_valid):
        assert is_car_number_valid_kharkiv(car_number) == is_valid

    @pytest.mark.parametrize(
        'car_number, is_valid',
        [
            ('!@#$%^', False),
            (r'.*', False),
            ('', False),
            ('PP0000AE', True),
            ('MI0001TP', True),
            ('AE0002HC', True),
            ('KE0003BE', True),
            ('AA1234AA', False),
            ('aa0001AA', False),
            ('KX12345AA', False),
            ('KX123OI', False),
            (123, False),
            ([], False),
            ({}, False),
            ((), False),
        ],
    )
    def test_car_number_match_dnepr(self, car_number, is_valid):
        assert is_car_number_valid_dnepr(car_number) == is_valid
