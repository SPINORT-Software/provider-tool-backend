from rest_framework.serializers import ModelSerializer
from .models import *
from clientpatient.serializers import ClientSerializer
from core.serializers.models import ExistingEMCAssessmentSerializer, ClientReAssessmentSerializer, NewEMCAssessmentSerializer


class DailyWorkLoadSerializer(ModelSerializer):
    class Meta:
        model = DailyWorkLoad
        fields = '__all__'


class ClientAssessmentSerializer(ModelSerializer):
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['client'] = ClientSerializer(instance.client).data
        response['clinician'] = ClientSerializer(instance.client).data
        return response

    class Meta:
        model = ClinicianClientAssessment
        fields = '__all__'


class ClientAssessmentDetailSerializer(ModelSerializer):
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['client'] = ClientSerializer(instance.client).data
        response['clinician'] = ClientSerializer(instance.client).data
        response['existing_assessment'] = ExistingEMCAssessmentSerializer(instance.existing_assessment).data
        response['reassessment'] = ClientReAssessmentSerializer(instance.reassessment).data
        response['newextramuralclient_assessment'] = NewEMCAssessmentSerializer(
            instance.newextramuralclient_assessment).data
        response['newextramuralclient_assessment'] = NewEMCAssessmentSerializer(
            instance.newextramuralclient_assessment).data
        return response

    class Meta:
        model = ClinicianClientAssessment
        fields = '__all__'
