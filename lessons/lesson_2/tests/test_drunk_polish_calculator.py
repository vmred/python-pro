import pytest

from lessons.lesson_2.drunk_polish_calculator import (
    main,
    op_divide,
    op_minus,
    op_multiply,
    op_plus
)


class TestUnitDrunkPolishCalculator:

    @pytest.mark.parametrize('x, y, expected', [
        (5, 3, 8),
        (0.1, 0.1, 0.2),
        (1, -1, 0),
        (1, 1, 2.0),
        ('1', '2', '12'),
    ])
    def test_plus_positive(self, x, y, expected):
        assert op_plus(x, y) == expected

    @pytest.mark.parametrize('x, y, expected', [
        (1, '1', TypeError),
        (None, [], TypeError),
    ])
    def test_plus_negative(self, x, y, expected):
        with pytest.raises(expected):
            op_plus(x, y)

    @pytest.mark.parametrize('x, y, expected', [
        (1, 1, 0),
        (1, -1, 2),
        (1, 0.2, 0.8),
    ])
    def test_minus_positive(self, x, y, expected):
        assert op_minus(x, y) == expected

    @pytest.mark.parametrize('x, y, expected', [
        (1, '1', TypeError),
        (None, [], TypeError),
        ('1', '2', TypeError),
        ([1], [1], TypeError)
    ])
    def test_minus_negative(self, x, y, expected):
        with pytest.raises(expected):
            op_minus(x, y)

    @pytest.mark.parametrize('x, y, expected', [
        (5, 3, 15),
        (2, 0.1, 0.2),
        (1, -1, -1),
        (10, 0, 0),
        ('1', 2, '11'),
        ([1], 2, [1, 1])
    ])
    def test_multiply_positive(self, x, y, expected):
        assert op_multiply(x, y) == expected

    @pytest.mark.parametrize('x, y, expected', [
        (1, '1', TypeError),
        (None, [], TypeError),
        ('1', '2', TypeError)
    ])
    def test_multiply_negative(self, x, y, expected):
        with pytest.raises(expected):
            op_multiply(x, y)

    @pytest.mark.parametrize('x, y, expected', [
        (5, 3, 1.6666666666666667),
        (2, 1, 2),
        (2, 0.1, 20)
    ])
    def test_division_positive(self, x, y, expected):
        assert op_divide(x, y) == expected

    @pytest.mark.parametrize('x, y, expected', [
        (1, '1', TypeError),
        (None, [], TypeError),
        (5, 0, ZeroDivisionError),
        ('1', '1', TypeError),
    ])
    def test_multiply_negative(self, x, y, expected):
        with pytest.raises(expected):
            op_divide(x, y)


class TestIntegrationDrunkPolishCalculator:

    @pytest.mark.parametrize('expression, expected', [
        ('2 2 +', '4.0\n'),
        ('2 2 4 * 8 / +', '3.0\n'),  # 2 + 2 * 4 / 8 == 3.0
        ('2 2 4 * 8 / -', '1.0\n'),  # 2 - 2 * 4 / 8 == 1.0
        ('3 1 -', '2.0\n'),
        ('4 2 /', '2.0\n'),
    ])
    def test_calculate_expression_positive(self, expression, expected, monkeypatch, capsys):
        monkeypatch.setattr('builtins.input', lambda _: expression)
        main()
        assert capsys.readouterr().out == expected

    @pytest.mark.parametrize('expression, expected', [
        ('', IndexError),
        ('2 2+', ValueError),
        (None, AttributeError),
        ('string string', ValueError)
    ])
    def test_calculate_expression_negative(self, expression, expected, monkeypatch, capsys):
        with pytest.raises(expected):
            monkeypatch.setattr('builtins.input', lambda _: expression)
            main()
