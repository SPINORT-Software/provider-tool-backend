from rest_framework.serializers import ModelSerializer
from .models import *


class DocumentsSerializer(ModelSerializer):
    class Meta:
        model = Documents
        fields = '__all__'


class ClinicianAssessmentFormsDocumentsSerializer(ModelSerializer):
    class Meta:
        model = ClinicianAssessmentFormsDocuments
        fields = '__all__'


class ClinicianAssessmentFormsDocumentsDetailSerializer(ModelSerializer):
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['document'] = DocumentsSerializer(instance.document).data
        return response

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


