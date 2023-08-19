import pytest
from sanic_testing.testing import SanicTestClient

from ..server import app


@pytest.fixture
def application():
    return SanicTestClient(app)
