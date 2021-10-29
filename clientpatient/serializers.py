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
