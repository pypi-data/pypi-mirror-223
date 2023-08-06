from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from .models import User_details
from rest_framework.exceptions import AuthenticationFailed,PermissionDenied
from django.contrib.auth.hashers import check_password

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        # UserModel = User()
        try:
            user = User_details.objects.get(email=username)
        except User_details.DoesNotExist:
                raise AuthenticationFailed ("Email is not valid")
        else:
            if check_password(password,user.password):
                return user
            raise PermissionDenied("Password is not valid")