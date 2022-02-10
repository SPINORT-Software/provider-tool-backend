from .models import ExternalCMClientIntervention
from .serializers import *
from rest_framework import generics, response
from django.core.exceptions import ValidationError
from documents.serializers import ExternalCMInterventionFormsDocumentsSerializer
import copy


class ClientInterventionList(generics.ListCreateAPIView):
    """
    List all client assessments
    """
    queryset = ExternalCMClientIntervention.objects.all()
    serializer_class = ExternalCMInterventionSerializer

    def post(self, request, *args, **kwargs):
        add_response = super().post(request, args, kwargs)

        if add_response.status_code == 201:
            intervention_id = add_response.data.get('intervention_id', None)
            self.create_intervention_forms(intervention_id, request.data.get('forms', []))

        return response.Response({
            'result': True if add_response.status_code == 201 else False,
            'data': add_response.data
        })

    def create_intervention_forms(self, intervention_id, forms_request_data):
        if not intervention_id:
            return False

        intervention_forms_create = True
        if isinstance(forms_request_data, list):
            for form_document in forms_request_data:
                serializer_data = {
                    "document": form_document,
                    "client_intervention": intervention_id
                }
                form_document_serializer = ExternalCMInterventionFormsDocumentsSerializer(data=serializer_data)
                if form_document_serializer.is_valid():
                    form_document_serializer.save()
                else:
                    intervention_forms_create = False

        return intervention_forms_create


class ClientInterventionListFilterByCaseManager(generics.ListAPIView):
    """
    List all client intervention.
    """
    pagination_class = None
    queryset = ExternalCMClientIntervention.objects.all()
    serializer_class = ExternalCMInterventionSerializer

    def get_queryset(self):
        try:
            casemanager = self.kwargs.get('casemanager')
            return super().get_queryset().filter(casemanager=casemanager)
        except ValidationError as e:
            return []

    def list(self, request, *args, **kwargs):
        list_response = super().list(request, args, kwargs)
        return response.Response({
            'result': True,
            'data': list_response.data
        })
