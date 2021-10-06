from rest_framework.serializers import ModelSerializer
from .models import *


class AssessmentFormsDocumentsSerializer(ModelSerializer):
    class Meta:
        model = AssessmentFormsDocuments
        fields = '__all__'


class InterventionFormsDocumentsSerializer(ModelSerializer):
    class Meta:
        model = InterventionFormsDocuments
        fields = '__all__'


class ReviewBoardReferralFormsDocumentsSerializer(ModelSerializer):
    class Meta:
        model = ReviewBoardReferralFormsDocuments
        fields = '__all__'
