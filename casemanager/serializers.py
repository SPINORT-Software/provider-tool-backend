from rest_framework.serializers import ModelSerializer
from .models import *
from clientpatient.serializers import ClientSerializer
from core.serializers.models import ExistingEMCAssessmentSerializer, ClientReAssessmentSerializer, \
    NewEMCAssessmentSerializer


class DailyWorkloadSerializer(ModelSerializer):
    class Meta:
        model = DailyWorkLoad
        fields = '__all__'


class ClientInterventionSerializer(ModelSerializer):
    class Meta:
        model = ClientIntervention
        fields = '__all__'

class ClientInterventionListSerializer(ModelSerializer):
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['client'] = ClientSerializer(instance.client).data
        return response

    class Meta:
        model = ClientIntervention
        fields = '__all__'


class CaseManagerClientAssessmentSerializer(ModelSerializer):
    def to_representation(self, instance):
        response = super().to_representation(instance)
        client = ClientSerializer(instance.client).data
        response['client_fullname'] = client['user']['fullname']
        response['client_status'] = client['client_status']
        response['client'] = ClientSerializer(instance.client).data
        response['existing_assessment'] = ExistingEMCAssessmentSerializer(instance.existing_assessment).data
        response['reassessment'] = ClientReAssessmentSerializer(instance.reassessment).data
        response['newextramuralclient_assessment'] = NewEMCAssessmentSerializer(
            instance.newextramuralclient_assessment).data
        response['newextramuralclient_assessment'] = NewEMCAssessmentSerializer(
            instance.newextramuralclient_assessment).data
        return response

    class Meta:
        model = CaseManagerClientAssessment
        fields = '__all__'



