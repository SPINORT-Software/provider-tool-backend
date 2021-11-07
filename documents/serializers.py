from rest_framework.serializers import ModelSerializer
from .models import *


class ClinicianAssessmentFormsDocumentsSerializer(ModelSerializer):
    class Meta:
        model = ClinicianAssessmentFormsDocuments
        fields = '__all__'


class CaseManagerAssessmentFormsDocumentsSerializer(ModelSerializer):
    class Meta:
        model = CaseManagerAssessmentFormsDocuments
        fields = '__all__'


class InterventionFormsDocumentsSerializer(ModelSerializer):
    class Meta:
        model = InterventionFormsDocuments
        fields = '__all__'


class ReviewBoardReferralFormsDocumentsSerializer(ModelSerializer):
    class Meta:
        model = ReviewBoardReferralFormsDocuments
        fields = '__all__'
