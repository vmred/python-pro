from datetime import datetime, timedelta

import deepdiff
import pytest

from faker import Faker
from faker.providers import credit_card
from rest_framework.test import APITestCase

from ..tests import get_card_cvv, get_card_number, get_name

faker = Faker()
faker.add_provider(credit_card)


@pytest.mark.django_db
@pytest.mark.usefixtures('url', 'autotest_user')
class TestIntegration(APITestCase):
    time_now = datetime.now().strftime('%Y-%m-%d')
    expiry_date = (datetime.now() + timedelta(days=365 * 2)).strftime('%Y-%m-%d')
    pan = get_card_number()
    cvv = get_card_cvv()
    printed_name, edit_printed_name = get_name(), get_name()

    def test_create_card(self):
        self.client.login(username=self.autotest_user_name, password=self.autotest_user_password)
        response = self.client.post(
            self.url, data={"pan": self.pan, "cvv": self.cvv, "printed_name": self.printed_name}
        )
        assert response.status_code == 200

        response_json = response.json()
        self.assertEquals(list(response_json.keys()), ['id'])
        entity_id = response_json['id']

        response = self.client.get(f'{self.url}{entity_id}')
        assert response.status_code == 200
        response_json = response.json()
        self.assertEquals(
            deepdiff.DeepDiff(
                response_json,
                {
                    'pan': self.pan, 'cvv': self.cvv, 'printed_name': self.printed_name, 'status': 'new',
                    'owner': self.autotest_user.id,
                    'issue_date': self.time_now, 'expiry_date': self.expiry_date,
                    'created_at': self.time_now, 'updated_at': self.time_now
                },
                exclude_paths=["root['id']"]
            ),
            {}
        )
        self.client.logout()

    def test_update_card(self):
        self.client.login(username=self.autotest_user_name, password=self.autotest_user_password)
        response = self.client.post(
            self.url, data={"pan": self.pan, "cvv": self.cvv, "printed_name": self.printed_name}
        )
        assert response.status_code == 200
        entity_id = response.json()['id']

        response = self.client.get(f'{self.url}{entity_id}')
        assert response.status_code == 200
        card = response.json()

        response = self.client.put(f'{self.url}{entity_id}', data={
            'id': 10,
            'cvv': faker.credit_card_security_code(),
            'pan': faker.credit_card_number(),
            'printed_name': self.edit_printed_name,
            'owner': 2,
            'expiry_date': '1971-01-01',
            'issue_date': '1971-01-01',
            'created_at': '1971-01-01',
            'updated_at': '1971-01-01',
            'status': 'active',
        })
        assert response.status_code == 200

        response = self.client.get(f'{self.url}{entity_id}')
        card_edited = response.json()

        card['printed_name'] = self.edit_printed_name
        self.assertEquals(deepdiff.DeepDiff(card, card_edited), {})

    def test_get_cards(self):
        self.client.login(username=self.autotest_user_name, password=self.autotest_user_password)
        self.client.post(
            self.url, data={"pan": get_card_number(), "cvv": get_card_cvv(), "printed_name": get_name()}
        )
        response = self.client.get(self.url)
        assert response.status_code == 200

    @pytest.mark.usefixtures('autotest_user_2')
    def test_get_another_user_card(self):
        self.client.login(username=self.autotest_user_name, password=self.autotest_user_password)
        response = self.client.post(
            self.url, data={
                "pan": get_card_number(), "cvv": get_card_cvv(), "printed_name": get_name(),
                'owner': self.autotest_user.id
            }
        )
        assert response.status_code == 200
        entity_id = response.json()['id']

        self.client.login(username=self.autotest_user_2_name, password=self.autotest_user_2_password)
        response = self.client.get(f'{self.url}{entity_id}')
        assert response.status_code == 403
        assert response.json() == {'detail': 'You do not have permission to perform this action.'}
