from rest_framework import serializers
from .models import *


class DocumentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Documents
        fields = '__all__'


class DocumentUploadSerializer(serializers.Serializer):
    file = serializers.FileField()
    type = serializers.CharField(max_length=100)


class ClinicianAssessmentFormsDocumentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClinicianAssessmentFormsDocuments
        fields = '__all__'


class ClinicianAssessmentFormsDocumentsDetailSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['document'] = DocumentsSerializer(instance.document).data
        return response

    class Meta:
        model = ClinicianAssessmentFormsDocuments
        fields = '__all__'


class CaseManagerAssessmentFormsDocumentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CaseManagerAssessmentFormsDocuments
        fields = '__all__'


class InterventionFormsDocumentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterventionFormsDocuments
        fields = '__all__'


class ReviewBoardReferralFormsDocumentsSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['document'] = DocumentsSerializer(instance.document).data
        return response

    class Meta:
        model = ReviewBoardReferralFormsDocuments
        fields = '__all__'
