from django.conf import settings
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from project.models import User

class Authentication(BaseBackend):
    
    def authenticate(self, request, email=None, password=None):
        try:
            user = User.objects.get(email=email)
            if(user.check_password(password)):
                return user
        except User.DoesNotExist:
            return None
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None