import copy
from rest_framework.permissions import IsAuthenticated, AllowAny
from casemanager.serializers import *
from documents.serializers import InterventionFormsDocumentsSerializer
from rest_framework import status, generics, response
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import *
import json
from core.views import ClientAssessmentFactory
from core.constants import USER_TYPE_CASE_MANAGER
from .serializers import CaseManagerClientAssessmentSerializer


class WorkloadList(generics.ListCreateAPIView):
    """
    List all workload, or create a new daily workload.
    """
    queryset = DailyWorkLoad.objects.all()
    serializer_class = DailyWorkloadSerializer


class WorkloadDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Add a workload, update a workload detail, delete a workload
    """
    queryset = DailyWorkLoad.objects.all()
    serializer_class = DailyWorkloadSerializer


class ClientAssessmentList(generics.ListAPIView):
    """
    List all client assessments
    """
    queryset = CaseManagerClientAssessment.objects.all()
    serializer_class = CaseManagerClientAssessmentSerializer


class ClientAssessmentCreate(APIView):
    """
    Create a new client assessment
    """

    def post(self, request):
        casemanager_client_assessment = ClientAssessmentFactory(request, USER_TYPE_CASE_MANAGER)
        return casemanager_client_assessment.process_request()


class ClientAssessmentDetail(APIView):
    """
    Add a client assessment, update a client assessment detail, delete a client assessment
    """
    pass


class ClientInterventionList(generics.ListAPIView):
    queryset = ClientIntervention.objects.all()
    serializer_class = ClientInterventionSerializer


class ClientInterventionCreate(APIView):
    """
    Create a new client intervention.
    """

    def post(self, request):
        try:
            if 'intervention' not in request.data:
                return Response({
                    'result': False,
                    'message': 'Invalid assessment request data'
                }, status=HTTP_400_BAD_REQUEST)

            intervention_data = copy.deepcopy(request.data['intervention'])

            if "clinical_type" in intervention_data:
                clinical_type_json = json.dumps(intervention_data["clinical_type"])
                intervention_data["clinical_type"] = clinical_type_json

            serializer = ClientInterventionSerializer(data=intervention_data)
            if serializer.is_valid():
                client_intervention = serializer.save()
                if client_intervention:
                    forms_request_data = request.data["forms"]
                    forms_create_result = self.create_intervention_forms(client_intervention, forms_request_data)

                    if forms_create_result:
                        return Response({
                            'result': True,
                            'message': 'Client Intervention record created.'
                        }, status=HTTP_201_CREATED)
                    else:
                        return Response({
                            'result': True,
                            'message': 'Failed to create Client Intervention record.'
                        }, status=HTTP_500_INTERNAL_SERVER_ERROR)
                else:
                    return Response({
                        'result': False,
                        'message': 'Failed to create Client Intervention record.'
                    }, status=HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                print(serializer.errors)
                return Response({
                    'result': False,
                    'message': 'Invalid assessment request data'
                }, status=HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(str(e))
            return Response({
                'result': False,
                'message': 'Failed to process your request. '
            }, status=HTTP_500_INTERNAL_SERVER_ERROR)

    def create_intervention_forms(self, client_intervention, forms_request_data):
        interventionFormsCreate = True
        if isinstance(forms_request_data, dict):
            for form in forms_request_data:
                if isinstance(forms_request_data[form], list):
                    for form_document in forms_request_data[form]:
                        serializer_data = {
                            "document": form_document,
                            "client_intervention": client_intervention.intervention_id
                        }
                        form_document_serializer = InterventionFormsDocumentsSerializer(data=serializer_data)
                        if form_document_serializer.is_valid():
                            form_document_serializer.save()
                        else:
                            interventionFormsCreate = False
        else:
            return False

        return interventionFormsCreate
