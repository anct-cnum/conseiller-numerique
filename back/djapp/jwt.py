from django.contrib.auth.models import update_last_login
from djapp.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class CnumTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user: User):
        token = super().get_token(user)
        update_last_login(None, user)

        # Add custom claims
        token['email'] = user.email
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['username'] = user.username
        token['is_admin'] = user.is_superuser
        token['is_staff'] = user.is_staff

        return token


class CnumTokenObtainPairView(TokenObtainPairView):
    serializer_class = CnumTokenObtainPairSerializer
