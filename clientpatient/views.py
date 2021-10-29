from rest_framework import status, generics, response, views
from rest_framework.response import Response
from .models import *
from .serializers import *


class CommunicationLogs:
    class CommunicationLogList(generics.ListCreateAPIView):
        """
        List all communication logs.
        """
        queryset = CommunicationLog.objects.all()
        serializer_class = CommunicationLogSerializer

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
                'status': 200,
                'data': response.data
            })

    class VisitorsLogUpdateDeleteRetrieve(generics.RetrieveUpdateDestroyAPIView):
        """
        Retrieve, Update and Delete visitor logs.
        """
        queryset = VisitorLog.objects.all()
        serializer_class = VisitorLogSerializer


class PersonalInformation:
    class PersonalInformationList(generics.ListAPIView):
        """
        List all client's Personal Information
        """
        queryset = PersonalInformation.objects.all()
        serializer_class = PersonalInformationSerializer

    class PersonalInformationUpdateDeleteRetrieve(generics.RetrieveUpdateDestroyAPIView):
        queryset = PersonalInformation.objects.all()
        serializer_class = PersonalInformationSerializer

        def update(self, request, *args, **kwargs):
            existing_client = str(super().get_object().client.client_id)

            if request.data['client'] == existing_client:
                response_personal = super().update(request, *args, **kwargs)
                return Response({
                    'status': 200,
                    'data': response_personal.data
                })
            else:
                return Response({
                    'status': 400,
                    'data': 'Failed to update the personal information. Incorrect Client value provided.'
                })

    class PersonalInformationCreate(generics.CreateAPIView):
        """
        Add a Client Personal Information record.
        """
        queryset = PersonalInformation.objects.all()
        serializer_class = PersonalInformationSerializer

        def create(self, request, *args, **kwargs):
            for data_key in request.data.keys():
                if data_key != "home_safety_assessment":
                    request.data[data_key] = request.data[data_key].replace("&$#", " ")
            response_personal = super().create(request, *args, **kwargs)

            # Add Home Safety Assessment data
            home_safety_assessment = request.data["home_safety_assessment"]
            personal_id = response_personal.data["personal_id"]

            for assessment_item in home_safety_assessment:
                assessment_item['answer'] = assessment_item['answer'].replace("&$#", " ")
                assessment_item['question'] = assessment_item['question'].replace("&$#", " ")
                assessment_item['question_group'] = assessment_item['question_group'].replace("&$#", " ")
                assessment_item['personal_information'] = personal_id

            # personal_information
            home_safety_assessment_serializer = HomeSafetyAssessmentSerialzer(data=home_safety_assessment, many=True)
            response_result = True
            if home_safety_assessment_serializer.is_valid():
                home_safety_assessment_serializer.save()
            else:
                # TODO log error
                response_result = False

            return Response({
                'status': 200,
                'data': response_personal.data
            })
