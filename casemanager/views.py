from .models import DailyWorkLoad, ClientAssessment
from casemanager.serializers import DailyWorkloadSerializer, ClientAssessmentSerializer
from documents.serializers import AssessmentFormsDocumentsSerializer
from rest_framework import status, generics, response
from rest_framework.views import APIView
from .constants import CLIENT_ASSESSMENT_TYPE_SERIALIZER, CLIENT_ASSESSMENT_TYPE_FIELD
from rest_framework.response import Response
from rest_framework.status import *


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
                assessment_type_record = self.create_assessment_type_object(request_assessment_type, client_assessment,
                                                                            request)
                if assessment_type_record:
                    assessment_forms_create_result = self.create_assessment_forms(client_assessment, request)
                    if assessment_forms_create_result:
                        return Response({
                            'result': True,
                            'message': 'Client Assessment record created.'
                        }, status=HTTP_201_CREATED)

                return Response({
                    'result': True,
                    'message': 'Failed to create Client Assessment record.'
                }, status=HTTP_500_INTERNAL_SERVER_ERROR)
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

    def create_assessment_forms(self, client_assessment, request):
        assessmentFormsCreate = True
        if 'assessment_type_forms' in request.data:
            forms_request_data = request.data['assessment_type_forms']
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

    def create_assessment_type_object(self, assessment_type, client_assessment, request):
        AssessmentTypeSerializer = CLIENT_ASSESSMENT_TYPE_SERIALIZER.get(assessment_type, None)
        if AssessmentTypeSerializer:
            assessment_type_request_data = request.data['assessment_type_data']
            assessment_type_serializer = AssessmentTypeSerializer(data=assessment_type_request_data)

            if assessment_type_serializer.is_valid():
                assessment_type_record = assessment_type_serializer.save()
                client_assessment_field = CLIENT_ASSESSMENT_TYPE_FIELD.get(assessment_type, None)
                setattr(client_assessment, client_assessment_field, assessment_type_record)
                client_assessment.save()
                return assessment_type_record
            print(assessment_type_serializer.errors)
        return False


class ClientAssessmentDetail(APIView):
    """
    Add a client assessment, update a client assessment detail, delete a client assessment
    """
    pass
