from core.models import *
from rest_framework.serializers import ModelSerializer


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