from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import *


class DailyWorkLoadSerialzer(ModelSerializer):
    class Meta:
        model = DailyWorkLoad
        fields = '__all__'


class ClientAssessmentSerialzer(ModelSerializer):
    class Meta:
        model = ClinicianClientAssessment
        fields = '__all__'
