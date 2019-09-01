from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)
from django.utils.translation import ugettext_lazy as _

from phonenumber_field.modelfields import PhoneNumberField
from django_countries.fields import CountryField


class PersonManager(BaseUserManager):
    """
    A custom manager for custom User model
    """
    def create_user(self, first_name, last_name, country_code,
                    phone_number, gender, birth_date, avatar, password=None):
        """
        creates and saves a User with the given first_name, last_name,
        country_code, phone_number, gender, birth_date, avatar and password
        """
        user = self.model(
            first_name=first_name,
            last_name=last_name,
            country_code=country_code,
            phone_number=phone_number,
            gender=gender,
            birth_date=birth_date,
            avatar=avatar,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


class Person(AbstractBaseUser):
    """
    A custom User model that represents users
    """
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    first_name = models.CharField(_("First name of User"), max_length=50)
    last_name = models.CharField(_("Last name of User"), max_length=50)
    # Using django_countries third party app to get countries codes
    country_code = CountryField(_("Country code of User"), max_length=10)
    # Using phonenumber_field third package to
    # define phonenumber in E.164 format
    phone_number = PhoneNumberField(_("Phone number of User"), unique=True)
    gender = models.CharField(_("Gender of User"), max_length=1,
                              choices=GENDER_CHOICES)
    birth_date = models.DateField(_("Birth date of User"))
    avatar = models.ImageField(_("Image of User"), upload_to='images/')
    email = models.EmailField(_("Email of User"), blank=True, unique=True,
                              max_length=255)
    objects = PersonManager()
    USERNAME_FIELD = 'phone_number'
    REQUIRED = [
        'first_name', 'last_name',
        'country_code', 'gender',
        'birth_date', 'avatar',
    ]

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class Status(models.Model):
    """
    A model that represents status updated by users
    """
    content = models.TextField(_("Content of status"), max_length=500)
    user = models.ForeignKey(Person, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user) + ': ' + self.content


