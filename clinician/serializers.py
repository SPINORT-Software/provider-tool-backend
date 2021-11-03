from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import *


class DailyWorkLoadSerialzer(ModelSerializer):
    class Meta:
        model = DailyWorkLoad
        fields = '__all__'
