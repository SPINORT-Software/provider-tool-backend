from rest_framework.serializers import ModelSerializer
from .models import *


class CommunicationLogSerializer(ModelSerializer):
    class Meta:
        model = CommunicationLog
        fields = '__all__'


class VisitorLogSerializer(ModelSerializer):
    class Meta:
        model = VisitorLog
        fields = '__all__'
