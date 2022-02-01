import datetime

from rest_framework import status, generics, response, views
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from .serializers import *
from django.core import serializers
from django.forms.models import model_to_dict
from django.core.exceptions import *
import copy


class CommunicationLogs:
    class CommunicationLogList(generics.ListCreateAPIView):
        """
        List all communication logs.
        """
        queryset = CommunicationLog.objects.all()
        serializer_class = CommunicationLogSerializer

        def create(self, request, *args, **kwargs):
            response = super().create(request, *args, **kwargs)
            return Response({
                'status': True,
                'data': response.data
            }, status=status.HTTP_201_CREATED)

    class CommunicationLogUpdateDeleteRetrieve(generics.RetrieveUpdateDestroyAPIView):
        """
        Retrieve, Update and Delete communication logs.
        """
        queryset = CommunicationLog.objects.all()
        serializer_class = CommunicationLogSerializer


class VisitorLogs:
    class VisitorsLogList(generics.ListCreateAPIView):
        """
        List all visitor logs.
        """
        queryset = VisitorLog.objects.all()
        serializer_class = VisitorLogSerializer

        def create(self, request, *args, **kwargs):
            response = super().create(request, *args, **kwargs)
            return Response({
                'status': True,
                'data': response.data
            }, status=status.HTTP_201_CREATED)

    class VisitorsLogUpdateDeleteRetrieve(generics.RetrieveUpdateDestroyAPIView):
        """
        Retrieve, Update and Delete visitor logs.
        """
        queryset = VisitorLog.objects.all()
        serializer_class = VisitorLogSerializer


