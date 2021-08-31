# model doesn't need to create field manually and default implementation is there
from registerapp.models import UserRegistration
from rest_framework.serializers import ModelSerializer


class UserRegistrationSerializer(ModelSerializer):
    class Meta:
        model = UserRegistration
        fields = '__all__'
