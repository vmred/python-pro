import pytest
from rest_framework.test import APIRequestFactory


@pytest.fixture
def created_user(request, django_user_model):
    request.cls.created_user = django_user_model.objects.create_user(username='user_test', password='user_test')


# @pytest.fixture
# def rest_client(request):
#     request.cls.client = APIRequestFactory()
