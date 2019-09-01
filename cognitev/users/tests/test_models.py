import os

from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile

from cognitev.users.models import Person, Status


dir_path = os.getcwd()
image = os.path.join(dir_path, 'cognitev/users/tests/images/default.png')


class PersonModelTest(TestCase):
    @classmethod
    def setUp(cls):
        Person.objects.create_user(
            first_name='Salah',
            last_name='Hegazi',
            country_code='EG',
            phone_number='+201023075957',
            gender='M',
            birth_date='1996-09-28',
            avatar=SimpleUploadedFile(
                name='test_default.png',
                content=open(image, 'rb').read(),
                content_type='image/png'
            ),
            password='147258369'
        )

    def test_object_name_is_first_name_space_last_name(self):
        person = Person.objects.get(pk=1)
        expected_object_name = person.first_name + ' ' + person.last_name
        self.assertEquals(expected_object_name, str(person))

