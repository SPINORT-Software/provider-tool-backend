from rest_framework.serializers import ModelSerializer
from .models import *


class DailyWorkloadSerializer(ModelSerializer):
    class Meta:
        model = DailyWorkLoad
        fields = '__all__'


class CommunityClientAssessmentSerializer(ModelSerializer):
    class Meta:
        model = CommunityClientAssessment
        fields = '__all__'


class HomeSafetyAssessmentSerializer(ModelSerializer):
    class Meta:
        model = HomeSafetyAssessment
        fields = '__all__'


class ExistingCaseClientAssessmentChangeInConditionSerializer(ModelSerializer):
    class Meta:
        model = ExistingCaseClientAssessmentChangeInCondition
        fields = '__all__'


class NewCaseClientAssessmentSerializer(ModelSerializer):
    class Meta:
        model = NewCaseClientAssessment
        fields = '__all__'


class ExistingCaseClientAssessmentSerializer(ModelSerializer):
    class Meta:
        model = ExistingCaseClientAssessment
        fields = '__all__'


class ClientVitalSignsSerializer(ModelSerializer):
    class Meta:
        model = ClientVitalSigns
        fields = '__all__'
