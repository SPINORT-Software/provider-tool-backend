from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from rest_framework import permissions, status
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView

import casemanager.serializers
import clinician.serializers
# from .serializers.auth import UserSerializer, UserSerializerWithToken
from authentication.serializers import UserSearchSerializer
from .constants import *
from rest_framework.status import *
from documents.serializers import *
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from providertool.errors import default_error_response
from rest_framework import filters
from authentication.models import User as CustomAuthUser, Types as ApplicationUserTypes
from clientpatient.models import Client, ClientStatus
from clientpatient.serializers import ClientSerializer
from django.core.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from authentication.models import ApplicationUser
from authentication.serializers import ApplicationUserListSerializer, ApplicationUserSearchRequestDataSerializer
from django.contrib.postgres.search import SearchVector
from django.db.models import Value as V
from django.db.models.functions import Concat


class UserSearch(ListAPIView):
    queryset = CustomAuthUser.objects.all()
    serializer_class = UserSearchSerializer
    filter_backends = (filters.SearchFilter,)
    pagination_class = None
    search_fields = ('first_name', 'last_name', 'email')


class ClientSearch(ListAPIView):
    queryset = CustomAuthUser.objects.all()
    serializer_class = UserSearchSerializer
    filter_backends = (filters.SearchFilter,)
    pagination_class = None
    search_fields = ('first_name', 'last_name', 'email')

    def get_queryset(self):
        try:
            return super().get_queryset().filter(user_type=ApplicationUserTypes.TYPE_CLIENT,
                                                 application_user__client_status=ClientStatus.ACTIVE_CLIENT)
        except ValidationError as e:
            return []


class ClientSearchByEmail(ListAPIView):
    queryset = CustomAuthUser.objects.all()
    serializer_class = UserSearchSerializer
    filter_backends = (filters.SearchFilter,)
    pagination_class = None
    search_fields = ('email',)


