import datetime

from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django_countries.serializer_fields import CountryField
from phonenumber_field.serializerfields import PhoneNumberField

from .models import Person, Status


class PersonSerializer(serializers.ModelSerializer):
    """
    A serializer that serializes retrieved data from the Person model that
    will be sent after succeeded registration
    """
    class Meta:
        model = Person
        exclude = [
            'password', 'email', 'avatar', 'last_login'
        ]


class RegistrationSerializer(serializers.ModelSerializer):
    """
    A serializer that used with Person model during the registration model
    """
    first_name = serializers.CharField(error_messages={'blank': 'blank'})
    last_name = serializers.CharField(error_messages={'blank': 'blank'})
    country_code = CountryField(
        error_messages={'invalid_choice': 'inclusion'}
    )
    phone_number = PhoneNumberField(
        error_messages={
            'blank': 'blank',
            'invalid': 'not_a_number',
        },
        validators=[
            UniqueValidator(
                queryset=Person.objects.all(),
                message='taken'
            )
        ]
    )
    birth_date = serializers.DateField(
        error_messages={'blank': 'blank'}
    )
    email = serializers.EmailField(
        error_messages={'invalid': 'invalid'},
        validators=[
            UniqueValidator(
                queryset=Person.objects.all(),
                message='taken'
            )
        ]
    )

    # A custom validation that used to prevent in_future_birth_date
    def validate_birth_date(self, value):
        if value > datetime.datetime.today().date():
            raise serializers.ValidationError(_("in_the_future"))
        return value

    class Meta:
        model = Person
        exclude = ['last_login']


class StatusSerializer(serializers.ModelSerializer):
    """
    A serializer used for rendering and parsing updated status data
    of Status model
    """
    phone_number = PhoneNumberField()
    token = serializers.CharField()

    class Meta:
        model = Status
        fields = ['phone_number', 'token', 'content']
