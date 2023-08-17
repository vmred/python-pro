import pytest


@pytest.mark.lesson_21_homework
class TestBakery:
    def test_bakery(self, application):
        request, response = application.get('/bakery')
        assert response.status_code == 200
        assert response.json['buns_to_bake'] == 50
