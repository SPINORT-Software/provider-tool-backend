from django.shortcuts import render
from rest_framework import generics
from .models import *
from .serializers import *
import datetime
from rest_framework.response import Response
from rest_framework.exceptions import *
from rest_framework.views import APIView
from core.views import ClientAssessmentFactory
from core.constants import USER_TYPE_CLINICIAN
from documents.models import ClinicianAssessmentFormsDocuments
from documents.serializers import ClinicianAssessmentFormsDocumentsDetailSerializer


class Workload:
    class WorkloadListCreateView(generics.ListCreateAPIView):
        queryset = DailyWorkLoad.objects.all()
        serializer_class = DailyWorkLoadSerializer

    class WorkloadUpdateDeleteRetrieve(generics.RetrieveUpdateDestroyAPIView):
        """
        Retrieve, Update and Delete workload.
        """
        queryset = DailyWorkLoad.objects.all()
        serializer_class = DailyWorkLoadSerializer

        def update(self, request, *args, **kwargs):
            existing_clinician = str(super().get_object().clinician.clinician_id)

            if request.data['clinician'] == existing_clinician:
                request.data['revision_date'] = datetime.date.today().strftime('%Y-%m-%d')
                response_workload = super().update(request, *args, **kwargs)

                return Response({
                    'status': 200,
                    'data': response_workload.data
                })
            else:
                return Response({
                    'status': 400,
                    'data': 'Failed to update the workload information. Incorrect Clinician value provided.'
                })

    class ClinicianWorkloadList(generics.ListAPIView):
        queryset = DailyWorkLoad.objects.all()
        serializer_class = DailyWorkLoadSerializer

        def list(self, request, *args, **kwargs):
            clinician_id = kwargs.get('clinician')
            workload_objects = DailyWorkLoad.objects.filter(clinician=clinician_id)

            return Response({
                'status': 200,
                'data': DailyWorkLoadSerializer(workload_objects, many=True).data
            })


class AssessmentViews:
    class AssessmentList(generics.ListAPIView):
        queryset = ClinicianClientAssessment.objects.all()
        serializer_class = ClientAssessmentSerializer

    class AssessmentCreate(APIView):
        def post(self, request):
            casemanager_client_assessment = ClientAssessmentFactory(request, USER_TYPE_CLINICIAN)
            return casemanager_client_assessment.process_request()

    class AssessmentDetail(generics.RetrieveUpdateDestroyAPIView):
        queryset = ClinicianClientAssessment.objects.all()
        serializer_class = ClientAssessmentDetailSerializer

        def retrieve(self, request, *args, **kwargs):
            retrieve_response = super().retrieve(request, *args, **kwargs)
            assessment_forms = ClinicianAssessmentFormsDocuments.objects.filter(client_assessment=kwargs.get('pk'))
            for assessment_form in assessment_forms:
                assessment_key = assessment_form.assessment_type
                form_serialized_data = ClinicianAssessmentFormsDocumentsDetailSerializer(assessment_form).data
                if assessment_key in retrieve_response.data:
                    assessment_key_data = retrieve_response.data[assessment_key]
                    if 'assessment_forms' not in assessment_key_data:
                        assessment_key_data['assessment_forms'] = []
                    assessment_key_data['assessment_forms'].append(form_serialized_data)

            return Response({
                'status': 200,
                'data': retrieve_response.data
            })

# class InterventionsViews:
#     class WorkloadListCreateView(generics.ListCreateAPIView):
#         queryset = DailyWorkLoad.objects.all()
#         serializer_class = DailyWorkLoadSerialzer
