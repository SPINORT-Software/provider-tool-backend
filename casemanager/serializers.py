from rest_framework.serializers import ModelSerializer
from .models import *


class DailyWorkloadSerializer(ModelSerializer):
    class Meta:
        model = DailyWorkLoad
        fields = '__all__'


class ClientInterventionSerializer(ModelSerializer):
    class Meta:
        model = ClientIntervention
        fields = '__all__'


class CaseManagerClientAssessmentSerializer(ModelSerializer):
    class Meta:
        model = CaseManagerClientAssessment
        fields = '__all__'
