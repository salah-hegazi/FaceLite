import os
import json

from django.test import TestCase

from cognitev.users.serializers import RegistrationSerializer


dir_path = os.getcwd()
image = os.path.join(dir_path, 'cognitev/users/tests/images/default.png')


class RegistrationSerializerTest(TestCase):

    def test_validate_in_future_birth_date(self):
        data = {
            'first_name': 'Salah',
            'last_name': 'Hegazi',
            'country_code': 'EG',
            'phone_number': '+201023075957',
            'gender': 'M',
            'birth_date': '2022-09-28',
            'avatar': image,
            'password': '147258369'
        }
        json_date = json.dumps(data)
        serialized_data = RegistrationSerializer(data=json_date)
        self.assertFalse(serialized_data.is_valid())
        # self.assertEquals(serialized_data.errors['birth_date'], 'in_the_future')

