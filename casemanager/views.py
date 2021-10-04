import copy

from .models import DailyWorkLoad, ClientAssessment, ClientIntervention
from casemanager.serializers import *
from documents.serializers import AssessmentFormsDocumentsSerializer
from rest_framework import status, generics, response
from rest_framework.views import APIView
from .constants import CLIENT_ASSESSMENT_TYPE_SERIALIZER, CLIENT_ASSESSMENT_TYPE_FIELD, \
    CLIENT_ASSESSMENT_FIELD_SERIALIZER
from rest_framework.response import Response
from rest_framework.status import *
import json


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
    queryset = ClientAssessment.objects.all()
    serializer_class = ClientAssessmentSerializer


class ClientAssessmentCreate(APIView):
    """
    Create a new client assessment
    """

    def post(self, request):
        try:
            serializer = ClientAssessmentSerializer(data=request.data['assessment'])
            if serializer.is_valid():
                client_assessment = serializer.save()
                request_assessment_type = request.data['assessment']['client_status']

                if request_assessment_type == "NEW_CASE_CLIENT_EXISTING_EMC_REASSESS":
                    return self.multiple_assessment_type_process(client_assessment, request, request_assessment_type)
                else:
                    return self.single_assessment_type_process(client_assessment, request, request_assessment_type)
            else:
                return Response({
                    'result': False,
                    'message': 'Invalid assessment request data'
                }, status=HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'result': False,
                'message': 'Failed to process your request. '
            }, status=HTTP_500_INTERNAL_SERVER_ERROR)

    def multiple_assessment_type_process(self, client_assessment, request, request_assessment_type):
        assessment_type_request_fields = CLIENT_ASSESSMENT_TYPE_FIELD.get('NEW_CASE_CLIENT_EXISTING_EMC_REASSESS', None)
        assessment_type_record_create = True

        if assessment_type_request_fields:
            assessment_type_data = request.data['assessment_type_data']
            for assessment_type_key in assessment_type_request_fields:
                type_data = assessment_type_data[assessment_type_key]['data']
                type_forms = assessment_type_data[assessment_type_key]['assessment_type_forms']

                AssessmentTypeSerializer = CLIENT_ASSESSMENT_FIELD_SERIALIZER.get(assessment_type_key)
                client_assessment_model_field = assessment_type_key

                assessment_type_record = self.create_assessment_type_object(AssessmentTypeSerializer,
                                                                            client_assessment_model_field,
                                                                            client_assessment,
                                                                            type_data)
                if assessment_type_record:
                    assessment_forms_create_result = self.create_assessment_forms(client_assessment, type_forms)
                    if not assessment_forms_create_result:
                        assessment_type_record_create = False
                else:
                    assessment_type_record_create = False

        if assessment_type_record_create:
            return Response({
                'result': True,
                'message': 'Client Assessment record created.'
            }, status=HTTP_201_CREATED)

        return Response({
            'result': True,
            'message': 'Failed to create Client Assessment record.'
        }, status=HTTP_500_INTERNAL_SERVER_ERROR)

    def single_assessment_type_process(self, client_assessment, request, request_assessment_type):
        assessment_type_request_data = request.data['assessment_type_data']
        AssessmentTypeSerializer = CLIENT_ASSESSMENT_TYPE_SERIALIZER.get(request_assessment_type, None)
        client_assessment_model_field = CLIENT_ASSESSMENT_TYPE_FIELD.get(request_assessment_type, None)

        assessment_type_record = self.create_assessment_type_object(AssessmentTypeSerializer,
                                                                    client_assessment_model_field,
                                                                    client_assessment,
                                                                    assessment_type_request_data)
        if assessment_type_record:
            if 'assessment_type_forms' in request.data:
                forms_request_data = request.data['assessment_type_forms']
                assessment_forms_create_result = self.create_assessment_forms(client_assessment, forms_request_data)
                if assessment_forms_create_result:
                    return Response({
                        'result': True,
                        'message': 'Client Assessment record created.'
                    }, status=HTTP_201_CREATED)
        return Response({
            'result': True,
            'message': 'Failed to create Client Assessment record.'
        }, status=HTTP_500_INTERNAL_SERVER_ERROR)

    def create_assessment_forms(self, client_assessment, forms_request_data):
        assessmentFormsCreate = True
        if any(key in forms_request_data for key in ("provider_specific_forms", "assessment_forms")) and isinstance(
                forms_request_data, dict):
            for form in forms_request_data:
                if isinstance(forms_request_data[form], list):
                    for form_document in forms_request_data[form]:
                        serializer_data = {
                            "document": form_document,
                            "client_assessment": client_assessment.client_assessment_id
                        }
                        if form == "provider_specific_forms":
                            serializer_data["is_provider_form"] = True
                        form_document_serializer = AssessmentFormsDocumentsSerializer(data=serializer_data)
                        if form_document_serializer.is_valid():
                            form_document_serializer.save()
                        else:
                            assessmentFormsCreate = False
        else:
            return False

        return assessmentFormsCreate

    def create_assessment_type_object(self, AssessmentTypeSerializer, client_assessment_model_field, client_assessment,
                                      assessment_type_request_data):
        if AssessmentTypeSerializer:
            assessment_type_serializer = AssessmentTypeSerializer(data=assessment_type_request_data)

            if assessment_type_serializer.is_valid():
                assessment_type_record = assessment_type_serializer.save()
                setattr(client_assessment, client_assessment_model_field, assessment_type_record)
                client_assessment.save()
                return assessment_type_record
        return False


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
                    return Response({
                        'result': True,
                        'message': 'Client Intervention record created. '
                    }, status=HTTP_201_CREATED)
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
