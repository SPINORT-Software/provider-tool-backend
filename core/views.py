from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from rest_framework import permissions, status
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response
from rest_framework.views import APIView

import casemanager.serializers
import clinician.serializers
from .serializers.auth import UserSerializer, UserSerializerWithToken
from .constants import *
from rest_framework.status import *
from documents.serializers import *
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from providertool.errors import default_error_response


@api_view(['GET'])
@authentication_classes((JSONWebTokenAuthentication,))
def current_user(request):
    """
    Determine the current user by their token, and return their data
    """
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


def my_jwt_response_handler(token, user=None, request=None):
    return {
        'token': token,
        'user': UserSerializer(user, context={'request': request}).data
    }


class UserList(APIView):
    """
    Create a new user. It's called 'UserList' because normally we'd have a get
    method here too, for retrieving a list of all User objects.
    """
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = UserSerializerWithToken(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
            self.ClientAssessmentSerializer = casemanager.serializers.ClientAssessmentSerializer
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
                request_assessment_type = assessment_data_serializer.validated_data['client_status']

                if request_assessment_type == NEW_CASE_CLIENT_EXISTING_EMC_REASSESS:
                    return self.multiple_assessment_type_process(client_assessment, request_assessment_type)
                elif request_assessment_type in (
                        NEW_CASE_CLIENT_NEW_EXTRA_MURAL_CLIENT, NEW_CASE_CLIENT_EXISTING_EMC_NO_REASSESS,
                        EXISTING_CASE_CLIENT_REASSESS):
                    return self.single_assessment_type_process(client_assessment, request_assessment_type)
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

    def multiple_assessment_type_process(self, client_assessment, request_assessment_type):
        assessment_type_request_fields = CLIENT_ASSESSMENT_TYPE_FIELD.get('NEW_CASE_CLIENT_EXISTING_EMC_REASSESS', None)
        assessment_type_record_create = True

        if assessment_type_request_fields:
            assessment_type_data = self.request_data['assessment_type_data']

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

        return Response({
            'result': True,
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
                'message': 'Failed to create Client Assessment record.'
            }, status=HTTP_500_INTERNAL_SERVER_ERROR)

    def create_assessment_forms(self, client_assessment, forms_request_data, assessment_type):
        assessment_forms_create = True

        if any(key in forms_request_data for key in ("provider_specific_forms", "assessment_forms")) and isinstance(
                forms_request_data, dict):
            for form in forms_request_data:
                if isinstance(forms_request_data[form], list):
                    for form_document in forms_request_data[form]:

                        print(assessment_type)

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
