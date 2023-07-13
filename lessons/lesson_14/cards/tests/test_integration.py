from datetime import datetime, timedelta

import deepdiff
import pytest
from django.contrib.auth.models import Permission
from django.urls import reverse
from rest_framework.test import APITestCase


@pytest.mark.django_db
@pytest.mark.usefixtures('created_user')
class TestIntegration(APITestCase):
    def test_create_card(self):
        permissions = Permission.objects.all()
        self.created_user.user_permissions.set(permissions)

        self.client.login(username='user_test', password='user_test')
        url = reverse('cards')

        response = self.client.post(
            url, data={"pan": "572451221715", "cvv": "879", "status": "New", "printed_name": "Jenny Gibson"}
        )
        assert response.status_code == 200
        self.assertEquals(list(response.json().keys()), ['id'])
