from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import *
from authentication.serializers import UserSearchSerializer


class ClientSerializer(ModelSerializer):
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['user'] = UserSearchSerializer(instance.user).data
        return response

    class Meta:
        model = Client
        fields = '__all__'


class CommunicationLogSerializer(ModelSerializer):
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['client'] = ClientSerializer(instance.client).data
        return response

    class Meta:
        model = CommunicationLog
        fields = '__all__'


class VisitorLogSerializer(ModelSerializer):
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['client'] = ClientSerializer(instance.client).data
        return response

    class Meta:
        model = VisitorLog
        fields = '__all__'


class PersonalInformationSerializer(ModelSerializer):
    # def to_representation(self, instance):
    #     response = super().to_representation(instance)
    #     # response['client'] = ClientSerializer(instance.client).data
    #     # home_safety_data = HomeSafetyAssessment.objects.values().filter(personal_information=instance.personal_id)
    #     # response['home_safety_assessment'] = HomeSafetyAssessmentSerialzer(home_safety_data, many=True).data
    #     return response

    class Meta:
        model = PersonalInformation
        fields = '__all__'


class HomeSafetyAssessmentSerialzer(ModelSerializer):
    class Meta:
        model = HomeSafetyAssessment
        fields = '__all__'


class ClinicalInformationSerializer(ModelSerializer):
    # def to_representation(self, instance):
    #     response = super().to_representation(instance)
    #     response['client'] = ClientSerializer(instance.client).data
    #     return response

    class Meta:
        model = ClinicalInformation
        fields = '__all__'
