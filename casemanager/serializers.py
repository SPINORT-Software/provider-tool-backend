from rest_framework.serializers import ModelSerializer
from .models import *


class DailyWorkloadSerializer(ModelSerializer):
    class Meta:
        model = DailyWorkLoad
        fields = '__all__'


class ClientAssessmentSerializer(ModelSerializer):
    class Meta:
        model = ClientAssessment
        fields = '__all__'


class ExistingEMCAssessmentSerializer(ModelSerializer):
    class Meta:
        model = ExistingEMCAssessment
        fields = '__all__'


class NewEMCAssessmentSerializer(ModelSerializer):
    class Meta:
        model = NewEMCAssessment
        fields = '__all__'


class ClientReAssessmentSerializer(ModelSerializer):
    class Meta:
        model = ClientReAssessment
        fields = '__all__'
