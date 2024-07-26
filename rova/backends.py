from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from .models import CustomUser
from django.core.exceptions import ObjectDoesNotExist

class EmailBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        UserModel = CustomUser
        try:
            user = UserModel.objects.get(email=email)
            if user.check_password(password):
                return user
        except ObjectDoesNotExist:
            return None

    def get_user(self, user_id):
        UserModel = CustomUser
        try:
            return UserModel.objects.get(pk=user_id)
        except ObjectDoesNotExist:
            return None
