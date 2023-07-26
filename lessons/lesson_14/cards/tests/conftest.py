import pytest
from django.contrib.auth.models import Permission, User
from django.urls import reverse


@pytest.fixture(scope='class')
def autotest_user(request):
    request.cls.autotest_user_name = 'autotest_user'
    request.cls.autotest_user_password = 'autotest_pwd'
    request.cls.autotest_user = User.objects.create_user(
        username=request.cls.autotest_user_name, password=request.cls.autotest_user_password
    )
    permissions = Permission.objects.all()
    request.cls.autotest_user.user_permissions.set(permissions)

    yield

    User.objects.get(username=request.cls.autotest_user_name).delete()


@pytest.fixture
def autotest_user_2(request):
    request.cls.autotest_user_2_name = 'autotest_user_2'
    request.cls.autotest_user_2_password = 'autotest_pwd_2'
    request.cls.autotest_user_2 = User.objects.create_user(
        username=request.cls.autotest_user_2_name, password=request.cls.autotest_user_2_password
    )
    permissions = Permission.objects.all()
    request.cls.autotest_user_2.user_permissions.set(permissions)

    yield

    User.objects.get(username=request.cls.autotest_user_2_name).delete()


@pytest.fixture(scope='class')
def url(request):
    request.cls.url = reverse('cards')


@pytest.fixture
def pre_test(request):
    request.cls.user = User.objects.create_user(username='12345', password='12345')
