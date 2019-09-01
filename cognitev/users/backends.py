from .models import Person


class MyAuthBackend(object):
    @staticmethod
    def authenticate(phone_number, password):
        try:
            user = Person.objects.get(phone_number=phone_number)
            if user.check_password(password):
                return user
            else:
                return None
        except Person.DoesNotExist:
            return None

    @staticmethod
    def get_user(user_id):
        try:
            user = Person.objects.get(pk=user_id)
            if user.is_active:
                return user
            return None
        except UserModel.DoesNotExist:
            return None

