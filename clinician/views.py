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
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from django.core.exceptions import *
from rest_framework.status import *
import json
import copy
from documents.serializers import InterventionFormsDocumentsSerializer


class Workload:
    class WorkloadListCreateView(generics.ListCreateAPIView):
        queryset = DailyWorkLoad.objects.all()
        serializer_class = DailyWorkLoadSerializer

        def list(self, request, *args, **kwargs):
            list_response = super().list(request, args, kwargs)
            return Response({
                'result': True,
                'messages': 'Daily workload list generated for Case Manager.',
                'data': list_response.data
            })

        def create(self, request, *args, **kwargs):
            create_response = super().create(request, args, kwargs)

            return Response({
                'result': True,
                'message': 'Daily workload list created for Clinician.',
                'data': create_response.data
            })

    class WorkloadUpdateDeleteRetrieve(generics.RetrieveUpdateDestroyAPIView):
        """
        Retrieve, Update and Delete workload.
        """
        queryset = DailyWorkLoad.objects.all()
        serializer_class = DailyWorkLoadSerializer

        def retrieve(self, request, *args, **kwargs):
            retrieve_response = super().retrieve(request, args, kwargs)
            return Response({
                'result': True,
                'data': retrieve_response.data
            })

        def update(self, request, *args, **kwargs):
            existing_clinician = str(super().get_object().clinician.app_user_id)

            if request.data['clinician'] == existing_clinician:
                request.data['revision_date'] = datetime.date.today().strftime('%Y-%m-%d')
                response_workload = super().update(request, *args, **kwargs)

                return Response({
                    'result': True,
                    'status': 200,
                    'data': response_workload.data
                }, status=HTTP_200_OK)
            else:
                return Response({
                    'result': False,
                    'status': 400,
                    'data': 'Failed to update the workload information. Incorrect Clinician value provided.'
                }, status=HTTP_400_BAD_REQUEST)

    class ClinicianWorkloadList(generics.ListAPIView):
        queryset = DailyWorkLoad.objects.all()
        serializer_class = DailyWorkLoadSerializer

        def list(self, request, *args, **kwargs):
            clinician_id = kwargs.get('clinician')
            workload_objects = DailyWorkLoad.objects.filter(clinician=clinician_id)

            return Response({
                'result': True,
                'status': 200,
                'data': DailyWorkLoadSerializer(workload_objects, many=True).data
            })


class AssessmentViews:
    class AssessmentList(generics.ListAPIView):
        queryset = ClinicianClientAssessment.objects.all()
        serializer_class = ClientAssessmentSerializer

    class AssessmentCreate(APIView):
        def post(self, request):
            clinician_client_assessment = ClientAssessmentFactory(request, USER_TYPE_CLINICIAN)
            return clinician_client_assessment.process_create_request()

    class AssessmentRetrieveView(generics.RetrieveUpdateAPIView):
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

        def update(self, request, *args, **kwargs):
            existing_object_client = super().get_object().client
            casemanager_client_assessment = ClientAssessmentFactory(request, USER_TYPE_CLINICIAN)
            return casemanager_client_assessment.process_update_request(existing_object_client)

    class ClinicianAssessmentList(ModelViewSet):
        queryset = ClinicianClientAssessment.objects.all()
        serializer_class = ClientAssessmentSerializer
        pagination_class = PageNumberPagination

        def get_queryset(self):
            try:
                clinician_id = self.kwargs.get('clinician')
                return super().get_queryset().filter(clinician=clinician_id)
            except ValidationError as e:
                return []

        def list(self, request, *args, **kwargs):
            list_response = super().list(request, args, kwargs)
            return Response({
                'result': True,
                'message': 'Assessment list generated for Clinician.',
                'data': list_response.data
            })


class ClientInterventionViews:
    class ClientInterventionList(generics.ListAPIView):
        queryset = ClinicianClientInterventions.objects.all()
        serializer_class = ClinicianClientInterventions

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

                serializer = ClientInterventionSerializer(data=request.data['intervention'])
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
                        'message': 'Invalid intervention request data'
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

    class ClientInterventionListFilterByCaseManager(generics.ListAPIView):
        """
        List all client intervention for a Case Manager.
        """
        pagination_class = None
        queryset = ClinicianClientInterventions.objects.all()
        serializer_class = ClientInterventionListSerializer

        def get_queryset(self):
            try:
                clinician = self.kwargs.get('clinician')
                return super().get_queryset().filter(clinician=clinician)
            except ValidationError as e:
                return []

        def list(self, request, *args, **kwargs):
            list_response = super().list(request, args, kwargs)
            return Response({
                'result': True,
                'data': list_response.data
            })
