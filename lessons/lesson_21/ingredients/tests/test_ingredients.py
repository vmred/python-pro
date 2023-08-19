import pytest


@pytest.mark.lesson_21_homework
class TestIngredients:
    def test_ingredients(self, application):
        request, response = application.get('/ingredients')
        assert response.status_code == 200
        assert response.json['meal'] == 5000
