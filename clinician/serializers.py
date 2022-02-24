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
        response['clinician'] = ClientSerializer(instance.clinician).data

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

class ClientAssessmentBasicDataSerializer(ModelSerializer):
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['client'] = ClientSerializer(instance.client).data
        response['clinician'] = ClientSerializer(instance.client).data
        return response

    class Meta:
        model = ClinicianClientAssessment
        fields = '__all__'


class ClientInterventionSerializer(ModelSerializer):
    class Meta:
        model = ClinicianClientInterventions
        fields = '__all__'

class ClientInterventionListSerializer(ModelSerializer):
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['client'] = ClientSerializer(instance.client).data
        return response

    class Meta:
        model = ClinicianClientInterventions
        fields = '__all__'

class ClientInterventionBasicDataSerializer(ModelSerializer):
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['client'] = ClientSerializer(instance.client).data
        return response

    class Meta:
        model = ClinicianClientInterventions
        fields = '__all__'
