import os

from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK,
    HTTP_403_FORBIDDEN,
)
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from cognitev.users.models import Person, Status


dir_path = os.getcwd()
image = os.path.join(dir_path, 'cognitev/users/tests/images/default.png')


class RegistrationTest(APITestCase):
    def test_bad_request(self):
        url = reverse('users:registration')
        data = {
            'first_name': '',
            'last_name': 'Hegazi',
            'country_code': 'EG',
            'phone_number': '+2010',
            'gender': 'M',
            'birth_date': '1996-09-28',
            'avatar': '',
            'password': '147258369'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)


class LoginTest(APITestCase):
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

    def test_bad_request(self):
        url = reverse('users:login')
        data = {
            'phone_number': None,
            'password': None
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

    def test_not_found(self):
        url = reverse('users:login')
        data = {
            'phone_number': '+201023055555',
            'password': '753951456852'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)

    def test_authenticated(self):
        url = reverse('users:login')
        data = {
            'phone_number': '+201023075957',
            'password': '147258369'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, HTTP_200_OK)


class UpdateStatusTest(APITestCase):
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
        person = Person.objects.all()
        for per in person:
            Token.objects.get_or_create(user=per)

    def test_forbidden(self):
        url = reverse('users:status')
        data = {
            'phone_number': '+201023075957',
            'token': '5489532561kebfklbiflbvw;ie',
            'content': 'Hi I am here'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    def test_create_status(self):
        url = reverse('users:status')
        person = Person.objects.get(phone_number='+201023075957')
        data = {
            'phone_number': '+201023075957',
            'token': str(Token.objects.get(user=person)),
            'content': 'Hi I am here'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, HTTP_201_CREATED)

    def test_bad_request(self):
        url = reverse('users:status')
        data = {
            'phone_number': '+2010230',
            'token': '',
            'content': 1256874
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)



