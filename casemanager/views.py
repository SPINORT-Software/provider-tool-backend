from .models import DailyWorkLoad, ClientAssessment
from casemanager.serializers import DailyWorkloadSerializer, ClientAssessmentSerializer
from django.http import Http404
from rest_framework import status, generics, response
from rest_framework.views import APIView
from .constants import CLIENT_ASSESSMENT_TYPE_SERIALIZER, CLIENT_ASSESSMENT_TYPE_FIELD
from rest_framework.response import Response

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
                assessment_type = request.data['assessment']['client_status']
                return self.create_assessment_type_object(assessment_type, client_assessment, request)
            else:
                return Response('Invalid input')
        except Exception as e:
            return Response('Error')

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
                return Response('Assessment type created')
            else:
                return Response('Assessment Serializer invalid')
        else:
            return Response('Assessment Serializer Error')




class ClientAssessmentDetail(APIView):
    """
    Add a client assessment, update a client assessment detail, delete a client assessment
    """
    pass
