from rest_framework.serializers import ModelSerializer
from .models import *
from clientpatient.serializers import ClientSerializer
from documents.serializers import ExternalCMInterventionFormsDocumentsSerializer
from documents.models import ExternalCMInterventionFormsDocuments


class ExternalCMInterventionSerializer(ModelSerializer):
    def to_representation(self, instance):
        response = super().to_representation(instance)

        client = ClientSerializer(instance.client).data
        response['client_fullname'] = client['user']['fullname']
        response['client_status'] = client['client_status']
        response['client'] = ClientSerializer(instance.client).data
        response['forms'] = ExternalCMInterventionFormsDocumentsSerializer(
            ExternalCMInterventionFormsDocuments.objects.filter(
                client_intervention=instance.intervention_id
            ), many=True).data

        return response

    class Meta:
        model = ExternalCMClientIntervention
        fields = '__all__'