class PersonalInformationViews:
    @staticmethod
    def add_home_safety(personal_id, home_safety_assessment):
        # Add Home Safety Assessment data
        for assessment_item in home_safety_assessment:
            assessment_item['answer'] = assessment_item['answer'].replace("&$#", " ")
            assessment_item['question'] = assessment_item['question'].replace("&$#", " ")
            assessment_item['question_group'] = assessment_item['question_group'].replace("&$#", " ")
            assessment_item['personal_information'] = personal_id

        home_safety_assessment_serializer = HomeSafetyAssessmentSerialzer(data=home_safety_assessment, many=True)

        if home_safety_assessment_serializer.is_valid():
            home_safety_assessment_serializer.save()
            return True, home_safety_assessment_serializer.data
        else:
            # TODO log error
            return False, None

    class ClientPersonalInformationRetrieve(generics.RetrieveAPIView):
        queryset = ClinicalInformation.objects.all()
        serializer_class = ClinicalInformationSerializer
        lookup_field = 'client'

        def get_queryset(self):
            try:
                client = self.kwargs.get('client')
                return super().get_queryset().filter(client=client)
            except ValidationError as e:
                return []

        def retrieve(self, request, *args, **kwargs):
            retrieve_response = super().retrieve(request, *args, **kwargs)

            return Response({
                'status': 200,
                'data': retrieve_response.data
            })

    class PersonalInformationList(generics.ListAPIView):
        """
        List all client's Personal Information
        """
        queryset = PersonalInformation.objects.all()
        serializer_class = PersonalInformationSerializer

    class PersonalInformationRetrieve(generics.RetrieveAPIView):
        queryset = PersonalInformation.objects.all()
        serializer_class = PersonalInformationSerializer

        def retrieve(self, request, *args, **kwargs):
            retrieve_response = super().retrieve(request, *args, **kwargs)
            return Response({
                'status': 200,
                'data': retrieve_response.data
            })

    class PersonalInformationCreate(APIView):
        """
        Add or Update a Client Personal Information record.
        """

        def post(self, request):
            try:
                data_without_homesafety = copy.deepcopy(request.data)
                data_without_client = copy.deepcopy(data_without_homesafety)
                client_id = data_without_homesafety['client']
                del data_without_client['client']  # To avoid Unique constraint error while updating in the Try Block
                data_without_homesafety.pop('home_safety_assessment', None)

                try:
                    pi_get = PersonalInformation.objects.get(client__client_id=client_id)
                    personal_id = pi_get.personal_id

                    # Add revision_date to the data
                    data_without_client['revision_date'] = datetime.date.today().strftime('%Y-%m-%d')

                    for key, value in data_without_client.items():
                        setattr(pi_get, key, value)
                    pi_get.save()

                    return Response({
                        'status': 200,
                        'data': PersonalInformationSerializer(pi_get).data
                    }, status=status.HTTP_200_OK)
                except PersonalInformation.DoesNotExist:
                    pi_serializer = PersonalInformationSerializer(data=request.data)
                    if pi_serializer.is_valid():
                        response_personal = PersonalInformation.objects.create(**pi_serializer.validated_data)
                        return Response({
                            'status': 201,
                            'data': PersonalInformationSerializer(response_personal).data
                        }, status=status.HTTP_201_CREATED)
                    else:
                        print(pi_serializer.errors)
                        return Response({
                            'status': 400,
                            'message': 'Please provide valid data for personal information.'
                        }, status=status.HTTP_400_BAD_REQUEST)
                except Exception:
                    return Response({
                        'status': 400,
                        'message': 'Please provide valid data for personal information.'
                    }, status=status.HTTP_400_BAD_REQUEST)
            except Exception:
                return Response({
                    'status': 500,
                    'message': 'Failed to process your request. '
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ClinicalInformationViews:
    class ClinicalInformationCreateUpdate(APIView):
        """
        Add/Update Clinical Information.
        """

        def post(self, request):
            try:
                client_id = request.data['client']

                try:
                    data_without_client = copy.deepcopy(request.data)
                    del data_without_client['client']
                    data_without_client['revision_date'] = datetime.date.today().strftime('%Y-%m-%d')

                    ci_get = ClinicalInformation.objects.get(client__client_id=client_id)

                    for key, value in data_without_client.items():
                        setattr(ci_get, key, value)
                    ci_get.save()

                    return Response({
                        'status': 200,
                        'data': PersonalInformationSerializer(ci_get).data
                    }, status=status.HTTP_200_OK)

                except ClinicalInformation.DoesNotExist:
                    print(1)
                    ci_serializer = ClinicalInformationSerializer(data=request.data)

                    if ci_serializer.is_valid():
                        response_clinical = ClinicalInformation.objects.create(**ci_serializer.validated_data)
                        return Response({
                            'status': 200,
                            'data': ClinicalInformationSerializer(response_clinical).data,
                        }, status=status.HTTP_201_CREATED)
                    else:
                        print(ci_serializer.errors)
                        return Response({
                            'status': 400,
                            'message': 'Please provide valid data for Clinical Information.'
                        }, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                print(str(e))
                return Response({
                    'status': 500,
                    'message': str(e)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    class ClinicalInformationList(generics.ListAPIView):
        """
        List all clients Clinical Information
        """
        queryset = ClinicalInformation.objects.all()
        serializer_class = ClinicalInformationSerializer

    class ClinicalInformationRetrieve(generics.RetrieveAPIView):
        queryset = ClinicalInformation.objects.all()
        serializer_class = ClinicalInformationSerializer

        def retrieve(self, request, *args, **kwargs):
            retrieve_response = super().retrieve(request, *args, **kwargs)
            return Response({
                'status': 200,
                'data': retrieve_response.data
            })


class ClientViews:
    class ClientDataRetrieve(views.APIView):
        def get(self, request, client_id):
            try:
                client = Client.objects.get(client_id=client_id)
                pi_data = self.fetch_personal(client)
                ci_data = self.fetch_clinical(client)
                visitor_log_data = self.fetch_visitor_logs(client)
                communication_log_data = self.fetch_communication_logs(client)

                return Response({
                    'status': 200,
                    'data': {
                        'personal_information': pi_data,
                        'clinical_information': ci_data,
                        'visitor_logs': visitor_log_data,
                        'communication_logs': communication_log_data
                    }
                })

            except Exception as e:
                return Response({
                    'status': 400,
                    'data': 'Failed to fetch data for the given client.'
                })

        def fetch_communication_logs(self, client):
            # Get Communication Logs
            communication_logs_objects = CommunicationLog.objects.filter(client=client)
            communication_log_data = False
            if communication_logs_objects.exists():
                communication_log_data = CommunicationLogSerializer(communication_logs_objects, many=True).data
            return communication_log_data

        def fetch_visitor_logs(self, client):
            # Get Visitor Logs
            visitor_logs_objects = VisitorLog.objects.filter(client=client)
            visitor_log_data = False
            if visitor_logs_objects.exists():
                visitor_log_data = VisitorLogSerializer(visitor_logs_objects).data
            return visitor_log_data

        def fetch_clinical(self, client):
            # Get Clinical Information Object
            ci_object_exists = ClinicalInformation.objects.filter(client=client).exists()
            ci_data = False
            if ci_object_exists:
                ci_object = ClinicalInformation.objects.get(client=client)
                ci_data = ClinicalInformationSerializer(ci_object).data

                # if CurrentMedication.objects.filter(clinical_id=ci_data['clinical_id']).exists():
                #     ci_medication_object = CurrentMedication.objects.filter(clinical_id=ci_data['clinical_id'])
                #     ci_data['current_medication'] = CurrentMedicationSerializer(ci_medication_object,
                #                                                                 many=True).data
            return ci_data

        def fetch_personal(self, client):
            # Get Personal Information Object
            pi_object_exists = PersonalInformation.objects.filter(client=client).exists()
            pi_data = False
            if pi_object_exists:
                pi_object = PersonalInformation.objects.get(client=client)
                pi_data = PersonalInformationSerializer(pi_object).data

                if HomeSafetyAssessment.objects.filter(personal_information=pi_object).exists():
                    pi_home_data = HomeSafetyAssessment.objects.filter(personal_information=pi_object)
                    pi_data['home_safety_assessment'] = HomeSafetyAssessmentSerialzer(pi_home_data, many=True).data
            return pi_data

    class ClientProfileRetrieve(views.APIView):
        def get(self, request, client_id):
            """
            Retrieve basic details of the Client by Client UUID
            {email, phone, location}
            :param request:
            :param client_id:
            :return:
            """
            return Response("OK")