class ApplicationUserView(ListAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = None

    model = ApplicationUser
    queryset = ApplicationUser.objects.all()
    serializer_class = ApplicationUserListSerializer

    def filter_queryset(self, queryset):
        request_data = ApplicationUserSearchRequestDataSerializer(data=self.request.data)
        filtered_queryset = queryset
        if request_data.is_valid():
            if "name" in dict(request_data.validated_data):
                name_data = request_data.validated_data["name"]
                del request_data.validated_data["name"]

                filtered_queryset = filtered_queryset.annotate(
                    full_name=Concat('user__first_name', V(' '), 'user__last_name')). \
                    filter(full_name__icontains=name_data)

            filtered_queryset = filtered_queryset.filter(**request_data.validated_data)

        return filtered_queryset

    def get_queryset(self):
        queryset = super(ApplicationUserView, self).get_queryset()
        return queryset


class ClientAssessmentFactory:
    """
    Create a new client assessment
    """

    def __init__(self, request, user_type):
        self.request = request
        self.request_data = request.data
        self.user_type = user_type

        if user_type == USER_TYPE_CASE_MANAGER:
            """
            Client Assessment serializers for Case Manager 
            """
            self.ClientAssessmentSerializer = casemanager.serializers.CaseManagerClientAssessmentSerializer
            self.AssessmentFormsSerializer = CaseManagerAssessmentFormsDocumentsSerializer
        if user_type == USER_TYPE_CLINICIAN:
            """
            Client Assessment serializers for Clinician 
            """
            self.ClientAssessmentSerializer = clinician.serializers.ClientAssessmentSerializer
            self.AssessmentFormsSerializer = ClinicianAssessmentFormsDocumentsSerializer

    def process_create_request(self):
        try:
            assessment_data_serializer = self.ClientAssessmentSerializer(data=self.request_data['assessment'])
            if assessment_data_serializer.is_valid():
                client_assessment = assessment_data_serializer.save()
                request_assessment_type = assessment_data_serializer.validated_data['assessment_status']

                if request_assessment_type == NEW_CASE_CLIENT_EXISTING_EMC_REASSESS:
                    return self.multiple_assessment_type_process(client_assessment, request_assessment_type)
                elif request_assessment_type in (
                        NEW_CASE_CLIENT_NEW_EXTRA_MURAL_CLIENT, NEW_CASE_CLIENT_EXISTING_EMC_NO_REASSESS,
                        EXISTING_CASE_CLIENT_REASSESS):
                    return self.single_assessment_type_process(client_assessment, request_assessment_type)
            else:
                return Response({
                    'result': False,
                    'message': assessment_data_serializer.errors
                }, status=HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'result': False,
                'message': 'Failed to process your request. ',
            }, status=HTTP_500_INTERNAL_SERVER_ERROR)

    def multiple_assessment_type_process(self, client_assessment, request_assessment_type):
        try:
            assessment_type_record_create = True
            assessments_created = []

            assessment_type_request_fields = CLIENT_ASSESSMENT_TYPE_FIELD.get('NEW_CASE_CLIENT_EXISTING_EMC_REASSESS',
                                                                              None)

            if assessment_type_request_fields:
                assessment_type_data = self.request_data['assessment_type_data']

                for assessment_type_key in assessment_type_request_fields:
                    type_data = assessment_type_data[assessment_type_key]['data']

                    AssessmentTypeSerializer = CLIENT_ASSESSMENT_FIELD_SERIALIZER.get(assessment_type_key)
                    client_assessment_model_field = assessment_type_key

                    assessment_type_record = self.create_assessment_type_object(AssessmentTypeSerializer,
                                                                                client_assessment_model_field,
                                                                                client_assessment,
                                                                                type_data)

                    if assessment_type_record:
                        assessments_created.append(assessment_type_record)

                    if assessment_type_record:
                        """
                        If assessment_type_forms exists in request body. 
                        """
                        if "assessment_type_forms" in assessment_type_data[assessment_type_key]:
                            type_forms = assessment_type_data[assessment_type_key]['assessment_type_forms']
                            assessment_forms_create_result = self.create_assessment_forms(client_assessment, type_forms,
                                                                                          assessment_type_key)
                            if not assessment_forms_create_result:
                                assessment_type_record_create = False
                    else:
                        assessment_type_record_create = False

            if assessment_type_record_create:
                return Response({
                    'result': True,
                    'message': 'Client Assessment record created.',
                    'data': self.ClientAssessmentSerializer(client_assessment).data
                }, status=HTTP_201_CREATED)

            client_assessment.delete()
            for single_assessment_record in assessments_created:
                single_assessment_record.delete() if single_assessment_record is not None else None

            return Response({
                'result': False,
                'message': 'Failed to create Client Assessment record.'
            }, status=HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            client_assessment.delete()
            for single_assessment_record in assessments_created:
                single_assessment_record.delete() if single_assessment_record is not None else None
            return Response({
                'result': False,
                'message': 'Failed to create Client Assessment record.'
            }, status=HTTP_500_INTERNAL_SERVER_ERROR)

    def single_assessment_type_process(self, client_assessment, request_assessment_type):
        assessment_type_request_data = self.request_data['assessment_type_data']

        AssessmentTypeSerializer = CLIENT_ASSESSMENT_TYPE_SERIALIZER.get(request_assessment_type, None)
        client_assessment_model_field = CLIENT_ASSESSMENT_TYPE_FIELD.get(request_assessment_type, None)

        assessment_type_record = self.create_assessment_type_object(AssessmentTypeSerializer,
                                                                    client_assessment_model_field,
                                                                    client_assessment,
                                                                    assessment_type_request_data)

        if assessment_type_record:
            if 'assessment_type_forms' in self.request_data:
                forms_request_data = self.request_data['assessment_type_forms']

                assessment_forms_create_result = self.create_assessment_forms(client_assessment, forms_request_data,
                                                                              client_assessment_model_field)
                if assessment_forms_create_result:
                    return Response({
                        'result': True,
                        'message': 'Client Assessment record created.',
                        'data': self.ClientAssessmentSerializer(client_assessment).data
                    }, status=HTTP_201_CREATED)
                else:
                    return Response({
                        'result': True,
                        'message': 'Failed to create Client Assessment forms.'
                    }, status=HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                return Response({
                    'result': True,
                    'message': 'Client Assessment record created.',
                    'data': self.ClientAssessmentSerializer(client_assessment).data
                }, status=HTTP_201_CREATED)
        else:
            return Response({
                'result': True,
                'message': 'Failed to create Client Assessment record.'
            }, status=HTTP_500_INTERNAL_SERVER_ERROR)

    def create_assessment_forms(self, client_assessment, forms_request_data, assessment_type):
        assessment_forms_create = True

        if any(key in forms_request_data for key in ("provider_specific_forms", "assessment_forms")):
            for form in forms_request_data:
                if isinstance(forms_request_data[form], list):
                    for form_document in forms_request_data[form]:
                        serializer_data = {
                            "document": form_document,
                            "client_assessment": client_assessment.client_assessment_id,
                            "assessment_type": assessment_type
                        }
                        if form == "provider_specific_forms":
                            serializer_data["is_provider_form"] = True
                        form_document_serializer = self.AssessmentFormsSerializer(data=serializer_data)
                        if form_document_serializer.is_valid():
                            form_document_serializer.save()
                        else:
                            assessment_forms_create = False
        else:
            return False

        return assessment_forms_create

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

    def process_update_request(self, existing_object_client):
        try:
            assessment_data_serializer = self.ClientAssessmentSerializer(data=self.request_data['assessment'])
            if assessment_data_serializer.is_valid():
                return Response("OK")
                # client_assessment = assessment_data_serializer.save()
                # request_assessment_type = assessment_data_serializer.validated_data['client_status']
                #
                # if request_assessment_type == NEW_CASE_CLIENT_EXISTING_EMC_REASSESS:
                #     return self.multiple_assessment_type_process(client_assessment, request_assessment_type)
                # elif request_assessment_type in (
                #         NEW_CASE_CLIENT_NEW_EXTRA_MURAL_CLIENT, NEW_CASE_CLIENT_EXISTING_EMC_NO_REASSESS,
                #         EXISTING_CASE_CLIENT_REASSESS):
                #     return self.single_assessment_type_process(client_assessment, request_assessment_type)
            else:
                return Response({
                    'result': False,
                    'message': default_error_response(assessment_data_serializer)
                }, status=HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'result': False,
                'message': 'Failed to process your request. '
            }, status=HTTP_500_INTERNAL_SERVER_ERROR)
