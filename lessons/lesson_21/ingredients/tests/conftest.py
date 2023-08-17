import pytest
from sanic_testing.testing import SanicTestClient

from lessons.lesson_21.ingredients.server import app


@pytest.fixture
def application():
    return SanicTestClient(app)
