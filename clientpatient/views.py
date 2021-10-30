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
    @staticmethod
    def add_home_safety(request, personal_id, home_safety_assessment):
        # Add Home Safety Assessment data
        for assessment_item in home_safety_assessment:
            assessment_item['answer'] = assessment_item['answer'].replace("&$#", " ")
            assessment_item['question'] = assessment_item['question'].replace("&$#", " ")
            assessment_item['question_group'] = assessment_item['question_group'].replace("&$#", " ")
            assessment_item['personal_information'] = personal_id

        home_safety_assessment_serializer = HomeSafetyAssessmentSerialzer(data=home_safety_assessment, many=True)
        response_result = True
        if home_safety_assessment_serializer.is_valid():
            home_safety_assessment_serializer.save()
        else:
            # TODO log error
            response_result = False

    class PersonalInformationList(generics.ListAPIView):
        """
        List all client's Personal Information
        """
        queryset = PersonalInformation.objects.all()
        serializer_class = PersonalInformationSerializer

    class PersonalInformationUpdateDeleteRetrieve(generics.RetrieveUpdateDestroyAPIView):
        queryset = PersonalInformation.objects.all()
        serializer_class = PersonalInformationSerializer

        def retrieve(self, request, *args, **kwargs):
            retrieve_response = super().retrieve(request, *args, **kwargs)

            # Retrieve Home Safety Assessment Data
            retrieve_response.data['home_safety_assessment'] = HomeSafetyAssessment.objects.values().filter(
                personal_information=kwargs.get('pk'))

            return Response({
                'status': 200,
                'data': retrieve_response.data
            })

        def update(self, request, *args, **kwargs):
            existing_client = str(super().get_object().client.client_id)

            if request.data['client'] == existing_client:
                response_personal = super().update(request, *args, **kwargs)
                personal_id = kwargs.get('pk')

                # Remove existing Home safety assessment objects before updating with new data
                HomeSafetyAssessment.objects.filter(personal_information=personal_id).delete()
                PersonalInformation.add_home_safety(request, personal_id, request.data["home_safety_assessment"])

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

            personal_id = response_personal.data["personal_id"]
            PersonalInformation.add_home_safety(request, personal_id, request.data["home_safety_assessment"])

            return Response({
                'status': 200,
                'data': response_personal.data
            })
