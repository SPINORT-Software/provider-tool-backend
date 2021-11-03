import datetime

from rest_framework import status, generics, response, views
from rest_framework.response import Response
from .models import *
from .serializers import *
from django.core import serializers
from django.forms.models import model_to_dict


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


class PersonalInformationViews:
    @staticmethod
    def add_home_safety(request, personal_id, home_safety_assessment):
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
            home_safety_add_result, home_safety_serialized_data = PersonalInformationViews.add_home_safety(request,
                                                                                                           personal_id,
                                                                                                           request.data[
                                                                                                               "home_safety_assessment"])

            if home_safety_add_result:
                return Response({
                    'status': 200,
                    'data': response_personal.data
                })
            else:
                # Could not add home safety data - hence remove the personal information object.
                PersonalInformation.objects.get(personal_id=personal_id).delete()
                return Response({
                    'status': 500,
                    'data': "Failed to add personal information. Please try again"
                })


class ClinicalInformationViews:
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
            self.add_medical_diagnosis(nested_process, request)
            self.add_home_support(nested_process, request)
            self.add_previous_hospitalization(nested_process, request)
            self.add_emergency_room_visits(nested_process, request)
            self.add_ambulance_use(nested_process, request)

            if not nested_process['result']:
                return Response({
                    'status': 400,
                    'data': nested_process['message']
                })
            else:
                response = super().create(request, *args, **kwargs)
                self.add_current_medication(nested_process, request, response.data['clinical_id'])

                if not nested_process['result']:
                    ClinicalInformation.objects.get(clinical_id=response.data['clinical_id']).delete()
                    return Response({
                        'status': 400,
                        'data': nested_process['message']
                    })
                else:
                    return Response({
                        'status': 200,
                        'data': response.data
                    })

        @staticmethod
        def add_ambulance_use(nested_process, request):
            ambulance_use_serializer = AmbulanceUseSerializer(data=request.data['ambulance_use'])
            if ambulance_use_serializer.is_valid():
                ambulance_use = ambulance_use_serializer.save()
                request.data['ambulance_use'] = ambulance_use.ambulance_use_id
            else:
                nested_process['result'] = False
                nested_process['message'] = "Invalid ambulance use  values provided."

        @staticmethod
        def add_emergency_room_visits(nested_process, request):
            emergency_room_visits_serializer = EmergencyRoomVisitsSerializer(data=request.data['emergency_room_visits'])
            if emergency_room_visits_serializer.is_valid():
                emergency_room_visits = emergency_room_visits_serializer.save()
                request.data['emergency_room_visits'] = emergency_room_visits.emergency_room_visit_id
            else:
                nested_process['result'] = False
                nested_process['message'] = "Invalid emergency room visits values provided."

        @staticmethod
        def add_previous_hospitalization(nested_process, request):
            last_hospitalization_serializer = PreviousHospitalizationSerializer(
                data=request.data['last_hospitalization'])
            if last_hospitalization_serializer.is_valid():
                last_hospitalization = last_hospitalization_serializer.save()
                request.data['last_hospitalization'] = last_hospitalization.previous_hospitalization_id
            else:
                nested_process['result'] = False
                nested_process['message'] = "Invalid last hospitalization values provided."

        @staticmethod
        def add_home_support(nested_process, request):
            for home_support_key in request.data['home_support_services'].keys():
                request.data['home_support_services'][home_support_key] = request.data['home_support_services'][
                    home_support_key].replace("&$#", " ")

            home_support_services_serializer = HomeSupportServicesSerializer(data=request.data['home_support_services'])
            if home_support_services_serializer.is_valid():
                home_support_services = home_support_services_serializer.save()
                request.data['home_support_services'] = home_support_services.home_support_services_id
            else:
                nested_process['result'] = False
                nested_process['message'] = "Invalid home support services values provided."

        @staticmethod
        def add_medical_diagnosis(nested_process, request):
            for medical_data_key in request.data['medical_diagnosis'].keys():
                request.data['medical_diagnosis'][medical_data_key] = request.data['medical_diagnosis'][
                    medical_data_key].replace("&$#", " ")

            medical_diagnosis_serializer = MedicalDiagnosisSerializer(data=request.data['medical_diagnosis'])
            if medical_diagnosis_serializer.is_valid():
                medical_diagnosis = medical_diagnosis_serializer.save()
                request.data['medical_diagnosis'] = medical_diagnosis.medical_id
            else:
                nested_process['result'] = False
                nested_process['message'] = "Invalid medical diagnosis values provided."

        @staticmethod
        def add_current_medication(nested_process, request, clinical_id):
            if "current_medication" in request.data:
                current_medication_data = request.data['current_medication']
                for medication_item in current_medication_data:
                    medication_item['clinical_id'] = clinical_id
                current_medication_serializer = CurrentMedicationSerializer(data=current_medication_data, many=True)
                if current_medication_serializer.is_valid():
                    current_medication_serializer.save()
                else:
                    nested_process['result'] = False
                    nested_process['message'] = "Invalid current medication values provided."

    class ClinicalInformationList(generics.ListAPIView):
        """
        List all clients Clinical Information
        """
        queryset = ClinicalInformation.objects.all()
        serializer_class = ClinicalInformationSerializer

    class ClinicalInformationUpdateDeleteRetrieve(generics.RetrieveUpdateDestroyAPIView):
        queryset = ClinicalInformation.objects.all()
        serializer_class = ClinicalInformationSerializer

        def retrieve(self, request, *args, **kwargs):
            retrieve_response = super().retrieve(request, *args, **kwargs)

            # Retrieve Current Medication Data
            retrieve_response.data['current_medication'] = CurrentMedication.objects.values().filter(
                clinical_id=kwargs.get('pk'))

            return Response({
                'status': 200,
                'data': retrieve_response.data
            })

        def update(self, request, *args, **kwargs):
            nested_process = {'result': True, 'message': ''}
            existing_client = str(super().get_object().client.client_id)

            try:
                if request.data['client'] == existing_client:
                    request.data['revision_date'] = datetime.date.today().strftime('%Y-%m-%d')
                    self.update_medical_diagnosis(request)
                    self.update_home_support_services(request)
                    self.update_last_hospitalization(request)
                    self.update_emergency_room_visits(request)
                    self.update_ambulance_use(request)
                    response_clinical = super().update(request, *args, **kwargs)

                    if "current_medication" in request.data:
                        clinical_id = kwargs.get('pk')
                        CurrentMedication.objects.filter(clinical_id=clinical_id).delete()
                        ClinicalInformationViews.ClinicalInformationCreate.add_current_medication(nested_process,
                                                                                                  request,
                                                                                                  clinical_id)
                    return Response({
                        'status': 200,
                        'data': response_clinical.data
                    })
                else:
                    return Response({
                        'status': 400,
                        'data': 'Failed to update the clinical information. Incorrect Client value provided.'
                    })
            except Exception as e:
                return Response({
                    'status': 400,
                    'data': str(e)
                })

        def update_home_support_services(self, request):
            if "home_support_services" in request.data:
                home_support_services_id = request.data['home_support_services']['home_support_services_id']
                home_support_services_object = HomeSupportServices.objects.get(
                    home_support_services_id=home_support_services_id)
                home_support_services_serializer = HomeSupportServicesSerializer(home_support_services_object,
                                                                                 data=request.data[
                                                                                     'home_support_services'])

                if home_support_services_serializer.is_valid():
                    home_support_services_serializer.save()
                    request.data['home_support_services'] = home_support_services_id

        def update_medical_diagnosis(self, request):
            if "medical_diagnosis" in request.data:
                medical_diagnosis_id = request.data['medical_diagnosis']['medical_id']
                medical_diagnosis_object = MedicalDiagnosis.objects.get(medical_id=medical_diagnosis_id)
                medical_diagnosis_serializer = MedicalDiagnosisSerializer(medical_diagnosis_object,
                                                                          data=request.data['medical_diagnosis'])

                if medical_diagnosis_serializer.is_valid():
                    medical_diagnosis_serializer.save()
                    request.data['medical_diagnosis'] = medical_diagnosis_id

        def update_last_hospitalization(self, request):
            if "last_hospitalization" in request.data:
                previous_hospitalization_id = request.data['last_hospitalization']['previous_hospitalization_id']
                previous_hospitalization_object = PreviousHospitalization.objects.get(
                    previous_hospitalization_id=previous_hospitalization_id)
                previous_hospitalization_serializer = PreviousHospitalizationSerializer(previous_hospitalization_object,
                                                                                        data=request.data[
                                                                                            'last_hospitalization'])

                if previous_hospitalization_serializer.is_valid():
                    previous_hospitalization_serializer.save()
                    request.data['last_hospitalization'] = previous_hospitalization_id

        def update_emergency_room_visits(self, request):
            if "emergency_room_visits" in request.data:
                emergency_room_visit_id = request.data['emergency_room_visits']['emergency_room_visit_id']
                emergency_room_visit_object = EmergencyRoomVisits.objects.get(
                    emergency_room_visit_id=emergency_room_visit_id)
                emergency_room_visit_serializer = EmergencyRoomVisitsSerializer(emergency_room_visit_object,
                                                                                data=request.data[
                                                                                    'emergency_room_visits'])

                if emergency_room_visit_serializer.is_valid():
                    emergency_room_visit_serializer.save()
                    request.data['emergency_room_visits'] = emergency_room_visit_id

        def update_ambulance_use(self, request):
            if "ambulance_use" in request.data:
                ambulance_use_id = request.data['ambulance_use']['ambulance_use_id']
                ambulance_use_object = AmbulanceUse.objects.get(ambulance_use_id=ambulance_use_id)
                ambulance_use_serializer = AmbulanceUseSerializer(ambulance_use_object, data=request.data[
                    'ambulance_use'])

                if ambulance_use_serializer.is_valid():
                    ambulance_use_serializer.save()


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

                if CurrentMedication.objects.filter(clinical_id=ci_data['clinical_id']).exists():
                    ci_medication_object = CurrentMedication.objects.filter(clinical_id=ci_data['clinical_id'])
                    ci_data['current_medication'] = CurrentMedicationSerializer(ci_medication_object,
                                                                                many=True).data
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
