# model doesn't need to create field manually and default implementation is there
from registerapp.models import Registration
from registerapp.views import User
from rest_framework.serializers import ModelSerializer

class RegisterSerializer(ModelSerializer):
    class Meta:
        model = Registration
        fields='__all__'

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields='__all__'
