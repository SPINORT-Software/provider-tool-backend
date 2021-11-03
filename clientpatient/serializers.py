from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import *


class ClientSerialzer(ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'


class CommunicationLogSerializer(ModelSerializer):
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['client'] = ClientSerialzer(instance.client).data
        return response

    class Meta:
        model = CommunicationLog
        fields = '__all__'


class VisitorLogSerializer(ModelSerializer):
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['client'] = ClientSerialzer(instance.client).data
        return response

    class Meta:
        model = VisitorLog
        fields = '__all__'


class PersonalInformationSerializer(ModelSerializer):
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['client'] = ClientSerialzer(instance.client).data
        return response

    class Meta:
        model = PersonalInformation
        fields = '__all__'


class HomeSafetyAssessmentSerialzer(ModelSerializer):
    class Meta:
        model = HomeSafetyAssessment
        fields = '__all__'


class MedicalDiagnosisSerializer(ModelSerializer):
    class Meta:
        model = MedicalDiagnosis
        fields = '__all__'


class HomeSupportServicesSerializer(ModelSerializer):
    class Meta:
        model = HomeSupportServices
        fields = '__all__'


class PreviousHospitalizationSerializer(ModelSerializer):
    class Meta:
        model = PreviousHospitalization
        fields = '__all__'


class EmergencyRoomVisitsSerializer(ModelSerializer):
    class Meta:
        model = EmergencyRoomVisits
        fields = '__all__'


class AmbulanceUseSerializer(ModelSerializer):
    class Meta:
        model = AmbulanceUse
        fields = '__all__'


class CurrentMedicationSerializer(ModelSerializer):
    class Meta:
        model = CurrentMedication
        fields = '__all__'


class ClinicalInformationSerializer(ModelSerializer):
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['client'] = ClientSerialzer(instance.client).data
        response['medical_diagnosis'] = MedicalDiagnosisSerializer(instance.medical_diagnosis).data
        response['home_support_services'] = HomeSupportServicesSerializer(instance.home_support_services).data
        response['last_hospitalization'] = PreviousHospitalizationSerializer(instance.last_hospitalization).data
        response['emergency_room_visits'] = EmergencyRoomVisitsSerializer(instance.emergency_room_visits).data
        response['ambulance_use'] = AmbulanceUseSerializer(instance.ambulance_use).data
        return response

    class Meta:
        model = ClinicalInformation
        fields = '__all__'
