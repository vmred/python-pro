import pytest

from lessons.lesson_3.app.db_practice import get_invoice_items_profit, get_repeatable_customers


class TestDbPractise:

    @pytest.mark.homework4
    def test_get_invoice_items_profit(self):
        assert get_invoice_items_profit() == 2328.599999999957

    @pytest.mark.homework4
    def test_get_repeatable_customers(self):
        assert get_repeatable_customers() == [('Frank', 2), ('Mark', 2)]
