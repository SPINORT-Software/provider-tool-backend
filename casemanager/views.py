import copy
from rest_framework.permissions import IsAuthenticated, AllowAny
from casemanager.serializers import *
from documents.models import CaseManagerAssessmentFormsDocuments
from documents.serializers import InterventionFormsDocumentsSerializer, \
    CaseManagerAssessmentFormsDocumentsDetailSerializer
from rest_framework import status, generics, response
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import *
import json
from core.views import ClientAssessmentFactory
from core.constants import USER_TYPE_CASE_MANAGER
from django.core.exceptions import *

class WorkloadViews:
    class WorkloadList(generics.ListCreateAPIView):
        """
        List all workload, or create a new daily workload.
        """
        queryset = DailyWorkLoad.objects.all()
        serializer_class = DailyWorkloadSerializer
        pagination_class = None

        def create(self, request, *args, **kwargs):
            create_response = super().create(request, args, kwargs)

            return Response({
                'result': True,
                'message': 'Daily workload list created for Case Manager.',
                'data': create_response.data
            })

        def list(self, request, *args, **kwargs):
            list_response = super().list(request, args, kwargs)
            return Response({
                'result': True,
                'message': 'Daily workload list generated.',
                'data': list_response.data
            })

    class WorkloadListFilterByCaseManager(generics.ListCreateAPIView):
        """
        List all workload, or create a new daily workload.
        """
        pagination_class = None

        def get_queryset(self):
            try:
                casemanager = self.kwargs.get('casemanager')
                return super().get_queryset().filter(casemanager=casemanager)
            except ValidationError as e:
                return []

        def list(self, request, *args, **kwargs):
            list_response = super().list(request, args, kwargs)
            return Response({
                'result': True,
                'messages': 'Daily workload list generated for Case Manager.',
                'data': list_response.data
            })

        queryset = DailyWorkLoad.objects.all()
        serializer_class = DailyWorkloadSerializer

    class WorkloadDetail(generics.RetrieveUpdateDestroyAPIView):
        """
        Add a workload, update a workload detail, delete a workload
        """
        queryset = DailyWorkLoad.objects.all()
        serializer_class = DailyWorkloadSerializer

        def retrieve(self, request, *args, **kwargs):
            retrieve_response = super().retrieve(request, args, kwargs)
            return Response({
                'result': True,
                'data': retrieve_response.data
            })

        def update(self, request, *args, **kwargs):
            update_response = super().update(request, args, kwargs)
            return Response({
                'result': True,
                'data': update_response.data
            })


class ClientAssessmentViews:
    class ClientAssessmentList(generics.ListAPIView):
        """
        List all client assessments
        """
        queryset = CaseManagerClientAssessment.objects.all()
        serializer_class = CaseManagerClientAssessmentSerializer

    class ClientAssessmentListFilterByCaseManager(generics.ListAPIView):
        """
        List all client assessment.
        """
        pagination_class = None

        def get_queryset(self):
            try:
                casemanager = self.kwargs.get('casemanager')
                return super().get_queryset().filter(casemanager=casemanager)
            except ValidationError as e:
                return []

        def list(self, request, *args, **kwargs):
            list_response = super().list(request, args, kwargs)
            return Response({
                'result': True,
                'data': list_response.data
            })

        queryset = CaseManagerClientAssessment.objects.all()
        serializer_class = CaseManagerClientAssessmentSerializer

    class ClientAssessmentCreate(APIView):
        """
        Create a new client assessment
        """

        def post(self, request):
            casemanager_client_assessment = ClientAssessmentFactory(request, USER_TYPE_CASE_MANAGER)
            return casemanager_client_assessment.process_create_request()

    class ClientAssessmentDetail(generics.RetrieveAPIView):
        queryset = CaseManagerClientAssessment.objects.all()
        serializer_class = CaseManagerClientAssessmentSerializer

        def retrieve(self, request, *args, **kwargs):
            try:
                retrieve_response = super().retrieve(request, *args, **kwargs)
                assessment_forms = CaseManagerAssessmentFormsDocuments.objects.filter(
                    client_assessment=kwargs.get('pk'))

                for assessment_form in assessment_forms:
                    assessment_key = assessment_form.assessment_type
                    form_serialized_data = CaseManagerAssessmentFormsDocumentsDetailSerializer(assessment_form).data

                    if assessment_key in retrieve_response.data:
                        assessment_key_data = retrieve_response.data[assessment_key]
                        if 'assessment_forms' not in assessment_key_data:
                            assessment_key_data['assessment_forms'] = []
                        assessment_key_data['assessment_forms'].append(form_serialized_data)

                return Response({
                    'status': 200,
                    'data': retrieve_response.data
                })
            except Exception as e:
                return Response({
                    'status': 500,
                    'data': 'There was an error processing the request.'
                })


class ClientInterventionViews:
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
                        'message': 'Invalid intervention request data'
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
        queryset = ClientIntervention.objects.all()
        serializer_class = ClientInterventionListSerializer

        def get_queryset(self):
            try:
                casemanager = self.kwargs.get('casemanager')
                return super().get_queryset().filter(casemanager=casemanager)
            except ValidationError as e:
                return []

        def list(self, request, *args, **kwargs):
            list_response = super().list(request, args, kwargs)
            return Response({
                'result': True,
                'data': list_response.data
            })
