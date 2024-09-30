from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import AbstractUser
from django.http.request import HttpRequest

User = get_user_model()


class EmailAuthBackend(ModelBackend):

    @staticmethod
    def authenticate(
        request: HttpRequest, username=None, password=None, **kwargs
    ) -> AbstractUser | None:

        try:
            user = User.objects.get(email=username)
            return user if user.check_password(password) else None
        except User.DoesNotExist:
            return None

    @staticmethod
    def get_user(pk) -> AbstractUser | None:
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            return None
