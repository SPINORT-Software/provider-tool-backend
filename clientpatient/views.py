import datetime

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
                request.data['revision_date'] = datetime.date.today().strftime('%Y-%m-%d')
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


class ClinicalInformation:
    class ClinicalInformationCreate(generics.CreateAPIView):
        """
        Add Clinical Information.
        """
        queryset = ClinicalInformation.objects.all()
        serializer_class = ClinicalInformationSerializer

        def create(self, request, *args, **kwargs):
            # Create Nested Model fields and append to request data
            nested_process = {
                'result': True,
                'message': ''
            }
            self.add_medical(nested_process, request)
            self.add_home_support(nested_process, request)
            self.add_previous_hospitalization(nested_process, request)
            self.add_emergency_room_visits(nested_process, request)
            self.add_ambulance_use(nested_process, request)

            response = super().create(request, *args, **kwargs)
            return Response({
                'status': 200,
                'data': response.data
            })

        def add_ambulance_use(self, nested_process, request):
            ambulance_use_serializer = AmbulanceUseSerializer(data=request.data['ambulance_use'])
            if ambulance_use_serializer.is_valid():
                ambulance_use = ambulance_use_serializer.save()
                request.data['ambulance_use'] = ambulance_use.ambulance_use_id
            else:
                nested_process['result'] = False
                nested_process['message'] = "Invalid ambulance use  values provided."

        def add_emergency_room_visits(self, nested_process, request):
            emergency_room_visits_serializer = EmergencyRoomVisitsSerializer(data=request.data['emergency_room_visits'])
            if emergency_room_visits_serializer.is_valid():
                emergency_room_visits = emergency_room_visits_serializer.save()
                request.data['emergency_room_visits'] = emergency_room_visits.emergency_room_visit_id
            else:
                nested_process['result'] = False
                nested_process['message'] = "Invalid emergency room visits values provided."

        def add_previous_hospitalization(self, nested_process, request):
            last_hospitalization_serializer = PreviousHospitalizationSerializer(
                data=request.data['last_hospitalization'])
            if last_hospitalization_serializer.is_valid():
                last_hospitalization = last_hospitalization_serializer.save()
                request.data['last_hospitalization'] = last_hospitalization.previous_hospitalization_id
            else:
                nested_process['result'] = False
                nested_process['message'] = "Invalid last hospitalization values provided."

        def add_home_support(self, nested_process, request):
            home_support_services_serializer = HomeSupportServicesSerializer(data=request.data['home_support_services'])
            if home_support_services_serializer.is_valid():
                home_support_services = home_support_services_serializer.save()
                request.data['home_support_services'] = home_support_services.home_support_services_id
            else:
                nested_process['result'] = False
                nested_process['message'] = "Invalid home support services values provided."

        def add_medical(self, nested_process, request):
            medical_diagnosis_serializer = MedicalDiagnosisSerializer(data=request.data['medical_diagnosis'])
            if medical_diagnosis_serializer.is_valid():
                medical_diagnosis = medical_diagnosis_serializer.save()
                request.data['medical_diagnosis'] = medical_diagnosis.medical_id
            else:
                nested_process['result'] = False
                nested_process['message'] = "Invalid medical diagnosis values provided."
