from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import get_object_or_404

from rest_framework.generics import CreateAPIView
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK,
    HTTP_403_FORBIDDEN,
)
from rest_framework.response import Response

from .serializers import (
    RegistrationSerializer,
    StatusSerializer,
    PersonSerializer
)
from .models import Person, Status


class Registration(CreateAPIView):
    """
    A view that handles registration process. using two serializers, one for
    accepting persons' data from frontend and another for sending back a
    specific data of the saved person after a succeeded registration process.
    """
    permission_classes = [AllowAny]
    serializer_class = RegistrationSerializer

    # A custom create method that overrides CreateAPIView's method.
    def create(self, request, *args, **kwargs):
        serialized_person = RegistrationSerializer(data=request.data)
        if serialized_person.is_valid():
            person = Person.objects.create_user(
                first_name=serialized_person.initial_data['first_name'],
                last_name=serialized_person.initial_data['last_name'],
                password=serialized_person.initial_data['password'],
                country_code=serialized_person.initial_data['country_code'],
                phone_number=serialized_person.initial_data['phone_number'],
                avatar=serialized_person.initial_data['avatar'],
                gender=serialized_person.initial_data['gender'],
                birth_date=serialized_person.initial_data['birth_date'],
            )
            person.email = serialized_person.initial_data['email']
            person.save()
            returned_serialized_person = PersonSerializer(person)
            return Response(returned_serialized_person.data,
                            status=HTTP_201_CREATED)
        else:
            return Response(serialized_person.errors,
                            status=HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(["POST"])
@permission_classes([AllowAny])
def login(request):
    """
    A view that handles authentication process and returns an authentication
    token for authenticated users
    :param request:
    :return error or token if user is authenticated:
    """
    phone_number = request.data.get("phone_number")
    password = request.data.get("password")
    if phone_number is None or password is None:
        return Response(
            {'error': _("Please provide both phone number and password"), },
            status=HTTP_400_BAD_REQUEST
        )
    user = authenticate(phone_number=phone_number, password=password)
    if not user:
        return Response(
            {'error': _("Invalid credentials"), },
            status=HTTP_404_NOT_FOUND
        )
    token, created = Token.objects.get_or_create(user=user)
    return Response(
        {'token': token.key, },
        status=HTTP_200_OK
    )


class UpdateStatus(CreateAPIView):
    """
    A view that handles status updating and authenticate the person with his
    phone number and token.
    """

    serializer_class = StatusSerializer

    # A custom create method that overrides CreateAPIView's method.
    def create(self, request, *args, **kwargs):
        serialized_status = StatusSerializer(data=request.data)
        if serialized_status.is_valid():
            person = get_object_or_404(
                Person,
                phone_number=serialized_status.data['phone_number']
            )
            if not (str(Token.objects.get(user=person))
                    == serialized_status.data['token']):
                return Response(
                    {'error': _("Invalid credentials")},
                    status=HTTP_403_FORBIDDEN
                    )

            status = Status.objects.create(
                content=serialized_status.data['content'],
                user=person
            )
            status.save()
            return Response(status=HTTP_201_CREATED)
        else:
            return Response(status=HTTP_400_BAD_REQUEST)

